"""Terminal rendering for fractal grids."""

import sys
from .palettes import PALETTES, CHARS, RESET


def render_smooth(
    grid: list[list[float]],
    palette: str = "fire",
    char_set: str = "block",
    width: int | None = None,
) -> str:
    """Render a smooth (float) fractal grid to an ANSI string."""
    colors = PALETTES.get(palette, PALETTES["fire"])
    chars = CHARS.get(char_set, CHARS["block"])
    n_colors = len(colors)
    n_chars = len(chars)
    lines = []

    for row in grid:
        buf = []
        for val in row:
            if val == 0.0:
                buf.append(colors[0] + chars[0])
            else:
                ci = int(val * (n_colors - 1))
                chi = int(val * (n_chars - 1))
                ci = max(1, min(n_colors - 1, ci))
                chi = max(1, min(n_chars - 1, chi))
                buf.append(colors[ci] + chars[chi])
        lines.append("".join(buf) + RESET)

    return "\n".join(lines)


def render_bool(
    grid: list[list[bool]],
    on_color: str = "matrix",
    char_set: str = "block",
) -> str:
    """Render a boolean fractal grid to an ANSI string."""
    colors = PALETTES.get(on_color, PALETTES["matrix"])
    chars = CHARS.get(char_set, CHARS["block"])
    on_char = chars[-1]
    off_char = chars[0]
    on_clr = colors[-1]
    off_clr = colors[0]
    lines = []

    for row in grid:
        buf = []
        for cell in row:
            if cell:
                buf.append(on_clr + on_char)
            else:
                buf.append(off_clr + off_char)
        lines.append("".join(buf) + RESET)

    return "\n".join(lines)


def print_header(title: str, subtitle: str = "") -> None:
    bold = "\033[1m"
    cyan = "\033[38;5;51m"
    dim = "\033[2m"
    reset = RESET
    width = 60
    border = cyan + "═" * width + reset
    print(border)
    print(bold + cyan + title.center(width) + reset)
    if subtitle:
        print(dim + subtitle.center(width) + reset)
    print(border)


def print_legend(palette: str, char_set: str) -> None:
    colors = PALETTES.get(palette, PALETTES["fire"])
    chars = CHARS.get(char_set, CHARS["block"])
    n = min(len(colors), len(chars))
    dim = "\033[2m"
    reset = RESET
    swatch = "  " + dim + "gradient: " + reset
    for i in range(n):
        swatch += colors[i] + chars[min(i, len(chars) - 1)]
    swatch += reset + f"  palette={palette}  chars={char_set}"
    print(swatch)
