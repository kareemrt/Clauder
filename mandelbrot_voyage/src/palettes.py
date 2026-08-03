"""
Color palettes and smooth coloring for fractal visualization.
"""

import math
import colorsys
from typing import Tuple

ColorRGB = Tuple[int, int, int]


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _lerp_rgb(c1: ColorRGB, c2: ColorRGB, t: float) -> ColorRGB:
    return (
        max(0, min(255, int(_lerp(c1[0], c2[0], t)))),
        max(0, min(255, int(_lerp(c1[1], c2[1], t)))),
        max(0, min(255, int(_lerp(c1[2], c2[2], t)))),
    )


def _gradient(stops: list, t: float) -> ColorRGB:
    """Map t ∈ [0,1] through a list of RGB color stops."""
    t = max(0.0, min(1.0, t))
    n = len(stops) - 1
    pos = t * n
    idx = min(int(pos), n - 1)
    return _lerp_rgb(stops[idx], stops[idx + 1], pos - idx)


# Each palette is a list of RGB tuples. Index 0 = t=0, last = t=1.
PALETTES: dict = {
    "classic": [
        (0,   0,   0),
        (0,   7,  100),
        (32,  107, 203),
        (237, 255, 255),
        (255, 170,   0),
        (0,   2,   0),
    ],
    "fire": [
        (0,   0,   0),
        (35,  0,   0),
        (120, 15,   0),
        (220, 70,   0),
        (255, 165,   0),
        (255, 235, 120),
        (255, 255, 220),
    ],
    "electric": [
        (0,   0,   0),
        (5,   0,  50),
        (40,  0, 130),
        (0,  70, 220),
        (0, 200, 255),
        (100, 240, 255),
        (220, 255, 255),
    ],
    "ocean": [
        (0,   0,   0),
        (0,   5,  30),
        (0,  25,  80),
        (0,  70, 130),
        (0, 130, 180),
        (40, 175, 210),
        (150, 220, 245),
        (240, 250, 255),
    ],
    "neon": [
        (0,   0,   0),
        (20,   0,  20),
        (80,   0, 100),
        (180,   0, 200),
        (255,   0, 255),
        (255, 100,   0),
        (255, 255,   0),
        (255, 255, 255),
    ],
    "matrix": [
        (0,   0,   0),
        (0,  10,   0),
        (0,  40,   0),
        (0, 100,  10),
        (0, 180,  30),
        (50, 230,  80),
        (180, 255, 180),
    ],
    "sunset": [
        (5,   0,  30),
        (40,   0,  80),
        (130,   0,  80),
        (220,  40,  20),
        (255, 110,   0),
        (255, 190,  60),
        (255, 245, 200),
    ],
    "ice": [
        (0,   0,   0),
        (0,  10,  30),
        (0,  40, 100),
        (30, 110, 200),
        (100, 190, 255),
        (200, 235, 255),
        (255, 255, 255),
    ],
}


def smooth_color(iteration: int, smooth_val: float, max_iter: int, palette_name: str = "classic") -> ColorRGB:
    """
    Map smooth escape value → RGB using the chosen palette.
    Points inside the set (iteration == max_iter) return black.
    """
    if iteration >= max_iter:
        return (0, 0, 0)

    palette = PALETTES.get(palette_name, PALETTES["classic"])

    # Normalize the smooth value and apply a sqrt curve for visual depth
    t = smooth_val / max_iter
    t = math.sqrt(t)

    # Cycle through palette multiple times for banded effects
    t = (t * 3.5) % 1.0

    return _gradient(palette, t)


# ─── ANSI Terminal support ─────────────────────────────────────────────────────

def rgb_to_ansi_bg(r: int, g: int, b: int) -> str:
    """24-bit ANSI background color escape (xterm 256 / true-color terminals)."""
    return f"\033[48;2;{r};{g};{b}m"


RESET = "\033[0m"

# ASCII density characters, darkest to brightest (for monochrome terminals)
DENSITY = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
