"""
Color themes — each theme maps a [0,1] float t to an (R, G, B) tuple.
"""

import math
from typing import Callable, Tuple

RGB = Tuple[int, int, int]
Palette = Callable[[float], RGB]


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _lerp_rgb(c1: RGB, c2: RGB, t: float) -> RGB:
    return (
        int(_lerp(c1[0], c2[0], t)),
        int(_lerp(c1[1], c2[1], t)),
        int(_lerp(c1[2], c2[2], t)),
    )


def _gradient(stops: list[tuple[float, RGB]]) -> Palette:
    """Build a palette from a list of (position, color) stops."""
    stops = sorted(stops, key=lambda s: s[0])

    def palette(t: float) -> RGB:
        t = max(0.0, min(1.0, t))
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                local_t = (t - p0) / (p1 - p0) if p1 > p0 else 0.0
                return _lerp_rgb(c0, c1, local_t)
        return stops[-1][1]

    return palette


# ── Themes ──────────────────────────────────────────────────────────────────

FIRE: Palette = _gradient([
    (0.00, (0, 0, 0)),
    (0.15, (128, 0, 0)),
    (0.40, (220, 60, 0)),
    (0.65, (255, 180, 0)),
    (0.85, (255, 240, 128)),
    (1.00, (255, 255, 255)),
])

OCEAN: Palette = _gradient([
    (0.00, (0, 0, 30)),
    (0.20, (0, 20, 100)),
    (0.45, (0, 100, 180)),
    (0.70, (0, 200, 220)),
    (0.88, (100, 240, 255)),
    (1.00, (255, 255, 255)),
])

ELECTRIC: Palette = _gradient([
    (0.00, (0, 0, 0)),
    (0.25, (80, 0, 160)),
    (0.50, (0, 60, 255)),
    (0.72, (0, 220, 200)),
    (0.88, (180, 255, 80)),
    (1.00, (255, 255, 255)),
])

MIDNIGHT: Palette = _gradient([
    (0.00, (2, 2, 15)),
    (0.30, (10, 10, 60)),
    (0.55, (60, 0, 120)),
    (0.75, (160, 20, 200)),
    (0.90, (240, 160, 255)),
    (1.00, (255, 255, 255)),
])

GOLD: Palette = _gradient([
    (0.00, (10, 5, 0)),
    (0.30, (80, 40, 0)),
    (0.60, (200, 140, 0)),
    (0.82, (255, 220, 80)),
    (1.00, (255, 255, 220)),
])


def psychedelic(t: float) -> RGB:
    """Smooth HSV cycling — full rainbow loop."""
    h = (t * 6.0) % 6.0
    x = 1 - abs(h % 2 - 1)
    v = int(255 * min(1.0, t * 3))
    if h < 1:
        r, g, b = 1, x, 0
    elif h < 2:
        r, g, b = x, 1, 0
    elif h < 3:
        r, g, b = 0, 1, x
    elif h < 4:
        r, g, b = 0, x, 1
    elif h < 5:
        r, g, b = x, 0, 1
    else:
        r, g, b = 1, 0, x
    return (int(r * v), int(g * v), int(b * v))


THEMES: dict[str, tuple[str, Palette]] = {
    "fire":        ("Fire",        FIRE),
    "ocean":       ("Ocean",       OCEAN),
    "electric":    ("Electric",    ELECTRIC),
    "midnight":    ("Midnight",    MIDNIGHT),
    "gold":        ("Gold",        GOLD),
    "psychedelic": ("Psychedelic", psychedelic),
}

THEME_ORDER = list(THEMES.keys())
