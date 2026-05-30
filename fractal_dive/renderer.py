"""
Terminal renderer — converts a float escape array to ANSI truecolor output.

Uses Unicode half-block (▄) to double vertical resolution: each terminal
character cell renders TWO pixel rows (top in foreground, bottom in background).
"""

import sys
import numpy as np
from .themes import Palette, THEMES, THEME_ORDER


HALF_BLOCK = "▄"  # ▄


def _rgb_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def _rgb_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


RESET = "\033[0m"
CLEAR = "\033[2J\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def render_frame(
    data: np.ndarray,
    max_iter: int,
    palette: Palette,
    *,
    interior_color: tuple[int, int, int] = (5, 5, 20),
) -> str:
    """
    Render a [height × width] float array to a string of ANSI escape sequences.

    Half-block trick: pairs of rows are merged so each terminal line encodes 2 rows.
    Interior points (escaped at max_iter) are drawn with a deep dark color.
    """
    height, width = data.shape
    # Pad height to even number
    if height % 2:
        data = np.vstack([data, np.full((1, width), float(max_iter))])
        height += 1

    lines: list[str] = []
    for row in range(0, height, 2):
        top_row = data[row]
        bot_row = data[row + 1]
        chars: list[str] = []
        for col in range(width):
            tv = top_row[col]
            bv = bot_row[col]

            if tv >= max_iter:
                tr, tg, tb = interior_color
            else:
                t_norm = (tv % max_iter) / max_iter
                tr, tg, tb = palette(t_norm)

            if bv >= max_iter:
                br, bg, bb = interior_color
            else:
                b_norm = (bv % max_iter) / max_iter
                br, bg, bb = palette(b_norm)

            chars.append(
                _rgb_fg(tr, tg, tb) + _rgb_bg(br, bg, bb) + HALF_BLOCK
            )
        lines.append("".join(chars) + RESET)

    return "\n".join(lines)


def render_static(
    data: np.ndarray,
    max_iter: int,
    theme_name: str = "fire",
    *,
    show_info: bool = True,
) -> None:
    """Print a rendered fractal to stdout."""
    _, palette = THEMES[theme_name]
    frame = render_frame(data, max_iter, palette)
    sys.stdout.write(frame + "\n")
    if show_info:
        sys.stdout.write(
            f"\033[90m  theme: {theme_name}  |  max_iter: {max_iter}  |  "
            f"size: {data.shape[1]}×{data.shape[0]}\033[0m\n"
        )
    sys.stdout.flush()
