"""Terminal rendering — converts iteration grids to colored ASCII art."""

import sys
import os
from typing import List, Tuple, Optional

from .colors import (
    RESET, BOLD, ansi_fg, iter_to_char, iter_to_color, PALETTES, ASCII_SETS
)


def supports_color() -> bool:
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    term = os.environ.get("TERM", "")
    colorterm = os.environ.get("COLORTERM", "")
    return colorterm in ("truecolor", "24bit") or "256" in term or term == "xterm-color"


def render_grid_to_string(
    grid: List[List[int]],
    max_iters: int,
    palette: str = "plasma",
    charset: str = "dense",
    color: bool = True,
) -> str:
    use_color = color and supports_color()
    lines = []
    for row in grid:
        parts = []
        for iters in row:
            char = iter_to_char(iters, max_iters, charset)
            if use_color:
                r, g, b = iter_to_color(iters, max_iters, palette)
                parts.append(f"{ansi_fg(r, g, b)}{char}")
            else:
                parts.append(char)
        if use_color:
            lines.append("".join(parts) + RESET)
        else:
            lines.append("".join(parts))
    return "\n".join(lines)


def render_sierpinski_colored(rows: List[str], color: bool = True) -> str:
    use_color = color and supports_color()
    if not use_color:
        return "\n".join(rows)

    out = []
    total = len(rows)
    for i, row in enumerate(rows):
        t = i / max(total - 1, 1)
        # gradient: red → gold → white
        r = min(255, int(180 + 75 * t))
        g = min(255, int(100 + 155 * t))
        b = min(255, int(20 + 235 * t))
        colored = row.replace("▲", f"{ansi_fg(r, g, b)}▲{RESET}")
        out.append(colored)
    return "\n".join(out)


def print_header(title: str, subtitle: str = "") -> None:
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    border = "─" * width
    use_color = supports_color()
    if use_color:
        print(f"\033[38;2;100;200;255m{border}{RESET}")
        print(f"{BOLD}\033[38;2;150;255;200m{'  ' + title:^{width}}{RESET}")
        if subtitle:
            print(f"\033[38;2;180;180;180m{subtitle:^{width}}{RESET}")
        print(f"\033[38;2;100;200;255m{border}{RESET}")
    else:
        print(border)
        print(f"{'  ' + title:^{width}}")
        if subtitle:
            print(f"{subtitle:^{width}}")
        print(border)


def print_legend(palette: str, charset: str, fractal: str, params: dict) -> None:
    use_color = supports_color()
    info = (
        f"  Fractal: {fractal}  |  Palette: {palette}  |  "
        f"Charset: {charset}  |  " +
        "  ".join(f"{k}: {v}" for k, v in params.items())
    )
    if use_color:
        print(f"\033[38;2;150;150;150m{info}{RESET}")
    else:
        print(info)


def list_options() -> None:
    use_color = supports_color()

    def header(s: str) -> str:
        return f"\033[38;2;100;200;255m{BOLD}{s}{RESET}" if use_color else s

    def item(k: str, v: str) -> str:
        key = f"\033[38;2;200;230;100m{k}{RESET}" if use_color else k
        return f"  {key:<12} {v}"

    print(header("\nFractals:"))
    for name, desc in [
        ("mandelbrot", "The iconic Mandelbrot set"),
        ("julia",      "Julia set — configurable C parameter"),
        ("burning",    "Burning Ship fractal (a spiky variant)"),
    ]:
        print(item(name, desc))

    print(header("\nPalettes:"))
    for name in PALETTES:
        print(item(name, ""))

    print(header("\nCharacter Sets:"))
    for name, chars in ASCII_SETS.items():
        print(item(name, "".join(chars[:8]) + "…"))

    print()
