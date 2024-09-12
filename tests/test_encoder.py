# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest

from kbai import cli
from kbai.detector import Detector
from kbai.image import ImageSrc
from kbai.structs import AnnotatedBox, Size

# XXX boxes need to go in here - make debug_image print them
IMAGES = {
    # Person 4x3
    "https://picsum.photos/id/22/1280/960": {
        "size": Size(1280, 960),
        "boxes": [
            AnnotatedBox(
                xmin=672.5023803710938,
                ymin=272.8601989746094,
                xmax=806.8201293945312,
                ymax=712.7240600585938,
                annotation="person",
            )
        ],
        "features": ["person"],
    },
    # Person 3x4
    "https://picsum.photos/id/22/960/1280": {
        "size": Size(960, 1280),
        "boxes": [],
        "features": ["person"],
    },
    # Mug 16x9
    "https://picsum.photos/id/42/1280/720": {
        "size": Size(1280, 720),
        "boxes": [],
        "features": ["mug"],
    },
    # Bird 4x3
    "https://picsum.photos/id/50/1280/960": {
        "size": Size(1280, 960),
        "boxes": [],
        "features": ["bird"],
    },
}

encode_testdata = {
    "single_cover_4x3_to_16x9": (
        [
            "-v",
            "encode",
            "-s",
            "640x360",
            "-i",
            "https://picsum.photos/id/22/1280/960",
            "/ft",
            "person",
            "-o",
            "single_cover_4x3_to_16x9.mp4",
        ],
        [
            "ffmpeg",
            "-loglevel",
            "warning",
            "-i",
            "https://picsum.photos/id/22/1280/960",
            "-filter_complex",
            "[0]zoompan=z='st(0, clip(time / 5, 0, 1));"
            "st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3));"
            "lerp(1, 1.6363636363636365, ld(0))':"
            "x=(iw+iw*0.15547246932983394)/2-(iw/zoom/2):"
            "y=(ih+ih*0.026792081197102968)/2-(ih/zoom/2):"
            "s=640x480:fps=25:d=125,crop=w=640:h=360,setsar=sar=1",
            "-r",
            "25",
            "-s",
            "640x360",
            "-y",
            "single_cover_4x3_to_16x9.mp4",
        ],
    ),
}


@pytest.mark.parametrize(
    "kbai_args,expected_ffmpeg_args", encode_testdata.values(), ids=encode_testdata.keys()
)
def test_encode(skip_mocks, mocker, kbai_args, expected_ffmpeg_args):
    if "image" not in skip_mocks:

        def load_image_side_effect(src):
            image = mocker.Mock(size=IMAGES[src])
            return ImageSrc(image, src)

        load_image_mock = mocker.patch("kbai.image.load_image")
        load_image_mock.side_effect = load_image_side_effect

    if "detect" not in skip_mocks:

        def detect_side_effect(image_src, features):
            image = IMAGES[image_src.src]
            assert image["features"] == features
            return image["boxes"]

        detect_mock = mocker.patch.object(Detector, "detect")
        detect_mock.side_effect = detect_side_effect

    if "encode" not in skip_mocks:
        ffmpeg_mock = mocker.patch("subprocess.check_call")
    else:
        ffmpeg_mock = None

    cli.main(kbai_args)

    if ffmpeg_mock is not None:
        ffmpeg_mock.assert_called_once_with(expected_ffmpeg_args)
