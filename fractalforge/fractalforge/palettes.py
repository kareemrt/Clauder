"""Colour gradients for mapping escape-time values to RGB pixels.

Each palette is a list of `(stop, (r, g, b))` control points with `stop`
in `[0, 1]`. `colour_at` linearly interpolates between the two nearest
stops, and a constant colour is returned for points that never escape.
"""

from __future__ import annotations

RGB = tuple[int, int, int]

INSIDE_COLOUR: RGB = (8, 8, 16)

PALETTES: dict[str, list[tuple[float, RGB]]] = {
    "inferno": [
        (0.00, (0, 0, 4)),
        (0.25, (87, 16, 110)),
        (0.50, (188, 55, 84)),
        (0.75, (249, 142, 9)),
        (1.00, (252, 255, 164)),
    ],
    "ocean": [
        (0.00, (4, 11, 33)),
        (0.30, (8, 65, 92)),
        (0.60, (39, 150, 165)),
        (0.85, (146, 224, 217)),
        (1.00, (237, 255, 245)),
    ],
    "dawn": [
        (0.00, (20, 16, 64)),
        (0.35, (118, 58, 150)),
        (0.65, (235, 111, 113)),
        (0.85, (250, 188, 116)),
        (1.00, (255, 244, 214)),
    ],
    "forest": [
        (0.00, (8, 20, 12)),
        (0.30, (24, 78, 51)),
        (0.60, (92, 158, 87)),
        (0.85, (199, 219, 124)),
        (1.00, (247, 247, 214)),
    ],
}


def _lerp(a: RGB, b: RGB, t: float) -> RGB:
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def colour_at(palette_name: str, t: float) -> RGB:
    """Map `t` in `[0, 1]` to an RGB colour along the named palette."""
    stops = PALETTES[palette_name]
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for (s0, c0), (s1, c1) in zip(stops, stops[1:]):
        if s0 <= t <= s1:
            span = s1 - s0
            local_t = (t - s0) / span if span else 0.0
            return _lerp(c0, c1, local_t)
    return stops[-1][1]


def names() -> list[str]:
    return sorted(PALETTES)
