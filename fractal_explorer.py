#!/usr/bin/env python3
"""
Fractal Explorer — stunning terminal & SVG fractal renderer.
Explore the infinite complexity of Mandelbrot, Julia sets, and Burning Ship.
"""

import math
import argparse
import os
import sys
import multiprocessing
from typing import Tuple, List, Optional

# ─────────────────────── ANSI / Color utils ───────────────────────

RESET = "\033[0m"
BOLD  = "\033[1m"

def ansi_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def ansi_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """HSV (all 0-1) → RGB (0-255)."""
    if s == 0:
        c = int(v * 255)
        return c, c, c
    h %= 1.0
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = [(v, t, p), (q, v, p), (p, v, t),
               (p, q, v), (t, p, v), (v, p, q)][i % 6]
    return int(r * 255), int(g * 255), int(b * 255)

# ─────────────────────── Colour palettes ───────────────────────

def _palette_cosmic(t: float) -> Tuple[int, int, int]:
    return hsv_to_rgb(0.60 + t * 0.40, 0.80 + t * 0.20, math.sqrt(t))

def _palette_fire(t: float) -> Tuple[int, int, int]:
    return hsv_to_rgb(t * 0.13, 1.0, min(1.0, t * 1.9))

def _palette_ocean(t: float) -> Tuple[int, int, int]:
    return hsv_to_rgb(0.50 + t * 0.14, 0.65 + t * 0.35, 0.15 + t * 0.85)

def _palette_neon(t: float) -> Tuple[int, int, int]:
    return hsv_to_rgb(t, 1.0, 1.0)

def _palette_gold(t: float) -> Tuple[int, int, int]:
    return hsv_to_rgb(0.09 + t * 0.06, 1.0 - t * 0.25, 0.05 + t * 0.95)

def _palette_ice(t: float) -> Tuple[int, int, int]:
    return hsv_to_rgb(0.55 + t * 0.10, 0.60 - t * 0.30, 0.30 + t * 0.70)

PALETTES = {
    "cosmic": _palette_cosmic,
    "fire":   _palette_fire,
    "ocean":  _palette_ocean,
    "neon":   _palette_neon,
    "gold":   _palette_gold,
    "ice":    _palette_ice,
}

INTERIOR = (0, 0, 12)  # deep blue-black for points in the set

def smooth_to_rgb(smooth: float, max_iter: int, palette: str) -> Tuple[int, int, int]:
    if smooth >= max_iter:
        return INTERIOR
    t = pow(smooth / max_iter, 0.42)
    fn = PALETTES.get(palette, _palette_cosmic)
    return fn(t)

# ─────────────────────── Fractal math ───────────────────────

def _escape(zx: float, zy: float, max_iter: int, cx: float, cy: float, abs_z: bool = False) -> float:
    """Generic escape-time iteration with smooth colouring."""
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            # Normalised iteration count for smooth gradients
            try:
                log_zn = math.log(zx2 + zy2) / 2.0
                nu = math.log(log_zn / math.log(2)) / math.log(2)
                return i + 1.0 - nu
            except (ValueError, ZeroDivisionError):
                return i
        if abs_z:
            zy = abs(2 * zx * zy) + cy
            zx = zx2 - zy2 + cx
        else:
            zy = 2 * zx * zy + cy
            zx = zx2 - zy2 + cx
    return max_iter

def mandelbrot(cx: float, cy: float, max_iter: int) -> float:
    return _escape(0.0, 0.0, max_iter, cx, cy)

def julia(zx: float, zy: float, cx: float, cy: float, max_iter: int) -> float:
    return _escape(zx, zy, max_iter, cx, cy)

def burning_ship(cx: float, cy: float, max_iter: int) -> float:
    return _escape(0.0, 0.0, max_iter, cx, cy, abs_z=True)


# ─────────────────────── Row worker (for multiprocessing) ───────────────────────

