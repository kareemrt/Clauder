"""
Color themes and iteration-to-color mapping.
Each theme is a gradient defined as a list of RGB waypoints.
"""
from typing import Dict, List, Tuple
import math

Color = Tuple[int, int, int]
Gradient = List[Color]

THEMES: Dict[str, Gradient] = {
    "fire": [
        (0, 0, 0),
        (64, 0, 0),
        (192, 0, 0),
        (255, 100, 0),
        (255, 220, 0),
        (255, 255, 180),
    ],
    "ice": [
        (0, 4, 20),
        (0, 16, 80),
        (0, 60, 200),
        (20, 160, 255),
        (140, 220, 255),
        (240, 248, 255),
    ],
    "gold": [
        (0, 0, 0),
        (48, 20, 0),
        (128, 64, 0),
        (200, 148, 0),
        (255, 218, 40),
        (255, 255, 180),
    ],
    "neon": [
        (0, 0, 0),
        (24, 0, 64),
        (96, 0, 200),
        (200, 0, 255),
        (255, 80, 255),
        (255, 220, 255),
    ],
    "ocean": [
        (0, 4, 24),
        (0, 24, 80),
        (0, 88, 180),
        (0, 180, 192),
        (64, 228, 210),
        (200, 248, 245),
    ],
    "electric": [
        (0, 0, 0),
        (0, 12, 64),
        (0, 72, 220),
        (0, 196, 255),
        (0, 255, 128),
        (180, 255, 90),
    ],
    "inferno": [
        (0, 0, 4),
        (36, 10, 80),
        (96, 18, 110),
        (158, 40, 96),
        (210, 70, 60),
        (244, 124, 18),
        (252, 196, 52),
        (252, 255, 160),
    ],
    "plasma": [
        (13, 8, 135),
        (84, 2, 163),
        (139, 10, 165),
        (185, 50, 137),
        (219, 92, 104),
        (244, 136, 73),
        (254, 188, 43),
        (240, 249, 33),
    ],
    "viridis": [
        (68, 1, 84),
        (59, 82, 139),
        (33, 145, 140),
        (94, 201, 98),
        (253, 231, 37),
    ],
    "grayscale": [
        (0, 0, 0),
        (48, 48, 48),
        (128, 128, 128),
        (200, 200, 200),
        (255, 255, 255),
    ],
    "twilight": [
        (226, 217, 226),
        (166, 141, 175),
        (106, 82, 137),
        (49, 38, 95),
        (10, 10, 38),
        (49, 38, 95),
        (106, 82, 137),
        (166, 141, 175),
        (226, 217, 226),
    ],
    "tropical": [
        (0, 0, 0),
        (0, 80, 60),
        (0, 180, 100),
        (100, 230, 80),
        (255, 240, 20),
        (255, 140, 0),
        (220, 20, 60),
        (255, 255, 255),
    ],
}

THEME_NAMES = list(THEMES.keys())


def _lerp(a: int, b: int, t: float) -> int:
    return max(0, min(255, int(a + (b - a) * t)))


def _gradient_lookup(t: float, gradient: Gradient) -> Color:
    """Map t ∈ [0,1] to a color by interpolating along the gradient."""
    n = len(gradient) - 1
    t = max(0.0, min(1.0, t))
    pos = t * n
    lo = int(pos)
    hi = min(lo + 1, n)
    frac = pos - lo
    r = _lerp(gradient[lo][0], gradient[hi][0], frac)
    g = _lerp(gradient[lo][1], gradient[hi][1], frac)
    b = _lerp(gradient[lo][2], gradient[hi][2], frac)
    return (r, g, b)


def iteration_to_color(
    value: float,
    max_iter: int,
    theme_name: str = "electric",
    cycle_period: float = 64.0,
) -> Color:
    """
    Convert a smooth escape-time value to an RGB color.

    Points inside the set (value == max_iter) are always black.
    Escaped points cycle through the theme gradient based on their value.
    """
    if value >= max_iter:
        return (0, 0, 0)

    gradient = THEMES.get(theme_name, THEMES["electric"])
    # Cyclic coloring: value wraps every `cycle_period` iterations
    t = (value % cycle_period) / cycle_period
    return _gradient_lookup(t, gradient)


def get_colormap_preview(theme_name: str, width: int = 40) -> str:
    """Render a one-line ANSI preview of a color theme."""
    gradient = THEMES.get(theme_name, THEMES["electric"])
    parts = []
    for i in range(width):
        t = i / (width - 1)
        r, g, b = _gradient_lookup(t, gradient)
        parts.append(f"\033[48;2;{r};{g};{b}m ")
    return "".join(parts) + "\033[0m"
