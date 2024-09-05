import itertools
import pathlib
import subprocess

from .detector import ImageBoxes, Size


def encode(
    encode_size: Size,
    fps: int,
    images: list[ImageBoxes],
    image_duration: float,
    outfile: pathlib.Path | str,
) -> None:
    command = ["ffmpeg"]
    inputs = [("-i", image.src) for image in images]
    command.extend(itertools.chain.from_iterable(inputs))

    filters: list[str] = []
    for i, image in enumerate(images):
        zoom_duration = image_duration * fps
        # Compute a zoompan size that is object-fit=cover of the output size
        # XXX also support object-fit=contain, with a pad filter
        image_fit_scale = max(encode_size.width / image.size.width, encode_size.height / image.size.height)
        zoom_image_size = image.size * image_fit_scale
        if image.boxes:
            # Just use first box for now
            scaled_box = image.boxes[0].scaled(image_fit_scale)
            # Scale so box is object-fit=contain of the scaled image
            zoom = min(
                zoom_image_size.width / scaled_box.size.width,
                zoom_image_size.height / scaled_box.size.height,
            )
            # Normalized translation, -1..0..1
            translate_x = (2 * scaled_box.center[0] / zoom_image_size.width) - 1
            translate_y = 1 - (2 * scaled_box.center[1] / zoom_image_size.height)
            z_filter = f"z=zoom+{zoom / zoom_duration}"
        else:
            translate_x = 0
            translate_y = 0
            z_filter = "z=1"

        filterchain = (
            f"[{i}]zoompan={z_filter}"
            f":x=(iw/2+iw*{translate_x})-(iw/zoom/2)"
            f":y=(ih/2+ih*{translate_y})-(ih/zoom/2)"
            f":s={zoom_image_size}:fps={fps}:d={zoom_duration}"
            f",crop=w={encode_size.width}:h={encode_size.height}"
            f",setsar=1[{i}pz]"
        )
        filters.append(filterchain)

    concatsrc = "".join(f"[{i}pz]" for i in range(len(filters)))
    filters.append(f"{concatsrc}concat=n={len(filters)}")
    command.extend(["-filter_complex", ";".join(filters)])

    command.extend(["-r", str(fps), "-s", str(encode_size), "-y", str(outfile)])
    subprocess.check_call(command)  # noqa: S603
    print(command)


# XXX debugging
if __name__ == "__main__":
    images = [
        ImageBoxes(
            "/Users/aw/Projects/rectalogic/mediafx-qt/tests/fixtures/assets/bridge.jpg", Size(1024, 768), []
        ),
        # ImageBoxes("/Users/aw/Desktop/cat.jpg", Size(640, 480), []),
        # ImageBoxes("/Users/aw/Pictures/blackflag.jpg", Size(336, 400), []),
    ]
    encode(Size(640, 360), 30, images, 3, "/tmp/pz2.mp4")
