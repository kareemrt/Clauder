"""
FractalScope CLI entry point.

Usage examples:
    fractalscope                                # Mandelbrot, fire palette, terminal
    fractalscope --fractal julia --palette neon
    fractalscope --fractal burning_ship --save output.png
    fractalscope --fractal julia --c-real -0.7269 --c-imag 0.1889
    fractalscope --list
"""

import argparse
import sys
import time

from fractalscope.fractals import FRACTALS
from fractalscope.palettes import apply_palette, PALETTE_NAMES
from fractalscope.renderers.terminal import print_fractal
from fractalscope.renderers.image import render_image, is_available as pil_available


_FRACTAL_NAMES = list(FRACTALS.keys())


_FRACTAL_DEFAULTS = {
    "mandelbrot": dict(x_min=-2.5, x_max=1.0,  y_min=-1.25, y_max=1.25),
    "julia":      dict(x_min=-1.8, x_max=1.8,  y_min=-1.8,  y_max=1.8),
    "burning_ship": dict(x_min=-2.5, x_max=1.5, y_min=-2.0, y_max=0.5),
}

_JULIA_PRESETS = {
    "lightning":     (-0.7269, 0.1889),
    "seahorse":      (-0.75,   0.13),
    "douady_rabbit": (-0.123,  0.745),
    "san_marco":     (-0.75,   0.0),
    "siegel_disk":   (-0.391, -0.587),
    "spiral":        (0.285,   0.01),
    "dendrite":      (0.0,     1.0),
}


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fractalscope",
        description="FractalScope — terminal fractal explorer with PNG export",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        "--fractal", "-f",
        choices=_FRACTAL_NAMES,
        default="mandelbrot",
        help="Fractal to render (default: mandelbrot)",
    )
    p.add_argument(
        "--palette", "-p",
        choices=PALETTE_NAMES,
        default="fire",
        help="Colour palette (default: fire)",
    )
    p.add_argument(
        "--width", "-W", type=int, default=160,
        help="Output width in pixels (default: 160)",
    )
    p.add_argument(
        "--height", "-H", type=int, default=90,
        help="Output height in pixels (default: 90)",
    )
    p.add_argument(
        "--max-iter", "-i", type=int, default=256,
        help="Maximum iterations — higher → more detail (default: 256)",
    )
    p.add_argument(
        "--x-min", type=float, default=None, help="Real axis minimum",
    )
    p.add_argument(
        "--x-max", type=float, default=None, help="Real axis maximum",
    )
    p.add_argument(
        "--y-min", type=float, default=None, help="Imaginary axis minimum",
    )
    p.add_argument(
        "--y-max", type=float, default=None, help="Imaginary axis maximum",
    )
    p.add_argument(
        "--c-real", type=float, default=-0.7269,
        help="Julia set c parameter (real part, default: -0.7269)",
    )
    p.add_argument(
        "--c-imag", type=float, default=0.1889,
        help="Julia set c parameter (imaginary part, default: 0.1889)",
    )
    p.add_argument(
        "--julia-preset",
        choices=list(_JULIA_PRESETS.keys()),
        default=None,
        help="Julia set preset (overrides --c-real/--c-imag)",
    )
    p.add_argument(
        "--save", "-s", metavar="FILE",
        help="Save PNG to FILE (requires Pillow)",
    )
    p.add_argument(
        "--scale", type=int, default=2,
        help="PNG pixel upscale factor (default: 2)",
    )
    p.add_argument(
        "--no-terminal", action="store_true",
        help="Skip terminal rendering (useful with --save)",
    )
    p.add_argument(
        "--list", "-l", action="store_true",
        help="List available fractals and palettes",
    )
    p.add_argument(
        "--all", "-a", action="store_true",
        help="Render all fractals with all palettes to ./gallery/",
    )
    return p


def _render_one(args, fractal_name: str, palette: str, width: int, height: int) -> tuple:
    """Compute fractal data and apply palette. Returns (data, rgb)."""
    fn = FRACTALS[fractal_name]
    defaults = _FRACTAL_DEFAULTS[fractal_name]

    kwargs = dict(
        width=width,
        height=height,
        max_iter=args.max_iter,
        x_min=args.x_min if args.x_min is not None else defaults["x_min"],
        x_max=args.x_max if args.x_max is not None else defaults["x_max"],
        y_min=args.y_min if args.y_min is not None else defaults["y_min"],
        y_max=args.y_max if args.y_max is not None else defaults["y_max"],
    )
    if fractal_name == "julia":
        if args.julia_preset:
            kwargs["c_real"], kwargs["c_imag"] = _JULIA_PRESETS[args.julia_preset]
        else:
            kwargs["c_real"] = args.c_real
            kwargs["c_imag"] = args.c_imag

    data = fn(**kwargs)
    rgb = apply_palette(data, palette)
    return data, rgb


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list:
        print("Fractals:", ", ".join(_FRACTAL_NAMES))
        print("Palettes:", ", ".join(PALETTE_NAMES))
        print("\nJulia presets:")
        for name, (cr, ci) in _JULIA_PRESETS.items():
            sign = "+" if ci >= 0 else ""
            print(f"  {name:<16}  c = {cr}{sign}{ci}i")
        return 0

    if args.all:
        if not pil_available():
            print("ERROR: --all requires Pillow. Install with: pip install Pillow", file=sys.stderr)
            return 1
        total = len(_FRACTAL_NAMES) * len(PALETTE_NAMES)
        print(f"Generating gallery: {total} images …")
        for fractal_name in _FRACTAL_NAMES:
            for palette in PALETTE_NAMES:
                _, rgb = _render_one(args, fractal_name, palette, args.width, args.height)
                path = f"gallery/{fractal_name}/{palette}.png"
                render_image(rgb, path, scale=args.scale)
                print(f"  saved {path}")
        print(f"Done. Gallery written to ./gallery/")
        return 0

    t0 = time.perf_counter()
    _, rgb = _render_one(args, args.fractal, args.palette, args.width, args.height)
    elapsed = time.perf_counter() - t0

    title = f"{args.fractal.replace('_', ' ').title()}  [{args.palette}]"

    if not args.no_terminal:
        print_fractal(rgb, title=title)

    if args.save:
        if not pil_available():
            print("WARNING: Pillow not installed; skipping PNG export.", file=sys.stderr)
        else:
            out = render_image(rgb, args.save, scale=args.scale)
            print(f"Saved: {out}  ({rgb.shape[1]}×{rgb.shape[0]}px × {args.scale}× scale)")

    print(f"Rendered in {elapsed:.2f}s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
