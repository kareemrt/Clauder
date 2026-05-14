"""Command-line interface for Fractal Studio."""
import argparse
import os
import sys
import time

from . import __version__
from .colormaps import list_palettes
from .png_writer import write_png
from .presets import PRESETS
from .renderer import render_gallery, render_preset


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fractal_studio",
        description="Fractal Studio — generate stunning fractal art in pure Python.",
    )
    parser.add_argument("--version", action="version", version=f"Fractal Studio {__version__}")
    parser.add_argument("-o", "--output", default="fractal_output",
                        metavar="DIR", help="output directory (default: fractal_output)")
    parser.add_argument("-W", "--width",  type=int, default=320,
                        metavar="PX", help="image width  in pixels (default: 320)")
    parser.add_argument("-H", "--height", type=int, default=240,
                        metavar="PX", help="image height in pixels (default: 240)")
    parser.add_argument("-p", "--preset", default=None,
                        metavar="NAME", help="render a single preset (default: all)")
    parser.add_argument("--list-presets",  action="store_true",
                        help="list available presets and exit")
    parser.add_argument("--list-palettes", action="store_true",
                        help="list available palettes and exit")
    parser.add_argument("--ascii", action="store_true",
                        help="print an ASCII-art preview to stdout instead of writing files")

    args = parser.parse_args()

    if args.list_presets:
        print("Available presets:\n")
        for key, p in PRESETS.items():
            print(f"  {key:<28}  {p['description']}")
        return

    if args.list_palettes:
        print("Available palettes:", ", ".join(list_palettes()))
        return

    if args.ascii:
        key = args.preset or "mandelbrot_classic"
        if key not in PRESETS:
            _die(f"Unknown preset '{key}'")
        _ascii_preview(key, width=args.width or 80, height=args.height or 40)
        return

    print(f"Fractal Studio v{__version__}")
    print(f"Resolution : {args.width} x {args.height}")
    print(f"Output dir : {args.output}")
    print()

    t0 = time.perf_counter()

    if args.preset:
        if args.preset not in PRESETS:
            _die(f"Unknown preset '{args.preset}'. "
                 f"Run with --list-presets to see options.")
        print(f"Rendering {PRESETS[args.preset]['name']} ...")
        pixels = render_preset(args.preset, args.width, args.height)
        os.makedirs(args.output, exist_ok=True)
        out = os.path.join(args.output, f"{args.preset}.png")
        write_png(out, pixels, args.width, args.height)
        print(f"Saved: {out}")
    else:
        print("Rendering all presets ...")
        html = render_gallery(args.output, args.width, args.height, verbose=True)
        print(f"\nHTML gallery: {html}")

    print(f"\nDone in {time.perf_counter() - t0:.1f}s")


def _ascii_preview(key: str, width: int = 80, height: int = 40) -> None:
    """Render a fractal as colourised ASCII art and print it."""
    from .renderer import render_preset

    print(f"\n{PRESETS[key]['name']}\n", flush=True)
    pixels = render_preset(key, width, height)
    chars  = " .,:;+*%#@"

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[y * width + x]
            lum  = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            char = chars[min(int(lum * len(chars)), len(chars) - 1)]
            # 24-bit ANSI colour
            row.append(f"\033[38;2;{r};{g};{b}m{char}")
        print("".join(row) + "\033[0m")
    print()


def _die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)
