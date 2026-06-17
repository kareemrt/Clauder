"""Command-line interface for fracta.

Examples:
    python -m fracta mandelbrot -o out.png --palette ocean
    python -m fracta julia -o out.png --c -0.745+0.113j --palette fire
    python -m fracta lsystem -o out.png --preset tree
    python -m fracta chaos -o out.png --preset barnsley_fern --palette forest
"""

from __future__ import annotations

import argparse

from PIL import Image

from fracta.chaos_game import PRESETS as CHAOS_PRESETS
from fracta.chaos_game import render_chaos_game
from fracta.escape_fractals import render_julia, render_mandelbrot
from fracta.lsystem import PRESETS as LSYSTEM_PRESETS
from fracta.lsystem import render_lsystem
from fracta.palette import available_palettes


def _save(array_or_image, path: str) -> None:
    img = array_or_image if isinstance(array_or_image, Image.Image) else Image.fromarray(array_or_image)
    img.save(path)
    print(f"Saved {path} ({img.width}x{img.height})")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="fracta", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    common = dict(width=800, height=800)

    p_mandel = sub.add_parser("mandelbrot", help="Render the Mandelbrot set")
    p_mandel.add_argument("-o", "--output", default="mandelbrot.png")
    p_mandel.add_argument("--width", type=int, default=common["width"])
    p_mandel.add_argument("--height", type=int, default=common["height"])
    p_mandel.add_argument("--center", type=float, nargs=2, default=(-0.5, 0.0))
    p_mandel.add_argument("--scale", type=float, default=1.4)
    p_mandel.add_argument("--max-iter", type=int, default=300)
    p_mandel.add_argument("--palette", choices=available_palettes(), default="ocean")

    p_julia = sub.add_parser("julia", help="Render a Julia set")
    p_julia.add_argument("-o", "--output", default="julia.png")
    p_julia.add_argument("--width", type=int, default=common["width"])
    p_julia.add_argument("--height", type=int, default=common["height"])
    p_julia.add_argument("--c", type=complex, default=-0.74543 + 0.11301j)
    p_julia.add_argument("--scale", type=float, default=1.4)
    p_julia.add_argument("--max-iter", type=int, default=300)
    p_julia.add_argument("--palette", choices=available_palettes(), default="fire")

    p_lsys = sub.add_parser("lsystem", help="Render an L-system (plants, curves)")
    p_lsys.add_argument("-o", "--output", default="lsystem.png")
    p_lsys.add_argument("--preset", choices=sorted(LSYSTEM_PRESETS), default="tree")
    p_lsys.add_argument("--width", type=int, default=900)
    p_lsys.add_argument("--height", type=int, default=900)

    p_chaos = sub.add_parser("chaos", help="Render a chaos-game IFS fractal")
    p_chaos.add_argument("-o", "--output", default="chaos.png")
    p_chaos.add_argument("--preset", choices=sorted(CHAOS_PRESETS), default="barnsley_fern")
    p_chaos.add_argument("--width", type=int, default=800)
    p_chaos.add_argument("--height", type=int, default=900)
    p_chaos.add_argument("--points", type=int, default=300_000)
    p_chaos.add_argument("--palette", choices=available_palettes(), default="forest")
    p_chaos.add_argument("--seed", type=int, default=0)

    args = parser.parse_args(argv)

    if args.command == "mandelbrot":
        result = render_mandelbrot(
            width=args.width,
            height=args.height,
            center=tuple(args.center),
            scale=args.scale,
            max_iter=args.max_iter,
            palette=args.palette,
        )
    elif args.command == "julia":
        result = render_julia(
            width=args.width,
            height=args.height,
            c=args.c,
            scale=args.scale,
            max_iter=args.max_iter,
            palette=args.palette,
        )
    elif args.command == "lsystem":
        result = render_lsystem(preset=args.preset, width=args.width, height=args.height)
    elif args.command == "chaos":
        result = render_chaos_game(
            preset=args.preset,
            width=args.width,
            height=args.height,
            n_points=args.points,
            palette=args.palette,
            seed=args.seed,
        )
    else:  # pragma: no cover - argparse enforces valid choices
        raise SystemExit(1)

    _save(result, args.output)


if __name__ == "__main__":
    main()
