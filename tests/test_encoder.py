# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest

from kbai import cli
from kbai.detector import Detector
from kbai.image import ImageSrc
from kbai.structs import AnnotatedBox, Size

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
        "boxes": [
            AnnotatedBox(
                xmin=519.8785400390625,
                ymin=393.3056640625,
                xmax=678.2841186523438,
                ymax=916.767578125,
                annotation="person",
            )
        ],
        "features": ["person"],
    },
    # Mug 16x9
    "https://picsum.photos/id/42/1280/720": {
        "size": Size(1280, 720),
        "boxes": [
            AnnotatedBox(
                xmin=753.614501953125,
                ymin=478.3514099121094,
                xmax=901.26953125,
                ymax=598.5467529296875,
                annotation="mug",
            ),
            AnnotatedBox(
                xmin=786.5328979492188,
                ymin=431.84423828125,
                xmax=879.258544921875,
                ymax=493.6415710449219,
                annotation="mug",
            ),
        ],
        "features": ["mug"],
    },
    # Bird 4x3
    "https://picsum.photos/id/50/1280/960": {
        "size": Size(1280, 960),
        "boxes": [
            AnnotatedBox(
                xmin=541.7738037109375,
                ymin=461.9006042480469,
                xmax=765.8594970703125,
                ymax=564.3948974609375,
                annotation="bird",
            )
        ],
        "features": ["bird"],
    },
    # Bird 3x4
    "https://picsum.photos/id/50/960/1280": {
        "size": Size(960, 1280),
        "boxes": [
            AnnotatedBox(
                xmin=349.048095703125,
                ymin=616.0672607421875,
                xmax=648.376708984375,
                ymax=753.064697265625,
                annotation="bird",
            )
        ],
        "features": ["bird"],
    },
    # Watch 4x3
    "https://picsum.photos/id/26/1280/960": {
        "size": Size(1280, 960),
        "boxes": [
            AnnotatedBox(
                xmin=524.8804931640625,
                ymin=508.3810119628906,
                xmax=606.1829223632812,
                ymax=742.041748046875,
                annotation="watch",
            )
        ],
        "features": ["watch"],
    },
    # Cloud 4x3
    "https://picsum.photos/id/29/1280/960": {
        "size": Size(1280, 960),
        "boxes": [
            AnnotatedBox(
                xmin=418.1292419433594,
                ymin=131.03919982910156,
                xmax=1108.3411865234375,
                ymax=287.4080810546875,
                annotation="cloud",
            ),
            AnnotatedBox(
                xmin=34.503334045410156,
                ymin=50.6424446105957,
                xmax=248.73715209960938,
                ymax=168.67054748535156,
                annotation="cloud",
            ),
        ],
        "features": ["cloud"],
    },
    # Turntable needle 4x3
    "https://picsum.photos/id/39/1280/960": {
        "size": Size(1280, 960),
        "boxes": [
            AnnotatedBox(
                xmin=553.6900634765625,
                ymin=288.48541259765625,
                xmax=922.848388671875,
                ymax=523.9489135742188,
                annotation="turntable needle",
            )
        ],
        "features": ["turntable needle"],
    },
    # People 4x3
    "https://picsum.photos/id/42/1280/960": {
        "size": Size(1280, 960),
        "boxes": [
            AnnotatedBox(
                xmin=923.4943237304688,
                ymin=231.84860229492188,
                xmax=1002.992919921875,
                ymax=459.11309814453125,
                annotation="people",
            ),
            AnnotatedBox(
                xmin=713.2783203125,
                ymin=247.23782348632812,
                xmax=782.3455810546875,
                ymax=365.9229431152344,
                annotation="people",
            ),
        ],
        "features": ["people"],
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
            "-pix_fmt",
            "yuv420p",
            "-y",
            "single_cover_4x3_to_16x9.mp4",
        ],
    ),
    "multiple": (
        [
            "-v",
            "encode",
            "-s",
            "640x480",
            "-i",
            "https://picsum.photos/id/22/1280/960",
            "/ft",
            "person",
            "-i",
            "https://picsum.photos/id/26/1280/960",
            "/ft",
            "watch",
            "/id",
            "2",
            "/td",
            "0.5",
            "/tn",
            "circlecrop",
            "/te",
            "linear",
            "-i",
            "https://picsum.photos/id/29/1280/960",
            "/ft",
            "cloud",
            "/id",
            "7",
            "-i",
            "https://picsum.photos/id/39/1280/960",
            "/ft",
            "turntable needle",
            "/tn",
            "revealup",
            "-i",
            "https://picsum.photos/id/42/1280/960",
            "/ft",
            "people",
            "-i",
            "https://picsum.photos/id/50/960/1280",
            "/ft",
            "bird",
            "/if",
            "contain",
            "-o",
            "multiple.mp4",
        ],
        [
            "ffmpeg",
            "-loglevel",
            "warning",
            "-i",
            "https://picsum.photos/id/22/1280/960",
            "-i",
            "https://picsum.photos/id/26/1280/960",
            "-i",
            "https://picsum.photos/id/29/1280/960",
            "-i",
            "https://picsum.photos/id/39/1280/960",
            "-i",
            "https://picsum.photos/id/42/1280/960",
            "-i",
            "https://picsum.photos/id/50/960/1280",
            "-filter_complex",
            "[0]zoompan=z='st(0, clip(time / 5, 0, 1));"
            "st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3));"
            "lerp(1, 2.1818181818181817, ld(0))'"
            ":x=(iw+iw*0.15547246932983394)/2-(iw/zoom/2)"
            ":y=(ih+ih*0.026792081197102968)/2-(ih/zoom/2)"
            ":s=640x480:fps=25:d=125,setsar=sar=1[pz0];"
            "[1]zoompan=z='st(0, clip(time / 2.0, 0, 1));st(0, ld(0));"
            "lerp(1, 4.102564102564102, ld(0))'"
            ":x=(iw+iw*-0.11581172943115237)/2-(iw/zoom/2)"
            ":y=(ih+ih*0.3028771082560222)/2-(ih/zoom/2):s=640x480:fps=25:d=50.0,setsar=sar=1[pz1];"
            "[pz0][pz1]xfade=transition=fade:duration=1:offset=4[xf1];"
            "[2]zoompan=z='st(0, clip(time / 7.0, 0, 1));"
            "st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3));lerp(1, 1.855072463768116, ld(0))'"
            ":x=(iw+iw*0.19238944053649898)/2-(iw/zoom/2)"
            ":y=(ih+ih*-0.5645016670227051)/2-(ih/zoom/2):s=640x480:fps=25:d=175.0,setsar=sar=1[pz2];"
            "[xf1][pz2]xfade=transition=circlecrop:duration=0.5:offset=5.5[xf2];"
            "[3]zoompan=z='st(0, clip(time / 5, 0, 1));"
            "st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3));"
            "lerp(1, 3.4594594594594597, ld(0))'"
            ":x=(iw+iw*0.15420322418212895)/2-(iw/zoom/2)"
            ":y=(ih+ih*-0.15315539042154946)/2-(ih/zoom/2):s=640x480:fps=25:d=125,setsar=sar=1[pz3];"
            "[xf2][pz3]xfade=transition=fade:duration=1:offset=11.5[xf3];"
            "[4]zoompan=z='st(0, clip(time / 5, 0, 1));"
            "st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3));"
            "lerp(1, 4.2105263157894735, ld(0))'"
            ":x=(iw+iw*0.5054598808288575)/2-(iw/zoom/2)"
            ":y=(ih+ih*-0.27948207855224605)/2-(ih/zoom/2):s=640x480:fps=25:d=125,setsar=sar=1[pz4];"
            "[xf3][pz4]xfade=transition=revealup:duration=1:offset=15.5[xf4];"
            "[5]scale=w=360:h=480,pad=w=640:h=480:x=-1:y=-1,zoompan=z='st(0, clip(time / 5, 0, 1));"
            "st(0, if(lt(ld(0), 0.5), 4 * ld(0)^3, 1 - 4 * (1-ld(0))^3));"
            "lerp(1, 5.714285714285714, ld(0))'"
            ":x=(iw+iw*0.021540737152099698)/2-(iw/zoom/2)"
            ":y=(ih+ih*0.06885509490966801)/2-(ih/zoom/2):s=640x480:fps=25:d=125,setsar=sar=1[pz5];"
            "[xf4][pz5]xfade=transition=fade:duration=1:offset=19.5",
            "-r",
            "25",
            "-s",
            "640x480",
            "-pix_fmt",
            "yuv420p",
            "-y",
            "multiple.mp4",
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
