#!/usr/bin/env python3
"""TerraGen CLI — entry point."""

import sys

import click
from rich.console import Console

from terragen.renderer import render_world
from terragen.world import World


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--width",  "-W", default=140,  show_default=True, help="Map width in characters.")
@click.option("--height", "-H", default=45,   show_default=True, help="Map height in characters.")
@click.option("--seed",   "-s", default=None, type=int,          help="Seed for reproducible worlds.")
@click.option("--no-legend",  is_flag=True, help="Omit the biome legend.")
@click.option("--no-stats",   is_flag=True, help="Omit world statistics.")
@click.option("--no-cities",  is_flag=True, help="Omit the settlements table.")
@click.option(
    "--export-html",
    type=click.Path(writable=True),
    default=None,
    metavar="PATH",
    help="Also export map to a standalone HTML file.",
)
def main(
    width: int,
    height: int,
    seed: int | None,
    no_legend: bool,
    no_stats: bool,
    no_cities: bool,
    export_html: str | None,
) -> None:
    """
    \b
    ████████╗███████╗██████╗ ██████╗  █████╗  ██████╗ ███████╗███╗   ██╗
       ██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║
       ██║   █████╗  ██████╔╝██████╔╝███████║██║  ███╗█████╗  ██╔██╗ ██║
       ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║██║   ██║██╔══╝  ██║╚██╗██║
       ██║   ███████╗██║  ██║██║  ██║██║  ██║╚██████╔╝███████╗██║ ╚████║
       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝

    Procedural ASCII World Map Generator.

    Every invocation creates a unique world complete with terrain, biomes,
    rivers, and settlements — unless you pin the run with --seed.

    \b
    Examples:
      python main.py                         # random world
      python main.py --seed 42               # reproducible world
      python main.py -W 200 -H 60            # larger map
      python main.py --seed 7 --export-html world.html
    """
    console = Console()

    with console.status("[bold green]Generating world…[/]", spinner="earth"):
        world = World(width=width, height=height, seed=seed)
        world.generate()

    render_world(
        world,
        console=console,
        show_legend=not no_legend,
        show_stats=not no_stats,
        show_cities=not no_cities,
    )

    if export_html:
        rec = Console(record=True, width=width + 6)
        render_world(world, console=rec,
                     show_legend=not no_legend,
                     show_stats=not no_stats,
                     show_cities=not no_cities)
        html = rec.export_html(inline_styles=True)
        with open(export_html, "w", encoding="utf-8") as fh:
            fh.write(html)
        console.print(f"\n[green]✓[/] Exported to [bold]{export_html}[/]")

    sys.exit(0)


if __name__ == "__main__":
    main()
