"""Command-line interface for Fractal Forge."""

import argparse
import sys

from . import __version__
from .animate import mandelbrot_zoom_frames, save_gif
from .escape_time import burning_ship, julia, mandelbrot
from .ifs import barnsley_fern_points, koch_snowflake_points, sierpinski_points
from .palettes import available_palettes
from .render import render_escape_grid, render_point_cloud, render_polyline


def _add_common_image_args(parser, default_palette="fire"):
    parser.add_argument("-o", "--output", required=True, help="output file path")
    parser.add_argument("--width", type=int, default=800, help="image width in pixels")
    parser.add_argument("--height", type=int, default=600, help="image height in pixels")
    parser.add_argument(
        "--palette",
        default=default_palette,
        choices=available_palettes(),
        help="color palette to use",
    )


def _add_escape_args(parser):
    parser.add_argument("--max-iter", type=int, default=200, help="maximum iterations")
    parser.add_argument("--center-x", type=float, default=None, help="real part of the view center")
    parser.add_argument("--center-y", type=float, default=None, help="imaginary part of the view center")
    parser.add_argument("--zoom", type=float, default=1.0, help="zoom level (higher = closer)")


def _cmd_mandelbrot(args):
    center = (args.center_x if args.center_x is not None else -0.5,
              args.center_y if args.center_y is not None else 0.0)
    grid = mandelbrot(args.width, args.height, max_iter=args.max_iter, center=center, zoom=args.zoom)
    render_escape_grid(grid, args.palette).save(args.output)
    print(f"Saved Mandelbrot set to {args.output}")


def _cmd_julia(args):
    center = (args.center_x if args.center_x is not None else 0.0,
              args.center_y if args.center_y is not None else 0.0)
    c_param = complex(args.c_real, args.c_imag)
    grid = julia(args.width, args.height, c_param, max_iter=args.max_iter, center=center, zoom=args.zoom)
    render_escape_grid(grid, args.palette).save(args.output)
    print(f"Saved Julia set (c={c_param}) to {args.output}")


def _cmd_burning_ship(args):
    center = (args.center_x if args.center_x is not None else -0.5,
              args.center_y if args.center_y is not None else -0.5)
    grid = burning_ship(args.width, args.height, max_iter=args.max_iter, center=center, zoom=args.zoom)
    render_escape_grid(grid, args.palette).save(args.output)
    print(f"Saved Burning Ship fractal to {args.output}")


def _cmd_sierpinski(args):
    points = sierpinski_points(num_points=args.points, seed=args.seed)
    render_point_cloud(points, args.width, args.height, args.palette).save(args.output)
    print(f"Saved Sierpinski triangle ({args.points} points) to {args.output}")


def _cmd_fern(args):
    points = barnsley_fern_points(num_points=args.points, seed=args.seed)
    render_point_cloud(points, args.width, args.height, args.palette).save(args.output)
    print(f"Saved Barnsley fern ({args.points} points) to {args.output}")


def _cmd_koch(args):
    points = koch_snowflake_points(order=args.order)
    render_polyline(points, args.width, args.height).save(args.output)
    print(f"Saved Koch snowflake (order {args.order}, {len(points)} points) to {args.output}")


def _cmd_zoom(args):
    target = (args.target_x, args.target_y)
    frames = mandelbrot_zoom_frames(
        args.width,
        args.height,
        frames=args.frames,
        max_iter=args.max_iter,
        target=target,
        zoom_factor=args.zoom_factor,
        palette=args.palette,
    )
    save_gif(frames, args.output, duration=args.duration)
    print(f"Saved {len(frames)}-frame zoom animation to {args.output}")


def _cmd_palettes(_args):
    for name in available_palettes():
        print(name)


def build_parser():
    parser = argparse.ArgumentParser(prog="fractalforge", description="Generate fractal images and animations.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("mandelbrot", help="render the Mandelbrot set")
    _add_common_image_args(p)
    _add_escape_args(p)
    p.set_defaults(func=_cmd_mandelbrot)

    p = subparsers.add_parser("julia", help="render a Julia set")
    _add_common_image_args(p, default_palette="electric")
    _add_escape_args(p)
    p.add_argument("--c-real", type=float, default=-0.7, help="real part of the Julia constant c")
    p.add_argument("--c-imag", type=float, default=0.27015, help="imaginary part of the Julia constant c")
    p.set_defaults(func=_cmd_julia)

    p = subparsers.add_parser("burning-ship", help="render the Burning Ship fractal")
    _add_common_image_args(p, default_palette="ocean")
    _add_escape_args(p)
    p.set_defaults(func=_cmd_burning_ship)

    p = subparsers.add_parser("sierpinski", help="render a Sierpinski triangle via the chaos game")
    _add_common_image_args(p, default_palette="electric")
    p.add_argument("--points", type=int, default=200_000, help="number of points to plot")
    p.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    p.set_defaults(func=_cmd_sierpinski)

    p = subparsers.add_parser("fern", help="render a Barnsley fern")
    _add_common_image_args(p, default_palette="forest")
    p.add_argument("--points", type=int, default=200_000, help="number of points to plot")
    p.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    p.set_defaults(func=_cmd_fern)

    p = subparsers.add_parser("koch", help="render a Koch snowflake")
    _add_common_image_args(p)
    p.add_argument("--order", type=int, default=4, help="recursion depth")
    p.set_defaults(func=_cmd_koch)

    p = subparsers.add_parser("zoom", help="render an animated zoom into the Mandelbrot set")
    _add_common_image_args(p)
    p.add_argument("--max-iter", type=int, default=150, help="base maximum iterations")
    p.add_argument("--frames", type=int, default=40, help="number of animation frames")
    p.add_argument("--zoom-factor", type=float, default=1.3, help="zoom multiplier per frame")
    p.add_argument("--target-x", type=float, default=-0.7436438870371587, help="real part of the zoom target")
    p.add_argument("--target-y", type=float, default=0.13182590420533, help="imaginary part of the zoom target")
    p.add_argument("--duration", type=int, default=80, help="frame duration in milliseconds")
    p.set_defaults(func=_cmd_zoom)

    p = subparsers.add_parser("palettes", help="list available color palettes")
    p.set_defaults(func=_cmd_palettes)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
