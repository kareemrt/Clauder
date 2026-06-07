"""Command-line interface: `python -m fractalforge ...`."""

from __future__ import annotations

import argparse
import sys
import time

from . import palettes
from .fractals import FAMILIES, Viewport
from .render import render_to_file


def _parse_complex(text: str) -> complex:
    """Parse "re,im" (or a bare real number) into a complex coordinate."""
    text = text.strip()
    if "," in text:
        re_part, im_part = text.split(",", 1)
        return complex(float(re_part), float(im_part))
    return complex(float(text))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fractalforge",
        description="Render escape-time fractals straight to PNG, dependency-free.",
    )
    parser.add_argument(
        "fractal", choices=FAMILIES, help="Which fractal family to render."
    )
    parser.add_argument(
        "-o", "--output", default="fractal.png", help="Output PNG path (default: fractal.png)."
    )
    parser.add_argument(
        "--width", type=int, default=800, help="Image width in pixels (default: 800)."
    )
    parser.add_argument(
        "--height", type=int, default=600, help="Image height in pixels (default: 600)."
    )
    parser.add_argument(
        "--center",
        type=_parse_complex,
        default=complex(-0.5, 0.0),
        metavar="RE,IM",
        help="Centre of the view in the complex plane (default: -0.5,0).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.5,
        help="Half-height of the view in plane units; smaller = more zoomed in (default: 1.5).",
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=200,
        help="Maximum iterations before a point is considered inside the set (default: 200).",
    )
    parser.add_argument(
        "--palette",
        choices=palettes.names(),
        default="inferno",
        help="Colour gradient to use (default: inferno).",
    )
    parser.add_argument(
        "--julia-c",
        type=_parse_complex,
        default=complex(-0.7, 0.27015),
        metavar="RE,IM",
        help="Constant `c` for Julia sets (default: -0.7,0.27015).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    viewport = Viewport(
        width=args.width,
        height=args.height,
        center=args.center,
        scale=args.scale,
    )

    print(
        f"Rendering {args.fractal} -> {args.output} "
        f"({args.width}x{args.height}, max-iter={args.max_iter}, palette={args.palette})"
    )
    started = time.monotonic()
    render_to_file(
        args.output,
        args.fractal,
        viewport,
        args.max_iter,
        args.palette,
        julia_c=args.julia_c,
    )
    elapsed = time.monotonic() - started
    print(f"Done in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
