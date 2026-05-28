"""
FractalDreams CLI — command-line interface for rendering and exploring fractals.

Commands:
    render   — render a named preset or custom viewport
    gallery  — list all available presets
    explore  — render all presets in a category
    info     — show mathematical background
"""

from __future__ import annotations

import argparse
import os
import sys
import time

from fractal_dreams import fractals as fx
from fractal_dreams.renderer import render_frame, render_frame_plain, render_info_panel
from fractal_dreams.presets import ALL_PRESETS, MANDELBROT_PRESETS, JULIA_PRESETS, EXOTIC_PRESETS
from fractal_dreams.palette import PALETTES
from fractal_dreams.narrator import narrate


_FRACTAL_MAP = {
    "mandelbrot": fx.mandelbrot,
    "julia": fx.julia,
    "burning_ship": fx.burning_ship,
    "newton": fx.newton,
    "tricorn": fx.tricorn,
}

_BANNER = r"""
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

  ██████╗ ██████╗ ███████╗ █████╗ ███╗   ███╗███████╗
  ██╔══██╗██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔════╝
  ██║  ██║██████╔╝█████╗  ███████║██╔████╔██║███████╗
  ██║  ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║╚════██║
  ██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████║
  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                    A Journey Through Infinite Mathematics
"""


def _detect_color() -> bool:
    """Detect if the terminal supports ANSI colors."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


def _get_terminal_size(fallback: tuple[int, int] = (120, 40)) -> tuple[int, int]:
    try:
        import shutil
        size = shutil.get_terminal_size(fallback)
        return size.columns, size.lines
    except Exception:
        return fallback


def cmd_render(args: argparse.Namespace) -> None:
    """Render a single preset or custom viewport."""
    color = _detect_color() and not args.no_color

    # --- Find preset or build custom ---
    preset = None
    if args.preset:
        name_lower = args.preset.lower()
        for p in ALL_PRESETS:
            if p.name.lower() == name_lower or p.name.lower().startswith(name_lower):
                preset = p
                break
        if preset is None:
            print(f"Unknown preset: {args.preset!r}. Run `gallery` to list all presets.")
            sys.exit(1)

    if preset:
        fractal_fn = _FRACTAL_MAP[preset.fractal]
        xmin, xmax = preset.xmin, preset.xmax
        ymin, ymax = preset.ymin, preset.ymax
        max_iter = args.iter or preset.max_iter
        palette = args.palette or preset.palette
        julia_c = preset.julia_c
        name = preset.name
        description = preset.description
        fractal_type = preset.fractal
    else:
        fractal_type = args.fractal or "mandelbrot"
        fractal_fn = _FRACTAL_MAP[fractal_type]
        xmin = args.xmin if args.xmin is not None else -2.5
        xmax = args.xmax if args.xmax is not None else 1.0
        ymin = args.ymin if args.ymin is not None else -1.25
        ymax = args.ymax if args.ymax is not None else 1.25
        max_iter = args.iter or 256
        palette = args.palette or "fire"
        julia_c = complex(args.julia_c) if args.julia_c else None
        name = f"Custom {fractal_type.title()}"
        description = "User-defined viewport."

    term_w, term_h = _get_terminal_size()
    width = args.width or min(term_w - 2, 120)
    height = args.height or min(term_h - 8, 40)

    # --- Compute ---
    print(f"\nRendering {name} ({width}×{height}, {max_iter} iter)…", end="", flush=True)
    t0 = time.perf_counter()
    kwargs = {}
    if fractal_type == "julia" and julia_c is not None:
        from functools import partial
        fractal_fn_base = fractal_fn

        def fractal_fn(c, max_iter):
            return fractal_fn_base(c, max_iter, seed=c)

        # For julia, the "c" parameter is fixed; pixel coords are z
        def julia_render(pixel_c, mi, jc=julia_c):
            return fx.julia(jc, mi, seed=pixel_c)

        fractal_fn = julia_render

    frame = fx.compute_frame(fractal_fn, xmin, xmax, ymin, ymax, width, height, max_iter)
    elapsed = time.perf_counter() - t0
    print(f" done in {elapsed:.2f}s\n")

    # --- Render ---
    output = render_frame(frame, max_iter, palette_name=palette, charset=args.charset, color=color)
    panel = render_info_panel(name, fractal_type, (xmin, xmax, ymin, ymax), max_iter, palette, width, height)

    print(output)
    print()
    print(panel)

    # --- Narration ---
    if args.narrate:
        print("\n Generating AI narration…\n")
        text = narrate(
            fractal_type, name, description,
            (xmin, xmax, ymin, ymax),
            max_iter, palette, julia_c,
        )
        print(f"  ✦  {text}\n")

    # --- Save ---
    if args.save:
        plain = render_frame_plain(frame, max_iter, charset=args.charset)
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n")
            f.write(f"# Viewport: x=[{xmin}, {xmax}], y=[{ymin}, {ymax}]\n")
            f.write(f"# Iterations: {max_iter}, Palette: {palette}\n\n")
            f.write(plain)
        print(f"Saved to {args.save}")


def cmd_gallery(args: argparse.Namespace) -> None:
    """List all available presets with descriptions."""
    categories = [
        ("Mandelbrot Set", MANDELBROT_PRESETS),
        ("Julia Sets", JULIA_PRESETS),
        ("Exotic Fractals", EXOTIC_PRESETS),
    ]
    print()
    for cat_name, presets in categories:
        print(f"  ── {cat_name} {'─' * (50 - len(cat_name))}")
        for p in presets:
            julia_note = f"  (c = {p.julia_c.real:+.4f}{p.julia_c.imag:+.4f}i)" if p.julia_c else ""
            print(f"  • {p.name:<30} {p.description[:50]}…{julia_note}")
        print()
    print(f"  Palettes: {', '.join(PALETTES.keys())}")
    print()


def cmd_explore(args: argparse.Namespace) -> None:
    """Render all presets in a category, one after another."""
    category = args.category.lower()
    if category == "mandelbrot":
        presets = MANDELBROT_PRESETS
    elif category == "julia":
        presets = JULIA_PRESETS
    elif category == "exotic":
        presets = EXOTIC_PRESETS
    else:
        presets = ALL_PRESETS

    color = _detect_color() and not args.no_color
    term_w, term_h = _get_terminal_size()
    width = args.width or min(term_w - 2, 100)
    height = args.height or min(term_h - 10, 35)

    for p in presets:
        fractal_fn = _FRACTAL_MAP[p.fractal]

        if p.fractal == "julia" and p.julia_c:
            jc = p.julia_c

            def julia_render(pixel_c, mi, jc=jc):
                return fx.julia(jc, mi, seed=pixel_c)

            fn = julia_render
        else:
            fn = fractal_fn

        print(f"\n{'═' * width}")
        print(f"  {p.name.upper()}")
        print(f"  {p.description}")
        print(f"{'═' * width}\n")

        frame = fx.compute_frame(fn, p.xmin, p.xmax, p.ymin, p.ymax, width, height, p.max_iter)
        print(render_frame(frame, p.max_iter, palette_name=p.palette, charset="dense", color=color))
        print()

        if args.pause:
            input("  [Enter for next…]")


def cmd_info(_: argparse.Namespace) -> None:
    """Print mathematical background about fractal types."""
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                  THE MATHEMATICS OF FRACTALS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MANDELBROT SET                                                 │
│  f_c(z) = z² + c,  z₀ = 0                                     │
│  The set of all c ∈ ℂ for which the orbit {f_c^n(0)} is       │
│  bounded. Its boundary has Hausdorff dimension 2 (Shishikura). │
│                                                                 │
│  JULIA SETS                                                     │
│  f_c(z) = z² + c,  z₀ = pixel                                 │
│  For each c, Julia set J(c) is the boundary of basins of       │
│  attraction. Connected iff c ∈ Mandelbrot set (Fatou-Julia).  │
│                                                                 │
│  BURNING SHIP                                                   │
│  f_c(z) = (|Re(z)| + i|Im(z)|)² + c                          │
│  Absolute-value fold breaks holomorphic symmetry, creating     │
│  the haunted ship silhouette visible at full zoom.             │
│                                                                 │
│  NEWTON FRACTAL                                                 │
│  z ↦ z - f(z)/f'(z),  f(z) = z³ - 1                         │
│  Basins of attraction for Newton's method on three cube        │
│  roots of unity. Boundary is a fractal of measure zero.        │
│                                                                 │
│  TRICORN (MANDELBAR)                                           │
│  f_c(z) = z̄² + c  (z̄ = complex conjugate)                   │
│  Anti-holomorphic iteration produces thorn-like structures     │
│  incompatible with the Mandelbrot set's smooth spirals.        │
│                                                                 │
│  SMOOTH COLORING                                               │
│  escape_smooth = i + 1 - log(log|z|)/log(2)                  │
│  Removes banding artifacts by interpolating between integer    │
│  escape times using the potential function.                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fractal-dreams",
        description="FractalDreams — render beautiful fractals in your terminal",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── render ─────────────────────────────────────────────────────────────────
    r = sub.add_parser("render", help="Render a fractal preset or custom viewport")
    r.add_argument("preset", nargs="?", help="Preset name (see gallery)")
    r.add_argument("--fractal", choices=list(_FRACTAL_MAP), default="mandelbrot")
    r.add_argument("--xmin", type=float)
    r.add_argument("--xmax", type=float)
    r.add_argument("--ymin", type=float)
    r.add_argument("--ymax", type=float)
    r.add_argument("--iter", type=int, help="Maximum iterations")
    r.add_argument("--palette", choices=list(PALETTES), help="Color palette")
    r.add_argument("--charset", choices=["dense", "simple", "blocks"], default="dense")
    r.add_argument("--width", type=int, help="Output width in chars")
    r.add_argument("--height", type=int, help="Output height in chars")
    r.add_argument("--julia-c", metavar="COMPLEX", help='Julia parameter, e.g. "-0.7269+0.1889j"')
    r.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    r.add_argument("--narrate", action="store_true", help="Generate Claude AI narration")
    r.add_argument("--save", metavar="FILE", help="Save plain-text render to file")

    # ── gallery ────────────────────────────────────────────────────────────────
    sub.add_parser("gallery", help="List all available presets")

    # ── explore ────────────────────────────────────────────────────────────────
    e = sub.add_parser("explore", help="Render all presets in a category")
    e.add_argument("category", choices=["mandelbrot", "julia", "exotic", "all"])
    e.add_argument("--width", type=int)
    e.add_argument("--height", type=int)
    e.add_argument("--no-color", action="store_true")
    e.add_argument("--pause", action="store_true", help="Pause between renders")

    # ── info ───────────────────────────────────────────────────────────────────
    sub.add_parser("info", help="Mathematical background on fractal types")

    return parser


def main() -> None:
    print(_BANNER)
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "render": cmd_render,
        "gallery": cmd_gallery,
        "explore": cmd_explore,
        "info": cmd_info,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
