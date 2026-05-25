"""
Rendering engine: maps fractal values to ASCII art and terminal colors.
"""

import re
import sys
import time
from typing import Dict, List, Optional, Tuple

from .fractals import mandelbrot, julia, burning_ship, newton, tricorn, JULIA_PRESETS
from .palettes import (
    CHAR_SETS, COLOR_PALETTES, NEWTON_ROOT_PALETTES,
    RESET, map_to_char, map_to_color,
)


# Curated viewport presets — (fn_name, bounds, palette, chars, julia_c)
FRACTAL_PRESETS: Dict[str, dict] = {
    "mandelbrot":          {"fn": "mandelbrot",    "bounds": (-2.5,  1.0,  -1.25, 1.25), "palette": "fire",   "chars": "standard"},
    "mandelbrot_seahorse": {"fn": "mandelbrot",    "bounds": (-0.76, -0.74, 0.09,  0.12), "palette": "ocean",  "chars": "ultra"},
    "mandelbrot_elephant": {"fn": "mandelbrot",    "bounds": ( 0.27,  0.29,  0.0,   0.02), "palette": "gold",   "chars": "ultra"},
    "burning_ship":        {"fn": "burning_ship",  "bounds": (-2.0,  1.5,  -2.0,   0.5), "palette": "ocean",  "chars": "standard"},
    "newton":              {"fn": "newton",         "bounds": (-1.5,  1.5,  -1.5,   1.5), "palette": "mono",   "chars": "blocks"},
    "tricorn":             {"fn": "tricorn",        "bounds": (-2.5,  1.0,  -1.25,  1.25), "palette": "gold",   "chars": "standard"},
    "julia_rabbit":        {"fn": "julia", "julia_c": JULIA_PRESETS["rabbit"],    "bounds": (-1.5, 1.5, -1.0, 1.0), "palette": "violet", "chars": "standard"},
    "julia_dragon":        {"fn": "julia", "julia_c": JULIA_PRESETS["dragon"],    "bounds": (-1.5, 1.5, -1.0, 1.0), "palette": "forest", "chars": "standard"},
    "julia_spiral":        {"fn": "julia", "julia_c": JULIA_PRESETS["spiral"],    "bounds": (-1.5, 1.5, -1.0, 1.0), "palette": "ice",    "chars": "standard"},
    "julia_galaxy":        {"fn": "julia", "julia_c": JULIA_PRESETS["galaxy"],    "bounds": (-1.5, 1.5, -1.0, 1.0), "palette": "neon",   "chars": "standard"},
    "julia_lightning":     {"fn": "julia", "julia_c": JULIA_PRESETS["lightning"], "bounds": (-1.5, 1.5, -1.0, 1.0), "palette": "ice",    "chars": "standard"},
    "julia_coral":         {"fn": "julia", "julia_c": JULIA_PRESETS["coral"],     "bounds": (-1.5, 1.5, -1.0, 1.0), "palette": "fire",   "chars": "standard"},
}

_ANSI_STRIP = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def _strip_ansi(text: str) -> str:
    return _ANSI_STRIP.sub("", text)


def render_frame(
    fn_name: str,
    bounds: Tuple[float, float, float, float],
    width: int,
    height: int,
    max_iter: int,
    char_set_name: str = "standard",
    palette_name: str = "fire",
    julia_c: Optional[complex] = None,
) -> List[str]:
    """
    Render one fractal frame.  Returns one ANSI-colored string per row.
    Terminal aspect ratio: characters are ~2× taller than wide, so the
    y-span is halved relative to x-span when rendering square regions.
    """
    x_min, x_max, y_min, y_max = bounds
    chars   = CHAR_SETS.get(char_set_name, CHAR_SETS["standard"])
    palette = COLOR_PALETTES.get(palette_name, COLOR_PALETTES["fire"])

    lines: List[str] = []
    for row in range(height):
        parts: List[str] = []
        for col in range(width):
            x = x_min + (x_max - x_min) * col / width
            y = y_max - (y_max - y_min) * row / height
            z = complex(x, y)

            if fn_name == "mandelbrot":
                val   = mandelbrot(z, max_iter)
                char  = map_to_char(val, max_iter, chars)
                color = map_to_color(val, max_iter, palette)

            elif fn_name == "julia":
                c     = julia_c or JULIA_PRESETS["rabbit"]
                val   = julia(z, c, max_iter)
                char  = map_to_char(val, max_iter, chars)
                color = map_to_color(val, max_iter, palette)

            elif fn_name == "burning_ship":
                val   = burning_ship(z, max_iter)
                char  = map_to_char(val, max_iter, chars)
                color = map_to_color(val, max_iter, palette)

            elif fn_name == "newton":
                val, root_idx = newton(z, max_iter)
                root_pal = NEWTON_ROOT_PALETTES[root_idx % 3]
                char  = map_to_char(val, max_iter, chars)
                color = map_to_color(val, max_iter, root_pal)

            elif fn_name == "tricorn":
                val   = tricorn(z, max_iter)
                char  = map_to_char(val, max_iter, chars)
                color = map_to_color(val, max_iter, palette)

            else:
                char, color = " ", ""

            reset = RESET if color else ""
            parts.append(f"{color}{char}{reset}")

        lines.append("".join(parts))
    return lines


def print_frame(lines: List[str], title: str = "") -> None:
    """Print a rendered frame with an optional title box."""
    if title:
        inner = len(title) + 4
        print(f"\n  ╔{'═' * inner}╗")
        print(f"  ║  {title}  ║")
        print(f"  ╚{'═' * inner}╝\n")
    for line in lines:
        print(line)
    print()


def save_frame(lines: List[str], filename: str) -> None:
    """Save a frame to a plain-text file (ANSI codes stripped)."""
    with open(filename, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(_strip_ansi(line) + "\n")


def animate_zoom(
    fn_name: str,
    center: Tuple[float, float],
    width: int,
    height: int,
    max_iter: int,
    frames: int = 30,
    zoom_factor: float = 0.85,
    char_set_name: str = "standard",
    palette_name: str = "fire",
    delay: float = 0.08,
    julia_c: Optional[complex] = None,
) -> None:
    """Animate a smooth zoom into the fractal at *center*."""
    cx, cy = center
    span   = 3.0  # initial full-width span

    try:
        for frame in range(frames):
            half_x = span / 2.0
            # Compensate for terminal character aspect ratio (≈ 2:1 h:w)
            half_y = half_x * (height / width) * 0.5
            bounds = (cx - half_x, cx + half_x, cy - half_y, cy + half_y)

            lines = render_frame(
                fn_name, bounds, width, height, max_iter,
                char_set_name, palette_name, julia_c,
            )

            sys.stdout.write("\033[H\033[J")  # clear screen
            zoom_level = 1.0 / span
            print(f"  Frame {frame + 1:>3}/{frames}  │  Zoom ×{zoom_level:,.1f}  │  Ctrl-C to stop\n")
            sys.stdout.writelines(line + "\n" for line in lines)
            sys.stdout.flush()

            span *= zoom_factor
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n\nAnimation stopped.")
