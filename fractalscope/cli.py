"""Command-line interface for FractalScope."""

import argparse
import sys
import os
import shutil
from typing import Optional

from .fractals import render_mandelbrot, render_julia, render_burning_ship, render_sierpinski
from .display import (
    render_grid_to_string, render_sierpinski_colored,
    print_header, print_legend, list_options, supports_color
)
from .colors import PALETTES, ASCII_SETS, RESET, BOLD


BANNER = r"""
  ___             _        _  ___
 | __| _ __ _ __| |_ __ _| |/ __| __ ___ _ __  ___
 | _| '_/ _` / _|  _/ _` | |\__ \/ _/ _ \ '_ \/ -_)
 |_||_| \__,_\__|\__\__,_|_||___/\__\___/ .__/\___|
                                         |_|
"""

TAGLINE = "✦  Infinite complexity from simple rules  ✦"


def get_terminal_size() -> tuple:
    try:
        cols, rows = shutil.get_terminal_size(fallback=(120, 40))
        return cols, rows
    except Exception:
        return 120, 40


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fractalscope",
        description="FractalScope — render fractals in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fractalscope                                 Mandelbrot with defaults
  fractalscope --fractal julia --cx -0.4 --cy 0.6
  fractalscope --fractal burning --palette fire --zoom 2
  fractalscope --fractal sierpinski --depth 5
  fractalscope --palette plasma --charset blocks --iters 200
  fractalscope --list                          Show all options
  fractalscope --save output.txt              Save render to file
        """,
    )

    parser.add_argument(
        "--fractal", "-f",
        choices=["mandelbrot", "julia", "burning", "sierpinski"],
        default="mandelbrot",
        help="Fractal type to render (default: mandelbrot)",
    )
    parser.add_argument(
        "--palette", "-p",
        choices=list(PALETTES.keys()),
        default="plasma",
        help="Color palette (default: plasma)",
    )
    parser.add_argument(
        "--charset", "-c",
        choices=list(ASCII_SETS.keys()),
        default="dense",
        help="ASCII character set density (default: dense)",
    )
    parser.add_argument(
        "--width", "-W",
        type=int, default=None,
        help="Output width in characters (default: terminal width)",
    )
    parser.add_argument(
        "--height", "-H",
        type=int, default=None,
        help="Output height in lines (default: terminal height - 6)",
    )
    parser.add_argument(
        "--iters", "-i",
        type=int, default=100,
        help="Max iterations (higher = more detail, default: 100)",
    )
    parser.add_argument(
        "--zoom", "-z",
        type=float, default=1.0,
        help="Zoom factor (default: 1.0)",
    )
    parser.add_argument(
        "--cx",
        type=float, default=None,
        help="Real component of center/parameter",
    )
    parser.add_argument(
        "--cy",
        type=float, default=None,
        help="Imaginary component of center/parameter",
    )
    parser.add_argument(
        "--depth", "-d",
        type=int, default=4,
        help="Sierpinski recursion depth (default: 4)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable color output (plain ASCII)",
    )
    parser.add_argument(
        "--save", "-s",
        type=str, default=None,
        metavar="FILE",
        help="Save output to file (plain text, no ANSI codes)",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available fractals, palettes, and charsets",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="FractalScope 1.0.0",
    )

    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.list:
        list_options()
        return 0

    cols, rows = get_terminal_size()
    width  = args.width  or cols
    height = args.height or max(20, rows - 8)

    use_color = not args.no_color

    # Print header to stderr so it doesn't pollute --save output
    print_header("FractalScope", TAGLINE)

    # --- Render ---
    output: str

    if args.fractal == "sierpinski":
        depth = max(1, min(args.depth, 7))
        rows_data = render_sierpinski(size=width, depth=depth)
        output = render_sierpinski_colored(rows_data, color=use_color)
        params = {"depth": depth}

    elif args.fractal == "julia":
        cx = args.cx if args.cx is not None else -0.7
        cy = args.cy if args.cy is not None else 0.27015
        grid = render_julia(
            width=width, height=height,
            cx=cx, cy=cy,
            zoom=args.zoom, max_iters=args.iters,
        )
        output = render_grid_to_string(grid, args.iters, args.palette, args.charset, use_color)
        params = {"cx": cx, "cy": cy, "zoom": args.zoom, "iters": args.iters}

    elif args.fractal == "burning":
        cx = args.cx if args.cx is not None else -0.4
        cy = args.cy if args.cy is not None else -0.6
        grid = render_burning_ship(
            width=width, height=height,
            cx=cx, cy=cy,
            zoom=args.zoom, max_iters=args.iters,
        )
        output = render_grid_to_string(grid, args.iters, args.palette, args.charset, use_color)
        params = {"cx": cx, "cy": cy, "zoom": args.zoom, "iters": args.iters}

    else:  # mandelbrot
        cx = args.cx if args.cx is not None else -0.5
        cy = args.cy if args.cy is not None else 0.0
        grid = render_mandelbrot(
            width=width, height=height,
            cx=cx, cy=cy,
            zoom=args.zoom, max_iters=args.iters,
        )
        output = render_grid_to_string(grid, args.iters, args.palette, args.charset, use_color)
        params = {"cx": cx, "cy": cy, "zoom": args.zoom, "iters": args.iters}

    # Print to terminal
    print(output)
    print_legend(args.palette, args.charset, args.fractal, params)

    # Save plain-text version
    if args.save:
        # Strip ANSI codes for file output
        import re
        ansi_escape = re.compile(r"\033\[[0-9;]*m")
        plain = ansi_escape.sub("", output)
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(f"FractalScope — {args.fractal}\n")
            f.write("=" * 60 + "\n")
            f.write(plain)
            f.write("\n")
        print(f"\n  Saved to: {args.save}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
