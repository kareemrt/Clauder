"""
Terminal rendering engine.
Uses Unicode half-block characters (▀) with ANSI 24-bit true color.
Each printed character encodes TWO pixels: top (foreground) and bottom (background).
This doubles effective vertical resolution vs. whole-block approaches.
"""
import os
import sys
from typing import List, Optional, Tuple

from .colors import iteration_to_color, Color

UPPER_HALF = "▀"  # ▀
RESET = "\033[0m"


def _ansi_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def _ansi_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


def render_to_string(
    data: List[List[float]],
    max_iter: int,
    theme: str = "electric",
    cycle_period: float = 64.0,
) -> str:
    """
    Convert fractal data to an ANSI-colored terminal string.

    Each output row represents 2 pixel rows using half-block characters.
    """
    height = len(data)
    width = len(data[0]) if data else 0
    lines: List[str] = []

    for row in range(0, height - 1, 2):
        parts: List[str] = []
        for col in range(width):
            top_val = data[row][col]
            bot_val = data[row + 1][col] if row + 1 < height else max_iter

            tr, tg, tb = iteration_to_color(top_val, max_iter, theme, cycle_period)
            br, bg, bb = iteration_to_color(bot_val, max_iter, theme, cycle_period)

            parts.append(
                _ansi_fg(tr, tg, tb)
                + _ansi_bg(br, bg, bb)
                + UPPER_HALF
            )

        lines.append("".join(parts) + RESET)

    return "\n".join(lines)


def print_fractal(
    data: List[List[float]],
    max_iter: int,
    theme: str = "electric",
    cycle_period: float = 64.0,
    title: Optional[str] = None,
    stats: Optional[str] = None,
) -> None:
    """Print a fractal to stdout with optional title/stats."""
    if title:
        width = len(data[0]) if data else 40
        pad = max(0, (width - len(title)) // 2)
        print(" " * pad + f"\033[1;97m{title}\033[0m")
        print()

    rendered = render_to_string(data, max_iter, theme, cycle_period)
    sys.stdout.write(rendered + "\n")
    sys.stdout.flush()

    if stats:
        print(f"\033[90m{stats}\033[0m")


def get_terminal_size() -> Tuple[int, int]:
    """Return (columns, rows) of the current terminal."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 120, 40


def render_progress_bar(progress: float, width: int = 40, theme: str = "electric") -> str:
    """Render a colored progress bar string."""
    filled = int(progress * width)
    bar_chars = "█" * filled + "░" * (width - filled)
    pct = int(progress * 100)
    return f"\033[96m[{bar_chars}] {pct:3d}%\033[0m"


def clear_line() -> None:
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()


def render_info_panel(
    fractal_type: str,
    theme: str,
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    max_iter: int,
    width: int,
    height: int,
) -> str:
    """Render a bordered info panel string."""
    zoom = 3.5 / (x_max - x_min)
    cx = (x_min + x_max) / 2
    cy = (y_min + y_max) / 2

    lines = [
        f"  Fractal  : {fractal_type.replace('_', ' ').title()}",
        f"  Theme    : {theme}",
        f"  Center   : ({cx:.6f}, {cy:.6f})",
        f"  Zoom     : {zoom:.2f}×",
        f"  Max iter : {max_iter}",
        f"  Size     : {width}×{height} px",
    ]

    panel_width = max(len(l) for l in lines) + 4
    border = "─" * (panel_width - 2)
    result = [f"\033[90m╭{border}╮\033[0m"]
    for line in lines:
        padding = " " * (panel_width - 2 - len(line))
        result.append(f"\033[90m│\033[0m{line}{padding}\033[90m│\033[0m")
    result.append(f"\033[90m╰{border}╯\033[0m")
    return "\n".join(result)
