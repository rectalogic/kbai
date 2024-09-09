from PIL import Image, ImageDraw

from .structs import KBImage


def debug_image(image: Image.Image, image_boxes: KBImage) -> None:
    """
    Draw outline boxes on the image
    """
    draw = ImageDraw.Draw(image)
    for box in image_boxes.boxes:
        draw.rectangle((box.xmin, box.ymin, box.xmax, box.ymax), outline="red")
    image.show()