def _render_row(args_tuple) -> List[Tuple[int, int, int]]:
    """Render a single pixel row — used by the process pool."""
    (py, pixel_height, cols,
     x_min, x_max, y_min, y_max,
     max_iter, mode, jcx, jcy, palette) = args_tuple

    y = y_min + (y_max - y_min) * py / pixel_height
    row: List[Tuple[int, int, int]] = []
    for px in range(cols):
        x = x_min + (x_max - x_min) * px / cols
        if mode == "mandelbrot":
            v = mandelbrot(x, y, max_iter)
        elif mode == "julia":
            v = julia(x, y, jcx, jcy, max_iter)
        else:  # burning_ship
            v = burning_ship(x, y, max_iter)
        row.append(smooth_to_rgb(v, max_iter, palette))
    return row


# ─────────────────────── Terminal renderer ───────────────────────

def render_terminal(
    cols: int, rows: int,
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    max_iter: int,
    mode: str = "mandelbrot",
    julia_c: Tuple[float, float] = (-0.7, 0.27015),
    palette: str = "cosmic",
    workers: int = 4,
) -> None:
    """
    Render to terminal using Unicode half-block characters (▀).
    Each terminal row represents 2 pixel rows: top = foreground, bottom = background.
    This doubles vertical resolution.
    """
    pixel_height = rows * 2
    jcx, jcy = julia_c

    tasks = [
        (py, pixel_height, cols, x_min, x_max, y_min, y_max,
         max_iter, mode, jcx, jcy, palette)
        for py in range(pixel_height)
    ]

    # Use multiprocessing for speedup
    pixels: List[List[Tuple[int, int, int]]] = []
    try:
        with multiprocessing.Pool(workers) as pool:
            total = len(tasks)
            for i, row in enumerate(pool.imap(_render_row, tasks)):
                pixels.append(row)
                pct = (i + 1) / total * 100
                sys.stderr.write(f"\r  {ansi_fg(150,80,255)}Rendering...{RESET} {pct:.0f}%  ")
                sys.stderr.flush()
    except Exception:
        # Fallback: single-process
        pixels = [_render_row(t) for t in tasks]

    sys.stderr.write("\r" + " " * 40 + "\r")
    sys.stderr.flush()

    output_lines = []
    for r_idx in range(rows):
        top = pixels[r_idx * 2]
        bot = pixels[r_idx * 2 + 1] if r_idx * 2 + 1 < pixel_height else top
        line = ""
        for px in range(cols):
            tr, tg, tb = top[px]
            br, bg_, bb = bot[px]
            line += ansi_fg(tr, tg, tb) + ansi_bg(br, bg_, bb) + "▀" + RESET
        output_lines.append(line)

    print("\n".join(output_lines))


# ─────────────────────── SVG renderer ───────────────────────

def render_svg(
    width: int, height: int,
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    max_iter: int,
    mode: str = "mandelbrot",
    julia_c: Tuple[float, float] = (-0.7, 0.27015),
    palette: str = "cosmic",
    scale: int = 1,
    workers: int = 4,
) -> str:
    """Render fractal as SVG using run-length encoded rectangles."""
    jcx, jcy = julia_c

    tasks = [
        (py, height, width, x_min, x_max, y_min, y_max,
         max_iter, mode, jcx, jcy, palette)
        for py in range(height)
    ]

    rows_data: List[List[Tuple[int, int, int]]] = []
    try:
        with multiprocessing.Pool(workers) as pool:
            total = len(tasks)
            for i, row in enumerate(pool.imap(_render_row, tasks)):
                rows_data.append(row)
                pct = (i + 1) / total * 100
                sys.stderr.write(f"\r  {ansi_fg(100,200,255)}SVG render...{RESET} {pct:.0f}%  ")
                sys.stderr.flush()
    except Exception:
        rows_data = [_render_row(t) for t in tasks]

    sys.stderr.write("\r" + " " * 40 + "\r")
    sys.stderr.flush()

    # Run-length encode each row for compact SVG
    rects: List[str] = []
    for py, row in enumerate(rows_data):
        px = 0
        while px < len(row):
            r, g, b = row[px]
            run = 1
            while px + run < len(row) and row[px + run] == (r, g, b):
                run += 1
            if not (r == 0 and g == 0 and b == 12):  # skip interior (background)
                rects.append(
                    f'<rect x="{px*scale}" y="{py*scale}" '
                    f'width="{run*scale}" height="{scale}" '
                    f'fill="#{r:02x}{g:02x}{b:02x}"/>'
                )
            px += run

    titles = {
        "mandelbrot":   "Mandelbrot Set",
        "julia":        f"Julia Set  c = {jcx:+.4f} {jcy:+.4f}i",
        "burning_ship": "Burning Ship Fractal",
    }
    title = titles.get(mode, mode)
    sw, sh = width * scale, height * scale

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{sw}" height="{sh}" viewBox="0 0 {sw} {sh}">
  <title>Fractal Explorer — {title}</title>
  <desc>Region: ({x_min:.5f}, {y_min:.5f}) → ({x_max:.5f}, {y_max:.5f}) | iter={max_iter} | palette={palette}</desc>
  <rect width="{sw}" height="{sh}" fill="#00000c"/>
  {''.join(rects)}
