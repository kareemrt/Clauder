"""Rendering pipeline — terminal ASCII display and PNG export."""

import time
from pathlib import Path

import numpy as np
from PIL import Image
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text
from rich import box

from .colors import colorize, to_ascii, PALETTES
from .fractals import mandelbrot, julia, burning_ship, PRESETS


console = Console()


def _compute(preset_name: str, width: int, height: int, max_iter: int | None) -> tuple[np.ndarray, dict]:
    """Compute fractal data for a named preset."""
    preset = PRESETS[preset_name]
    iters = max_iter or preset["max_iter"]

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Computing {task.description}[/bold cyan]"),
        BarColumn(bar_width=40),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"[{preset_name}]", total=None)
        t0 = time.perf_counter()

        if preset["type"] == "mandelbrot":
            x_min, x_max, y_min, y_max = preset["bounds"]
            data = mandelbrot(width, height, x_min, x_max, y_min, y_max, iters)
        elif preset["type"] == "julia":
            c_re, c_im = preset["c"]
            x_min, x_max, y_min, y_max = preset["bounds"]
            data = julia(width, height, c_re, c_im, x_min, x_max, y_min, y_max, iters)
        elif preset["type"] == "burning_ship":
            x_min, x_max, y_min, y_max = preset["bounds"]
            data = burning_ship(width, height, x_min, x_max, y_min, y_max, iters)
        else:
            raise ValueError(f"Unknown fractal type: {preset['type']}")

        elapsed = time.perf_counter() - t0
        progress.update(task, completed=True)

    return data, {"elapsed": elapsed, "iters": iters, "preset": preset}


def render_ascii_terminal(preset_name: str, palette: str,
                          width: int = 120, height: int = 40,
                          max_iter: int | None = None):
    """Render a fractal as coloured ASCII art in the terminal."""
    console.print(Panel(
        f"[bold magenta]FractalForge[/bold magenta] — rendering [bold yellow]{preset_name}[/bold yellow] "
        f"with palette [bold cyan]{palette}[/bold cyan]",
        box=box.DOUBLE_EDGE,
        expand=False,
    ))

    data, meta = _compute(preset_name, width * 2, height * 2, max_iter)
    ascii_art = to_ascii(data, width=width, height=height)

    stops = PALETTES.get(palette, list(PALETTES.values())[0])

    # Pick a colour gradient for the text itself
    lines = ascii_art.split("\n")
    text = Text()
    gradient_colors = [
        f"rgb({r},{g},{b})"
        for (_, (r, g, b)) in stops[1:]  # skip the black stop
    ]
    for i, line in enumerate(lines):
        col = gradient_colors[i % len(gradient_colors)]
        text.append(line + "\n", style=col)

    console.print(text)
    console.print(
        f"[dim]preset=[green]{preset_name}[/green]  "
        f"type=[green]{meta['preset']['type']}[/green]  "
        f"max_iter=[green]{meta['iters']}[/green]  "
        f"computed in [green]{meta['elapsed']:.2f}s[/green][/dim]"
    )


def render_png(preset_name: str, palette: str, width: int = 1920, height: int = 1080,
               max_iter: int | None = None, output: str | None = None) -> Path:
    """Render a fractal to a high-resolution PNG file."""
    out_path = Path(output) if output else Path(f"{preset_name}_{palette}.png")

    console.print(Panel(
        f"[bold magenta]FractalForge[/bold magenta] — saving [bold yellow]{preset_name}[/bold yellow] → "
        f"[bold green]{out_path}[/bold green]  [dim]({width}×{height})[/dim]",
        box=box.ROUNDED,
        expand=False,
    ))

    data, meta = _compute(preset_name, width, height, max_iter)
    rgba = colorize(data, palette_name=palette)
    img = Image.fromarray(rgba, mode="RGBA")
    img.save(out_path)

    console.print(f"[bold green]✓[/bold green] Saved [cyan]{out_path}[/cyan] "
                  f"([dim]{out_path.stat().st_size // 1024} KB[/dim])")
    return out_path


def render_gallery(palette: str, ascii_width: int = 80, ascii_height: int = 24):
    """Render all presets as a quick ASCII gallery."""
    console.rule("[bold magenta]FractalForge Gallery[/bold magenta]")
    for name, preset in PRESETS.items():
        console.print(f"\n[bold yellow]▶ {name}[/bold yellow]  [dim]{preset['description']}[/dim]")
        data, _ = _compute(name, ascii_width * 2, ascii_height * 2, max_iter=128)
        art = to_ascii(data, width=ascii_width, height=ascii_height)
        stops = PALETTES.get(palette, list(PALETTES.values())[0])
        gradient_colors = [f"rgb({r},{g},{b})" for (_, (r, g, b)) in stops[1:]]
        text = Text()
        for i, line in enumerate(art.split("\n")):
            col = gradient_colors[i % len(gradient_colors)]
            text.append(line + "\n", style=col)
        console.print(text)
    console.rule("[bold magenta]End of Gallery[/bold magenta]")
