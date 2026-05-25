"""
Command-line interface for Fractal Canvas.
"""

import argparse
import sys

from .fractals import JULIA_PRESETS
from .palettes import CHAR_SETS, COLOR_PALETTES
from .renderer import FRACTAL_PRESETS, animate_zoom, print_frame, render_frame, save_frame


_GALLERY = [
    # (display_title,       fn_name,        julia_c,                         bounds,                    palette,  chars)
    ("Mandelbrot Set",      "mandelbrot",   None,                            (-2.5,  1.0, -1.25, 1.25), "fire",   "standard"),
    ("Burning Ship",        "burning_ship", None,                            (-2.0,  1.5, -2.0,  0.5),  "ocean",  "standard"),
    ("Newton Basins",       "newton",       None,                            (-1.5,  1.5, -1.5,  1.5),  "mono",   "blocks"),
    ("Tricorn",             "tricorn",      None,                            (-2.5,  1.0, -1.25, 1.25), "gold",   "standard"),
    ("Julia — Rabbit",      "julia",        JULIA_PRESETS["rabbit"],         (-1.5,  1.5, -1.0,  1.0),  "violet", "standard"),
    ("Julia — Dragon",      "julia",        JULIA_PRESETS["dragon"],         (-1.5,  1.5, -1.0,  1.0),  "forest", "standard"),
    ("Julia — Lightning",   "julia",        JULIA_PRESETS["lightning"],      (-1.5,  1.5, -1.0,  1.0),  "ice",    "standard"),
    ("Julia — Galaxy",      "julia",        JULIA_PRESETS["galaxy"],         (-1.5,  1.5, -1.0,  1.0),  "neon",   "standard"),
]

_DEFAULT_BOUNDS = {
    "mandelbrot":   (-2.5,  1.0,  -1.25, 1.25),
    "burning_ship": (-2.0,  1.5,  -2.0,   0.5),
    "newton":       (-1.5,  1.5,  -1.5,   1.5),
    "julia":        (-1.5,  1.5,  -1.0,   1.0),
    "tricorn":      (-2.5,  1.0,  -1.25,  1.25),
}

_EPILOG = """
examples:
  %(prog)s render mandelbrot
  %(prog)s render julia --preset dragon --palette violet --width 120
  %(prog)s render burning_ship --save ship.txt
  %(prog)s gallery --width 100 --height 36
  %(prog)s animate mandelbrot --cx -0.7453 --cy 0.1127 --frames 40
  %(prog)s list
"""

