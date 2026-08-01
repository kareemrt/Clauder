#!/usr/bin/env python3
"""
Cosmograph — Mathematical Art Generator
========================================
Generate stunning visualizations of fractals, prime spirals,
and natural mathematical patterns.

Usage:
    python cosmograph.py gallery           # Generate all example images
    python cosmograph.py mandelbrot        # Mandelbrot set
    python cosmograph.py julia             # Julia set (classic)
    python cosmograph.py julia --preset spiral
    python cosmograph.py burning-ship      # Burning Ship fractal
    python cosmograph.py ulam              # Ulam prime spiral
    python cosmograph.py sunflower         # Fibonacci sunflower
    python cosmograph.py lissajous         # Lissajous figure
    python cosmograph.py dragon            # Dragon Curve fractal

Options:
    --theme THEME     Color theme: cosmic, inferno, ocean, forest, gold, ice, neon
    --output PATH     Output file path (default: examples/<pattern>.png)
    --width  W        Image width in pixels
    --height H        Image height in pixels
    --iter   N        Max iterations (fractals only)
    --no-preview      Skip terminal preview
"""

import sys
import math
import time
import argparse
import os
from pathlib import Path

# Allow relative imports when run as script
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich import box
from rich.text import Text

import patterns as P
import themes as T
import renderer as R

console = Console()

BANNER = r"""
   ██████╗ ██████╗ ███████╗███╗   ███╗ ██████╗  ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
  ██╔════╝██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║
  ██║     ██║   ██║███████╗██╔████╔██║██║   ██║██║  ███╗██████╔╝███████║██████╔╝███████║
  ██║     ██║   ██║╚════██║██║╚██╔╝██║██║   ██║██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║
  ╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║
   ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝
"""

PATTERNS = {
    "mandelbrot":   "Mandelbrot Set — the most famous fractal",
    "julia":        "Julia Set — parameter-driven fractal beauty",
    "burning-ship": "Burning Ship — a fiery Mandelbrot variant",
    "ulam":         "Ulam Spiral — primes hiding in plain sight",
    "sunflower":    "Fibonacci Sunflower — nature's golden ratio",
    "lissajous":    "Lissajous Figure — wave interference art",
    "dragon":       "Dragon Curve — infinite paper-fold fractal",
}


def _progress_ctx(description: str):
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    )


def cmd_mandelbrot(args):
    w, h = args.width, args.height
    theme = args.theme or "cosmic"
    out = args.output or "examples/mandelbrot.png"
    max_iter = args.iter

    console.print(f"\n[bold cyan]Rendering Mandelbrot Set[/] · {w}×{h} · theme=[yellow]{theme}[/]\n")
    t0 = time.time()

    with _progress_ctx("Computing escape times…") as prog:
        task = prog.add_task("Computing…", total=None)
        imap = P.mandelbrot(w, h, max_iter=max_iter)
        prog.update(task, completed=1, total=1)

    elapsed = time.time() - t0
    console.print(f"  [dim]Computation: {elapsed:.2f}s[/]")

    path = R.render_fractal(imap, max_iter, out, theme,
                             title="Mandelbrot Set",
                             subtitle=f"max_iter={max_iter}  theme={theme}")
    console.print(f"  [green]Saved → {path}[/]")

    if not args.no_preview:
        import numpy as np
        from themes import apply_theme
        img = apply_theme(imap, max_iter, theme)
        R.terminal_preview(img)

    return path


def cmd_julia(args):
    w, h = args.width, args.height
    theme = args.theme or "ice"
    out = args.output or "examples/julia.png"
    max_iter = args.iter
    preset = getattr(args, "preset", "classic")
    c = P.JULIA_PRESETS.get(preset, P.JULIA_PRESETS["classic"])

    console.print(f"\n[bold cyan]Rendering Julia Set[/] · preset=[yellow]{preset}[/] · c={c:.4f}\n")
    t0 = time.time()

    with _progress_ctx("Computing escape times…") as prog:
        task = prog.add_task("Computing…", total=None)
        imap = P.julia(w, h, c=c, max_iter=max_iter)
        prog.update(task, completed=1, total=1)

    elapsed = time.time() - t0
    path = R.render_fractal(imap, max_iter, out, theme,
                             title=f"Julia Set — {preset}",
                             subtitle=f"c = {c.real:.4f} + {c.imag:.4f}i")
    console.print(f"  [green]Saved → {path}[/]")

    if not args.no_preview:
        from themes import apply_theme
        img = apply_theme(imap, max_iter, theme)
        R.terminal_preview(img)

    return path


