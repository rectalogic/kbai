import typing as ta
from dataclasses import dataclass
from fractions import Fraction

import torch
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from .image import ImageSrc


@dataclass
class Box:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class Size:
    width: int
    height: int

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.width, self.height)

    def __mul__(self, other: ta.Any):
        if isinstance(other, int | float | Fraction):
            return Size(round(self.width * other), round(self.height * other))
        return NotImplemented

    def __str__(self):
        return f"{self.width}x{self.height}"


@dataclass
class ImageBoxes:
    src: str
    size: Size
    boxes: list[Box]


class Detector:
    def __init__(self) -> None:
        model_id = "IDEA-Research/grounding-dino-tiny"
        if torch.backends.mps.is_available():
            # device = "mps"
            # mps is slower https://github.com/pytorch/pytorch/issues/77799
            device = "cpu"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        self.device = torch.device(device)

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(self.device)

    def detect(self, image: ImageSrc, features: ta.Sequence[str]) -> ImageBoxes:
        # End each feature with a dot
        text = " ".join(feature if feature.endswith(".") else f"{feature}." for feature in features)
        inputs = self.processor(images=image.image, text=text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)

        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            box_threshold=0.4,
            text_threshold=0.3,
            target_sizes=[image.size[::-1]],
        )
        return ImageBoxes(image.src, Fraction(*image.size), [Box(*box) for box in results[0]["boxes"]])
