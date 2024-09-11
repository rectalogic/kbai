# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import enum
import typing as ta
from dataclasses import dataclass, field
from fractions import Fraction
from functools import cached_property

from .easings import Easing
from .transitions import Transition


class Fit(enum.Enum):
    COVER = "cover"
    CONTAIN = "contain"


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
        if self.xmin >= self.xmax or self.ymin >= self.ymax:
            raise ValueError("Invalid Box")
        # We are frozen so can't assign to self.size
        object.__setattr__(
            self,
            "size",
            Size(round(self.xmax - self.xmin), round(self.ymax - self.ymin)),
        )

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


@dataclass(frozen=True)
class AnnotatedBox(Box):
    annotation: str


@dataclass
class KBImage:
    src: str
    size: Size
    fit: Fit
    boxes: list[AnnotatedBox]
    duration: float
    transition_duration: float
    transition: Transition
    transition_easing: Easing
    feature_text: list[str] | None = None

    def __post_init__(self) -> None:
        if self.duration - self.transition_duration <= 0:
            raise ValueError(
                f"Transition {self.transition.value} duration {self.duration} too short"
                " (transition duration {self.transition_duration})"
            )
