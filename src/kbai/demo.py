from .debug import debug_image
from .detector import Detector
from .image import load

image = load("http://images.cocodataset.org/val2017/000000039769.jpg")
detector = Detector()
image_boxes = detector.detect(image, ["a cat", "a remote control"])
debug_image(image.image, image_boxes)
