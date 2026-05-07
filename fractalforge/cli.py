"""Click-powered CLI for FractalForge."""

import click
from rich.console import Console
from rich.table import Table
from rich import box

from .fractals import PRESETS
from .colors import PALETTES
from .renderer import render_ascii_terminal, render_png, render_gallery

console = Console()

PALETTE_NAMES = list(PALETTES.keys())
PRESET_NAMES = list(PRESETS.keys())


@click.group()
@click.version_option("1.0.0", prog_name="FractalForge")
def cli():
    """
    \b
    ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
    ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
    █████╗  ██████╔╝███████║██║        ██║   ███████║██║
    ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
    ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

    \b
    ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
    █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
    ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
    ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

    Interactive fractal explorer — Mandelbrot, Julia, Burning Ship and more.
    """


@cli.command()
@click.argument("preset", type=click.Choice(PRESET_NAMES), default="classic")
@click.option("--palette", "-p", type=click.Choice(PALETTE_NAMES), default="fire",
              help="Color palette to use.")
@click.option("--width", "-W", default=120, help="ASCII output width (chars).")
@click.option("--height", "-H", default=40, help="ASCII output height (lines).")
@click.option("--max-iter", "-i", default=None, type=int,
              help="Override maximum iteration count.")
def view(preset, palette, width, height, max_iter):
    """Render a fractal as ASCII art in the terminal.

    PRESET is one of: classic, seahorse, elephant, spiral,
    julia_spiral, julia_dragon, julia_snowflake, burning_ship.
    """
    render_ascii_terminal(preset, palette, width=width, height=height, max_iter=max_iter)


@cli.command()
@click.argument("preset", type=click.Choice(PRESET_NAMES), default="classic")
@click.option("--palette", "-p", type=click.Choice(PALETTE_NAMES), default="fire",
              help="Color palette to use.")
@click.option("--width", "-W", default=1920, help="Image width in pixels.")
@click.option("--height", "-H", default=1080, help="Image height in pixels.")
@click.option("--max-iter", "-i", default=None, type=int,
              help="Override maximum iteration count.")
@click.option("--output", "-o", default=None,
              help="Output filename (default: <preset>_<palette>.png).")
def save(preset, palette, width, height, max_iter, output):
    """Render a fractal to a high-resolution PNG file.

    PRESET is one of: classic, seahorse, elephant, spiral,
    julia_spiral, julia_dragon, julia_snowflake, burning_ship.
    """
    render_png(preset, palette, width=width, height=height,
               max_iter=max_iter, output=output)


@cli.command()
@click.option("--palette", "-p", type=click.Choice(PALETTE_NAMES), default="psychedelic",
              help="Color palette for the gallery.")
@click.option("--width", "-W", default=80, help="ASCII width per fractal.")
@click.option("--height", "-H", default=24, help="ASCII height per fractal.")
def gallery(palette, width, height):
    """Show all presets in a quick ASCII gallery."""
    render_gallery(palette, ascii_width=width, ascii_height=height)


@cli.command()
def presets():
    """List all available fractal presets."""
    table = Table(title="Available Presets", box=box.ROUNDED, show_lines=True)
    table.add_column("Name", style="bold yellow")
    table.add_column("Type", style="cyan")
    table.add_column("Max Iter", style="green", justify="right")
    table.add_column("Description", style="white")
    for name, p in PRESETS.items():
        iters = str(p["max_iter"])
        table.add_row(name, p["type"], iters, p["description"])
    console.print(table)


@cli.command()
def palettes():
    """List all available color palettes."""
    table = Table(title="Available Palettes", box=box.ROUNDED)
    table.add_column("Name", style="bold cyan")
    table.add_column("Color stops", style="white")
    for name, stops in PALETTES.items():
        colors = "  ".join(f"[rgb({r},{g},{b})]██[/]" for (_, (r, g, b)) in stops)
        table.add_row(name, colors)
    console.print(table)


@cli.command()
@click.argument("preset", type=click.Choice(PRESET_NAMES))
@click.option("--palette", "-p", type=click.Choice(PALETTE_NAMES), default="fire")
@click.option("--frames", "-f", default=8, help="Number of zoom frames to generate.")
@click.option("--width", "-W", default=960, help="Frame width in pixels.")
@click.option("--height", "-H", default=540, help="Frame height in pixels.")
@click.option("--max-iter", "-i", default=None, type=int)
def zoom(preset, palette, frames, width, height, max_iter):
    """Generate a zoom sequence of PNG frames for a preset."""
    import numpy as np
    from .fractals import PRESETS as P
    from .renderer import render_png as _rpng

    p = P[preset]
    x_min0, x_max0, y_min0, y_max0 = p["bounds"]
    cx = (x_min0 + x_max0) / 2
    cy = (y_min0 + y_max0) / 2
    rx = (x_max0 - x_min0) / 2
    ry = (y_max0 - y_min0) / 2

    console.print(f"[bold cyan]Generating {frames} zoom frames for [yellow]{preset}[/yellow]...[/bold cyan]")
    for i in range(frames):
        scale = 0.7 ** i
        bounds = (cx - rx * scale, cx + rx * scale, cy - ry * scale, cy + ry * scale)
        out = f"{preset}_zoom_{i:03d}.png"
        # Temporarily patch the preset bounds for this frame
        original = P[preset]["bounds"]
        P[preset] = {**P[preset], "bounds": bounds}
        render_png(preset, palette, width=width, height=height,
                   max_iter=max_iter, output=out)
        P[preset] = {**P[preset], "bounds": original}
    console.print("[bold green]✓ Zoom sequence complete![/bold green]")
