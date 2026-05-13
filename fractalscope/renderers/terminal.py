"""
Terminal renderer using Unicode half-block characters.

Each terminal cell shows two pixel rows via '▀' (upper half block):
the foreground colour is the top pixel and the background is the bottom pixel.
This doubles the effective vertical resolution.
"""

import numpy as np
import sys


_RESET = "\033[0m"


def _ansi_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def _ansi_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


def render_terminal(rgb: np.ndarray, title: str = "") -> str:
    """
    Convert an (H, W, 3) uint8 array to a coloured terminal string.

    Height must be even; if odd, one blank row is appended.
    """
    h, w, _ = rgb.shape
    if h % 2 != 0:
        rgb = np.vstack([rgb, np.zeros((1, w, 3), dtype=np.uint8)])
        h += 1

    lines = []
    if title:
        pad = max(0, (w - len(title) - 4) // 2)
        lines.append(" " * pad + f"  {title}  ")
        lines.append("")

    for row in range(0, h, 2):
        top = rgb[row]
        bot = rgb[row + 1]
        line_parts = []
        for col in range(w):
            tr, tg, tb = int(top[col, 0]), int(top[col, 1]), int(top[col, 2])
            br, bg, bb = int(bot[col, 0]), int(bot[col, 1]), int(bot[col, 2])
            line_parts.append(
                _ansi_fg(tr, tg, tb) + _ansi_bg(br, bg, bb) + "▀"
            )
        line_parts.append(_RESET)
        lines.append("".join(line_parts))

    return "\n".join(lines)


def print_fractal(rgb: np.ndarray, title: str = "") -> None:
    """Print a fractal RGB array directly to stdout."""
    output = render_terminal(rgb, title)
    sys.stdout.write(output + "\n")
    sys.stdout.flush()
