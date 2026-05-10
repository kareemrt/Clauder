"""Color palettes and ANSI rendering for fractal output."""

import numpy as np
from typing import List, Tuple


# Each palette is a list of (r, g, b) tuples that get interpolated
PALETTES = {
    "fire": [
        (0, 0, 0),
        (64, 0, 0),
        (128, 0, 0),
        (192, 64, 0),
        (255, 128, 0),
        (255, 192, 64),
        (255, 255, 128),
        (255, 255, 255),
    ],
    "ice": [
        (0, 0, 0),
        (0, 0, 64),
        (0, 32, 128),
        (0, 96, 192),
        (32, 160, 224),
        (128, 208, 248),
        (200, 232, 255),
        (255, 255, 255),
    ],
    "electric": [
        (0, 0, 0),
        (0, 0, 64),
        (0, 0, 128),
        (32, 0, 192),
        (128, 0, 255),
        (192, 64, 255),
        (255, 128, 255),
        (255, 255, 255),
    ],
    "forest": [
        (0, 0, 0),
        (0, 32, 0),
        (0, 64, 32),
        (0, 128, 64),
        (32, 192, 96),
        (128, 224, 128),
        (200, 255, 180),
        (255, 255, 255),
    ],
    "ocean": [
        (0, 0, 0),
        (0, 16, 48),
        (0, 48, 96),
        (0, 96, 160),
        (0, 160, 192),
        (0, 200, 220),
        (128, 230, 240),
        (255, 255, 255),
    ],
    "classic": [
        (0, 0, 0),
        (32, 0, 0),
        (64, 0, 64),
        (0, 64, 128),
        (0, 128, 192),
        (64, 192, 255),
        (200, 240, 255),
        (255, 255, 255),
    ],
    "sunset": [
        (10, 10, 40),
        (80, 20, 60),
        (160, 40, 40),
        (220, 100, 20),
        (240, 160, 40),
        (250, 210, 100),
        (255, 240, 180),
        (255, 255, 255),
    ],
    "monochrome": [
        (0, 0, 0),
        (20, 20, 20),
        (60, 60, 60),
        (100, 100, 100),
        (150, 150, 150),
        (200, 200, 200),
        (230, 230, 230),
        (255, 255, 255),
    ],
}

# Dense ASCII characters ordered by visual density
CHARS_DENSE = " .`'^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
CHARS_SIMPLE = " .-:=+*#%@"
CHARS_BLOCKS = " ░▒▓█"
CHARS_DOTS = " ·∶∷⁘⁙▪▫■"


def _interpolate_palette(
    palette: List[Tuple[int, int, int]], n: int
) -> np.ndarray:
    """Expand a small palette to n colors via linear interpolation."""
    stops = np.array(palette, dtype=np.float64)
    out = np.zeros((n, 3), dtype=np.uint8)
    for i in range(n):
        t = i / max(n - 1, 1) * (len(stops) - 1)
        lo, hi = int(t), min(int(t) + 1, len(stops) - 1)
        frac = t - lo
        out[i] = np.clip(stops[lo] * (1 - frac) + stops[hi] * frac, 0, 255)
    return out


def iterations_to_ansi(
    iterations: np.ndarray,
    max_iter: int = 256,
    palette_name: str = "fire",
    char_set: str = "dense",
    invert: bool = False,
) -> str:
    """Convert a 2D iteration array into a colored ANSI terminal string."""
    palette_data = PALETTES.get(palette_name, PALETTES["fire"])
    colors = _interpolate_palette(palette_data, max_iter)

    chars = {
        "dense": CHARS_DENSE,
        "simple": CHARS_SIMPLE,
        "blocks": CHARS_BLOCKS,
        "dots": CHARS_DOTS,
    }.get(char_set, CHARS_DENSE)

    height, width = iterations.shape
    lines = []

    # Normalize: interior points (iter==0 or not escaped) get black
    norm = iterations.copy()
    interior = norm == 0
    norm = (norm % max_iter) / max_iter  # wrap-around for cycling colors

    for row in range(height):
        parts = []
        for col in range(width):
            raw = iterations[row, col]
            is_interior = interior[row, col]

            if is_interior:
                r, g, b = 0, 0, 0
                ch = " "
            else:
                idx = int(norm[row, col] * (max_iter - 1)) % max_iter
                if invert:
                    idx = max_iter - 1 - idx
                r, g, b = colors[idx]
                char_idx = int(norm[row, col] * (len(chars) - 1))
                ch = chars[min(char_idx, len(chars) - 1)]

            parts.append(f"\033[38;2;{r};{g};{b}m{ch}")
        lines.append("".join(parts) + "\033[0m")

    return "\n".join(lines)


def iterations_to_plain_ascii(
    iterations: np.ndarray,
    max_iter: int = 256,
    char_set: str = "simple",
) -> str:
    """Convert iteration array to plain ASCII art (no ANSI codes)."""
    chars = {
        "dense": CHARS_DENSE,
        "simple": CHARS_SIMPLE,
        "blocks": CHARS_BLOCKS,
    }.get(char_set, CHARS_SIMPLE)

    norm = iterations.copy()
    interior = norm == 0
    norm = (norm % max_iter) / max_iter

    rows = []
    for row in range(iterations.shape[0]):
        line = []
        for col in range(iterations.shape[1]):
            if interior[row, col]:
                line.append(" ")
            else:
                idx = int(norm[row, col] * (len(chars) - 1))
                line.append(chars[min(idx, len(chars) - 1)])
        rows.append("".join(line))
    return "\n".join(rows)
