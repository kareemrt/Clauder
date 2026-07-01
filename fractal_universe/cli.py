"""
Command-line interface for Fractal Universe.

Usage examples:
    python main.py render mandelbrot
    python main.py render julia --preset dragon --palette fire
    python main.py render burning_ship --palette ice --save fractal.png
    python main.py zoom seahorse_valley --frames 20
    python main.py explore
    python main.py list-presets
"""

import os
import sys
import time

import click
import numpy as np
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from . import fractals as F
from .renderer import render_terminal, render_to_image, render_ascii, render_info_panel
from .zoom import zoom_sequence, ZOOM_DESTINATIONS
from .palettes import PALETTES

console = Console()

FRACTAL_DEFAULTS = {
    "mandelbrot":   {"x_min": -2.5, "x_max": 1.0,  "y_min": -1.25, "y_max": 1.25},
    "julia":        {"x_min": -1.5, "x_max": 1.5,  "y_min": -1.5,  "y_max": 1.5},
    "burning_ship": {"x_min": -2.5, "x_max": 1.5,  "y_min": -2.0,  "y_max": 0.5},
    "tricorn":      {"x_min": -2.5, "x_max": 1.0,  "y_min": -1.5,  "y_max": 1.5},
}


def _terminal_size():
    try:
        cols, rows = os.get_terminal_size()
    except OSError:
        cols, rows = 120, 40
    # Subtract space for info panel; each terminal row = 2 pixel rows
    return cols, (rows - 8) * 2


def _compute_fractal(name, width, height, bounds, max_iter, julia_c=None):
    x_min, x_max, y_min, y_max = bounds
    w_cells = width
    h_cells = height // 2  # half-block: 2 pixel rows per terminal row

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]Computing {task.description}..."),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(name, total=None)
        if name == "mandelbrot":
            data = F.mandelbrot(w_cells, h_cells, x_min, x_max, y_min, y_max, max_iter)
        elif name == "julia":
            cr, ci = julia_c or F.JULIA_PRESETS["dragon"]
            data = F.julia(w_cells, h_cells, cr, ci, x_min, x_max, y_min, y_max, max_iter)
        elif name == "burning_ship":
            data = F.burning_ship(w_cells, h_cells, x_min, x_max, y_min, y_max, max_iter)
        elif name == "tricorn":
            data = F.tricorn(w_cells, h_cells, x_min, x_max, y_min, y_max, max_iter)
        else:
            console.print(f"[red]Unknown fractal: {name}[/red]")
            sys.exit(1)

    return data


@click.group()
def cli():
    """
    ✦ Fractal Universe — explore infinite mathematical beauty in your terminal.

    Render Mandelbrot sets, Julia sets, Burning Ships, and more with
    full color, smooth iteration coloring, and image export.
    """


