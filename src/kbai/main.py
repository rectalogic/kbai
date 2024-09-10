# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import argparse

from .debug import debug_image
from .detector import Detector
from .encoder import encode
from .image import load_image
from .structs import KBImage, Size


def encode_main(args: argparse.Namespace) -> None:
    fps = args.framerate
    size = args.size
    output = args.output
    default_image_duration = args.default_image_duration
    default_transition_duration = args.default_transition_duration
    default_transition_name = args.default_transition_name
    default_feature_text = args.default_feature_text
    detector = Detector()
    kbimages: list[KBImage] = []
    for imageinfo in args.image:
        image = load_image(imageinfo["image"])
        boxes = detector.detect(image, imageinfo.get("feature_text", default_feature_text))
        kbimages.append(
            KBImage(
                image.src,
                Size(*image.image.size),
                boxes,
                duration=imageinfo.get("image_duration", default_image_duration),
                transition_duration=imageinfo.get("transition_duration", default_transition_duration),
                transition=imageinfo.get("transition_name", default_transition_name),
                feature_text=imageinfo.get("feature_text", default_feature_text),
            )
        )

    encode(size, fps, kbimages, output)


def detect_main(args: argparse.Namespace) -> None:
    image = load_image(args.image)
    detector = Detector()
    boxes = detector.detect(image, args.feature)
    debug_image(image.image, boxes)
