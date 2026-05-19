"""Click-based CLI for FractalDreams."""

import os
import sys
import time
from pathlib import Path

import click

from .renderer import (
    render_mandelbrot, render_julia, render_burning_ship, render_newton,
    animate_julia_orbit, animate_mandelbrot_zoom, animate_palette_cycle,
    ascii_preview, MANDELBROT_PRESETS, JULIA_PRESETS,
)
from .fractals import mandelbrot, julia
from .colorizer import PALETTES


PALETTE_NAMES = list(PALETTES.keys())
FRACTAL_NAMES = ["mandelbrot", "julia", "burning-ship", "newton"]


def _save(img, path: str):
    img.save(path)
    size_kb = os.path.getsize(path) / 1024
    click.secho(f"  Saved → {path}  ({size_kb:.1f} KB)", fg="green")


@click.group()
@click.version_option("1.0.0", prog_name="fractal-dreams")
def cli():
    """
    \b
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

    Infinite mathematical beauty, one pixel at a time.
    """


# ─── render command ───────────────────────────────────────────────────────────

@cli.command()
@click.argument("fractal", type=click.Choice(FRACTAL_NAMES), default="mandelbrot")
@click.option("-o", "--output", default=None, help="Output PNG path")
@click.option("-W", "--width",  default=800, show_default=True, help="Image width")
@click.option("-H", "--height", default=600, show_default=True, help="Image height")
@click.option("-p", "--palette", default="inferno",
              type=click.Choice(PALETTE_NAMES), show_default=True)
@click.option("--preset",  default=None, help="Named preset (fractal-specific)")
@click.option("--max-iter", default=256, show_default=True)
@click.option("--julia-c",  default=None,
              help="Julia constant as 'real+imagj' e.g. '-0.7+0.27j'")
@click.option("--poly",     default="z3-1",
              type=click.Choice(["z3-1", "z4-1", "z6-1"]),
              help="Newton polynomial")
@click.option("--ascii", "show_ascii", is_flag=True, help="Print ASCII preview")
def render(fractal, output, width, height, palette, preset, max_iter,
           julia_c, poly, show_ascii):
    """Render a static fractal image."""
    t0 = time.time()
    click.secho(f"\n  Rendering {fractal.upper()} …", fg="cyan", bold=True)

    if fractal == "mandelbrot":
        if output is None:
            output = f"mandelbrot_{preset or 'classic'}_{palette}.png"
        preset = preset or "classic"
        img = render_mandelbrot(width, height, preset=preset,
                                palette=palette, max_iter=max_iter)
        if show_ascii:
            from .fractals import mandelbrot as _mb
            xmin, xmax, ymin, ymax = MANDELBROT_PRESETS.get(preset, MANDELBROT_PRESETS["classic"])
            data = _mb(80, 30, xmin, xmax, ymin, ymax, max_iter)
            click.echo("\n" + ascii_preview(data) + "\n")

    elif fractal == "julia":
        if output is None:
            output = f"julia_{preset or 'custom'}_{palette}.png"
        c = None
        if julia_c:
            try:
                c = complex(julia_c.replace(" ", ""))
            except ValueError:
                click.secho(f"  Invalid complex number: {julia_c}", fg="red")
                sys.exit(1)
        img = render_julia(width, height, preset=preset or "douady-rabbit",
                           palette=palette, max_iter=max_iter, c=c)
        if show_ascii:
            from .fractals import julia as _jl
            used_c = c or JULIA_PRESETS.get(preset or "douady-rabbit")
            data = _jl(80, 40, -1.8, 1.8, -1.8, 1.8, max_iter, used_c)
            click.echo("\n" + ascii_preview(data) + "\n")

    elif fractal == "burning-ship":
        if output is None:
            output = f"burning_ship_{palette}.png"
        img = render_burning_ship(width, height, palette=palette, max_iter=max_iter)

    else:  # newton
        if output is None:
            output = f"newton_{poly}.png"
        img = render_newton(width, height, poly=poly, max_iter=max_iter)

    _save(img, output)
    click.secho(f"  Done in {time.time()-t0:.2f}s\n", fg="yellow")


