"""Export simulations to GIF or PNG using Pillow."""

from __future__ import annotations

from typing import List

import numpy as np
from PIL import Image

# Colour maps: state value → RGB tuple
_MAPS: dict[str, dict[int, tuple[int, int, int]]] = {
    "life":          {0: (10, 12, 20),  1: (0, 230, 110)},
    "highlife":      {0: (10, 12, 20),  1: (0, 200, 255)},
    "seeds":         {0: (10, 12, 20),  1: (255, 80,  0)},
    "day_and_night": {0: (10, 12, 20),  1: (200, 200, 255)},
    "maze":          {0: (10, 12, 20),  1: (255, 215, 0)},
    "brain":         {0: (10, 12, 20),  1: (255, 255, 255), 2: (0, 120, 255)},
    "ant":           {0: (10, 12, 20),  1: (255, 215, 0),   2: (255, 40, 40)},
}
_DEFAULT_MAP: dict[int, tuple[int, int, int]] = {0: (10, 12, 20), 1: (0, 230, 110)}


def _to_image(cells: np.ndarray, cell_size: int, rule: str) -> Image.Image:
    h, w = cells.shape
    cmap = _MAPS.get(rule, _DEFAULT_MAP)
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for state, colour in cmap.items():
        mask = cells == state
        rgb[mask] = colour
    img = Image.fromarray(rgb, "RGB")
    if cell_size > 1:
        img = img.resize((w * cell_size, h * cell_size), Image.NEAREST)
    return img


def export_gif(
    frames: List[np.ndarray],
    output_path: str,
    rule: str = "life",
    cell_size: int = 4,
    fps: int = 12,
    loop: int = 0,
) -> None:
    """Save a list of grid snapshots as an animated GIF."""
    if not frames:
        return
    images = [_to_image(f, cell_size, rule) for f in frames]
    duration = max(1, int(1000 / fps))
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop,
        optimize=False,
    )


def export_png(
    cells: np.ndarray,
    output_path: str,
    rule: str = "life",
    cell_size: int = 6,
) -> None:
    """Save a single grid snapshot as a PNG."""
    _to_image(cells, cell_size, rule).save(output_path)
