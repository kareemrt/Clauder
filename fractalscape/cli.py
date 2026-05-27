"""
Command-line interface for FractalScape.
Handles argument parsing, rendering pipeline, and interactive exploration.
"""
import argparse
import os
import sys
import time
from typing import Optional

from .colors import THEME_NAMES, get_colormap_preview
from .core import compute_fractal
from .export import export_png, RESOLUTIONS, PILLOW_AVAILABLE
from .presets import PRESETS, list_presets, FEATURED_PRESETS
from .render import (
    get_terminal_size,
    print_fractal,
    render_info_panel,
    render_progress_bar,
    clear_line,
)

BANNER = r"""
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗      ███████╗ ██████╗ █████╗ ██████╗ ███████╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║      ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║      ███████╗██║     ███████║██████╔╝█████╗
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║      ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗ ███████║╚██████╗██║  ██║██║     ███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝
"""

SUBTITLE = "  Explore the infinite beauty of mathematical fractals in your terminal"


def _print_banner() -> None:
    print("\033[96m" + BANNER + "\033[0m")
    print(f"\033[90m{SUBTITLE}\033[0m\n")


def _progress_printer(label: str):
    start = time.time()

    def callback(p: float) -> None:
        elapsed = time.time() - start
        bar = render_progress_bar(p)
        clear_line()
        sys.stdout.write(f"  {label} {bar}  {elapsed:.1f}s")
        sys.stdout.flush()

    return callback


def _resolve_bounds(args, preset: Optional[dict] = None):
    """Determine viewport bounds from args or preset."""
    if args.bounds:
        parts = [float(v) for v in args.bounds.split(",")]
        return tuple(parts)  # x_min, x_max, y_min, y_max

    if preset:
        return preset["bounds"]

    # Sensible defaults per fractal type
    defaults = {
        "mandelbrot":   (-2.5, 1.0, -1.25, 1.25),
        "julia":        (-1.6, 1.6, -1.0, 1.0),
        "burning_ship": (-2.5, 1.5, -2.0, 0.5),
        "tricorn":      (-2.5, 1.0, -1.25, 1.25),
        "newton":       (-1.5, 1.5, -1.5, 1.5),
    }
    return defaults.get(args.fractal, (-2.5, 1.0, -1.25, 1.25))


def _resolve_julia_c(args, preset: Optional[dict] = None):
    if args.julia_c:
        parts = args.julia_c.split(",")
        return (float(parts[0]), float(parts[1]))
    if preset and "julia_c" in preset:
        return preset["julia_c"]
    return (-0.7, 0.27015)


