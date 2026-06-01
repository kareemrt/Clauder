"""
Rendering engine.

Two render modes:
  'block'  — Unicode half-blocks (▀) give 2× vertical resolution,
              producing near-square pixels in most terminal fonts.
  'ascii'  — Plain ASCII density characters, no color; portable everywhere.
"""

import math
import sys

from fractalforge.fractals import mandelbrot, julia, burning_ship, newton
from fractalforge.themes import (
    get_color, get_interior, fg, bg, RESET,
    NEWTON_ROOT_COLORS, THEMES,
)

# ASCII density palette (darkest → brightest)
_ASCII_CHARS = " .`-_':,;^~=+<>i!lI?/\\|()1{}[]rcvunxzjftLCJUYXZO0Qoahkbdpqwm*WMB8&%$#@"

# ── coordinate helpers ───────────────────────────────────────────────────────

def _build_viewport(
    width: int,
    height: int,
    center_x: float,
    center_y: float,
    zoom: float,
    mode: str,
) -> tuple:
    """
    Return (x_start, x_step, y_start, y_step, pixel_height).

    Terminal characters are ~2× taller than wide.  In 'block' mode the
    half-block trick provides 2 pixel rows per character row, making each
    pixel approximately square.  In 'ascii' mode we account for the tall
    characters by doubling the y coverage.
    """
    x_range = 3.5 / zoom
    # Both modes: y_range = x_range * 2 * height / width accounts for
    # character aspect ratio (2:1) and the pixel row count per term row.
    y_range = x_range * 2.0 * height / width

    pixel_height = height * 2 if mode == "block" else height

    x_start = center_x - x_range / 2.0
    y_start = center_y - y_range / 2.0
    x_step = x_range / width
    y_step = y_range / pixel_height

    return x_start, x_step, y_start, y_step, pixel_height


# ── per-pixel computation ────────────────────────────────────────────────────

def _pixel_color(
    fractal: str,
    px: float,
    py: float,
    max_iter: int,
    julia_c: tuple,
    theme: str,
) -> tuple:
    """Return the RGB color for a single fractal pixel."""
    if fractal == "newton":
        t, root_idx = newton(px, py, max_iter)
        if t >= 1.0:
            return (0, 0, 0)
        base = NEWTON_ROOT_COLORS[root_idx % 3]
        brightness = 1.0 - t ** 0.5
        return tuple(int(c * (0.25 + 0.75 * brightness)) for c in base)

    if fractal == "mandelbrot":
        val = mandelbrot(px, py, max_iter)
    elif fractal == "julia":
        val = julia(px, py, julia_c[0], julia_c[1], max_iter)
    elif fractal == "burning_ship":
        val = burning_ship(px, py, max_iter)
    else:
        raise ValueError(f"Unknown fractal: {fractal!r}")

    if val >= max_iter:
        return get_interior(theme)

    # Cyclic coloring: multiple passes through the palette create banding detail
    t = math.fmod(val / max_iter * 6.0, 1.0)
    return get_color(t, theme)


# ── main render function ─────────────────────────────────────────────────────

def render(
    fractal: str = "mandelbrot",
    width: int = 80,
    height: int = 24,
    center_x: float = -0.5,
    center_y: float = 0.0,
    zoom: float = 1.0,
    max_iter: int = 256,
    theme: str = "fire",
    mode: str = "block",
    julia_c: tuple = (-0.7, 0.27015),
    show_progress: bool = True,
) -> list:
    """
    Render a fractal and return a list of ANSI-colored (or plain ASCII) strings.

    Parameters
    ----------
    fractal     : 'mandelbrot' | 'julia' | 'burning_ship' | 'newton'
    width       : terminal columns
    height      : terminal rows
    center_x/y  : fractal-space center
    zoom        : magnification factor (1.0 = full default view)
    max_iter    : iteration depth (higher = more detail, slower)
    theme       : color theme name (see themes.THEMES)
    mode        : 'block' for colored Unicode output; 'ascii' for plain text
    julia_c     : (real, imag) constant for Julia / Burning Ship
    show_progress : write a progress indicator to stderr
    """
    x_start, x_step, y_start, y_step, pixel_height = _build_viewport(
        width, height, center_x, center_y, zoom, mode
    )

    lines: list = []

    if mode == "block":
        for row in range(height):
            if show_progress:
                pct = int((row + 1) / height * 100)
                sys.stderr.write(f"\r  Rendering... {pct:3d}%")
                sys.stderr.flush()

            top_py = y_start + (row * 2) * y_step
            bot_py = y_start + (row * 2 + 1) * y_step
            line_parts: list = []

            for col in range(width):
                px = x_start + col * x_step
                rt, gt, bt = _pixel_color(fractal, px, top_py, max_iter, julia_c, theme)
                rb, gb, bb = _pixel_color(fractal, px, bot_py, max_iter, julia_c, theme)
                line_parts.append(
                    f"\033[38;2;{rt};{gt};{bt}m\033[48;2;{rb};{gb};{bb}m▀"
                )

            lines.append("".join(line_parts) + RESET)

    else:  # ascii mode
        for row in range(height):
            if show_progress:
                pct = int((row + 1) / height * 100)
                sys.stderr.write(f"\r  Rendering... {pct:3d}%")
                sys.stderr.flush()

            py = y_start + row * y_step
            chars: list = []

            for col in range(width):
                px = x_start + col * x_step

                if fractal == "newton":
                    t, _ = newton(px, py, max_iter)
                    idx = int((1.0 - t) * (len(_ASCII_CHARS) - 1))
                elif fractal == "mandelbrot":
                    val = mandelbrot(px, py, max_iter)
                    idx = 0 if val >= max_iter else int(
                        val / max_iter * (len(_ASCII_CHARS) - 1)
                    )
                elif fractal == "julia":
                    val = julia(px, py, julia_c[0], julia_c[1], max_iter)
                    idx = 0 if val >= max_iter else int(
                        val / max_iter * (len(_ASCII_CHARS) - 1)
                    )
                elif fractal == "burning_ship":
                    val = burning_ship(px, py, max_iter)
                    idx = 0 if val >= max_iter else int(
                        val / max_iter * (len(_ASCII_CHARS) - 1)
                    )
                else:
                    idx = 0

                chars.append(_ASCII_CHARS[min(idx, len(_ASCII_CHARS) - 1)])

            lines.append("".join(chars))

    if show_progress:
        sys.stderr.write("\r" + " " * 30 + "\r")
        sys.stderr.flush()

    return lines
