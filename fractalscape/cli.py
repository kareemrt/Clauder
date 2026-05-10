"""Click-based CLI for FractalScape."""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .compute import JULIA_PRESETS, MANDELBROT_TOURS
from .palette import PALETTES
from .renderer import RenderConfig, render

console = Console()

BANNER = r"""
  ___             _        _  ____
 | __| _ __ _  __| |_ __ _| |/ ___|  __  __ _ _ __  ___
 | _| | '__/ \/ _| __/ _` | |\___ \ / _|/ _` | '_ \/ -_)
 |_|  |_|  \__/\__|\__\__,_|_| ___/ \__/\__,_| .__/\___|
                                               |_|
"""

FRACTAL_CHOICES = ["mandelbrot", "julia", "burning_ship"]
PALETTE_CHOICES = list(PALETTES.keys())
CHAR_CHOICES = ["dense", "simple", "blocks", "dots"]


@click.group()
@click.version_option("1.0.0", prog_name="fractalscape")
def cli():
    """FractalScape — Explore the Infinite in Your Terminal.

    Render Mandelbrot sets, Julia sets, and Burning Ship fractals
    directly in your terminal with beautiful ANSI colors.
    """
    pass


@cli.command("render")
@click.option("--fractal", "-f", default="mandelbrot",
              type=click.Choice(FRACTAL_CHOICES), show_default=True,
              help="Which fractal to render.")
@click.option("--width", "-W", default=120, show_default=True,
              help="Output width in characters.")
@click.option("--height", "-H", default=40, show_default=True,
              help="Output height in characters.")
@click.option("--max-iter", "-m", default=256, show_default=True,
              help="Maximum iterations (higher = more detail).")
@click.option("--palette", "-p", default="fire",
              type=click.Choice(PALETTE_CHOICES), show_default=True,
              help="Color palette.")
@click.option("--chars", "-c", default="dense",
              type=click.Choice(CHAR_CHOICES), show_default=True,
              help="ASCII character set.")
@click.option("--invert", is_flag=True, help="Invert the color mapping.")
@click.option("--julia-c", default=None,
              help="Julia set parameter as 'real+imagj', e.g. '-0.7+0.27i'.")
@click.option("--julia-preset", default=None,
              type=click.Choice(list(JULIA_PRESETS.keys())),
              help="Named Julia set preset.")
@click.option("--zoom", default=None,
              type=click.Choice(list(MANDELBROT_TOURS.keys())),
              help="Named Mandelbrot zoom location.")
@click.option("--x-min", default=None, type=float, help="Viewport x minimum.")
@click.option("--x-max", default=None, type=float, help="Viewport x maximum.")
@click.option("--y-min", default=None, type=float, help="Viewport y minimum.")
@click.option("--y-max", default=None, type=float, help="Viewport y maximum.")
@click.option("--save", "-s", default=None,
              help="Save plain ASCII output to a file.")
@click.option("--stats/--no-stats", default=True,
              help="Show render statistics.")
def render_cmd(fractal, width, height, max_iter, palette, chars, invert,
               julia_c, julia_preset, zoom, x_min, x_max, y_min, y_max,
               save, stats):
    """Render a fractal to the terminal."""
    # Parse custom Julia c
    c = -0.7 + 0.27015j
    if julia_c:
        try:
            c = complex(julia_c.replace("i", "j"))
        except ValueError:
            console.print(f"[red]Invalid complex number: {julia_c!r}[/]")
            sys.exit(1)

    # Apply named zoom
    if zoom and fractal == "mandelbrot":
        x_min, x_max, y_min, y_max = MANDELBROT_TOURS[zoom]

    cfg = RenderConfig(
        fractal=fractal,
        width=width,
        height=height,
        max_iter=max_iter,
        palette=palette,
        char_set=chars,
        invert=invert,
        julia_c=c,
        julia_preset=julia_preset,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
    )

    with console.status(f"[bold cyan]Computing {fractal}…[/]"):
        result = render(cfg)

    # Print the fractal
    print(result.ansi)

    if stats:
        _print_stats(result)

    if save:
        with open(save, "w") as fh:
            fh.write(result.plain)
        console.print(f"\n[green]Saved to {save}[/]")


