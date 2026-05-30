#!/usr/bin/env python3
"""
FractalDive — Interactive terminal fractal explorer.

Usage:
  python main.py                     # Launch interactive explorer
  python main.py render              # Render Mandelbrot and print to terminal
  python main.py render --julia      # Render a Julia set
  python main.py render --theme THEME  # Available: fire ocean electric midnight gold psychedelic
  python main.py demo                # Print a showcase of all themes (non-interactive)
"""

import argparse
import sys
import os

try:
    import numpy as np
except ImportError:
    print("FractalDive requires numpy.  Install with:  pip install numpy")
    sys.exit(1)

from fractal_dive.core import mandelbrot, julia
from fractal_dive.renderer import render_static
from fractal_dive.themes import THEMES, THEME_ORDER


BANNER = r"""
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗      ██████╗ ██╗██╗   ██╗███████╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║      ██╔══██╗██║██║   ██║██╔════╝
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║      ██║  ██║██║██║   ██║█████╗
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║      ██║  ██║██║╚██╗ ██╔╝██╔══╝
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗ ██████╔╝██║ ╚████╔╝ ███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚══════╝
"""

JULIA_PRESETS = {
    "classic":   -0.7 + 0.27015j,
    "spiral":    -0.4 + 0.6j,
    "galaxy":    0.285 + 0.01j,
    "dragon":    -0.70176 - 0.3842j,
    "lightning": -0.835 - 0.2321j,
    "star":      0.45 + 0.1428j,
}


def cmd_render(args):
    """Render a single frame and print it."""
    width, height = args.width, args.height

    if args.julia:
        preset = args.preset or "classic"
        c = JULIA_PRESETS.get(preset, JULIA_PRESETS["classic"])
        print(f"\033[1mJulia Set  c={c}  preset='{preset}'\033[0m")
        data = julia(width, height * 2, -1.8, 1.8, -1.8, 1.8, c, args.max_iter)
    else:
        print("\033[1mMandelbrot Set\033[0m")
        data = mandelbrot(width, height * 2, -2.5, 1.0, -1.3, 1.3, args.max_iter)

    render_static(data, args.max_iter, args.theme)


def cmd_demo(_args):
    """Print all themes side by side (as separate renders)."""
    print(BANNER)
    width, height = 100, 22
    data = mandelbrot(width, height * 2, -2.5, 1.0, -1.3, 1.3, 256)

    for name in THEME_ORDER:
        label, _ = THEMES[name]
        print(f"\n\033[1;97m  ── {label} ──\033[0m\n")
        render_static(data, 256, name, show_info=False)


def cmd_explore(args):
    """Launch the interactive curses explorer."""
    try:
        from fractal_dive.explorer import launch
    except ImportError as e:
        print(f"Interactive mode requires a terminal with curses support.\n{e}")
        sys.exit(1)

    print(BANNER)
    print("  Loading interactive explorer…  (press H for help, Q to quit)\n")
    launch(start_julia=args.julia)


def main():
    parser = argparse.ArgumentParser(
        description="FractalDive — explore infinite fractal complexity in your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command")

    # explore (default)
    p_explore = sub.add_parser("explore", help="Launch interactive explorer (default)")
    p_explore.add_argument("--julia", action="store_true", help="Start in Julia mode")

    # render
    p_render = sub.add_parser("render", help="Render a static frame to the terminal")
    p_render.add_argument("--julia", action="store_true")
    p_render.add_argument("--preset", choices=list(JULIA_PRESETS), default="classic",
                          help="Julia set preset (default: classic)")
    p_render.add_argument("--theme", choices=list(THEMES), default="fire",
                          help="Color theme (default: fire)")
    p_render.add_argument("--width",    type=int, default=120)
    p_render.add_argument("--height",   type=int, default=40)
    p_render.add_argument("--max-iter", type=int, default=256, dest="max_iter")

    # demo
    sub.add_parser("demo", help="Showcase all color themes")

    args = parser.parse_args()

    if args.command == "render":
        cmd_render(args)
    elif args.command == "demo":
        cmd_demo(args)
    else:
        # Default: interactive explorer
        explore_args = argparse.Namespace(julia=getattr(args, "julia", False))
        cmd_explore(explore_args)


if __name__ == "__main__":
    main()
