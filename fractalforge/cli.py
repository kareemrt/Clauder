"""Command-line interface for FractalForge."""

import argparse
import os
import re
import sys

from fractalforge import __version__
from fractalforge.renderer import render
from fractalforge.themes import THEMES, RESET, BOLD, HIDE_CURSOR, SHOW_CURSOR

# ── Preset configurations ────────────────────────────────────────────────────

PRESETS: dict = {
    "mandelbrot": {
        "fractal": "mandelbrot",
        "center_x": -0.5, "center_y": 0.0, "zoom": 1.0,
        "desc": "Classic full Mandelbrot view",
    },
    "seahorse": {
        "fractal": "mandelbrot",
        "center_x": -0.7436438885619, "center_y": 0.1318259042053, "zoom": 800.0,
        "desc": "Seahorse Valley — deep spiral arms",
    },
    "elephant": {
        "fractal": "mandelbrot",
        "center_x": 0.3, "center_y": 0.0, "zoom": 10.0,
        "desc": "Elephant Valley — bulging lobes",
    },
    "triple-spiral": {
        "fractal": "mandelbrot",
        "center_x": -0.7269, "center_y": 0.1889, "zoom": 200.0,
        "desc": "Triple-spiral — deep zoom detail",
    },
    "julia": {
        "fractal": "julia",
        "center_x": 0.0, "center_y": 0.0, "zoom": 1.0,
        "julia_cr": -0.7, "julia_ci": 0.27015,
        "desc": "Classic symmetric Julia set",
    },
    "julia-dragon": {
        "fractal": "julia",
        "center_x": 0.0, "center_y": 0.0, "zoom": 1.0,
        "julia_cr": -0.8, "julia_ci": 0.156,
        "desc": "Dragon-wing Julia set",
    },
    "julia-dendrite": {
        "fractal": "julia",
        "center_x": 0.0, "center_y": 0.0, "zoom": 1.0,
        "julia_cr": 0.0, "julia_ci": 1.0,
        "desc": "Dendrite (fractal tree) Julia set",
    },
    "burning-ship": {
        "fractal": "burning_ship",
        "center_x": -1.75, "center_y": -0.035, "zoom": 3.5,
        "desc": "Burning Ship — the iconic hull",
    },
    "newton": {
        "fractal": "newton",
        "center_x": 0.0, "center_y": 0.0, "zoom": 1.0,
        "desc": "Newton z³−1 root basins",
    },
}

# ── Helpers ──────────────────────────────────────────────────────────────────

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _term_size() -> tuple:
    try:
        cols, rows = os.get_terminal_size()
    except OSError:
        cols, rows = 80, 24
    return cols, max(rows - 2, 10)


def _print_banner():
    banner = f"""{BOLD}
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝{RESET}

  Terminal fractal art generator  v{__version__}
"""
    print(banner)


def _print_info():
    _print_banner()
    print(f"  {'PRESET':<20} {'FRACTAL':<15} DESCRIPTION")
    print("  " + "─" * 60)
    for name, p in PRESETS.items():
        print(f"  {name:<20} {p['fractal']:<15} {p['desc']}")

    print(f"\n  Themes: {', '.join(THEMES.keys())}")
    print(f"  Fractals: mandelbrot, julia, burning_ship, newton\n")


# ── CLI entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="fractalforge",
        description="FractalForge — render fractal art in your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python main.py                               default Mandelbrot, fire theme
  python main.py --preset seahorse             Seahorse Valley deep zoom
  python main.py --fractal julia --theme ocean ocean-blue Julia set
  python main.py --fractal newton --theme neon Newton root basins in neon
  python main.py --cx -0.745 --cy 0.1 --zoom 60 --theme plasma  custom zoom
  python main.py --ascii --preset mandelbrot   no-color ASCII output
  python main.py --save render.txt             save plain-text copy
  python main.py --list                        show all presets & themes
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--list", action="store_true", help="list presets and themes")

    frac = parser.add_argument_group("fractal")
    frac.add_argument(
        "--fractal", choices=["mandelbrot", "julia", "burning_ship", "newton"],
        default="mandelbrot",
    )
    frac.add_argument("--preset", choices=list(PRESETS.keys()), metavar="PRESET")
    frac.add_argument("--cx", type=float, metavar="X", help="center real coordinate")
    frac.add_argument("--cy", type=float, metavar="Y", help="center imaginary coordinate")
    frac.add_argument("--zoom", type=float, default=None, help="zoom level (default 1.0)")
    frac.add_argument("--max-iter", type=int, default=256, metavar="N")
    frac.add_argument("--julia-cr", type=float, default=-0.7, metavar="R",
                      help="Julia/custom c real part")
    frac.add_argument("--julia-ci", type=float, default=0.27015, metavar="I",
                      help="Julia/custom c imaginary part")

    disp = parser.add_argument_group("display")
    disp.add_argument("--theme", choices=list(THEMES.keys()), default="fire")
    disp.add_argument("--width", type=int, metavar="W")
    disp.add_argument("--height", type=int, metavar="H")
    disp.add_argument("--ascii", action="store_true",
                      help="ASCII density mode (no ANSI color)")
    disp.add_argument("--no-progress", action="store_true")

    out = parser.add_argument_group("output")
    out.add_argument("--save", metavar="FILE", help="save plain-text render to FILE")

    args = parser.parse_args()

    if args.list:
        _print_info()
        return

    # ── Build render parameters ──────────────────────────────────────────────

    # Start from preset defaults
    fractal = args.fractal
    center_x, center_y, zoom = -0.5, 0.0, 1.0
    julia_c = (args.julia_cr, args.julia_ci)

    if args.preset:
        p = PRESETS[args.preset]
        fractal = p["fractal"]
        center_x, center_y, zoom = p["center_x"], p["center_y"], p["zoom"]
        if "julia_cr" in p:
            julia_c = (p["julia_cr"], p["julia_ci"])

    # Explicit flags override preset
    if args.cx is not None:
        center_x = args.cx
    if args.cy is not None:
        center_y = args.cy
    if args.zoom is not None:
        zoom = args.zoom
    if args.fractal != "mandelbrot" or not args.preset:
        fractal = args.fractal if not args.preset else fractal

    term_w, term_h = _term_size()
    width = args.width or term_w
    height = args.height or term_h
    mode = "ascii" if args.ascii else "block"

    # ── Render ───────────────────────────────────────────────────────────────

    try:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()

        lines = render(
            fractal=fractal,
            width=width,
            height=height,
            center_x=center_x,
            center_y=center_y,
            zoom=zoom,
            max_iter=args.max_iter,
            theme=args.theme,
            mode=mode,
            julia_c=julia_c,
            show_progress=not args.no_progress,
        )

        print("\n".join(lines))

        if args.save:
            plain = [_strip_ansi(ln) for ln in lines]
            with open(args.save, "w", encoding="utf-8") as fh:
                fh.write("\n".join(plain) + "\n")
            print(f"\nSaved to {args.save}")

    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
