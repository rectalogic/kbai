from .detector import Detector
from .image import load
from .debug import debug_image


image = load("http://images.cocodataset.org/val2017/000000039769.jpg")
detector = Detector()
boxes = detector.detect(image.image, ["a cat", "a remote control"])
debug_image(image.image, boxes)
