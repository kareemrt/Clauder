#!/usr/bin/env python3
"""
Mandelbrot Voyage — Interactive Fractal Explorer
Usage: python voyage.py [command] [options]
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from src.renderer   import print_fractal, gallery, LANDMARKS
from src.fractals   import LANDMARKS as LANDMARK_DATA
from src.palettes   import PALETTES
from src.html_export import generate_html


def cmd_render(args):
    """Render a fractal to the terminal."""
    loc = LANDMARK_DATA.get(args.landmark, {})
    print_fractal(
        fractal  = args.fractal,
        cx       = args.cx   if args.cx   is not None else loc.get("cx",  -0.5),
        cy       = args.cy   if args.cy   is not None else loc.get("cy",   0.0),
        zoom     = args.zoom if args.zoom is not None else loc.get("zoom", 0.75),
        max_iter = args.iter if args.iter is not None else loc.get("max_iter", 100),
        palette  = args.palette,
        julia_c  = (args.jre, args.jim),
        title    = args.landmark or "",
    )


def cmd_gallery(_args):
    """Print all palettes."""
    gallery()


def cmd_html(args):
    """Generate the interactive HTML explorer."""
    out = args.output or "mandelbrot_voyage.html"
    path = generate_html(out)
    print(f"\n  ✅  HTML explorer written to: {path}")
    print(f"  📂  Open it in any modern browser.\n")


def cmd_landmarks(_args):
    """List all built-in landmarks."""
    BOLD  = "\033[1m"  if sys.stdout.isatty() else ""
    CYAN  = "\033[36m" if sys.stdout.isatty() else ""
    DIM   = "\033[2m"  if sys.stdout.isatty() else ""
    RESET = "\033[0m"  if sys.stdout.isatty() else ""

    print(f"\n{BOLD}{CYAN}  ◆ Built-in Landmarks{RESET}\n")
    for name, loc in LANDMARK_DATA.items():
        print(f"  {BOLD}{name:<22}{RESET}"
              f"  {DIM}cx={loc['cx']:+.6f}  cy={loc['cy']:+.6f}  "
              f"zoom={loc['zoom']:.1f}×  iter={loc.get('max_iter',200)}{RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="voyage",
        description="🌀  Mandelbrot Voyage — Fractal Explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  render     Render a fractal in the terminal
  html       Generate interactive HTML explorer
  gallery    Show all color palettes
  landmarks  List all built-in zoom locations

Examples:
  python voyage.py render
  python voyage.py render --fractal julia --palette fire --landmark "Dragon Spiral"
  python voyage.py render --cx -0.74529 --cy 0.11307 --zoom 320 --iter 300
  python voyage.py html --output explorer.html
  python voyage.py gallery
        """,
    )

    sub = parser.add_subparsers(dest="command")

    # ── render ──────────────────────────────────────────────────────────────────
    p_render = sub.add_parser("render", help="Render a fractal in the terminal")
    p_render.add_argument("--fractal",  "-f", default="mandelbrot",
                          choices=["mandelbrot","julia","burning_ship","tricorn","multibrot"],
                          help="Fractal type")
    p_render.add_argument("--palette",  "-p", default="classic",
                          choices=list(PALETTES.keys()), help="Color palette")
    p_render.add_argument("--landmark", "-l", default="",
                          metavar="NAME",  help="Jump to a landmark (see: landmarks)")
    p_render.add_argument("--cx",   type=float, default=None, metavar="REAL",  help="Center real part")
    p_render.add_argument("--cy",   type=float, default=None, metavar="IMAG",  help="Center imaginary part")
    p_render.add_argument("--zoom", type=float, default=None, metavar="FACTOR",help="Zoom level")
    p_render.add_argument("--iter", type=int,   default=None, metavar="N",     help="Max iterations")
    p_render.add_argument("--jre",  type=float, default=-0.7269, metavar="RE", help="Julia: Re(c)")
    p_render.add_argument("--jim",  type=float, default= 0.1889, metavar="IM", help="Julia: Im(c)")

    # ── html ────────────────────────────────────────────────────────────────────
    p_html = sub.add_parser("html", help="Generate interactive HTML explorer")
    p_html.add_argument("--output", "-o", default="mandelbrot_voyage.html",
                        help="Output file path (default: mandelbrot_voyage.html)")

    # ── gallery ─────────────────────────────────────────────────────────────────
    sub.add_parser("gallery", help="Show all color palettes")

    # ── landmarks ───────────────────────────────────────────────────────────────
    sub.add_parser("landmarks", help="List all built-in landmarks")

    args = parser.parse_args()

    if args.command == "render":
        cmd_render(args)
    elif args.command == "html":
        cmd_html(args)
    elif args.command == "gallery":
        cmd_gallery(args)
    elif args.command == "landmarks":
        cmd_landmarks(args)
    else:
        # Default: render the Mandelbrot set
        print_fractal(
            fractal  = "mandelbrot",
            cx       = -0.5,
            cy       = 0.0,
            zoom     = 0.75,
            max_iter = 100,
            palette  = "classic",
            title    = "Full View",
        )
        print("  Run  python voyage.py --help  for more options.\n")


if __name__ == "__main__":
    main()
