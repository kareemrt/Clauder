#!/usr/bin/env python3
"""FractalForge CLI — Interactive terminal fractal explorer."""

import argparse
import os
import sys
import time
from typing import Optional

import numpy as np

from .fractals import mandelbrot, julia, burning_ship, tricorn, FRACTAL_REGISTRY
from .palettes import PALETTES
from .presets import PRESETS, PRESET_MAP
from .renderer import print_fractal, render_terminal, save_png, render_ascii_art


BANNER = r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗         ║
║    ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║         ║
║    █████╗  ██████╔╝███████║██║        ██║   ███████║██║         ║
║    ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║         ║
║    ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗    ║
║    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝    ║
║                                                                  ║
║         ███████╗ ██████╗ ██████╗  ██████╗ ███████╗              ║
║         ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝              ║
║         █████╗  ██║   ██║██████╔╝██║  ███╗█████╗                ║
║         ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝                ║
║         ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗              ║
║         ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝              ║
║                                                                  ║
║   Explore the infinite beauty of mathematical complexity         ║
╚══════════════════════════════════════════════════════════════════╝
"""


def get_terminal_size() -> tuple:
    try:
        cols, rows = os.get_terminal_size()
        return cols, rows
    except OSError:
        return 120, 40


def compute_fractal(args, preset=None) -> np.ndarray:
    """Dispatch to the correct fractal renderer."""
    if preset:
        fractal_name = preset.fractal
        center = preset.center
        zoom = preset.zoom
        max_iter = preset.max_iter
        julia_c = preset.julia_c
    else:
        fractal_name = args.fractal
        center = (args.cx, args.cy)
        zoom = args.zoom
        max_iter = args.iterations
        julia_c = complex(args.julia_real, args.julia_imag) if fractal_name == "julia" else None

    width = args.width
    height = args.height

    print(f"  Rendering {fractal_name} at ({center[0]:.6f}, {center[1]:.6f})  "
          f"zoom={zoom:.2f}  iter={max_iter} ...", flush=True)
    t0 = time.perf_counter()

    if fractal_name == "mandelbrot":
        field = mandelbrot(width, height, center=center, zoom=zoom, max_iter=max_iter)
    elif fractal_name == "julia":
        field = julia(width, height, c=julia_c, center=center, zoom=zoom, max_iter=max_iter)
    elif fractal_name == "burning_ship":
        field = burning_ship(width, height, center=center, zoom=zoom, max_iter=max_iter)
    elif fractal_name == "tricorn":
        field = tricorn(width, height, center=center, zoom=zoom, max_iter=max_iter)
    else:
        raise ValueError(f"Unknown fractal: {fractal_name}")

    elapsed = time.perf_counter() - t0
    print(f"  Done in {elapsed:.2f}s\n", flush=True)
    return field


def cmd_render(args):
    """Render a fractal to the terminal."""
    preset = PRESET_MAP.get(args.preset) if args.preset else None
    palette_name = (preset.palette if preset else None) or args.palette

    cols, rows = get_terminal_size()
    if not hasattr(args, "width") or args.width is None:
        args.width = cols
    if not hasattr(args, "height") or args.height is None:
        args.height = (rows - 4) * 2  # half-block trick doubles rows

    field = compute_fractal(args, preset)

    title = (preset.description if preset else f"{args.fractal} — zoom {args.zoom}x")
    print_fractal(field, palette_name=palette_name, title=title)

    if args.output:
        palette = PALETTES.get(palette_name, PALETTES["electric"])
        save_png(field, palette, args.output, scale=args.scale)
        print(f"\n  Saved PNG: {args.output}")


def cmd_export(args):
    """Export a fractal to a high-resolution PNG."""
    preset = PRESET_MAP.get(args.preset) if args.preset else None
    palette_name = (preset.palette if preset else None) or args.palette

    args.width = args.width or 1920
    args.height = args.height or 1080

    field = compute_fractal(args, preset)
    palette = PALETTES.get(palette_name, PALETTES["electric"])

    out = args.output or f"{args.fractal or preset.fractal}_{int(time.time())}.png"
    save_png(field, palette, out, scale=args.scale)
    print(f"  Saved: {out}  ({args.width * args.scale} x {args.height * args.scale} px)")


def cmd_gallery(args):
    """Display all presets one after another."""
    print(BANNER)
    print("  Launching fractal gallery — press Ctrl+C to skip\n")
    time.sleep(1)

    cols, rows = get_terminal_size()
    args.width = min(cols, 160)
    args.height = min((rows - 6) * 2, 80)

    for preset in PRESETS:
        if args.fractal and preset.fractal != args.fractal:
            continue
        print(f"\n  ► {preset.name}: {preset.description}")
        try:
            field = compute_fractal(args, preset)
            print_fractal(field, palette_name=preset.palette, title=preset.description)
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n  Skipping...")
            continue

    print("\n  Gallery complete!")


def cmd_list(args):
    """List all available presets, palettes, and fractals."""
    print(BANNER)

    print("  FRACTALS")
    print("  " + "─" * 50)
    for name in FRACTAL_REGISTRY:
        print(f"    • {name}")

    print("\n  PALETTES")
    print("  " + "─" * 50)
    for name, palette in PALETTES.items():
        swatch = "".join(
            f"\033[38;2;{r};{g};{b}m█\033[0m"
            for r, g, b in palette.colors[::max(1, len(palette.colors) // 10)]
        )
        print(f"    {name:<16} {swatch}")

    print("\n  PRESETS")
    print("  " + "─" * 50)
    for preset in PRESETS:
        print(preset.display())
    print()


def cmd_ascii(args):
    """Render fractal as plain ASCII art (no color, 256-char wide)."""
    preset = PRESET_MAP.get(args.preset) if args.preset else None
    args.width = args.width or 100
    args.height = args.height or 40
    field = compute_fractal(args, preset)
    print(render_ascii_art(field))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fractalforge",
        description="FractalForge — Explore infinite mathematical beauty in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fractalforge render                         # Mandelbrot overview
  fractalforge render -p seahorse-valley      # Famous Seahorse Valley preset
  fractalforge render -f julia --palette fire # Julia set with fire palette
  fractalforge render --cx -0.75 --cy 0.1 --zoom 15
  fractalforge export -p julia-dragon -o dragon.png --scale 2
  fractalforge gallery                        # Cycle through all presets
  fractalforge list                           # Show all options
  fractalforge ascii -p burning-ship          # ASCII art mode
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # Shared fractal arguments
    def add_fractal_args(p):
        p.add_argument("-f", "--fractal", default="mandelbrot",
                       choices=list(FRACTAL_REGISTRY.keys()),
                       help="Fractal type (default: mandelbrot)")
        p.add_argument("-p", "--preset", default=None,
                       help="Named preset (overrides other fractal settings)")
        p.add_argument("--cx", type=float, default=-0.5, help="Center X (real axis)")
        p.add_argument("--cy", type=float, default=0.0, help="Center Y (imaginary axis)")
        p.add_argument("--zoom", type=float, default=1.0, help="Zoom level (default: 1.0)")
        p.add_argument("-i", "--iterations", type=int, default=256,
                       help="Max iterations (default: 256)")
        p.add_argument("--julia-real", type=float, default=-0.7269,
                       help="Julia c real part (default: -0.7269)")
        p.add_argument("--julia-imag", type=float, default=0.1889,
                       help="Julia c imaginary part (default: 0.1889)")
        p.add_argument("--width", type=int, default=None, help="Width in pixels")
        p.add_argument("--height", type=int, default=None, help="Height in pixels")
        p.add_argument("--palette", default="electric",
                       choices=list(PALETTES.keys()), help="Color palette")

    # render
    r = sub.add_parser("render", help="Render fractal to terminal")
    add_fractal_args(r)
    r.add_argument("-o", "--output", default=None, help="Also save as PNG")
    r.add_argument("--scale", type=int, default=1, help="PNG pixel scale factor")
    r.set_defaults(func=cmd_render)

    # export
    e = sub.add_parser("export", help="Export fractal as high-res PNG")
    add_fractal_args(e)
    e.add_argument("-o", "--output", default=None, help="Output PNG path")
    e.add_argument("--scale", type=int, default=2, help="Pixel scale factor (default: 2)")
    e.set_defaults(func=cmd_export)

    # gallery
    g = sub.add_parser("gallery", help="Cycle through all presets")
    g.add_argument("-f", "--fractal", default=None,
                   help="Filter by fractal type")
    g.add_argument("--width", type=int, default=None)
    g.add_argument("--height", type=int, default=None)
    g.add_argument("--zoom", type=float, default=None)
    g.add_argument("--cx", type=float, default=None)
    g.add_argument("--cy", type=float, default=None)
    g.add_argument("--iterations", type=int, default=None)
    g.add_argument("--julia-real", type=float, default=-0.7269)
    g.add_argument("--julia-imag", type=float, default=0.1889)
    g.set_defaults(func=cmd_gallery)

    # list
    l = sub.add_parser("list", help="List presets, palettes, fractals")
    l.set_defaults(func=cmd_list)

    # ascii
    a = sub.add_parser("ascii", help="Render as plain ASCII art")
    add_fractal_args(a)
    a.set_defaults(func=cmd_ascii)

    return parser


def main():
    print(BANNER)
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        # Default: show gallery overview
        args.func = cmd_list
        cmd_list(args)
        print("\n  Run 'fractalforge render' to explore, or 'fractalforge --help' for options.\n")
        return

    args.func(args)


if __name__ == "__main__":
    main()