def cmd_render(args) -> None:
    """Main render command: draw fractal to terminal and/or export PNG."""
    preset = PRESETS.get(args.preset) if args.preset else None

    fractal_type = args.fractal or (preset["fractal"] if preset else "mandelbrot")
    theme        = args.theme   or (preset["theme"]   if preset else "electric")
    max_iter     = args.max_iter or (preset["max_iter"] if preset else 256)
    cycle_period = args.cycle   or (preset["cycle"]   if preset else 64.0)
    bounds       = _resolve_bounds(args, preset)
    julia_c      = _resolve_julia_c(args, preset)

    x_min, x_max, y_min, y_max = bounds

    # ── Terminal size ─────────────────────────────────────────────────────
    term_w, term_h = get_terminal_size()
    width  = min(args.width  or term_w, term_w)
    height = min(args.height or (term_h - 8) * 2, (term_h - 8) * 2)
    height = max(4, height)

    if not args.quiet:
        _print_banner()

    # ── Compute ───────────────────────────────────────────────────────────
    progress_cb = None if args.quiet else _progress_printer("Rendering")
    t0 = time.time()
    data = compute_fractal(
        width, height, x_min, x_max, y_min, y_max,
        fractal_type=fractal_type,
        max_iter=max_iter,
        julia_c=julia_c,
        progress_callback=progress_cb,
    )
    elapsed = time.time() - t0

    if not args.quiet:
        clear_line()
        print(f"  \033[92m✓\033[0m Rendered {width}×{height} in {elapsed:.2f}s\n")

    # ── Display ───────────────────────────────────────────────────────────
    if not args.no_display:
        label = preset["description"] if preset else f"{fractal_type.title()} Fractal"
        print_fractal(data, max_iter, theme, cycle_period, title=label)

        if not args.quiet:
            print()
            print(render_info_panel(
                fractal_type, theme,
                x_min, x_max, y_min, y_max,
                max_iter, width, height,
            ))
            print()

    # ── Export ────────────────────────────────────────────────────────────
    if args.export:
        if not PILLOW_AVAILABLE:
            print("\033[91mPillow not installed. Run: pip install Pillow\033[0m")
        else:
            res_key = getattr(args, "resolution", "1080p") or "1080p"
            exp_w, exp_h = RESOLUTIONS.get(res_key, (1920, 1080))
            out_path = args.export

            if not args.quiet:
                print(f"  Exporting {exp_w}×{exp_h} PNG…")

            cb2 = None if args.quiet else _progress_printer("Exporting")
            from .export import export_hires
            ok = export_hires(
                exp_w, exp_h, x_min, x_max, y_min, y_max,
                fractal_type, max_iter, theme, out_path,
                julia_c=julia_c,
                cycle_period=cycle_period,
                progress_callback=cb2,
            )
            if not args.quiet:
                clear_line()
                if ok:
                    print(f"  \033[92m✓\033[0m Saved to \033[96m{out_path}\033[0m")
                else:
                    print(f"  \033[91m✗\033[0m Export failed")


def cmd_gallery(args) -> None:
    """Render multiple featured presets in sequence."""
    _print_banner()
    presets_to_show = FEATURED_PRESETS if not args.all else list(PRESETS.keys())
    term_w, term_h = get_terminal_size()
    width  = min(100, term_w)
    height = min(50, (term_h - 8) * 2)

    for name in presets_to_show:
        p = PRESETS[name]
        fractal_type = p["fractal"]
        bounds       = p["bounds"]
        julia_c      = p.get("julia_c", (-0.7, 0.27015))
        max_iter     = p["max_iter"]
        theme        = p["theme"]
        cycle        = p.get("cycle", 64)

        print(f"\033[1;97m  ▶ {name}\033[0m  \033[90m{p['description']}\033[0m")
        t0 = time.time()
        data = compute_fractal(
            width, height,
            bounds[0], bounds[1], bounds[2], bounds[3],
            fractal_type=fractal_type,
            max_iter=max_iter,
            julia_c=julia_c,
        )
        print_fractal(data, max_iter, theme, cycle)
        print(f"\033[90m  {time.time()-t0:.2f}s\033[0m\n")

        if not args.no_pause:
            try:
                input("  \033[90mPress Enter for next…\033[0m")
            except (EOFError, KeyboardInterrupt):
                break

    print("\n\033[96m  Gallery complete.\033[0m")


def cmd_themes(args) -> None:
    """Display all available color themes as gradient swatches."""
    _print_banner()
    print("  \033[1;97mAvailable Themes\033[0m\n")
    for name in THEME_NAMES:
        preview = get_colormap_preview(name, width=50)
        print(f"  \033[96m{name:<14}\033[0m  {preview}")
    print()


def cmd_presets(args) -> None:
    """List available presets."""
    _print_banner()
    print(list_presets(verbose=args.verbose))


