from .debug import debug_image
from .detector import Detector, Size
from .encoder import encode
from .image import load_image

# XXX debugging
if __name__ == "__main__":
    image = load_image("/Users/aw/Downloads/9-640x480.jpg")
    detector = Detector()
    image_boxes = detector.detect(image, ["a phone"])
    # debug_image(image.image, image_boxes)
    encode(Size(320, 240), 30, [image_boxes], 3, "/tmp/pz2.mp4")
