"""
Terminal renderer — draws fractals as ANSI-colored ASCII art.
Uses true-color (24-bit) ANSI codes; falls back to density characters on dumb terminals.
"""

import os
import sys
import math
from typing import Optional, Tuple

from .fractals import mandelbrot, julia, burning_ship, tricorn, multibrot, LANDMARKS
from .palettes import smooth_color, rgb_to_ansi_bg, RESET, DENSITY, PALETTES


def _tty() -> bool:
    return sys.stdout.isatty()


def _size() -> Tuple[int, int]:
    try:
        sz = os.get_terminal_size()
        return sz.columns, sz.lines
    except OSError:
        return 120, 40


def _compute_pixel(fractal: str, real: float, imag: float, max_iter: int,
                   julia_c: Tuple[float, float]) -> Tuple[int, float]:
    if fractal == "julia":
        return julia(real, imag, julia_c[0], julia_c[1], max_iter)
    if fractal == "burning_ship":
        return burning_ship(real, imag, max_iter)
    if fractal == "tricorn":
        return tricorn(real, imag, max_iter)
    if fractal == "multibrot":
        return multibrot(real, imag, power=3, max_iter=max_iter)
    return mandelbrot(real, imag, max_iter)


def render_to_string(
    fractal: str = "mandelbrot",
    cx: float = -0.5,
    cy: float = 0.0,
    zoom: float = 0.75,
    width: Optional[int] = None,
    height: Optional[int] = None,
    max_iter: int = 100,
    palette: str = "classic",
    julia_c: Tuple[float, float] = (-0.7269, 0.1889),
) -> str:
    """
    Render fractal to an ANSI-colored string.
    Each rendered pixel occupies 2 terminal columns (block characters are nearly square).
    """
    tw, th = _size()
    w = width if width else min(tw - 2, 200)
    h = height if height else min(th - 6, 55)

    # Half-width because we print 2 chars per pixel
    cols = w // 2
    rows = h

    scale = 2.0 / zoom
    aspect = cols / rows
    x_min = cx - scale * aspect
    x_max = cx + scale * aspect
    y_min = cy - scale
    y_max = cy + scale

    use_color = _tty()
    lines = []

    for row in range(rows):
        imag = y_max - (y_max - y_min) * row / rows
        line_parts = []

        for col in range(cols):
            real = x_min + (x_max - x_min) * col / cols
            itr, smooth = _compute_pixel(fractal, real, imag, max_iter, julia_c)

            if use_color:
                r, g, b = smooth_color(itr, smooth, max_iter, palette)
                line_parts.append(f"\033[48;2;{r};{g};{b}m  {RESET}")
            else:
                if itr >= max_iter:
                    line_parts.append("██")
                else:
                    t = itr / max_iter
                    idx = int(t * (len(DENSITY) - 1))
                    ch = DENSITY[idx]
                    line_parts.append(ch * 2)

        lines.append("".join(line_parts))

    return "\n".join(lines)


def print_fractal(
    fractal: str = "mandelbrot",
    cx: float = -0.5,
    cy: float = 0.0,
    zoom: float = 0.75,
    max_iter: int = 100,
    palette: str = "classic",
    julia_c: Tuple[float, float] = (-0.7269, 0.1889),
    title: str = "",
    show_info: bool = True,
) -> None:
    """Print a complete fractal panel to stdout."""
    W = _size()[0]
    bar = "━" * min(W - 2, 80)

    BOLD  = "\033[1m"  if _tty() else ""
    CYAN  = "\033[36m" if _tty() else ""
    DIM   = "\033[2m"  if _tty() else ""
    GREEN = "\033[32m" if _tty() else ""

    fractal_names = {
        "mandelbrot":   "Mandelbrot Set",
        "julia":        f"Julia Set  c = {julia_c[0]:+.4f} {julia_c[1]:+.4f}i",
        "burning_ship": "Burning Ship",
        "tricorn":      "Tricorn (Mandelbar)",
        "multibrot":    "Multibrot  d = 3",
    }

    display_name = fractal_names.get(fractal, fractal.title())
    header_text = f"  🌀  Mandelbrot Voyage  ◆  {display_name}"
    if title:
        header_text += f"  —  {title}"

    print(f"\n{BOLD}{CYAN}{bar}{RESET}")
    print(f"{BOLD}{header_text}{RESET}")
    print(f"{CYAN}{bar}{RESET}\n")

    output = render_to_string(fractal=fractal, cx=cx, cy=cy, zoom=zoom,
                               max_iter=max_iter, palette=palette, julia_c=julia_c)
    print(output)

    if show_info:
        palette_color = "  ".join(
            f"\033[48;2;{r};{g};{b}m  {RESET}"
            for r, g, b in (
                smooth_color(int(i / 7 * max_iter * 0.95), i / 7 * max_iter * 0.95, max_iter, palette)
                for i in range(1, 8)
            )
        ) if _tty() else ""

        print(f"\n  {DIM}Center: {cx:+.6f}  {cy:+.6f}i   "
              f"Zoom: {zoom:.2f}×   Max iter: {max_iter}   "
              f"Palette: {palette}{RESET}")
        if palette_color:
            print(f"  {DIM}Colors: {RESET}{palette_color}")

    print(f"\n{BOLD}{CYAN}{bar}{RESET}\n")


def gallery(palettes_to_show: Optional[list] = None, max_iter: int = 120) -> None:
    """Print a quick gallery of all available palettes side by side."""
    palettes_to_show = palettes_to_show or list(PALETTES.keys())
    tw = _size()[0]
    h = 20

    print("\n\033[1m\033[36m  ◆ Color Palette Gallery\033[0m\n")

    for pal in palettes_to_show:
        print(f"\033[1m  ► {pal.upper()}\033[0m")
        print_fractal(
            fractal="mandelbrot",
            cx=-0.5, cy=0.0, zoom=0.75,
            max_iter=max_iter,
            palette=pal,
            show_info=False,
        )
