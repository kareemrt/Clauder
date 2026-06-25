"""Command-line interface for fractalis."""

import argparse
import sys

from . import colormaps
from .burning_ship import DEFAULT_BOUNDS as SHIP_BOUNDS
from .burning_ship import render_burning_ship
from .julia import DEFAULT_BOUNDS as JULIA_BOUNDS
from .julia import PRESETS as JULIA_PRESETS
from .julia import render_julia
from .lsystem import PRESETS as LSYSTEM_PRESETS
from .lsystem import render_lsystem
from .mandelbrot import DEFAULT_BOUNDS as MANDELBROT_BOUNDS
from .mandelbrot import SEAHORSE_VALLEY
from .mandelbrot import render_mandelbrot
from .png_writer import write_png

MANDELBROT_VIEWS = {"full": MANDELBROT_BOUNDS, "seahorse": SEAHORSE_VALLEY}


def _bounds_type(s):
    parts = [float(p) for p in s.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bounds must be 'x_min,x_max,y_min,y_max'")
    return tuple(parts)


def _add_common_image_args(p, default_cmap):
    p.add_argument("-o", "--out", required=True, help="output PNG path")
    p.add_argument("-W", "--width", type=int, default=800)
    p.add_argument("-H", "--height", type=int, default=800)
    p.add_argument("--cmap", default=default_cmap, choices=sorted(colormaps.CMAPS))


def build_parser():
    parser = argparse.ArgumentParser(prog="fractalis", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("mandelbrot", help="render the Mandelbrot set")
    _add_common_image_args(p, "inferno")
    p.add_argument("--view", choices=sorted(MANDELBROT_VIEWS), default="full")
    p.add_argument("--bounds", type=_bounds_type, help="x_min,x_max,y_min,y_max")
    p.add_argument("--max-iter", type=int, default=200)

    p = sub.add_parser("julia", help="render a Julia set")
    _add_common_image_args(p, "ocean")
    p.add_argument("--c", choices=sorted(JULIA_PRESETS), default="classic")
    p.add_argument("--bounds", type=_bounds_type, default=JULIA_BOUNDS)
    p.add_argument("--max-iter", type=int, default=200)

    p = sub.add_parser("burningship", help="render the Burning Ship fractal")
    _add_common_image_args(p, "fire")
    p.add_argument("--bounds", type=_bounds_type, default=SHIP_BOUNDS)
    p.add_argument("--max-iter", type=int, default=200)

    p = sub.add_parser("lsystem", help="render an L-system curve")
    _add_common_image_args(p, "psychedelic")
    p.add_argument("preset", choices=sorted(LSYSTEM_PRESETS))
    p.add_argument("--iterations", type=int, default=None)
    p.add_argument("--stroke", type=int, default=1)

    sub.add_parser("gallery", help="regenerate every sample image into ./gallery")

    return parser


def _cmd_mandelbrot(args):
    bounds = args.bounds or MANDELBROT_VIEWS[args.view]
    pixels = render_mandelbrot(args.width, args.height, bounds, args.max_iter, args.cmap)
    write_png(args.out, args.width, args.height, pixels)


def _cmd_julia(args):
    pixels = render_julia(args.width, args.height, args.c, args.bounds, args.max_iter, args.cmap)
    write_png(args.out, args.width, args.height, pixels)


def _cmd_burningship(args):
    pixels = render_burning_ship(args.width, args.height, args.bounds, args.max_iter, args.cmap)
    write_png(args.out, args.width, args.height, pixels)


def _cmd_lsystem(args):
    pixels = render_lsystem(args.preset, args.width, args.height, args.cmap,
                             stroke=args.stroke, iterations=args.iterations)
    write_png(args.out, args.width, args.height, pixels)


def _cmd_gallery(_args):
    from scripts.generate_gallery import main as generate_gallery
    generate_gallery()


_HANDLERS = {
    "mandelbrot": _cmd_mandelbrot,
    "julia": _cmd_julia,
    "burningship": _cmd_burningship,
    "lsystem": _cmd_lsystem,
    "gallery": _cmd_gallery,
}


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    _HANDLERS[args.command](args)
    if args.command != "gallery":
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