def cmd_burning_ship(args):
    w, h = args.width, args.height
    theme = args.theme or "inferno"
    out = args.output or "examples/burning_ship.png"
    max_iter = args.iter

    console.print(f"\n[bold cyan]Rendering Burning Ship Fractal[/] · {w}×{h}\n")
    t0 = time.time()

    with _progress_ctx("Computing…") as prog:
        task = prog.add_task("…", total=None)
        imap = P.burning_ship(w, h, max_iter=max_iter)
        prog.update(task, completed=1, total=1)

    path = R.render_fractal(imap, max_iter, out, theme,
                             title="Burning Ship Fractal",
                             subtitle=f"max_iter={max_iter}")
    console.print(f"  [green]Saved → {path}[/]")

    if not args.no_preview:
        from themes import apply_theme
        img = apply_theme(imap, max_iter, theme)
        R.terminal_preview(img)

    return path


def cmd_ulam(args):
    size = getattr(args, "size", 401)
    theme = args.theme or "cosmic"
    out = args.output or "examples/ulam_spiral.png"

    console.print(f"\n[bold cyan]Rendering Ulam Spiral[/] · {size}×{size} grid\n")

    with _progress_ctx("Sieving primes & mapping spiral…") as prog:
        task = prog.add_task("…", total=None)
        grid = P.ulam_spiral(size)
        prog.update(task, completed=1, total=1)

    n_primes = int(grid.sum())
    console.print(f"  [dim]{n_primes:,} primes found in {size*size:,} numbers[/]")

    path = R.render_ulam(grid, out, theme_name=theme, dot_scale=1.5)
    console.print(f"  [green]Saved → {path}[/]")

    if not args.no_preview:
        import numpy as np
        from themes import THEMES
        fn = THEMES.get(theme, THEMES["cosmic"])
        h_g, w_g = grid.shape
        img = numpy_grid_to_img(grid, fn, h_g, w_g)
        R.terminal_preview(img)

    return path


