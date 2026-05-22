"""Coloring algorithms and palette generation for fractals."""

import numpy as np
from typing import Tuple


# Named palettes as (R, G, B) control points
PALETTES = {
    "inferno": [
        (0, 0, 4),
        (40, 11, 84),
        (101, 21, 110),
        (159, 42, 99),
        (212, 72, 66),
        (245, 125, 21),
        (250, 193, 39),
        (252, 255, 164),
    ],
    "ocean": [
        (3, 5, 18),
        (6, 22, 58),
        (10, 68, 120),
        (15, 130, 176),
        (40, 190, 200),
        (120, 220, 230),
        (200, 240, 250),
        (255, 255, 255),
    ],
    "fire": [
        (0, 0, 0),
        (30, 0, 0),
        (100, 10, 0),
        (180, 30, 0),
        (230, 80, 0),
        (255, 160, 20),
        (255, 230, 100),
        (255, 255, 200),
    ],
    "psychedelic": [
        (0, 0, 50),
        (80, 0, 120),
        (0, 80, 200),
        (0, 200, 100),
        (200, 200, 0),
        (255, 100, 0),
        (200, 0, 100),
        (100, 0, 200),
    ],
    "grayscale": [
        (0, 0, 0),
        (255, 255, 255),
    ],
    "copper": [
        (0, 0, 0),
        (50, 25, 10),
        (120, 70, 30),
        (180, 110, 60),
        (220, 150, 90),
        (255, 200, 140),
        (255, 230, 190),
        (255, 255, 230),
    ],
}


def _interpolate_palette(palette: list, n: int = 256) -> np.ndarray:
    """Linearly interpolate a control-point palette to n colors."""
    pts = np.array(palette, dtype=float)
    result = np.zeros((n, 3), dtype=np.uint8)
    stops = np.linspace(0, n - 1, len(pts))
    for ch in range(3):
        result[:, ch] = np.interp(np.arange(n), stops, pts[:, ch]).astype(np.uint8)
    return result


def apply_colormap(
    iteration_counts: np.ndarray,
    max_iter: int,
    palette_name: str = "inferno",
    cycle: float = 1.0,
) -> np.ndarray:
    """Map iteration counts to an RGB image array."""
    palette = _interpolate_palette(PALETTES.get(palette_name, PALETTES["inferno"]))

    normalized = np.where(
        iteration_counts >= max_iter,
        0.0,
        (iteration_counts % (max_iter * cycle)) / (max_iter * cycle),
    )

    indices = (normalized * 255).astype(int)
    rgb = palette[indices]

    # Interior of the set is always black
    rgb[iteration_counts >= max_iter] = [0, 0, 0]
    return rgb


def rgb_to_ansi_block(r: int, g: int, b: int) -> str:
    """Return ANSI escape sequence for a colored block character."""
    return f"\033[48;2;{r};{g};{b}m  \033[0m"


def rgb_to_ansi_char(r: int, g: int, b: int, char: str = "█") -> str:
    """Return ANSI escape for a colored foreground character."""
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"


ASCII_GRADIENT = " .:-=+*#%@█"


def iteration_to_ascii(value: float, max_iter: int) -> str:
    """Map an iteration count to an ASCII gradient character."""
    if value >= max_iter:
        return " "
    normalized = value / max_iter
    idx = int(normalized * (len(ASCII_GRADIENT) - 1))
    return ASCII_GRADIENT[idx]
