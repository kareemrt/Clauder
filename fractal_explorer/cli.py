"""CLI entry point for the fractal explorer."""

import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich import box

from .mandelbrot import compute_mandelbrot, ZOOM_PRESETS
from .julia import compute_julia, JULIA_PRESETS
from .sierpinski import compute_sierpinski, compute_dragon_curve, render_dragon_to_grid
from .renderer import (
    render_grid,
    render_sierpinski,
    render_dragon,
    make_info_table,
    make_palette_row,
    PALETTES,
    COLOR_SCHEMES,
)

console = Console()

BANNER = r"""
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
  ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗
  ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
  █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
  ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
  ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

SUBTITLE = "Infinite beauty rendered in your terminal"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Fractal Explorer — ASCII art fractals in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command", metavar="COMMAND")

    # --- mandelbrot ---
    m = sub.add_parser("mandelbrot", aliases=["mb"], help="Render the Mandelbrot set")
    m.add_argument("-W", "--width",    type=int, default=100, help="Width in characters")
    m.add_argument("-H", "--height",   type=int, default=40,  help="Height in characters")
    m.add_argument("--xmin",           type=float, default=-2.5)
    m.add_argument("--xmax",           type=float, default=1.0)
    m.add_argument("--ymin",           type=float, default=-1.25)
    m.add_argument("--ymax",           type=float, default=1.25)
    m.add_argument("--iter",           type=int, default=80,   help="Max iterations")
    m.add_argument("--palette",        default="blocks",       choices=list(PALETTES))
    m.add_argument("--color",          default="fire",         choices=list(COLOR_SCHEMES))
    m.add_argument("--preset",         type=int, default=None, help="Use zoom preset 0-%d" % (len(ZOOM_PRESETS) - 1))
    m.add_argument("--no-color",       action="store_true",    help="Disable color output")
    m.add_argument("--list-presets",   action="store_true",    help="List available zoom presets")

    # --- julia ---
    j = sub.add_parser("julia", aliases=["jl"], help="Render a Julia set")
    j.add_argument("-W", "--width",    type=int, default=100)
    j.add_argument("-H", "--height",   type=int, default=40)
    j.add_argument("--cx",             type=float, default=-0.7,     help="Real part of c")
    j.add_argument("--cy",             type=float, default=0.27015,  help="Imaginary part of c")
    j.add_argument("--iter",           type=int, default=80)
    j.add_argument("--palette",        default="blocks",       choices=list(PALETTES))
    j.add_argument("--color",          default="ocean",        choices=list(COLOR_SCHEMES))
    j.add_argument("--preset",         type=int, default=None, help="Use Julia preset 0-%d" % (len(JULIA_PRESETS) - 1))
    j.add_argument("--no-color",       action="store_true")
    j.add_argument("--list-presets",   action="store_true",    help="List available Julia presets")

    # --- sierpinski ---
    s = sub.add_parser("sierpinski", aliases=["si"], help="Render the Sierpinski triangle")
    s.add_argument("-s", "--size",     type=int, default=32,   help="Triangle size (power of 2 recommended)")
    s.add_argument("--color",          default="green")

    # --- dragon ---
    d = sub.add_parser("dragon", aliases=["dr"], help="Render the dragon curve fractal")
    d.add_argument("-i", "--iterations", type=int, default=13,  help="Fold iterations (max ~15)")
    d.add_argument("-W", "--width",    type=int, default=70)
    d.add_argument("-H", "--height",   type=int, default=30)
    d.add_argument("--color",          default="cyan")

    # --- gallery ---
    g = sub.add_parser("gallery", help="Show a gallery of all fractals side-by-side")
    g.add_argument("--palette",        default="blocks")
    g.add_argument("--mb-color",       default="fire")
    g.add_argument("--jl-color",       default="ocean")

    # --- list ---
    sub.add_parser("list", help="List all available palettes and color schemes")

    return p


def cmd_mandelbrot(args: argparse.Namespace) -> None:
    if args.list_presets:
        _print_presets_mb()
        return

    if args.preset is not None:
        if args.preset < 0 or args.preset >= len(ZOOM_PRESETS):
            console.print(f"[red]Preset index must be 0–{len(ZOOM_PRESETS)-1}[/]")
            sys.exit(1)
        xmin, xmax, ymin, ymax, pname = ZOOM_PRESETS[args.preset]
        console.print(f"[dim]Using preset {args.preset}: {pname}[/]")
    else:
        xmin, xmax, ymin, ymax = args.xmin, args.xmax, args.ymin, args.ymax
        pname = "Custom"

    console.print(f"[bold cyan]Computing Mandelbrot set...[/] ({args.width}×{args.height})")
    grid = compute_mandelbrot(args.width, args.height, xmin, xmax, ymin, ymax, args.iter)
    text = render_grid(grid, args.iter, args.palette, args.color, not args.no_color)

    info = make_info_table("Mandelbrot", {
        "Region":    f"[{xmin:.4f}, {xmax:.4f}] × [{ymin:.4f}, {ymax:.4f}]",
        "Size":      f"{args.width} × {args.height}",
        "Max iter":  str(args.iter),
        "Palette":   args.palette,
        "Colors":    args.color,
        "Preset":    pname,
    })

    console.print(Panel(text, title="[bold magenta]Mandelbrot Set[/]", border_style="magenta"))
    console.print(info)
    console.print(make_palette_row(args.palette, args.color, args.iter))


def cmd_julia(args: argparse.Namespace) -> None:
    if args.list_presets:
        _print_presets_jl()
        return

    cx, cy, name, desc = args.cx, args.cy, "Custom", ""
    if args.preset is not None:
        if args.preset < 0 or args.preset >= len(JULIA_PRESETS):
            console.print(f"[red]Preset index must be 0–{len(JULIA_PRESETS)-1}[/]")
            sys.exit(1)
        cx, cy, name, desc = JULIA_PRESETS[args.preset]
        console.print(f"[dim]Using preset {args.preset}: {name} — {desc}[/]")

    console.print(f"[bold cyan]Computing Julia set...[/] ({args.width}×{args.height})")
    grid = compute_julia(args.width, args.height, cx, cy, max_iter=args.iter)
    text = render_grid(grid, args.iter, args.palette, args.color, not args.no_color)

    info = make_info_table("Julia", {
        "Constant c": f"{cx:+.5f} {cy:+.5f}i",
        "Name":        name,
        "Size":        f"{args.width} × {args.height}",
        "Max iter":    str(args.iter),
        "Palette":     args.palette,
        "Colors":      args.color,
    })

    console.print(Panel(text, title=f"[bold blue]Julia Set — {name}[/]", border_style="blue"))
    console.print(info)
    console.print(make_palette_row(args.palette, args.color, args.iter))


def cmd_sierpinski(args: argparse.Namespace) -> None:
    rows = compute_sierpinski(args.size)
    text = render_sierpinski(rows, args.color)
    console.print(Panel(text, title="[bold green]Sierpiński Triangle[/]", border_style="green"))
    info = make_info_table("Sierpinski", {
        "Size":  f"{args.size} × {args.size}",
        "Color": args.color,
        "Rule":  "(row & col) == 0",
    })
    console.print(info)


def cmd_dragon(args: argparse.Namespace) -> None:
    console.print(f"[bold cyan]Computing dragon curve...[/] ({args.iterations} iterations)")
    points = compute_dragon_curve(args.iterations)
    grid = render_dragon_to_grid(points, args.width, args.height)
    text = render_dragon(grid, args.color)
    console.print(Panel(text, title="[bold yellow]Dragon Curve[/]", border_style="yellow"))
    info = make_info_table("Dragon Curve", {
        "Iterations": str(args.iterations),
        "Points":     str(len(points)),
        "Grid":       f"{args.width} × {args.height}",
        "Color":      args.color,
    })
    console.print(info)


def cmd_gallery(args: argparse.Namespace) -> None:
    console.print("[bold]Rendering gallery (this may take a moment)...[/]")
    w, h = 50, 20

    # Mandelbrot
    grid_mb = compute_mandelbrot(w, h, max_iter=60)
    text_mb = render_grid(grid_mb, 60, args.palette, args.mb_color)

    # Julia
    grid_jl = compute_julia(w, h, -0.7, 0.27015, max_iter=60)
    text_jl = render_grid(grid_jl, 60, args.palette, args.jl_color)

    # Sierpinski
    text_si = render_sierpinski(compute_sierpinski(20))

    # Dragon
    pts = compute_dragon_curve(10)
    dg = render_dragon_to_grid(pts, w, h)
    text_dr = render_dragon(dg, "cyan")

    from rich.panel import Panel
    panels = [
        Panel(text_mb, title="[magenta]Mandelbrot[/]", border_style="magenta", width=w + 4),
        Panel(text_jl, title="[blue]Julia[/]",        border_style="blue",    width=w + 4),
        Panel(text_si, title="[green]Sierpiński[/]",  border_style="green",   width=24),
        Panel(text_dr, title="[yellow]Dragon[/]",     border_style="yellow",  width=w + 4),
    ]

    console.print(Columns(panels, equal=False, expand=False))
    console.print("\n[bold]Gallery complete.[/] Run individual commands to explore each fractal in detail.\n")


def cmd_list(_args: argparse.Namespace) -> None:
    p_table = Table(title="Available Palettes", box=box.ROUNDED)
    p_table.add_column("Name",    style="cyan")
    p_table.add_column("Preview", no_wrap=True)
    from .renderer import PALETTES
    for name, chars in PALETTES.items():
        p_table.add_row(name, "".join(chars))

    c_table = Table(title="Available Color Schemes", box=box.ROUNDED)
    c_table.add_column("Name",   style="cyan")
    c_table.add_column("Colors", no_wrap=True)
    from .renderer import COLOR_SCHEMES
    from rich.text import Text
    for name, colors in COLOR_SCHEMES.items():
        t = Text()
        for i, c in enumerate(colors):
            t.append(f" {i} ", style=c)
        c_table.add_row(name, t)

    console.print(p_table)
    console.print(c_table)


def _print_presets_mb() -> None:
    t = Table(title="Mandelbrot Zoom Presets", box=box.ROUNDED)
    t.add_column("#",    style="cyan", justify="right")
    t.add_column("Name", style="bold")
    t.add_column("x range")
    t.add_column("y range")
    for i, (xmin, xmax, ymin, ymax, name) in enumerate(ZOOM_PRESETS):
        t.add_row(str(i), name, f"[{xmin}, {xmax}]", f"[{ymin}, {ymax}]")
    console.print(t)


def _print_presets_jl() -> None:
    t = Table(title="Julia Set Presets", box=box.ROUNDED)
    t.add_column("#",    style="cyan", justify="right")
    t.add_column("Name", style="bold")
    t.add_column("c (real + imag·i)")
    t.add_column("Description")
    for i, (cx, cy, name, desc) in enumerate(JULIA_PRESETS):
        t.add_row(str(i), name, f"{cx:+.5f} {cy:+.5f}i", desc)
    console.print(t)


def main() -> None:
    parser = _build_parser()

    if len(sys.argv) == 1:
        # Show banner + help
        banner_text = Text(BANNER, style="bold cyan")
        console.print(banner_text)
        console.print(f"  [bold yellow]{SUBTITLE}[/]\n")
        parser.print_help()
        return

    args = parser.parse_args()

    dispatch = {
        "mandelbrot": cmd_mandelbrot,
        "mb":         cmd_mandelbrot,
        "julia":      cmd_julia,
        "jl":         cmd_julia,
        "sierpinski": cmd_sierpinski,
        "si":         cmd_sierpinski,
        "dragon":     cmd_dragon,
        "dr":         cmd_dragon,
        "gallery":    cmd_gallery,
        "list":       cmd_list,
    }

    fn = dispatch.get(args.command)
    if fn is None:
        parser.print_help()
        sys.exit(1)

    fn(args)
