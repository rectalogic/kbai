from PIL import Image, ImageDraw

from .detector import ImageBoxes


def debug_image(image: Image.Image, image_boxes: ImageBoxes) -> None:
    draw = ImageDraw.Draw(image)
    for box in image_boxes.boxes:
        draw.rectangle((box.x1, box.y1, box.x2, box.y2), outline="red")
    image.show()
