import typing as ta
from dataclasses import dataclass

import torch
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from PIL import Image


@dataclass
class Box:
    x1: float
    y1: float
    x2: float
    y2: float
    width: int
    height: int


class Detector:
    def __init__(self) -> None:
        model_id = "IDEA-Research/grounding-dino-tiny"
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(self.device)

    def detect(self, image: Image.Image, features: ta.Sequence[str]) -> list[Box]:
        # End each feature with a dot
        text = " ".join(feature if feature.endswith(".") else f"{feature}." for feature in features)
        inputs = self.processor(images=image, text=text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)

        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            box_threshold=0.4,
            text_threshold=0.3,
            target_sizes=[image.size[::-1]],
        )
        return [Box(*box, *image.size) for box in results[0]["boxes"]]
