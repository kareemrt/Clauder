"""Command-line interface for FractalForge."""

import argparse
import os
import sys

from . import mandelbrot, julia, sierpinski, renderer
from .palettes import PALETTE_NAMES, CHAR_NAMES


def _terminal_size() -> tuple[int, int]:
    try:
        cols, rows = os.get_terminal_size()
    except OSError:
        cols, rows = 120, 40
    # Each character is taller than wide; halve columns for aspect ratio
    return cols, rows - 6  # leave room for header/legend


def cmd_mandelbrot(args: argparse.Namespace) -> None:
    w, h = _terminal_size()
    if args.width:
        w = args.width
    if args.height:
        h = args.height

    preset = mandelbrot.PRESETS.get(args.preset, mandelbrot.PRESETS["classic"])
    grid = mandelbrot.compute(
        width=w, height=h,
        x_min=args.x_min if args.x_min is not None else preset["x_min"],
        x_max=args.x_max if args.x_max is not None else preset["x_max"],
        y_min=args.y_min if args.y_min is not None else preset["y_min"],
        y_max=args.y_max if args.y_max is not None else preset["y_max"],
        max_iter=args.iterations or preset["max_iter"],
    )
    renderer.print_header(
        "✦ FractalForge — Mandelbrot Set ✦",
        f"preset={args.preset}  size={w}×{h}  iters={args.iterations or preset['max_iter']}",
    )
    print(renderer.render_smooth(grid, palette=args.palette, char_set=args.chars))
    renderer.print_legend(args.palette, args.chars)


def cmd_julia(args: argparse.Namespace) -> None:
    w, h = _terminal_size()
    if args.width:
        w = args.width
    if args.height:
        h = args.height

    preset = julia.PRESETS.get(args.preset, julia.PRESETS["snowflake"])
    cx = args.cx if args.cx is not None else preset["cx"]
    cy = args.cy if args.cy is not None else preset["cy"]

    grid = julia.compute(
        width=w, height=h,
        cx=cx, cy=cy,
        max_iter=args.iterations or 256,
    )
    renderer.print_header(
        "✦ FractalForge — Julia Set ✦",
        f"c = {cx:.4f} + {cy:.4f}i   preset={args.preset}",
    )
    print(renderer.render_smooth(grid, palette=args.palette, char_set=args.chars))
    renderer.print_legend(args.palette, args.chars)


def cmd_sierpinski(args: argparse.Namespace) -> None:
    w, h = _terminal_size()
    if args.width:
        w = args.width
    if args.height:
        h = args.height

    variant = args.variant.lower()
    if variant == "triangle":
        grid = sierpinski.triangle(w, h, depth=args.depth)
        title = "✦ FractalForge — Sierpiński Triangle ✦"
    elif variant == "carpet":
        grid = sierpinski.carpet(w, h, depth=args.depth)
        title = "✦ FractalForge — Sierpiński Carpet ✦"
    elif variant == "fern":
        grid = sierpinski.barnsley_fern(w, h, iterations=args.iterations or 80000)
        title = "✦ FractalForge — Barnsley Fern ✦"
    else:
        print(f"Unknown variant '{variant}'. Choose: triangle, carpet, fern")
        sys.exit(1)

    renderer.print_header(title, f"variant={variant}  depth={args.depth}  size={w}×{h}")
    print(renderer.render_bool(grid, on_color=args.palette, char_set=args.chars))
    renderer.print_legend(args.palette, args.chars)


def cmd_showcase(args: argparse.Namespace) -> None:
    """Render a quick showcase of several fractals back-to-back."""
    w = min(args.width or 80, 80)
    h = min(args.height or 24, 24)

    demos = [
        ("Mandelbrot — Classic", lambda: mandelbrot.compute(w, h, **{k: v for k, v in mandelbrot.PRESETS["classic"].items() if k != "max_iter"}, max_iter=128), "fire", "block", True),
        ("Mandelbrot — Seahorse Valley", lambda: mandelbrot.compute(w, h, **{k: v for k, v in mandelbrot.PRESETS["seahorse"].items() if k != "max_iter"}, max_iter=256), "ocean", "block", True),
        ("Julia — Dragon", lambda: julia.compute(w, h, **julia.PRESETS["dragon"], max_iter=128), "plasma", "block", True),
        ("Julia — Galaxy", lambda: julia.compute(w, h, **julia.PRESETS["galaxy"], max_iter=128), "neon", "dots", True),
        ("Sierpiński Triangle", lambda: sierpinski.triangle(w, h, depth=5), "matrix", "block", False),
        ("Barnsley Fern", lambda: sierpinski.barnsley_fern(w, h, iterations=40000), "matrix", "dots", False),
    ]

    for title, compute_fn, palette, chars, smooth in demos:
        renderer.print_header(f"✦ FractalForge ✦", title)
        grid = compute_fn()
        if smooth:
            print(renderer.render_smooth(grid, palette=palette, char_set=chars))
        else:
            print(renderer.render_bool(grid, on_color=palette, char_set=chars))
        renderer.print_legend(palette, chars)
        print()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fractalforge",
        description="FractalForge — Terminal fractal art engine",
    )
    p.add_argument("--version", action="version", version="FractalForge 1.0.0")

    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--palette", "-p", choices=PALETTE_NAMES, default="fire",
                        help="Color palette (default: fire)")
    shared.add_argument("--chars", "-c", choices=CHAR_NAMES, default="block",
                        help="Character set (default: block)")
    shared.add_argument("--width", "-W", type=int, default=None)
    shared.add_argument("--height", "-H", type=int, default=None)
    shared.add_argument("--iterations", "-i", type=int, default=None,
                        help="Max iterations")

    sub = p.add_subparsers(dest="command", required=True)

    # mandelbrot
    mb = sub.add_parser("mandelbrot", aliases=["mb"], parents=[shared],
                        help="Render the Mandelbrot set")
    mb.add_argument("--preset", choices=list(mandelbrot.PRESETS.keys()), default="classic")
    mb.add_argument("--x-min", dest="x_min", type=float, default=None)
    mb.add_argument("--x-max", dest="x_max", type=float, default=None)
    mb.add_argument("--y-min", dest="y_min", type=float, default=None)
    mb.add_argument("--y-max", dest="y_max", type=float, default=None)
    mb.set_defaults(func=cmd_mandelbrot)

    # julia
    jl = sub.add_parser("julia", aliases=["jl"], parents=[shared],
                        help="Render a Julia set")
    jl.add_argument("--preset", choices=list(julia.PRESETS.keys()), default="snowflake")
    jl.add_argument("--cx", type=float, default=None, help="Real part of c")
    jl.add_argument("--cy", type=float, default=None, help="Imaginary part of c")
    jl.set_defaults(func=cmd_julia)

    # sierpinski
    sk = sub.add_parser("sierpinski", aliases=["sk"], parents=[shared],
                        help="Render Sierpiński fractals")
    sk.add_argument("--variant", choices=["triangle", "carpet", "fern"],
                    default="triangle")
    sk.add_argument("--depth", type=int, default=5)
    sk.set_defaults(func=cmd_sierpinski)

    # showcase
    sc = sub.add_parser("showcase", aliases=["demo"], parents=[shared],
                        help="Show a tour of all fractals")
    sc.set_defaults(func=cmd_showcase)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
