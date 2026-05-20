"""Colour palette definitions — each maps a normalised [0,1] value to an RGB tuple."""

import numpy as np
from typing import Tuple

RGB = Tuple[int, int, int]


def _interp(t: float, stops: list) -> RGB:
    """Linearly interpolate between colour stops.

    Each stop is (position, r, g, b) with position in [0, 1].
    """
    stops = sorted(stops, key=lambda s: s[0])
    if t <= stops[0][0]:
        return stops[0][1], stops[0][2], stops[0][3]
    if t >= stops[-1][0]:
        return stops[-1][1], stops[-1][2], stops[-1][3]
    for i in range(len(stops) - 1):
        p0, r0, g0, b0 = stops[i]
        p1, r1, g1, b1 = stops[i + 1]
        if p0 <= t <= p1:
            f = (t - p0) / (p1 - p0)
            return (int(r0 + f * (r1 - r0)),
                    int(g0 + f * (g1 - g0)),
                    int(b0 + f * (b1 - b0)))
    return 0, 0, 0


def nebula(t: float) -> RGB:
    """Deep-space purple → cyan → white."""
    stops = [
        (0.0,  10,   0,  30),
        (0.2,  60,   0, 120),
        (0.45, 0,  100, 200),
        (0.65, 0,  220, 220),
        (0.85, 180, 240, 255),
        (1.0,  255, 255, 255),
    ]
    return _interp(t, stops)


def fire(t: float) -> RGB:
    """Black → deep red → orange → yellow → white."""
    stops = [
        (0.0,  0,   0,   0),
        (0.25, 180,  0,   0),
        (0.5,  255, 80,   0),
        (0.75, 255, 200,  0),
        (1.0,  255, 255, 200),
    ]
    return _interp(t, stops)


def ocean(t: float) -> RGB:
    """Black → navy → teal → aqua → white."""
    stops = [
        (0.0,  0,   0,  20),
        (0.3,  0,  40, 120),
        (0.6,  0, 160, 180),
        (0.85, 80, 220, 210),
        (1.0, 220, 255, 255),
    ]
    return _interp(t, stops)


def psychedelic(t: float) -> RGB:
    """Cycling rainbow with high saturation."""
    angle = t * 2 * np.pi * 3          # 3 full cycles
    r = int(128 + 127 * np.sin(angle))
    g = int(128 + 127 * np.sin(angle + 2.094))   # 2π/3
    b = int(128 + 127 * np.sin(angle + 4.189))   # 4π/3
    return r, g, b


def cosmic(t: float) -> RGB:
    """Black → gold → white with deep midnight tones."""
    stops = [
        (0.0,   0,   0,   0),
        (0.2,  40,  10,  60),
        (0.45, 120,  40,   0),
        (0.65, 220, 160,   0),
        (0.85, 255, 230, 100),
        (1.0,  255, 255, 255),
    ]
    return _interp(t, stops)


def grayscale(t: float) -> RGB:
    v = int(t * 255)
    return v, v, v


COLORMAPS = {
    "nebula":       nebula,
    "fire":         fire,
    "ocean":        ocean,
    "psychedelic":  psychedelic,
    "cosmic":       cosmic,
    "grayscale":    grayscale,
}


def apply_colormap(data: np.ndarray, name: str = "nebula",
                   gamma: float = 0.5) -> np.ndarray:
    """Convert a 2-D float array (escape values) to an RGB image array (H×W×3)."""
    fn = COLORMAPS.get(name, nebula)
    # Normalise: exclude interior (0) points
    exterior = data > 0
    if exterior.any():
        vmin = data[exterior].min()
        vmax = data[exterior].max()
    else:
        vmin, vmax = 0, 1

    norm = np.where(exterior, (data - vmin) / max(vmax - vmin, 1e-9), 0.0)
    norm = np.clip(norm, 0.0, 1.0)
    norm = np.where(exterior, norm ** gamma, 0.0)   # gamma for contrast

    h, w = data.shape
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Vectorise over unique-enough values
    # Build a 256-entry LUT then index into it — avoids per-pixel Python calls.
    lut = np.array([fn(t / 255.0) for t in range(256)], dtype=np.uint8)  # (256, 3)
    indices = (norm * 255).astype(np.uint8)
    img = lut[indices]   # (H, W, 3)
    return img
