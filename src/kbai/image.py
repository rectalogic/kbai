# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import io
from dataclasses import dataclass

import httpx
from PIL import Image


@dataclass
class ImageSrc:
    image: Image.Image
    src: str


def load_image(src: str) -> ImageSrc:
    image: Image.Image
    url = httpx.URL(src)
    if url.is_absolute_url:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
    else:
        image = Image.open(src)

    # DINO can't handle alpha
    if image.mode in ("RGBA", "LA"):
        image = image.convert("RGB")
    return ImageSrc(image, src)
