"""Terminal rendering engine for fractal visualizations."""
from __future__ import annotations
import sys
import os
import shutil
import time

from .colormap import PALETTES, RESET, colorize, fg, bg


HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
CLEAR_SCREEN = "\x1b[2J\x1b[H"
GOTO_TOP = "\x1b[H"


def clear_screen() -> None:
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def hide_cursor() -> None:
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()


def show_cursor() -> None:
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()


def terminal_size() -> tuple[int, int]:
    """Return (width, height) of the terminal."""
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines


def _status_bar(
    fractal: str,
    cx: float,
    cy: float,
    zoom: float,
    palette: str,
    max_iter: int,
    render_time: float,
    width: int,
) -> str:
    p = PALETTES[palette]
    info = (
        f" {fg(15)}{fractal}{RESET}  "
        f"{fg(244)}cx={cx:.6f} cy={cy:.6f}  "
        f"zoom={zoom:.1f}x  "
        f"iter={max_iter}  "
        f"palette={p['name']}  "
        f"{render_time*1000:.0f}ms "
    )
    # Pad to width
    plain_len = len(
        f" {fractal}  cx={cx:.6f} cy={cy:.6f}  zoom={zoom:.1f}x  "
        f"iter={max_iter}  palette={p['name']}  {render_time*1000:.0f}ms "
    )
    padding = max(0, width - plain_len) * " "
    return f"{bg(236)}{info}{padding}{RESET}"


def _help_bar(width: int) -> str:
    keys = (
        " [WASD/arrows] pan   [+/-] zoom   "
        "[1-6] palette   [q]uit   [r]eset   "
        "[j]ulia [m]andelbrot [f]ern "
    )
    plain = keys
    pad = max(0, width - len(plain)) * " "
    return f"{bg(234)}{fg(250)}{keys}{pad}{RESET}"


def _normalize_grid(grid: list[list[float]]) -> list[list[float]]:
    """Per-frame normalization with sqrt gamma to maximize color range."""
    import math
    escaped = [t for row in grid for t in row if t > 0.0]
    if not escaped:
        return grid
    tmin = min(escaped)
    tmax = max(escaped) or 1.0
    span = tmax - tmin or 1.0
    out = []
    for row in grid:
        out.append([
            math.sqrt((t - tmin) / span) if t > 0.0 else 0.0
            for t in row
        ])
    return out


def render_fractal(
    grid: list[list[float]],
    palette_name: str,
    width: int,
    height: int,
    fractal: str,
    cx: float,
    cy: float,
    zoom: float,
    max_iter: int,
    render_time: float,
) -> None:
    """Render a computed fractal grid to the terminal."""
    p = PALETTES[palette_name]
    interior_color, interior_char = p["interior"]

    grid = _normalize_grid(grid)

    lines: list[str] = []
    for row in range(height):
        parts: list[str] = []
        for col in range(width):
            t = grid[row][col]
            if t == 0.0:
                parts.append(f"{interior_color}{interior_char}")
            else:
                parts.append(colorize(t, palette_name))
        parts.append(RESET)
        lines.append("".join(parts))

    # Status and help bars use last 2 lines
    status = _status_bar(fractal, cx, cy, zoom, palette_name, max_iter, render_time, width)
    help_b = _help_bar(width)

    output = GOTO_TOP + "\n".join(lines) + "\n" + status + "\n" + help_b
    sys.stdout.write(output)
    sys.stdout.flush()


def render_fern(
    grid: list[list[bool]],
    palette_name: str,
    width: int,
    height: int,
    ifs_name: str,
    render_time: float,
) -> None:
    """Render a Barnsley IFS fractal to the terminal."""
    p = PALETTES[palette_name]
    stops = p["color_stops"]

    lines: list[str] = []
    for row_idx, row in enumerate(grid):
        parts: list[str] = []
        # Vary color by row for a gradient effect
        t = row_idx / max(1, height - 1)
        from .colormap import _interp
        code = _interp(t, stops)
        color = fg(code)
        for cell in row:
            parts.append(f"{color}{'█' if cell else ' '}")
        parts.append(RESET)
        lines.append("".join(parts))

    status_text = (
        f"{bg(236)}{fg(15)} IFS Fractal: {ifs_name}  "
        f"{fg(244)}palette={p['name']}  "
        f"{render_time*1000:.0f}ms "
    )
    pad = max(0, width - len(f" IFS Fractal: {ifs_name}  palette={p['name']}  {render_time*1000:.0f}ms ")) * " "
    status = f"{status_text}{pad}{RESET}"
    help_b = _help_bar(width)

    output = GOTO_TOP + "\n".join(lines) + "\n" + status + "\n" + help_b
    sys.stdout.write(output)
    sys.stdout.flush()


def render_splash(width: int, height: int) -> None:
    """Render the splash/intro screen."""
    logo = [
        r"",
        r"  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗     ███████╗",
        r"  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║     ██╔════╝",
        r"  █████╗  ██████╔╝███████║██║        ██║   ███████║██║     ███████╗ ",
        r"  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║     ╚════██║ ",
        r"  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗███████║ ",
        r"  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝ ",
        r"",
        r"              T E R M I N A L   F R A C T A L   E X P L O R E R",
        r"",
    ]

    subtitle = [
        "  Explore infinite mathematical beauty in your terminal.",
        "",
        "  Fractals available:",
        "    [m]  Mandelbrot Set   — The iconic infinity-zoom fractal",
        "    [j]  Julia Sets       — 8 stunning seed variations",
        "    [f]  Barnsley Fern    — IFS attractors (fern / tree / snowflake)",
        "",
        "  Color palettes:  [1] Cosmic  [2] Fire  [3] Matrix  [4] Ocean  [5] Neon  [6] Gold",
        "",
        "  Navigation:  WASD / arrow keys to pan  |  + / - to zoom",
        "               i / o to change max iterations",
        "               s to save current view as text file",
        "",
        "  Press any key to start...",
    ]

    clear_screen()
    padding_top = max(0, (height - len(logo) - len(subtitle)) // 2)
    print("\n" * padding_top, end="")

    colors = [17, 18, 19, 20, 21, 27, 33, 39, 45, 51]
    for i, line in enumerate(logo):
        color_idx = colors[i % len(colors)]
        print(f"{fg(color_idx)}{line}{RESET}")

    print(f"{fg(252)}", end="")
    for line in subtitle:
        print(line)
    print(RESET, end="", flush=True)
