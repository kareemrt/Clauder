"""Terminal and PNG rendering for fractals."""

import sys
from typing import Optional
import numpy as np

from .palettes import Palette, PALETTES


# Unicode block characters for half-pixel vertical resolution
_UPPER_HALF = "▀"  # ▀
_LOWER_HALF = "▄"  # ▄
_FULL_BLOCK = "█"  # █
_EMPTY = " "

# ANSI escape sequences
_RESET = "\033[0m"


def _rgb_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def _rgb_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


def render_terminal(
    field: np.ndarray,
    palette: Palette,
    width_chars: Optional[int] = None,
) -> str:
    """
    Render a fractal field to a colored terminal string.

    Uses ▀ block characters so each terminal row encodes two pixel rows,
    effectively doubling the vertical resolution.
    """
    height_px, width_px = field.shape

    # Ensure even height for half-block technique
    if height_px % 2 != 0:
        field = field[:-1, :]
        height_px -= 1

    lines = []
    for row in range(0, height_px, 2):
        row_chars = []
        for col in range(width_px):
            t_upper = field[row, col]
            t_lower = field[row + 1, col]
            r_up, g_up, b_up = palette.get_color(t_upper)
            r_lo, g_lo, b_lo = palette.get_color(t_lower)
            # ▀ char: foreground = upper half, background = lower half
            row_chars.append(
                f"{_rgb_fg(r_up, g_up, b_up)}{_rgb_bg(r_lo, g_lo, b_lo)}{_UPPER_HALF}"
            )
        lines.append("".join(row_chars) + _RESET)

    return "\n".join(lines)


def save_png(
    field: np.ndarray,
    palette: Palette,
    path: str,
    scale: int = 1,
) -> None:
    """Save fractal field as a PNG image."""
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow is required for PNG export: pip install Pillow")

    height, width = field.shape
    img_array = np.zeros((height * scale, width * scale, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            color = palette.get_color(field[y, x])
            for dy in range(scale):
                for dx in range(scale):
                    img_array[y * scale + dy, x * scale + dx] = color

    img = Image.fromarray(img_array, "RGB")
    img.save(path)


def render_ascii_art(
    field: np.ndarray,
    chars: str = " .:-=+*#%@",
) -> str:
    """Render fractal as classic ASCII art (no color)."""
    height, width = field.shape
    n = len(chars)
    lines = []
    for row in range(height):
        line = ""
        for col in range(width):
            t = field[row, col]
            if t >= 1.0:
                line += chars[-1]
            else:
                idx = int(t * (n - 1))
                line += chars[idx]
        lines.append(line)
    return "\n".join(lines)


def print_fractal(
    field: np.ndarray,
    palette_name: str = "electric",
    title: str = "",
) -> None:
    """Print a fractal to stdout with optional title."""
    palette = PALETTES.get(palette_name, PALETTES["electric"])
    if title:
        width = field.shape[1]
        border = "═" * (width + 2)
        print(f"╔{border}╗")
        padded = title.center(width + 2)
        print(f"║{padded}║")
        print(f"╚{border}╝")
    rendered = render_terminal(field, palette)
    print(rendered)
    print(_RESET, end="")
