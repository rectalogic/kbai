import itertools
import pathlib
import subprocess

from .detector import ImageBoxes, Size


def encode(size: Size, fps: int, images: list[ImageBoxes], outfile: pathlib.Path | str):
    duration = 3  # XXX duration per image, make configurable
    command = ["ffmpeg"]
    inputs = [("-i", image.src) for image in images]
    command.extend(itertools.chain.from_iterable(inputs))

    filters: list[str] = []
    for i, image in enumerate(images):
        # Compute a zoompan size that is object-fit=cover of the output size
        # XXX also support object-fit=contain, with a pad filter
        if image.size.fraction > size.fraction:
            fitscale = size.height / image.size.height
        else:
            fitscale = size.width / image.size.width
        zoomsize = image.size * fitscale
        zoomduration = duration * fps
        zoom = 2  # XXX hardcode for now, need to compute
        translate_x = 0  #XXX hardcode for now, normalized -1..0..1
        translate_y = 0
        filterchain = (
            f"[{i}]zoompan=z=zoom+{zoom / zoomduration}"
            f":x=(iw/2+iw*{translate_x})-(iw/zoom/2)"
            f":y=(ih/2+ih*{translate_y})-(ih/zoom/2)"
            f":s={zoomsize}:fps={fps}:d={zoomduration}"
            f",crop=w={size.width}:h={size.height}"
            f",setsar=1[{i}pz]"
        )
        filters.append(filterchain)

    concatsrc = "".join(f"[{i}pz]" for i in range(len(filters)))
    filters.append(f"{concatsrc}concat=n={len(filters)}")
    command.extend(["-filter_complex", ";".join(filters)])

    command.extend(["-r", str(fps), "-s", str(size), "-y", str(outfile)])
    subprocess.check_call(command)
    print(command)


if __name__ == "__main__":
    images = [
        ImageBoxes("/Users/aw/Desktop/cat.jpg", Size(640, 480), []),
        ImageBoxes("/Users/aw/Pictures/blackflag.jpg", Size(336, 400), []),
        ImageBoxes(
            "/Users/aw/Projects/rectalogic/mediafx-qt/tests/fixtures/assets/bridge.jpg", Size(1024, 768), []
        ),
    ]
    encode(Size(640, 360), 30, images, "/tmp/pz.mp4")
