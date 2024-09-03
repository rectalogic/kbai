import typing as ta

from PIL import Image, ImageDraw

from .detector import Box


def debug_image(image: Image.Image, boxes: ta.Sequence[Box]) -> None:
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle((box.x1, box.y1, box.x2, box.y2), outline="red")
    image.show()
