# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import enum
import typing as ta
from dataclasses import dataclass, field
from fractions import Fraction
from functools import cached_property


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


class Transition(enum.StrEnum):
    fade: str = "fade"
    wipeleft: str = "wipeleft"
    wiperight: str = "wiperight"
    wipeup: str = "wipeup"
    wipedown: str = "wipedown"
    slideleft: str = "slideleft"
    slideright: str = "slideright"
    slideup: str = "slideup"
    slidedown: str = "slidedown"
    circlecrop: str = "circlecrop"
    rectcrop: str = "rectcrop"
    distance: str = "distance"
    fadeblack: str = "fadeblack"
    fadewhite: str = "fadewhite"
    radial: str = "radial"
    smoothleft: str = "smoothleft"
    smoothright: str = "smoothright"
    smoothup: str = "smoothup"
    smoothdown: str = "smoothdown"
    circleopen: str = "circleopen"
    circleclose: str = "circleclose"
    vertopen: str = "vertopen"
    vertclose: str = "vertclose"
    horzopen: str = "horzopen"
    horzclose: str = "horzclose"
    dissolve: str = "dissolve"
    pixelize: str = "pixelize"
    diagtl: str = "diagtl"
    diagtr: str = "diagtr"
    diagbl: str = "diagbl"
    diagbr: str = "diagbr"
    hlslice: str = "hlslice"
    hrslice: str = "hrslice"
    vuslice: str = "vuslice"
    vdslice: str = "vdslice"
    hblur: str = "hblur"
    fadegrays: str = "fadegrays"
    wipetl: str = "wipetl"
    wipetr: str = "wipetr"
    wipebl: str = "wipebl"
    wipebr: str = "wipebr"
    squeezeh: str = "squeezeh"
    squeezev: str = "squeezev"
    zoomin: str = "zoomin"
    fadefast: str = "fadefast"
    fadeslow: str = "fadeslow"
    hlwind: str = "hlwind"
    hrwind: str = "hrwind"
    vuwind: str = "vuwind"
    vdwind: str = "vdwind"
    coverleft: str = "coverleft"
    coverright: str = "coverright"
    coverup: str = "coverup"
    coverdown: str = "coverdown"
    revealleft: str = "revealleft"
    revealright: str = "revealright"
    revealup: str = "revealup"
    revealdown: str = "revealdown"


@dataclass
class KBImage:
    src: str
    size: Size
    boxes: list[AnnotatedBox]
    duration: float
    transition_duration: float
    transition: Transition
    feature_text: list[str] | None = None

    def __post_init__(self):
        if self.duration - self.transition_duration <= 0:
            raise ValueError(
                f"Transition {self.transition} duration {self.duration} too short"
                " (transition duration {self.transition_duration})"
            )
