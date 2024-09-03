import io
from dataclasses import dataclass

import httpx
from PIL import Image


@dataclass
class ImageSrc:
    image: Image.Image
    src: str


def load(src: str) -> ImageSrc:
    url = httpx.URL(src)
    if url.is_absolute_url:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
    else:
        with open(src, "rb") as f:
            image = Image.open(f.read())

    return ImageSrc(image, src)
