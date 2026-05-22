"""Command-line interface for FractalForge."""

import sys
import os
import argparse
import time
from typing import Optional

from .core import (
    compute_mandelbrot,
    compute_julia,
    compute_burning_ship,
    compute_tricorn,
    zoom_region,
)
from .renderer import render_terminal, save_png, generate_zoom_frames
from .colormap import PALETTES

FRACTALS = {
    "mandelbrot": compute_mandelbrot,
    "julia": compute_julia,
    "burning_ship": compute_burning_ship,
    "tricorn": compute_tricorn,
}

JULIA_PRESETS = {
    "dragon":    -0.7269 + 0.1889j,
    "snowflake": -0.4 + 0.6j,
    "spiral":     0.285 + 0.01j,
    "lightning": -0.8 + 0.156j,
    "nebula":    -0.7 + 0.27015j,
    "galaxy":     0.37 + 0.1j,
}

BANNER = r"""
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

  Infinite complexity, rendered in your terminal.
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fractalforge",
        description="FractalForge — Terminal fractal art generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fractalforge render mandelbrot
  fractalforge render julia --preset dragon --palette ocean
  fractalforge render burning_ship --width 120 --height 60 --save art.png
  fractalforge zoom mandelbrot --cx -0.7436 --cy 0.1318 --end-zoom 1000
  fractalforge gallery
  fractalforge list-palettes
        """,
    )
    sub = p.add_subparsers(dest="command", required=True)

    # --- render ---
    r = sub.add_parser("render", help="Render a fractal in the terminal")
    r.add_argument("fractal", choices=list(FRACTALS), help="Which fractal to render")
    r.add_argument("--width", type=int, default=100, help="Terminal columns (default 100)")
    r.add_argument("--height", type=int, default=40, help="Terminal rows (default 40)")
    r.add_argument("--max-iter", type=int, default=256, help="Maximum iterations (default 256)")
    r.add_argument("--palette", choices=list(PALETTES), default="inferno", help="Color palette")
    r.add_argument("--mode", choices=["block", "ascii", "color_ascii"], default="color_ascii")
    r.add_argument("--save", metavar="FILE", help="Save PNG to this path")
    r.add_argument("--scale", type=int, default=2, help="PNG upscale factor (default 2)")
    r.add_argument("--preset", choices=list(JULIA_PRESETS), help="Julia set preset")
    r.add_argument("--cx", type=float, help="Julia real component")
    r.add_argument("--cy", type=float, help="Julia imaginary component")
    r.add_argument("--zoom", type=float, default=1.0, help="Zoom level")
    r.add_argument("--center-x", type=float, default=0.0, help="View center X")
    r.add_argument("--center-y", type=float, default=0.0, help="View center Y")

    # --- zoom ---
    z = sub.add_parser("zoom", help="Generate a zoom sequence as PNG frames")
    z.add_argument("fractal", choices=list(FRACTALS))
    z.add_argument("--cx", type=float, default=-0.7436, help="Zoom center X")
    z.add_argument("--cy", type=float, default=0.1318, help="Zoom center Y")
    z.add_argument("--start-zoom", type=float, default=1.0)
    z.add_argument("--end-zoom", type=float, default=500.0)
    z.add_argument("--frames", type=int, default=30)
    z.add_argument("--width", type=int, default=800)
    z.add_argument("--height", type=int, default=600)
    z.add_argument("--max-iter", type=int, default=512)
    z.add_argument("--palette", choices=list(PALETTES), default="inferno")
    z.add_argument("--output-dir", default="zoom_frames")

    # --- gallery ---
    g = sub.add_parser("gallery", help="Render all fractals and save as PNG")
    g.add_argument("--output-dir", default="gallery")
    g.add_argument("--width", type=int, default=800)
    g.add_argument("--height", type=int, default=600)
    g.add_argument("--max-iter", type=int, default=256)

    # --- list-palettes ---
    sub.add_parser("list-palettes", help="Show all available color palettes")

    # --- info ---
    sub.add_parser("info", help="Show fractal type descriptions and Julia presets")

    return p