# ─── animate command ──────────────────────────────────────────────────────────

@cli.command()
@click.argument("animation",
                type=click.Choice(["julia-orbit", "mandelbrot-zoom", "palette-cycle"]))
@click.option("-o", "--output", default=None)
@click.option("-W", "--width",  default=480, show_default=True)
@click.option("-H", "--height", default=480, show_default=True)
@click.option("-f", "--frames", default=48, show_default=True)
@click.option("-p", "--palette", default="aurora",
              type=click.Choice(PALETTE_NAMES), show_default=True)
@click.option("--max-iter", default=128, show_default=True)
def animate(animation, output, width, height, frames, palette, max_iter):
    """Generate an animated GIF."""
    t0 = time.time()
    click.secho(f"\n  Animating {animation} ({frames} frames) …", fg="cyan", bold=True)

    if animation == "julia-orbit":
        out = output or "julia_orbit.gif"
        animate_julia_orbit(width, height, frames, palette, max_iter, out)
    elif animation == "mandelbrot-zoom":
        out = output or "mandelbrot_zoom.gif"
        animate_mandelbrot_zoom(width, height, frames, palette, max_iter,
                                output_path=out)
    else:
        out = output or "palette_cycle.gif"
        animate_palette_cycle(output_path=out)

    size_kb = os.path.getsize(out) / 1024
    click.secho(f"  Saved → {out}  ({size_kb:.1f} KB)", fg="green")
    click.secho(f"  Done in {time.time()-t0:.2f}s\n", fg="yellow")


# ─── gallery command ──────────────────────────────────────────────────────────

@cli.command()
@click.option("-o", "--outdir", default="gallery", show_default=True)
@click.option("-W", "--width",  default=600, show_default=True)
@click.option("-H", "--height", default=500, show_default=True)
def gallery(outdir, width, height):
    """Render a full gallery of every fractal type and palette combination."""
    import os
    os.makedirs(outdir, exist_ok=True)
    click.secho(f"\n  Generating gallery in ./{outdir}/\n", fg="cyan", bold=True)
    total = 0

    # Mandelbrot — all presets, selected palettes
    for preset in MANDELBROT_PRESETS:
        for pal in ["inferno", "ocean", "midnight"]:
            path = f"{outdir}/mandelbrot_{preset}_{pal}.png"
            img = render_mandelbrot(width, height, preset=preset,
                                    palette=pal, max_iter=512)
            _save(img, path)
            total += 1

    # Julia — all presets
    for preset in JULIA_PRESETS:
        path = f"{outdir}/julia_{preset}_aurora.png"
        img = render_julia(width, width, preset=preset,
                           palette="aurora", max_iter=256)
        _save(img, path)
        total += 1

    # Burning Ship
    path = f"{outdir}/burning_ship_fire.png"
    img = render_burning_ship(width, height, palette="fire", max_iter=200)
    _save(img, path)
    total += 1

    # Newton — all polynomials
    for poly in ["z3-1", "z4-1", "z6-1"]:
        path = f"{outdir}/newton_{poly}.png"
        img = render_newton(width, width, poly=poly)
        _save(img, path)
        total += 1

    click.secho(f"\n  Gallery complete! {total} images saved to ./{outdir}/\n",
                fg="green", bold=True)


# ─── info command ─────────────────────────────────────────────────────────────

@cli.command()
def info():
    """List all available presets and palettes."""
    click.secho("\n  MANDELBROT PRESETS", fg="cyan", bold=True)
    for k, v in MANDELBROT_PRESETS.items():
        click.echo(f"    {k:<20} {v}")

    click.secho("\n  JULIA PRESETS", fg="cyan", bold=True)
    for k, v in JULIA_PRESETS.items():
        click.echo(f"    {k:<20} c = {v}")

    click.secho("\n  COLOUR PALETTES", fg="cyan", bold=True)
    for p in PALETTE_NAMES:
        click.echo(f"    {p}")

    click.echo()
