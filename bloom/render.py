"""Turning a Bloom world into images and animated GIFs."""

from __future__ import annotations

import numpy as np
from PIL import Image

# A small "ember" colormap: black -> deep red -> orange -> white, so live
# cells read as glowing organisms rather than flat greyscale blobs.
_STOPS = np.array(
    [
        [0.00, 0.00, 0.00],
        [0.40, 0.00, 0.05],
        [0.80, 0.20, 0.00],
        [1.00, 0.65, 0.10],
        [1.00, 1.00, 0.85],
    ]
)


def colorize(state: np.ndarray) -> np.ndarray:
    """Map a float grid in [0, 1] to an RGB uint8 image using the ember colormap."""
    clipped = np.clip(state, 0.0, 1.0)
    positions = np.linspace(0.0, 1.0, len(_STOPS))
    rgb = np.stack(
        [np.interp(clipped, positions, _STOPS[:, c]) for c in range(3)], axis=-1
    )
    return (rgb * 255).astype(np.uint8)


def frame_to_image(state: np.ndarray, scale: int = 1) -> Image.Image:
    img = Image.fromarray(colorize(state))
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    return img


def save_png(state: np.ndarray, path: str, scale: int = 4) -> None:
    frame_to_image(state, scale=scale).save(path)


def save_gif(frames: list[np.ndarray], path: str, scale: int = 4, fps: int = 20) -> None:
    images = [
        frame_to_image(f, scale=scale).convert("P", palette=Image.ADAPTIVE, colors=48)
        for f in frames
    ]
    duration_ms = int(1000 / fps)
    images[0].save(
        path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
