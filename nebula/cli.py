"""Nebula CLI — render fractals from the command line."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .renderer import render
from .palettes import list_palettes
from .fractals.julia import JULIA_PRESETS

console = Console()

BANNER = r"""
  ███╗   ██╗███████╗██████╗ ██╗   ██╗██╗      █████╗
  ████╗  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔══██╗
  ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ███████║
  ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██╔══██║
  ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗██║  ██║
  ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
         A Fractal Universe Explorer  ✦  v1.0
"""


def cmd_render(args):
    console.print(f"[bold cyan]Rendering [yellow]{args.fractal}[/yellow] with [magenta]{args.palette}[/magenta] palette...[/bold cyan]")
    console.print(f"  Resolution: [green]{args.width}×{args.height}[/green]  |  Iterations: [green]{args.max_iter}[/green]  |  Zoom: [green]{args.zoom}×[/green]")

    try:
        result = render(
            fractal=args.fractal,
            palette=args.palette,
            width=args.width,
            height=args.height,
            max_iter=args.max_iter,
            output=args.output,
            ascii_mode=args.ascii,
            julia_preset=args.julia_preset,
            zoom=args.zoom,
            cx=args.cx,
            cy=args.cy,
        )
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    if args.ascii:
        console.print(result)
    else:
        img, elapsed = result
        if args.output:
            console.print(f"  [bold green]✓[/bold green] Saved to [cyan]{args.output}[/cyan]  ([dim]{elapsed:.2f}s[/dim])")
        else:
            console.print(f"  [bold green]✓[/bold green] Rendered in [dim]{elapsed:.2f}s[/dim]")
            img.show()


def cmd_gallery(args):
    """Render a showcase gallery of all fractals and palettes."""
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    configs = [
        ("mandelbrot", "fire",       {},                       "mandelbrot_fire"),
        ("mandelbrot", "deep_space", {},                       "mandelbrot_space"),
        ("julia",      "psychedelic", {"julia_preset": "spiral"}, "julia_spiral"),
        ("julia",      "aurora",      {"julia_preset": "galaxy"}, "julia_galaxy"),
        ("burning_ship", "neon",     {},                       "burning_ship_neon"),
        ("newton",     "deep_space", {},                       "newton"),
    ]

    total = len(configs)
    console.print(f"\n[bold cyan]Rendering gallery ({total} images) → {out_dir}/[/bold cyan]\n")

    for i, (fractal, palette, extra, name) in enumerate(configs, 1):
        path = str(out_dir / f"{name}.png")
        console.print(f"  [{i}/{total}] [yellow]{fractal}[/yellow] + [magenta]{palette}[/magenta]...")
        render(
            fractal=fractal,
            palette=palette,
            width=args.width,
            height=args.height,
            max_iter=args.max_iter,
            output=path,
            **extra,
        )
        console.print(f"         [green]✓[/green] {path}")

    console.print(f"\n[bold green]Gallery complete![/bold green] {total} images saved to [cyan]{out_dir}/[/cyan]")


def cmd_list(args):
    table = Table(title="Available Options", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Options", style="white")

    table.add_row("Fractals", "mandelbrot  julia  burning_ship  newton")
    table.add_row("Palettes", "  ".join(list_palettes()))
    table.add_row("Julia Presets", "  ".join(JULIA_PRESETS.keys()))

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        prog="nebula",
        description="Nebula — A Fractal Universe Explorer",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- render ---
    r = sub.add_parser("render", help="Render a single fractal")
    r.add_argument("fractal", choices=["mandelbrot", "julia", "burning_ship", "newton"])
    r.add_argument("-p", "--palette", default="deep_space", choices=list_palettes())
    r.add_argument("-W", "--width",   type=int, default=1200)
    r.add_argument("-H", "--height",  type=int, default=800)
    r.add_argument("-i", "--max-iter", dest="max_iter", type=int, default=256)
    r.add_argument("-o", "--output",  default=None, help="Save path (e.g. out.png)")
    r.add_argument("--ascii",         action="store_true", help="Render as ASCII art")
    r.add_argument("--julia-preset",  default="spiral", choices=list(JULIA_PRESETS.keys()))
    r.add_argument("--zoom",          type=float, default=1.0)
    r.add_argument("--cx",            type=float, default=0.0, help="Center X")
    r.add_argument("--cy",            type=float, default=0.0, help="Center Y")
    r.set_defaults(func=cmd_render)

    # --- gallery ---
    g = sub.add_parser("gallery", help="Render a full showcase gallery")
    g.add_argument("-o", "--output-dir", default="gallery", help="Output directory")
    g.add_argument("-W", "--width",   type=int, default=1200)
    g.add_argument("-H", "--height",  type=int, default=800)
    g.add_argument("-i", "--max-iter", dest="max_iter", type=int, default=256)
    g.set_defaults(func=cmd_gallery)

    # --- list ---
    l = sub.add_parser("list", help="List available fractals, palettes, and presets")
    l.set_defaults(func=cmd_list)

    args = parser.parse_args()

    rprint(f"[bold blue]{BANNER}[/bold blue]")
    args.func(args)


if __name__ == "__main__":
    main()