def cmd_benchmark(args) -> None:
    """Benchmark fractal computation speed."""
    import math
    _print_banner()
    print("  \033[1;97mPerformance Benchmark\033[0m\n")

    configs = [
        ("Mandelbrot  320×240  iter=128",  "mandelbrot",   320,  240, 128),
        ("Mandelbrot  640×480  iter=256",  "mandelbrot",   640,  480, 256),
        ("Mandelbrot 1280×720  iter=512",  "mandelbrot",  1280,  720, 512),
        ("Julia       640×480  iter=256",  "julia",        640,  480, 256),
        ("Burning Ship 640×480 iter=256",  "burning_ship", 640,  480, 256),
    ]

    for label, ftype, w, h, iters in configs:
        t0 = time.time()
        compute_fractal(w, h, -2.5, 1.0, -1.25, 1.25,
                         fractal_type=ftype, max_iter=iters)
        elapsed = time.time() - t0
        mpps = (w * h * iters) / elapsed / 1e6
        print(f"  {label:<40}  {elapsed:5.2f}s  ({mpps:.1f}M iter/s)")

    print()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fractalscape",
        description="FractalScape — terminal fractal explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Classic Mandelbrot in terminal
  python main.py --preset julia-rabbit              # Douady Rabbit Julia set
  python main.py --fractal burning_ship --theme fire
  python main.py --preset deep-spiral --export spiral.png
  python main.py gallery                            # Cycle through featured presets
  python main.py themes                             # Show color swatches
  python main.py presets --verbose                  # List all presets with bounds
  python main.py benchmark                          # Performance test
""",
    )
    sub = p.add_subparsers(dest="command")

    # ── render (default) ─────────────────────────────────────────────────
    r = sub.add_parser("render", help="Render a fractal (default command)")
    _add_render_args(r)

    # ── gallery ───────────────────────────────────────────────────────────
    g = sub.add_parser("gallery", help="Cycle through featured presets")
    g.add_argument("--all", action="store_true", help="Show all presets (not just featured)")
    g.add_argument("--no-pause", action="store_true", help="Don't pause between renders")

    # ── themes ────────────────────────────────────────────────────────────
    sub.add_parser("themes", help="Show all color theme swatches")

    # ── presets ───────────────────────────────────────────────────────────
    ps = sub.add_parser("presets", help="List available presets")
    ps.add_argument("-v", "--verbose", action="store_true")

    # ── benchmark ─────────────────────────────────────────────────────────
    sub.add_parser("benchmark", help="Benchmark computation speed")

    # Allow top-level render args (no subcommand)
    _add_render_args(p)

    return p


def _add_render_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--preset", "-p",    metavar="NAME",
                   help=f"Load a preset location ({', '.join(list(PRESETS)[:5])}…)")
    p.add_argument("--fractal", "-f",   metavar="TYPE",
                   choices=["mandelbrot","julia","burning_ship","tricorn","newton"],
                   help="Fractal type")
    p.add_argument("--theme", "-t",     metavar="NAME",
                   choices=THEME_NAMES, help="Color theme")
    p.add_argument("--max-iter", "-i",  metavar="N", type=int,
                   help="Maximum iterations (default: 256)")
    p.add_argument("--cycle", "-c",     metavar="N", type=float,
                   help="Color cycle period (default: 64)")
    p.add_argument("--bounds", "-b",    metavar="x0,x1,y0,y1",
                   help="Viewport bounds as comma-separated floats")
    p.add_argument("--julia-c",         metavar="re,im",
                   help="Julia set constant e.g. -0.7,0.27015")
    p.add_argument("--width", "-W",     metavar="N", type=int,
                   help="Output width in pixels")
    p.add_argument("--height", "-H",    metavar="N", type=int,
                   help="Output height in pixels (2× terminal rows with half-blocks)")
    p.add_argument("--export", "-e",    metavar="FILE",
                   help="Also export a high-res PNG to this path")
    p.add_argument("--resolution",      metavar="RES",
                   choices=list(RESOLUTIONS.keys()), default="1080p",
                   help="Export resolution (default: 1080p)")
    p.add_argument("--no-display",      action="store_true",
                   help="Skip terminal display (useful with --export)")
    p.add_argument("--quiet", "-q",     action="store_true",
                   help="Suppress progress output")


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "render":    cmd_render,
        "gallery":   cmd_gallery,
        "themes":    cmd_themes,
        "presets":   cmd_presets,
        "benchmark": cmd_benchmark,
    }

    cmd = args.command
    if cmd in dispatch:
        dispatch[cmd](args)
    else:
        # No subcommand: default render
        cmd_render(args)
