"""Color palettes for fractal rendering."""

import numpy as np
from typing import Tuple

# Each palette is a list of (r, g, b) control points; values are interpolated.
_PALETTES: dict = {
    "fire": [
        (0,   0,   0),
        (128, 0,   0),
        (255, 64,  0),
        (255, 200, 0),
        (255, 255, 200),
    ],
    "ocean": [
        (0,   0,   32),
        (0,   40,  128),
        (0,   140, 200),
        (80,  220, 255),
        (220, 255, 255),
    ],
    "neon": [
        (0,   0,   0),
        (120, 0,   200),
        (0,   0,   255),
        (0,   200, 255),
        (200, 255, 50),
    ],
    "sunset": [
        (15,  10,  40),
        (100, 20,  80),
        (220, 80,  30),
        (255, 180, 50),
        (255, 240, 200),
    ],
    "forest": [
        (0,   5,   0),
        (0,   60,  10),
        (20,  140, 40),
        (120, 220, 80),
        (230, 255, 200),
    ],
    "ice": [
        (0,   0,   20),
        (0,   50,  120),
        (30,  130, 200),
        (150, 210, 255),
        (240, 248, 255),
    ],
    "gold": [
        (10,  0,   0),
        (80,  30,  0),
        (180, 100, 0),
        (255, 200, 50),
        (255, 255, 200),
    ],
    "grayscale": [
        (0,   0,   0),
        (64,  64,  64),
        (128, 128, 128),
        (192, 192, 192),
        (255, 255, 255),
    ],
}

PALETTE_NAMES = list(_PALETTES.keys())


def _build_lut(name: str, size: int = 1024) -> np.ndarray:
    """Build a (size, 3) uint8 lookup table from a named palette."""
    points = _PALETTES[name]
    n = len(points)
    lut = np.zeros((size, 3), dtype=np.uint8)
    for i in range(size):
        t = i / (size - 1) * (n - 1)
        lo = int(t)
        hi = min(lo + 1, n - 1)
        frac = t - lo
        for ch in range(3):
            lut[i, ch] = int(points[lo][ch] * (1 - frac) + points[hi][ch] * frac)
    return lut


def apply_palette(data: np.ndarray, name: str) -> np.ndarray:
    """
    Map a (H, W) float array in [0, 1] to an (H, W, 3) uint8 RGB image.

    Points inside the set (value == 0) are always mapped to black.
    """
    if name not in _PALETTES:
        raise ValueError(f"Unknown palette '{name}'. Choose from: {PALETTE_NAMES}")
    lut = _build_lut(name)
    size = lut.shape[0]
    indices = (data * (size - 1)).astype(int).clip(0, size - 1)
    rgb = lut[indices]
    # Force interior points to black
    rgb[data == 0.0] = [0, 0, 0]
    return rgb


def get_palette_names() -> list:
    return PALETTE_NAMES
