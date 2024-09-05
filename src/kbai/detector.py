from __future__ import annotations

import typing as ta
from dataclasses import dataclass, field
from fractions import Fraction
from functools import cached_property

import torch
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from .image import ImageSrc


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    @cached_property
    def fraction(self) -> Fraction:
        return Fraction(self.width, self.height)

    def __mul__(self, other: ta.Any) -> Size:
        if isinstance(other, int | float | Fraction):
            return Size(round(self.width * other), round(self.height * other))
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"


@dataclass(frozen=True)
class Box:
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    size: Size = field(init=False)

    def __post_init__(self) -> None:
        # We are frozen so can't assign to self.size
        object.__setattr__(self, "size", Size(round(self.xmax - self.xmin), round(self.ymax - self.ymin)))

    @cached_property
    def center(self) -> tuple[float, float]:
        return self.xmin + self.size.width / 2, self.ymin + self.size.height / 2

    def scaled(self, scale: float) -> Box:
        return Box(
            self.xmin * scale,
            self.ymin * scale,
            self.xmax * scale,
            self.ymax * scale,
        )


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
        if not features:
            return ImageBoxes(image.src, Size(*image.image.size), [])

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
            target_sizes=[image.image.size[::-1]],
        )
        # XXX test if not features found, what is results?
        return ImageBoxes(
            image.src, Size(*image.image.size), [Box(*box.tolist()) for box in results[0]["boxes"]]
        )
