"""Nebula CLI — generate fractal art from the command line."""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich import box

from .presets import PRESETS
from .colormaps import COLORMAPS
from .renderer import compute, render_terminal, render_png, save_png

console = Console()

BANNER = r"""
  _   _      _           _
 | \ | | ___| |__  _   _| | __ _
 |  \| |/ _ \ '_ \| | | | |/ _` |
 | |\  |  __/ |_) | |_| | | (_| |
 |_| \_|\___|_.__/ \__,_|_|\__,_|

  Fractal Art Generator  •  v1.0.0
"""


@click.group()
def cli():
    """Nebula — generate stunning fractal art in your terminal or as PNG images."""
    pass


@cli.command("render")
@click.option("--preset",   "-p", default=None,  help="Use a named preset scene")
@click.option("--fractal",  "-f", default="mandelbrot",
              type=click.Choice(["mandelbrot", "julia", "burning_ship"]),
              help="Fractal type")
@click.option("--width",    "-W", default=800,   show_default=True, help="Image width (px)")
@click.option("--height",   "-H", default=600,   show_default=True, help="Image height (px)")
@click.option("--x-min",          default=-2.5,  show_default=True)
@click.option("--x-max",          default=1.0,   show_default=True)
@click.option("--y-min",          default=-1.25, show_default=True)
@click.option("--y-max",          default=1.25,  show_default=True)
@click.option("--max-iter", "-i", default=256,   show_default=True, help="Max iterations")
@click.option("--colormap",  "-c", default="nebula",
              type=click.Choice(list(COLORMAPS.keys())), show_default=True)
@click.option("--julia-c",        default=None,  help="Complex constant for Julia sets, e.g. '-0.7+0.27i'")
@click.option("--output",   "-o", default=None,  help="Output PNG file path")
@click.option("--gamma",          default=0.5,   show_default=True, help="Gamma correction")
@click.option("--terminal","-t",  is_flag=True,  help="Print ASCII preview to terminal")
def render(preset, fractal, width, height, x_min, x_max, y_min, y_max,
           max_iter, colormap, julia_c, output, gamma, terminal):
    """Render a fractal — to PNG file, terminal ASCII preview, or both."""
    console.print(Panel(BANNER.strip(), border_style="bright_blue"))

    # ── load preset ──────────────────────────────────────────────────────────
    if preset:
        if preset not in PRESETS:
            console.print(f"[red]Unknown preset '{preset}'. Run 'nebula list-presets'.[/red]")
            sys.exit(1)
        sc = PRESETS[preset]
        fractal  = sc.fractal
        x_min, x_max = sc.x_min, sc.x_max
        y_min, y_max = sc.y_min, sc.y_max
        max_iter = sc.max_iter
        colormap = sc.colormap
        julia_c  = sc.julia_c
        console.print(f"[bold cyan]Preset:[/bold cyan] {sc.name}")
        if sc.description:
            console.print(f"[dim]{sc.description}[/dim]")

    # ── parse julia_c if given as string ─────────────────────────────────────
    if isinstance(julia_c, str):
        try:
            julia_c = complex(julia_c.replace("i", "j"))
        except ValueError:
            console.print(f"[red]Cannot parse julia-c value '{julia_c}'. Use e.g. '-0.7+0.27j'[/red]")
            sys.exit(1)

    # ── render ────────────────────────────────────────────────────────────────
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                  TimeElapsedColumn(), console=console) as progress:
        task = progress.add_task(
            f"[bright_blue]Computing {fractal} ({width}×{height}, {max_iter} iters)…", total=None)
        t0 = time.perf_counter()
        data = compute(fractal, width, height, x_min, x_max, y_min, y_max,
                       max_iter, julia_c=julia_c)
        elapsed = time.perf_counter() - t0
        progress.update(task, description=f"[green]Done in {elapsed:.2f}s")

    if terminal:
        console.print("\n[dim]── Terminal Preview ──────────────────────────────[/dim]")
        print(render_terminal(data))

    if output or not terminal:
        out_path = output or f"examples/{fractal}_{colormap}.png"
        img  = render_png(data, colormap=colormap, gamma=gamma)
        path = save_png(img, out_path)
        console.print(f"\n[green]✓[/green] Saved → [bold]{path}[/bold]  "
                      f"[dim]({img.width}×{img.height} px)[/dim]")

    console.print()


@cli.command("batch")
@click.option("--output-dir", "-d", default="examples", show_default=True,
              help="Directory to save all renders")
@click.option("--width",  "-W", default=800,  show_default=True)
@click.option("--height", "-H", default=600,  show_default=True)
@click.option("--presets", default=None, help="Comma-separated preset names (default: all)")
def batch(output_dir, width, height, presets):
    """Render every preset (or a selection) and save them all to a directory."""
    console.print(Panel(BANNER.strip(), border_style="bright_blue"))

    names = presets.split(",") if presets else list(PRESETS.keys())
    invalid = [n for n in names if n not in PRESETS]
    if invalid:
        console.print(f"[red]Unknown presets: {invalid}[/red]")
        sys.exit(1)

    console.print(f"[bold]Rendering {len(names)} scenes → {output_dir}/[/bold]\n")

    for name in names:
        sc = PRESETS[name]
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task(
                f"[cyan]{sc.name}[/cyan] ({sc.max_iter} iters)…", total=None)
            t0 = time.perf_counter()
            data = compute(sc.fractal, width, height,
                           sc.x_min, sc.x_max, sc.y_min, sc.y_max,
                           sc.max_iter, julia_c=sc.julia_c)
            elapsed = time.perf_counter() - t0
            progress.update(task, description=f"[green]{sc.name}[/green] — done in {elapsed:.2f}s")

        img = render_png(data, colormap=sc.colormap, gamma=0.5)
        path = save_png(img, f"{output_dir}/{name}.png")
        console.print(f"  [green]✓[/green] {path}")

    console.print(f"\n[bold green]All done![/bold green] {len(names)} images in '{output_dir}/'")


@cli.command("list-presets")
def list_presets():
    """Show all built-in preset scenes."""
    console.print(Panel(BANNER.strip(), border_style="bright_blue"))

    table = Table(title="Built-in Scenes", box=box.ROUNDED, border_style="bright_blue",
                  show_lines=True)
    table.add_column("Key",         style="bold cyan", no_wrap=True)
    table.add_column("Name",        style="bold white")
    table.add_column("Fractal",     style="yellow")
    table.add_column("Colormap",    style="magenta")
    table.add_column("Max Iters",   style="green", justify="right")
    table.add_column("Description", style="dim")

    for key, sc in PRESETS.items():
        table.add_row(key, sc.name, sc.fractal, sc.colormap,
                      str(sc.max_iter), sc.description)

    console.print(table)


@cli.command("list-colormaps")
def list_colormaps():
    """Show all available colour palettes."""
    console.print(Panel(BANNER.strip(), border_style="bright_blue"))
    table = Table(title="Colour Palettes", box=box.ROUNDED, border_style="bright_blue")
    table.add_column("Name", style="bold cyan")
    table.add_column("Style", style="white")

    descriptions = {
        "nebula":      "Deep space purple → cyan → white",
        "fire":        "Black → red → orange → yellow → white",
        "ocean":       "Black → navy → teal → aqua → white",
        "psychedelic": "Cycling rainbow — 3 full hue rotations",
        "cosmic":      "Black → midnight purple → gold → white",
        "grayscale":   "Pure luminance, no colour",
    }
    for name, desc in descriptions.items():
        table.add_row(name, desc)
    console.print(table)


def main():
    cli()


if __name__ == "__main__":
    main()