</svg>"""


# ─────────────────────── Named presets ───────────────────────

PRESETS: dict = {
    "full": {
        "bounds": (-2.5, 1.0, -1.25, 1.25),
        "desc":   "Classic Mandelbrot overview",
    },
    "seahorse": {
        "bounds": (-0.765, -0.690, 0.095, 0.175),
        "desc":   "Seahorse Valley — swirling spirals",
    },
    "elephant": {
        "bounds": (0.240, 0.520, -0.155, 0.105),
        "desc":   "Elephant Valley — fractal proboscises",
    },
    "triple_spiral": {
        "bounds": (-0.093, 0.010, 0.820, 0.925),
        "desc":   "Triple Spiral — mesmerising whorls",
    },
    "deep_zoom": {
        "bounds": (-1.4016, -1.3958, -0.0065, 0.0065),
        "desc":   "Deep zoom near a Misiurewicz point",
    },
    "julia_siegel": {
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "mode":   "julia",
        "c":      (-0.391, -0.587),
        "desc":   "Julia — Siegel disc  c = -0.391 - 0.587i",
    },
    "julia_rabbit": {
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "mode":   "julia",
        "c":      (-0.123, 0.745),
        "desc":   "Douady Rabbit  c = -0.123 + 0.745i",
    },
    "julia_dragon": {
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "mode":   "julia",
        "c":      (-0.4, 0.6),
        "desc":   "Dragon flame  c = -0.4 + 0.6i",
    },
    "julia_dendrite": {
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "mode":   "julia",
        "c":      (0.0, 1.0),
        "desc":   "Dendrite  c = i  (tree-like)",
    },
    "burning_ship": {
        "bounds": (-2.5, 1.5, -2.0, 0.5),
        "mode":   "burning_ship",
        "desc":   "Full Burning Ship fractal",
    },
}


# ─────────────────────── CLI ───────────────────────

def _header() -> None:
    grad_chars = "F R A C T A L   E X P L O R E R"
    coloured = ""
    for i, ch in enumerate(grad_chars):
        t = i / len(grad_chars)
        r, g, b = hsv_to_rgb(0.65 + t * 0.35, 0.9, 1.0)
        coloured += ansi_fg(r, g, b) + ch
    coloured += RESET

    print(f"""
{BOLD}{ansi_fg(120,60,220)}╔══════════════════════════════════════════════════════╗
║     ✦  {coloured}{BOLD}{ansi_fg(120,60,220)}  ✦     ║
║       Infinite complexity, terminal-rendered beauty      ║
╚══════════════════════════════════════════════════════╝{RESET}
""")


def _list_presets() -> None:
    _header()
    print(f"  {BOLD}Available presets:{RESET}\n")
    for name, data in PRESETS.items():
        mode = data.get("mode", "mandelbrot")
        print(f"  {ansi_fg(100,200,255)}{name:<20}{RESET}  {data['desc']}  "
              f"{ansi_fg(180,180,80)}[{mode}]{RESET}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fractal_explorer",
        description="Fractal Explorer — terminal & SVG renderer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fractal_explorer.py                         # full Mandelbrot
  python fractal_explorer.py -p seahorse             # Seahorse Valley
  python fractal_explorer.py -p julia_rabbit         # Douady Rabbit
  python fractal_explorer.py -p burning_ship --palette fire
  python fractal_explorer.py -p triple_spiral -s out.svg
  python fractal_explorer.py --mode julia -c -0.7 0.27015 --palette neon
  python fractal_explorer.py --list-presets
""",
    )

    parser.add_argument("-p", "--preset",       help="Named preset region")
    parser.add_argument("-l", "--list-presets", action="store_true")
    parser.add_argument("--mode", "-m",         choices=["mandelbrot", "julia", "burning_ship"],
                        default="mandelbrot")
    parser.add_argument("-c", "--julia-c",      nargs=2, type=float, metavar=("RE","IM"),
                        default=[-0.7, 0.27015],
                        help="Julia set constant (default: -0.7 0.27015)")
    parser.add_argument("-W", "--width",        type=int, default=110, help="Terminal columns (default: 110)")
    parser.add_argument("-H", "--height",       type=int, default=36,  help="Terminal rows (default: 36)")
    parser.add_argument("-i", "--max-iter",     type=int, default=256)
    parser.add_argument("--palette",            choices=list(PALETTES), default="cosmic")
    parser.add_argument("--bounds",             nargs=4, type=float, metavar=("XMIN","XMAX","YMIN","YMAX"))
    parser.add_argument("-s", "--svg",          metavar="FILE", help="Export SVG")
    parser.add_argument("--svg-size",           nargs=2, type=int, default=[800,600], metavar=("W","H"))
    parser.add_argument("--svg-scale",          type=int, default=1, help="Pixel scale factor for SVG")
    parser.add_argument("-j", "--jobs",         type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--no-header",          action="store_true")

    args = parser.parse_args()

    if args.list_presets:
        _list_presets()
        return

    if not args.no_header:
        _header()

    # Resolve settings
    if args.preset:
        if args.preset not in PRESETS:
            print(f"Unknown preset '{args.preset}'. Run with --list-presets to see options.")
            sys.exit(1)
        p = PRESETS[args.preset]
        x_min, x_max, y_min, y_max = p["bounds"]
        mode    = p.get("mode", "mandelbrot")
        julia_c = tuple(p.get("c", args.julia_c))   # type: ignore[arg-type]
        print(f"  Preset : {BOLD}{args.preset}{RESET}  —  {p['desc']}")
    elif args.bounds:
        x_min, x_max, y_min, y_max = args.bounds
        mode    = args.mode
        julia_c = tuple(args.julia_c)
    else:
        x_min, x_max, y_min, y_max = -2.5, 1.0, -1.25, 1.25
        mode    = args.mode
        julia_c = tuple(args.julia_c)

    palette  = args.palette
    max_iter = args.max_iter

    print(f"  Mode   : {BOLD}{mode}{RESET}  |  Palette : {BOLD}{palette}{RESET}  |  Iterations : {BOLD}{max_iter}{RESET}")
    print(f"  Region : ({x_min:.5f}, {y_min:.5f}) → ({x_max:.5f}, {y_max:.5f})\n")

    # ── Terminal render ──────────────────────────────────────
    render_terminal(
        args.width, args.height,
        x_min, x_max, y_min, y_max,
        max_iter, mode, julia_c, palette,
        workers=args.jobs,
    )

    # ── SVG export ──────────────────────────────────────────
    if args.svg:
        print(f"\n  Generating SVG → {ansi_fg(100,255,150)}{args.svg}{RESET} …")
        svg_w, svg_h = args.svg_size
        svg_content = render_svg(
            svg_w, svg_h,
            x_min, x_max, y_min, y_max,
            max_iter, mode, julia_c, palette,
            scale=args.svg_scale,
            workers=args.jobs,
        )
        with open(args.svg, "w", encoding="utf-8") as fh:
            fh.write(svg_content)
        kb = os.path.getsize(args.svg) // 1024
        print(f"  Saved  : {args.svg}  ({kb} KB)\n")


if __name__ == "__main__":
    main()
