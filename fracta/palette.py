"""Color palettes used to map scalar fields to RGB images."""

from __future__ import annotations

import numpy as np

# Each palette is a list of (stop, r, g, b) control points, stop in [0, 1].
# Colors are linearly interpolated between stops.
_PALETTES: dict[str, list[tuple[float, int, int, int]]] = {
    "ocean": [
        (0.00, 4, 7, 30),
        (0.20, 9, 38, 87),
        (0.45, 12, 90, 145),
        (0.70, 80, 188, 196),
        (0.90, 220, 240, 220),
        (1.00, 255, 255, 255),
    ],
    "fire": [
        (0.00, 5, 0, 10),
        (0.25, 60, 8, 30),
        (0.50, 160, 30, 20),
        (0.75, 235, 120, 15),
        (0.92, 255, 220, 90),
        (1.00, 255, 255, 240),
    ],
    "forest": [
        (0.00, 6, 14, 8),
        (0.30, 12, 60, 30),
        (0.55, 40, 110, 45),
        (0.80, 150, 190, 80),
        (1.00, 245, 250, 220),
    ],
    "ultraviolet": [
        (0.00, 5, 0, 15),
        (0.30, 50, 5, 90),
        (0.55, 120, 20, 160),
        (0.78, 210, 80, 220),
        (1.00, 255, 220, 250),
    ],
    "mono": [
        (0.00, 0, 0, 0),
        (1.00, 255, 255, 255),
    ],
}


def available_palettes() -> list[str]:
    return sorted(_PALETTES)


def get_palette_lut(name: str, size: int = 2048) -> np.ndarray:
    """Build a lookup table of shape (size, 3) uint8 for the named palette."""
    if name not in _PALETTES:
        raise ValueError(f"Unknown palette {name!r}. Options: {available_palettes()}")
    stops = _PALETTES[name]
    positions = np.array([s[0] for s in stops])
    colors = np.array([s[1:] for s in stops], dtype=np.float64)
    xs = np.linspace(0.0, 1.0, size)
    lut = np.empty((size, 3), dtype=np.float64)
    for channel in range(3):
        lut[:, channel] = np.interp(xs, positions, colors[:, channel])
    return np.clip(lut, 0, 255).astype(np.uint8)


def apply_palette(values: np.ndarray, name: str) -> np.ndarray:
    """Map a 2D array of values in [0, 1] to an RGB uint8 image."""
    lut = get_palette_lut(name)
    idx = np.clip((values * (len(lut) - 1)).astype(np.int64), 0, len(lut) - 1)
    return lut[idx]