def cmd_render(args):
    fn = FRACTALS[args.fractal]
    kwargs = dict(width=args.width, height=args.height, max_iter=args.max_iter)

    if args.fractal == "julia":
        if args.preset:
            c = JULIA_PRESETS[args.preset]
        elif args.cx is not None and args.cy is not None:
            c = complex(args.cx, args.cy)
        else:
            c = JULIA_PRESETS["dragon"]
        kwargs["c"] = c

    if args.zoom != 1.0 or args.center_x != 0.0 or args.center_y != 0.0:
        x_min, x_max, y_min, y_max = zoom_region(
            args.center_x, args.center_y, args.zoom, args.width / args.height
        )
        kwargs.update(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)

    print(f"\n  Rendering {args.fractal} | {args.width}×{args.height} | palette: {args.palette}\n")
    t0 = time.perf_counter()
    counts = fn(**kwargs)
    elapsed = time.perf_counter() - t0

    output = render_terminal(counts, args.max_iter, args.palette, args.mode)
    print(output)
    print(f"\n  Rendered in {elapsed:.3f}s")

    if args.save:
        path = save_png(counts, args.max_iter, args.save, args.palette, args.scale)
        print(f"  Saved PNG → {path}")


def cmd_zoom(args):
    fn = FRACTALS[args.fractal]
    print(f"\n  Generating {args.frames} zoom frames into {args.fractal}")
    print(f"  Center: ({args.cx}, {args.cy})  Zoom: {args.start_zoom}x → {args.end_zoom}x\n")

    paths = generate_zoom_frames(
        fn,
        center_x=args.cx,
        center_y=args.cy,
        start_zoom=args.start_zoom,
        end_zoom=args.end_zoom,
        frames=args.frames,
        width=args.width,
        height=args.height,
        max_iter=args.max_iter,
        palette=args.palette,
        output_dir=args.output_dir,
    )
    print(f"\n  {len(paths)} frames saved to ./{args.output_dir}/")
    print("  Tip: stitch with ffmpeg: ffmpeg -r 24 -i frame_%04d.png zoom.mp4")


def cmd_gallery(args):
    import os

    os.makedirs(args.output_dir, exist_ok=True)
    configs = [
        ("mandelbrot", {}, "inferno"),
        ("julia", {"c": JULIA_PRESETS["dragon"]}, "ocean"),
        ("julia", {"c": JULIA_PRESETS["snowflake"]}, "psychedelic"),
        ("julia", {"c": JULIA_PRESETS["lightning"]}, "fire"),
        ("burning_ship", {}, "copper"),
        ("tricorn", {}, "grayscale"),
    ]
    print(f"\n  Generating gallery ({len(configs)} images)...\n")
    for fractal_name, extra, palette in configs:
        fn = FRACTALS[fractal_name]
        label = f"{fractal_name}_{palette}"
        kwargs = dict(width=args.width, height=args.height, max_iter=args.max_iter, **extra)
        counts = fn(**kwargs)
        path = os.path.join(args.output_dir, f"{label}.png")
        save_png(counts, args.max_iter, path, palette)
        print(f"  ✓ {label}.png")
    print(f"\n  Gallery saved to ./{args.output_dir}/")


def cmd_list_palettes(args):
    print("\n  Available palettes:\n")
    for name in PALETTES:
        bar = ""
        palette_data = PALETTES[name]
        for pt in palette_data:
            r, g, b = pt
            bar += f"\033[48;2;{r};{g};{b}m   \033[0m"
        print(f"  {name:<14} {bar}")
    print()


def cmd_info(args):
    print("""
  FractalForge — Fractal Types
  ════════════════════════════

  mandelbrot    The classic. z → z² + c, where c varies across the plane.
                The boundary between chaos and order, infinitely detailed.

  julia         z → z² + c, where c is a fixed parameter and z varies.
                Each value of c produces a unique snowflake-like shape.
                Use --preset or --cx/--cy to explore different forms.

  burning_ship  z → (|Re(z)| + i·|Im(z)|)² + c
                A ship ablaze in the complex plane — jagged, gothic beauty.

  tricorn       z → conj(z)² + c  (Mandelbar set)
                Uses the complex conjugate — produces three-fold symmetry.

  Julia Presets:
  ──────────────""")
    for name, c in JULIA_PRESETS.items():
        print(f"  {name:<12} c = {c.real:+.4f} {c.imag:+.4f}i")
    print()


def main():
    print(BANNER)
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "render": cmd_render,
        "zoom": cmd_zoom,
        "gallery": cmd_gallery,
        "list-palettes": cmd_list_palettes,
        "info": cmd_info,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