BANNER = r"""
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

   ██████╗ █████╗ ███╗   ██╗██╗   ██╗ █████╗ ███████╗
  ██╔════╝██╔══██╗████╗  ██║██║   ██║██╔══██╗██╔════╝
  ██║     ███████║██╔██╗ ██║██║   ██║███████║███████╗
  ██║     ██╔══██║██║╚██╗██║╚██╗ ██╔╝██╔══██║╚════██║
  ╚██████╗██║  ██║██║ ╚████║ ╚████╔╝ ██║  ██║███████║
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
  ─────────────────────────────────────────────────────
   Terminal Fractal Art Generator  ·  Infinite Depth
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fractal_canvas",
        description="Fractal Canvas — terminal fractal art generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_EPILOG,
    )
    sub = parser.add_subparsers(dest="command")

    # ── render ──────────────────────────────────────────────────────────────
    rp = sub.add_parser("render", help="render a single fractal to the terminal")
    rp.add_argument("fractal", choices=list(_DEFAULT_BOUNDS))
    rp.add_argument("--preset",   choices=list(JULIA_PRESETS), default="rabbit",
                    help="Julia preset (only used when fractal=julia)")
    rp.add_argument("--julia-c",  nargs=2, type=float, metavar=("RE", "IM"),
                    help="custom Julia parameter overrides --preset")
    rp.add_argument("--width",    type=int, default=100)
    rp.add_argument("--height",   type=int, default=40)
    rp.add_argument("--max-iter", type=int, default=100)
    rp.add_argument("--palette",  choices=list(COLOR_PALETTES), default="fire")
    rp.add_argument("--chars",    choices=list(CHAR_SETS), default="standard")
    rp.add_argument("--xmin",     type=float)
    rp.add_argument("--xmax",     type=float)
    rp.add_argument("--ymin",     type=float)
    rp.add_argument("--ymax",     type=float)
    rp.add_argument("--save",     metavar="FILE", help="also write plain-text copy to FILE")

    # ── gallery ──────────────────────────────────────────────────────────────
    gp = sub.add_parser("gallery", help="cycle through a curated fractal gallery")
    gp.add_argument("--width",    type=int, default=80)
    gp.add_argument("--height",   type=int, default=30)
    gp.add_argument("--max-iter", type=int, default=80)
    gp.add_argument("--pause",    type=float, default=0.0,
                    help="seconds to pause between gallery items")

    # ── animate ──────────────────────────────────────────────────────────────
    ap = sub.add_parser("animate", help="animate a zoom into a fractal")
    ap.add_argument("fractal", choices=list(_DEFAULT_BOUNDS))
    ap.add_argument("--preset",   choices=list(JULIA_PRESETS), default="rabbit")
    ap.add_argument("--cx",       type=float, default=-0.7453,
                    help="zoom center X (real axis)")
    ap.add_argument("--cy",       type=float, default=0.1127,
                    help="zoom center Y (imaginary axis)")
    ap.add_argument("--width",    type=int, default=100)
    ap.add_argument("--height",   type=int, default=40)
    ap.add_argument("--max-iter", type=int, default=150)
    ap.add_argument("--frames",   type=int, default=30)
    ap.add_argument("--zoom",     type=float, default=0.85,
                    help="per-frame zoom factor (0 < z < 1, smaller = faster zoom)")
    ap.add_argument("--delay",    type=float, default=0.08,
                    help="seconds between frames")
    ap.add_argument("--palette",  choices=list(COLOR_PALETTES), default="fire")
    ap.add_argument("--chars",    choices=list(CHAR_SETS), default="standard")

    # ── list ─────────────────────────────────────────────────────────────────
    sub.add_parser("list", help="list available fractals, presets, palettes, and char sets")

    args = parser.parse_args()

    if args.command is None:
        print(BANNER)
        parser.print_help()
        return

    if args.command == "list":
        print(BANNER)
        _section("Fractals",       list(_DEFAULT_BOUNDS))
        _section("Julia presets",  list(JULIA_PRESETS))
        _section("Color palettes", list(COLOR_PALETTES))
        _section("Char sets",      list(CHAR_SETS))
        return

    if args.command == "render":
        bounds = list(_DEFAULT_BOUNDS[args.fractal])
        if args.xmin is not None: bounds[0] = args.xmin
        if args.xmax is not None: bounds[1] = args.xmax
        if args.ymin is not None: bounds[2] = args.ymin
        if args.ymax is not None: bounds[3] = args.ymax

        julia_c = None
        if args.fractal == "julia":
            julia_c = (
                complex(args.julia_c[0], args.julia_c[1]) if args.julia_c
                else JULIA_PRESETS[args.preset]
            )

        lines = render_frame(
            args.fractal, tuple(bounds), args.width, args.height,
            args.max_iter, args.chars, args.palette, julia_c,
        )

        title = args.fractal.replace("_", " ").title()
        if args.fractal == "julia":
            title += f"  ({args.preset})"
        print_frame(lines, title)

        if args.save:
            save_frame(lines, args.save)
            print(f"Saved plain-text copy → {args.save}")

    elif args.command == "gallery":
        import time as _time
        print(BANNER)
        for title, fn_name, julia_c, bounds, palette, chars in _GALLERY:
            lines = render_frame(
                fn_name, bounds, args.width, args.height,
                args.max_iter, chars, palette, julia_c,
            )
            print_frame(lines, title)
            if args.pause > 0:
                _time.sleep(args.pause)

    elif args.command == "animate":
        julia_c = JULIA_PRESETS.get(args.preset) if args.fractal == "julia" else None
        animate_zoom(
            args.fractal, (args.cx, args.cy),
            args.width, args.height, args.max_iter,
            args.frames, args.zoom, args.chars, args.palette, args.delay, julia_c,
        )


def _section(heading: str, items: list) -> None:
    print(f"\n  {heading}:")
    print("    " + "  ·  ".join(items))