@cli.command()
@click.argument("fractal", type=click.Choice(["mandelbrot", "julia", "burning_ship", "tricorn"]))
@click.option("--palette", "-p", default="classic", type=click.Choice(list(PALETTES)), show_default=True)
@click.option("--width",  "-w", default=None, type=int, help="Width in terminal columns (default: terminal width)")
@click.option("--height", "-h", default=None, type=int, help="Height in pixel rows (default: terminal height × 2)")
@click.option("--max-iter", "-n", default=256, show_default=True, help="Max escape iterations")
@click.option("--x-min",  default=None, type=float)
@click.option("--x-max",  default=None, type=float)
@click.option("--y-min",  default=None, type=float)
@click.option("--y-max",  default=None, type=float)
@click.option("--preset", default=None, help="Julia set preset name (e.g. dragon, seahorse)")
@click.option("--c-real", default=None, type=float, help="Julia c real part")
@click.option("--c-imag", default=None, type=float, help="Julia c imaginary part")
@click.option("--save",   default=None, help="Save PNG to this path")
@click.option("--ascii",  is_flag=True, help="Plain ASCII output (no color)")
@click.option("--no-info", is_flag=True, help="Suppress the info panel")
def render(fractal, palette, width, height, max_iter, x_min, x_max, y_min, y_max,
           preset, c_real, c_imag, save, ascii, no_info):
    """Render a fractal to the terminal (and optionally save as PNG)."""
    tw, th = _terminal_size()
    width  = width  or tw
    height = height or th

    defaults = FRACTAL_DEFAULTS[fractal]
    bounds = (
        x_min if x_min is not None else defaults["x_min"],
        x_max if x_max is not None else defaults["x_max"],
        y_min if y_min is not None else defaults["y_min"],
        y_max if y_max is not None else defaults["y_max"],
    )

    julia_c = None
    extra = {}
    if fractal == "julia":
        if preset and preset in F.JULIA_PRESETS:
            julia_c = F.JULIA_PRESETS[preset]
        elif c_real is not None and c_imag is not None:
            julia_c = (c_real, c_imag)
        else:
            julia_c = F.JULIA_PRESETS["dragon"]
            preset = "dragon"
        extra["Julia c"] = f"{julia_c[0]} + {julia_c[1]}i  (preset: {preset or 'custom'})"

    data = _compute_fractal(fractal, width, height, bounds, max_iter, julia_c)

    if ascii:
        click.echo(render_ascii(data, max_iter))
    else:
        render_terminal(data, max_iter, palette=palette, console=console)

    if not no_info and not ascii:
        render_info_panel(console, fractal, palette, bounds, max_iter,
                          width, height // 2, extra=extra if extra else None)

    if save:
        path = render_to_image(data, max_iter, palette=palette, output_path=save, scale=2)
        console.print(f"[green]Saved image → {path}[/green]")


@cli.command()
@click.argument("destination", type=click.Choice(list(ZOOM_DESTINATIONS)))
@click.option("--frames", "-f", default=12, show_default=True)
@click.option("--palette", "-p", default="classic", type=click.Choice(list(PALETTES)), show_default=True)
@click.option("--max-iter", "-n", default=300, show_default=True)
@click.option("--delay",   "-d", default=0.05, show_default=True, help="Seconds between frames")
@click.option("--width",  "-w", default=None, type=int)
@click.option("--height", "-h", default=None, type=int)
def zoom(destination, frames, palette, max_iter, delay, width, height):
    """Animate a zoom into a famous fractal location."""
    cfg = ZOOM_DESTINATIONS[destination]
    fractal = cfg["fractal"]
    tx, ty = cfg["target"]
    zf = cfg["zoom_factor"]

    tw, th = _terminal_size()
    width  = width  or tw
    height = height or th

    defaults = FRACTAL_DEFAULTS[fractal]
    start = (defaults["x_min"], defaults["x_max"], defaults["y_min"], defaults["y_max"])

    console.print(f"[bold magenta]✦ Zooming into [cyan]{destination}[/cyan] ({frames} frames)[/bold magenta]")

    for i, bounds in enumerate(zoom_sequence(start, tx, ty, zf, frames), 1):
        data = _compute_fractal(fractal, width, height, bounds, max_iter)
        # Clear screen for animation effect
        console.clear()
        render_terminal(data, max_iter, palette=palette, console=console)
        console.print(f"[dim]Frame {i}/{frames}  zoom ×{zf**(i/frames):.1f}[/dim]")
        time.sleep(delay)

    console.print("[bold green]Zoom complete![/bold green]")


@cli.command("list-presets")
def list_presets():
    """Show all available fractal presets, palettes, and zoom destinations."""
    from rich.table import Table
    from rich.columns import Columns

    console.print("\n[bold magenta]✦ Fractal Universe — Available Options[/bold magenta]\n")

    # Julia presets
    jt = Table(title="Julia Set Presets", header_style="bold cyan")
    jt.add_column("Name"); jt.add_column("c (real)"); jt.add_column("c (imag)")
    for name, (r, i) in F.JULIA_PRESETS.items():
        jt.add_row(name, f"{r}", f"{i}")

    # Palettes
    pt = Table(title="Color Palettes", header_style="bold cyan")
    pt.add_column("Name"); pt.add_column("Description")
    descs = {
        "classic": "Blue & gold — the timeless look",
        "fire":    "Black → red → orange → white",
        "ice":     "Deep navy → cyan → white",
        "electric":"Black → purple → blue → white",
        "gold":    "Black → brown → gold",
        "neon":    "Cycling vivid hues",
        "aurora":  "Deep blue → green → white",
        "sunset":  "Purple → orange → gold",
    }
    for name in PALETTES:
        pt.add_row(name, descs.get(name, ""))

    # Zoom destinations
    zt = Table(title="Zoom Destinations", header_style="bold cyan")
    zt.add_column("Name"); zt.add_column("Fractal"); zt.add_column("Zoom factor")
    for name, cfg in ZOOM_DESTINATIONS.items():
        zt.add_row(name, cfg["fractal"], f"×{cfg['zoom_factor']:,}")

    console.print(Columns([jt, pt]), "\n")
    console.print(zt)


@cli.command()
def explore():
    """Interactive fractal explorer — renders all fractals with all palettes."""
    fractals = ["mandelbrot", "julia", "burning_ship", "tricorn"]
    palettes = list(PALETTES.keys())
    tw, th = _terminal_size()

    console.print("[bold magenta]✦ Fractal Universe — Auto-Explorer[/bold magenta]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    try:
        for f_name in fractals:
            for pal in palettes:
                defaults = FRACTAL_DEFAULTS[f_name]
                bounds = (defaults["x_min"], defaults["x_max"],
                          defaults["y_min"], defaults["y_max"])
                julia_c = F.JULIA_PRESETS["dragon"] if f_name == "julia" else None
                data = _compute_fractal(f_name, tw, th, bounds, 256, julia_c)
                console.clear()
                render_terminal(data, 256, palette=pal, console=console)
                render_info_panel(console, f_name, pal, bounds, 256, tw, th // 2)
                time.sleep(3.0)
    except KeyboardInterrupt:
        console.print("\n[yellow]Explorer stopped.[/yellow]")