def numpy_grid_to_img(grid, fn, h, w):
    import numpy as np
    img = np.zeros((h, w, 3), dtype=np.uint8)
    ys, xs = np.where(grid == 1)
    for y, x in zip(ys, xs):
        t = math.sqrt((x - w // 2) ** 2 + (y - h // 2) ** 2) / (min(w, h) / 2)
        img[y, x] = fn(min(t ** 0.5, 1.0))
    return img


def cmd_sunflower(args):
    n = getattr(args, "seeds", 3000)
    canvas = max(args.width, args.height)
    theme = args.theme or "gold"
    out = args.output or "examples/fibonacci_sunflower.png"

    console.print(f"\n[bold cyan]Rendering Fibonacci Sunflower[/] · {n} seeds\n")
    seeds = P.fibonacci_sunflower(n, canvas)
    path = R.render_sunflower(seeds, canvas, out, theme_name=theme)
    console.print(f"  [green]Saved → {path}[/]")
    return path


def cmd_lissajous(args):
    a = getattr(args, "a", 5)
    b = getattr(args, "b", 6)
    delta = getattr(args, "delta", math.pi / 4)
    canvas = max(args.width, args.height)
    theme = args.theme or "neon"
    out = args.output or "examples/lissajous.png"

    console.print(f"\n[bold cyan]Rendering Lissajous Figure[/] · a={a}, b={b}\n")
    x_arr, y_arr = P.lissajous(a, b, delta)
    path = R.render_lissajous(x_arr, y_arr, out, a=a, b=b, delta=delta,
                               theme_name=theme, canvas=canvas)
    console.print(f"  [green]Saved → {path}[/]")
    return path


def cmd_dragon(args):
    iters = getattr(args, "iterations", 14)
    canvas = max(args.width, args.height)
    theme = args.theme or "inferno"
    out = args.output or "examples/dragon_curve.png"

    console.print(f"\n[bold cyan]Rendering Dragon Curve[/] · {iters} iterations\n")
    verts = P.dragon_curve(iters)
    console.print(f"  [dim]{len(verts):,} vertices[/]")
    path = R.render_dragon(verts, out, theme_name=theme, canvas=canvas)
    console.print(f"  [green]Saved → {path}[/]")
    return path


def cmd_gallery(args):
    """Generate all patterns as a complete example gallery."""
    console.print(Panel.fit(
        BANNER.strip(),
        border_style="bold magenta",
        padding=(0, 2),
    ))
    console.print()
    console.print("[bold white]Generating full gallery…[/]\n")

    Path("examples").mkdir(exist_ok=True)
    results = []

    gallery_items = [
        ("mandelbrot",   lambda: cmd_mandelbrot(args)),
        ("julia",        lambda: cmd_julia(args)),
        ("burning-ship", lambda: cmd_burning_ship(args)),
        ("ulam",         lambda: cmd_ulam(args)),
        ("sunflower",    lambda: cmd_sunflower(args)),
        ("lissajous",    lambda: cmd_lissajous(args)),
        ("dragon",       lambda: cmd_dragon(args)),
    ]

    for name, fn in gallery_items:
        console.rule(f"[bold]{name}[/]")
        try:
            path = fn()
            results.append((name, str(path), "[green]✓ OK[/]"))
        except Exception as exc:
            console.print(f"  [red]Error: {exc}[/]")
            results.append((name, "—", f"[red]✗ {exc}[/]"))

    console.rule()
    table = Table(title="Gallery Summary", box=box.ROUNDED)
    table.add_column("Pattern", style="cyan")
    table.add_column("Output")
    table.add_column("Status")
    for row in results:
        table.add_row(*row)
    console.print(table)
    console.print()
    console.print("[bold green]Done![/] Open [cyan]examples/[/] to view your gallery.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="cosmograph",
        description="Cosmograph — Mathematical Art Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--width",      type=int, default=1200)
    parser.add_argument("--height",     type=int, default=900)
    parser.add_argument("--theme",      type=str, default=None,
                        choices=list(T.THEMES.keys()))
    parser.add_argument("--output",     type=str, default=None)
    parser.add_argument("--iter",       type=int, default=300,
                        dest="iter")
    parser.add_argument("--no-preview", action="store_true")

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("gallery",      help="Generate all patterns")
    sub.add_parser("mandelbrot",   help="Mandelbrot set")
    j = sub.add_parser("julia",    help="Julia set")
    j.add_argument("--preset", default="classic",
                   choices=list(P.JULIA_PRESETS.keys()))
    sub.add_parser("burning-ship", help="Burning Ship fractal")

    u = sub.add_parser("ulam",     help="Ulam prime spiral")
    u.add_argument("--size", type=int, default=401)

    sf = sub.add_parser("sunflower", help="Fibonacci sunflower")
    sf.add_argument("--seeds", type=int, default=3000)

    li = sub.add_parser("lissajous", help="Lissajous figure")
    li.add_argument("--a", type=int, default=5)
    li.add_argument("--b", type=int, default=6)
    li.add_argument("--delta", type=float, default=math.pi / 4)

    dr = sub.add_parser("dragon", help="Dragon Curve fractal")
    dr.add_argument("--iterations", type=int, default=14)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    os.chdir(Path(__file__).parent)
    Path("examples").mkdir(exist_ok=True)

    cmd = args.command or "gallery"

    dispatch = {
        "gallery":      cmd_gallery,
        "mandelbrot":   cmd_mandelbrot,
        "julia":        cmd_julia,
        "burning-ship": cmd_burning_ship,
        "ulam":         cmd_ulam,
        "sunflower":    cmd_sunflower,
        "lissajous":    cmd_lissajous,
        "dragon":       cmd_dragon,
    }

    fn = dispatch.get(cmd)
    if fn is None:
        parser.print_help()
        sys.exit(1)

    fn(args)


if __name__ == "__main__":
    main()
