# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
from collections.abc import Sequence

from PIL import Image, ImageDraw

from .structs import Box


def debug_image(image: Image.Image, boxes: Sequence[Box]) -> None:
    """
    Draw outline boxes on the image
    """
    draw = ImageDraw.Draw(image)
    print(image.size)
    for box in boxes:
        print(box)
        draw.rectangle((box.xmin, box.ymin, box.xmax, box.ymax), outline="red")
    image.show()