@cli.command("tour")
@click.option("--fractal", "-f", default="mandelbrot",
              type=click.Choice(["mandelbrot", "julia"]), show_default=True)
@click.option("--palette", "-p", default="fire",
              type=click.Choice(PALETTE_CHOICES), show_default=True)
@click.option("--width", "-W", default=100, show_default=True)
@click.option("--height", "-H", default=30, show_default=True)
def tour_cmd(fractal, palette, width, height):
    """Take an automatic tour of famous fractal locations."""
    import time as _time

    console.print(Panel(Text(BANNER, style="bold cyan"), title="FractalScape Tour"))

    if fractal == "mandelbrot":
        locations = list(MANDELBROT_TOURS.items())
        for name, (xn, xx, yn, yx) in locations:
            console.rule(f"[bold yellow]{name.replace('_', ' ').title()}[/]")
            cfg = RenderConfig(
                fractal="mandelbrot",
                width=width, height=height,
                palette=palette,
                x_min=xn, x_max=xx, y_min=yn, y_max=yx,
            )
            result = render(cfg)
            print(result.ansi)
            console.print(
                f"  [dim]Bounds: x=[{xn:.4f}, {xx:.4f}]  "
                f"y=[{yn:.4f}, {yx:.4f}]  "
                f"render: {result.elapsed_ms:.0f}ms[/]"
            )
            _time.sleep(0.3)

    elif fractal == "julia":
        presets = list(JULIA_PRESETS.items())
        for name, c_val in presets:
            console.rule(f"[bold magenta]{name.replace('_', ' ').title()}[/]")
            cfg = RenderConfig(
                fractal="julia",
                width=width, height=height,
                palette=palette,
                julia_c=c_val,
            )
            result = render(cfg)
            print(result.ansi)
            console.print(
                f"  [dim]c = {c_val}   render: {result.elapsed_ms:.0f}ms[/]"
            )
            _time.sleep(0.3)


@cli.command("list")
def list_cmd():
    """List all available palettes, presets, and zoom locations."""
    t = Table(title="Color Palettes", box=box.ROUNDED, style="cyan")
    t.add_column("Name", style="bold")
    t.add_column("Colors")
    for name, stops in PALETTES.items():
        swatch = "  ".join(
            f"\033[38;2;{r};{g};{b}m██\033[0m" for r, g, b in stops
        )
        t.add_row(name, swatch)
    console.print(t)

    t2 = Table(title="Julia Presets", box=box.ROUNDED, style="magenta")
    t2.add_column("Preset", style="bold")
    t2.add_column("c value")
    for name, c in JULIA_PRESETS.items():
        t2.add_row(name, str(c))
    console.print(t2)

    t3 = Table(title="Mandelbrot Zoom Locations", box=box.ROUNDED, style="yellow")
    t3.add_column("Name", style="bold")
    t3.add_column("x range")
    t3.add_column("y range")
    for name, (xn, xx, yn, yx) in MANDELBROT_TOURS.items():
        t3.add_row(name, f"[{xn}, {xx}]", f"[{yn}, {yx}]")
    console.print(t3)


def _print_stats(result):
    cfg = result.config
    t = Table(box=box.SIMPLE, show_header=False, style="dim")
    t.add_column("", style="bold")
    t.add_column("")
    t.add_row("Fractal",    cfg.fractal)
    t.add_row("Dimensions", f"{cfg.width} × {cfg.height}")
    t.add_row("Max iter",   str(cfg.max_iter))
    t.add_row("Palette",    cfg.palette)
    t.add_row("Render time", f"{result.elapsed_ms:.1f} ms")
    t.add_row("Interior",   f"{result.stats['interior_pct']:.1f}%")
    t.add_row("Mean iter",  f"{result.stats['mean_iter']:.1f}")
    console.print(t)
