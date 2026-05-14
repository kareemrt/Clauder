"""Color palettes for fractal rendering.

Each palette is a list of (t, r, g, b) control points, t ∈ [0, 1].
Colors are interpolated linearly between adjacent control points.
"""
from typing import Tuple

_PALETTES = {
    "inferno": [
        (0.000,   0,   0,   4),
        (0.125,  40,  11,  84),
        (0.250, 101,  21, 110),
        (0.375, 159,  42,  99),
        (0.500, 212,  72,  66),
        (0.625, 237, 105,  37),
        (0.750, 245, 148,  16),
        (0.875, 249, 193,  38),
        (1.000, 252, 255, 164),
    ],
    "plasma": [
        (0.000,  13,   8, 135),
        (0.125,  84,   2, 163),
        (0.250, 139,  10, 165),
        (0.375, 185,  50, 137),
        (0.500, 219,  92, 104),
        (0.625, 244, 136,  73),
        (0.750, 254, 188,  43),
        (0.875, 240, 249,  33),
        (1.000, 240, 249,  33),
    ],
    "viridis": [
        (0.000,  68,   1,  84),
        (0.125,  71,  44, 122),
        (0.250,  59,  81, 139),
        (0.375,  44, 113, 142),
        (0.500,  33, 145, 140),
        (0.625,  39, 173, 129),
        (0.750,  92, 200,  99),
        (0.875, 170, 220,  50),
        (1.000, 253, 231,  37),
    ],
    "electric": [
        (0.000,   0,   0,   0),
        (0.100,   0,   0,  80),
        (0.250,   0,  30, 160),
        (0.400,   0, 100, 220),
        (0.550,   0, 200, 255),
        (0.700, 100, 230, 255),
        (0.850, 200, 240, 255),
        (1.000, 255, 255, 255),
    ],
    "fire": [
        (0.000,   0,   0,   0),
        (0.200,  80,   0,   0),
        (0.400, 160,  20,   0),
        (0.600, 220,  80,   0),
        (0.750, 240, 160,   0),
        (0.875, 255, 220,  50),
        (0.950, 255, 255, 180),
        (1.000, 255, 255, 255),
    ],
    "psychedelic": [
        (0.000,   0,   0,   0),
        (0.143, 100,   0, 128),
        (0.286,   0,   0, 255),
        (0.429,   0, 255, 128),
        (0.571,   0, 255,   0),
        (0.714, 255, 255,   0),
        (0.857, 255, 128,   0),
        (1.000, 255,   0, 128),
    ],
}


def get_color(t: float, palette_name: str = "inferno") -> Tuple[int, int, int]:
    """Return an (r, g, b) tuple for position t ∈ [0, 1] in the given palette."""
    t = max(0.0, min(1.0, t))
    palette = _PALETTES.get(palette_name, _PALETTES["inferno"])
    for i in range(len(palette) - 1):
        t0, r0, g0, b0 = palette[i]
        t1, r1, g1, b1 = palette[i + 1]
        if t0 <= t <= t1:
            a = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
            return (
                int(r0 + a * (r1 - r0)),
                int(g0 + a * (g1 - g0)),
                int(b0 + a * (b1 - b0)),
            )
    t_last, r, g, b = palette[-1]
    return (r, g, b)


def list_palettes():
    return list(_PALETTES.keys())
