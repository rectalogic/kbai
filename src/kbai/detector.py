# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import typing as ta

import torch
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from .image import ImageSrc
from .structs import AnnotatedBox


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

    def detect(self, image: ImageSrc, features: ta.Sequence[str]) -> list[AnnotatedBox]:
        if not features:
            return []

        # End each lowercase feature with a dot
        text = " ".join(
            feature.lower() if feature.endswith(".") else f"{feature.lower()}." for feature in features
        )

        inputs = self.processor(images=image.image, text=text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)

        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            box_threshold=0.5,
            text_threshold=0.3,
            target_sizes=[image.image.size[::-1]],
        )
        return [
            AnnotatedBox(*box.tolist(), label)
            for box, label in zip(results[0]["boxes"], results[0]["labels"], strict=True)
        ]
