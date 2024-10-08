# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import itertools
import pathlib
import re
import subprocess
from dataclasses import dataclass, field

from .structs import Fit, KBImage, Size


@dataclass
class Filter:
    name: str
    options: dict[str, str] = field(default_factory=dict)
    needs_quoting = re.compile("[,;]")

    def __str__(self) -> str:
        if self.options:
            options = ":".join(
                f"{key}='{value}'" if self.needs_quoting.search(value) else f"{key}={value}"
                for key, value in self.options.items()
            )
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
    verbose: int = 0,
) -> None:
    command = [
        "ffmpeg",
        "-loglevel",
        {
            0: "error",
            1: "warning",
            2: "info",
            3: "verbose",
            4: "debug",
            5: "trace",
        }.get(verbose, "trace"),
    ]
    inputs = [("-i", image.src) for image in kbimages]
    command.extend(itertools.chain.from_iterable(inputs))

    filtergraph = FilterGraph()
    prev_filterchain: FilterChain | None = None
    prev_image: KBImage | None = None
    xfade_offset: float = 0
    for i, image in enumerate(kbimages):
        zoom_duration = image.duration * fps
        # Compute a zoompan size that is fit to the output size
        match image.fit:
            case Fit.COVER:
                image_fit_scale = max(
                    encode_size.width / image.size.width, encode_size.height / image.size.height
                )
            case Fit.CONTAIN:
                image_fit_scale = min(
                    encode_size.width / image.size.width, encode_size.height / image.size.height
                )
        zoom_image_size = image.size * image_fit_scale
        if image.boxes:
            filterchain = FilterChain([], input_pads=[str(i)])

            # Just use first box for now
            # XXX look for highest threshold that matches requested feature?
            scaled_box = image.boxes[0].scaled(image_fit_scale)
            if zoom_image_size != encode_size and image.fit is Fit.CONTAIN:
                scaled_box = scaled_box.translated(
                    (encode_size.width - zoom_image_size.width) / 2,
                    (encode_size.height - zoom_image_size.height) / 2,
                )
                filterchain.filters.extend(
                    [
                        Filter(
                            "scale",
                            {
                                "w": str(zoom_image_size.width),
                                "h": str(zoom_image_size.height),
                            },
                        ),
                        Filter(
                            "pad",
                            {
                                "w": str(encode_size.width),
                                "h": str(encode_size.height),
                                # Centered
                                "x": "-1",
                                "y": "-1",
                            },
                        ),
                    ]
                )
                zoom_image_size = encode_size

            # Normalized translation, -1..0..1
            translate_x = (2 * scaled_box.center[0] / zoom_image_size.width) - 1
            translate_y = (2 * scaled_box.center[1] / zoom_image_size.height) - 1
            # Scale so box is object-fit=contain of the encoded image
            zoom = min(
                encode_size.width / scaled_box.size.width,
                encode_size.height / scaled_box.size.height,
                10,  # Max allowed ffmpeg zoom is 10
            )
            z_filter = Filter(
                "zoompan",
                {
                    "z": f"st(0, clip(time / {image.duration}, 0, 1));"
                    f"{image.transition_easing.value};"
                    f"lerp(1, {zoom}, ld(0))"
                },
            )
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
        filterchain.filters.append(z_filter)
        if zoom_image_size != encode_size and image.fit is Fit.COVER:
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
                            "transition": prev_image.transition.value,
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

    # yuv420p otherwise ffmpeg uses H.264 High 4:4:4 Profile, some players don't support that
    command.extend(["-r", str(fps), "-s", str(encode_size), "-pix_fmt", "yuv420p", "-y", str(outfile)])
    subprocess.check_call(command)  # noqa: S603
    if verbose > 0:
        print(command)
