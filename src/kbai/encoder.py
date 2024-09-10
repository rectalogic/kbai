# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import itertools
import pathlib
import subprocess
from dataclasses import dataclass, field

from .structs import KBImage, Size


@dataclass
class Filter:
    name: str
    options: dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
        if self.options:
            options = ":".join(f"{key}={value.replace(",", "\\,")}" for key, value in self.options.items())
            return f"{self.name}={options}"
        return self.name


@dataclass
class FilterChain:
    filters: list[Filter]
    input_pads: list[str] | None = None
    output_pads: list[str] | None = None

    def _pads(self, pads: list[str] | None) -> str:
        if pads is None:
            return ""
        return "".join(f"[{p}]" for p in pads)

    def __str__(self) -> str:
        return (
            self._pads(self.input_pads)
            + ",".join(str(filter_) for filter_ in self.filters)
            + self._pads(self.output_pads)
        )


@dataclass
class FilterGraph:
    filterchains: list[FilterChain] = field(default_factory=list)

    def __str__(self) -> str:
        return ";".join(str(filterchain) for filterchain in self.filterchains)


def encode(
    encode_size: Size,
    fps: int,
    kbimages: list[KBImage],
    outfile: pathlib.Path | str,
) -> None:
    command = ["ffmpeg"]
    inputs = [("-i", image.src) for image in kbimages]
    command.extend(itertools.chain.from_iterable(inputs))

    filtergraph = FilterGraph()
    prev_filterchain: FilterChain | None = None
    prev_image: KBImage | None = None
    xfade_offset: float = 0
    for i, image in enumerate(kbimages):
        zoom_duration = image.duration * fps
        # Compute a zoompan size that is object-fit=cover of the output size
        # XXX also support object-fit=contain, with a pad filter
        image_fit_scale = max(encode_size.width / image.size.width, encode_size.height / image.size.height)
        zoom_image_size = image.size * image_fit_scale
        if image.boxes:
            # Just use first box for now
            scaled_box = image.boxes[0].scaled(image_fit_scale)
            # Normalized translation, -1..0..1
            translate_x = (2 * scaled_box.center[0] / zoom_image_size.width) - 1
            translate_y = (2 * scaled_box.center[1] / zoom_image_size.height) - 1
            # Scale so box is object-fit=contain of the scaled image
            zoom = min(
                zoom_image_size.width / scaled_box.size.width,
                zoom_image_size.height / scaled_box.size.height,
                10,  # Max allowed zoom is 10
            )
            # Don't start incrementing z until after the first frame
            z_filter = Filter("zoompan", {"z": f"if(gt(on,0),zoom+{zoom / zoom_duration},1)"})
        else:
            translate_x = 0
            translate_y = 0
            z_filter = Filter("zoompan", {"z": "1"})

        z_filter.options.update(
            {
                "x": f"(iw+iw*{translate_x})/2-(iw/zoom/2)",
                "y": f"(ih+ih*{translate_y})/2-(ih/zoom/2)",
                "s": f"{zoom_image_size}:fps={fps}:d={zoom_duration}",
            }
        )
        filterchain = FilterChain([z_filter], input_pads=[str(i)])
        if zoom_image_size != encode_size:
            filterchain.filters.append(
                Filter("crop", {"w": str(encode_size.width), "h": str(encode_size.height)})
            )
        filterchain.filters.append(Filter("setsar", {"sar": "1"}))
        if len(kbimages) > 1:
            filterchain.output_pads = [f"pz{i}"]
        filtergraph.filterchains.append(filterchain)

        if prev_filterchain is not None and prev_image is not None:
            xfade_offset += prev_image.duration - prev_image.transition_duration
            xfade = FilterChain(
                [
                    Filter(
                        "xfade",
                        {
                            "transition": prev_image.transition,
                            "duration": str(prev_image.transition_duration),
                            "offset": str(xfade_offset),
                        },
                    )
                ],
                input_pads=[
                    prev_filterchain.output_pads[0],
                    filterchain.output_pads[0],
                ],
                output_pads=[f"xf{i}"] if i < len(kbimages) - 1 else None,
            )
            filtergraph.filterchains.append(xfade)
            prev_filterchain = xfade
        else:
            prev_filterchain = filterchain

        prev_image = image

    command.extend(["-filter_complex", str(filtergraph)])

    command.extend(["-r", str(fps), "-s", str(encode_size), "-y", str(outfile)])
    subprocess.check_call(command)  # noqa: S603
    print(command)  # XXX
