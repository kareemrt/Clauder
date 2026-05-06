#!/usr/bin/env python3
"""
CelluVerse — Multi-Rule Cellular Automata Playground
=====================================================
Usage:
    python main.py run --rule life --pattern glider
    python main.py run --rule brain --density 0.4
    python main.py run --rule ant --ants 3
    python main.py run --rule life --pattern gosper_gun --export out.gif
    python main.py list-rules
    python main.py list-patterns
    python main.py show glider
    python main.py demo
"""

import sys
import time

import click
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from celluverse.exporter import export_gif, export_png
from celluverse.grid import Grid
from celluverse.langton import LangtonsAnt
from celluverse.patterns import CATEGORIES, PATTERNS
from celluverse.renderer import SCHEME_NAMES, render_frame, render_grid, render_stats
from celluverse.rules import RULE_DESCRIPTIONS, RULES

console = Console()

BANNER = r"""
   ██████╗███████╗██╗     ██╗     ██╗   ██╗██╗   ██╗███████╗██████╗ ███████╗███████╗
  ██╔════╝██╔════╝██║     ██║     ██║   ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝
  ██║     █████╗  ██║     ██║     ██║   ██║██║   ██║█████╗  ██████╔╝███████╗█████╗
  ██║     ██╔══╝  ██║     ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝
  ╚██████╗███████╗███████╗███████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████║███████╗
   ╚═════╝╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
         M u l t i - R u l e   C e l l u l a r   A u t o m a t a   P l a y g r o u n d
"""

ALL_RULES = list(RULES.keys()) + ["ant"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_automaton(rule, width, height, pattern, density, seed, ants):
    if rule == "ant":
        return LangtonsAnt(width, height, num_ants=ants, seed=seed)

    grid = Grid(width, height)
    if pattern == "random":
        grid.randomize(density=density, seed=seed)
    elif pattern in PATTERNS:
        grid.place_pattern(PATTERNS[pattern].cells, width // 2, height // 2)
    else:
        console.print(
            f"[red]Pattern '[bold]{pattern}[/bold]' not found. "
            "Run [bold]list-patterns[/bold] to see options.[/red]"
        )
        sys.exit(1)
    return grid


def _cells(automaton, rule):
    return automaton.snapshot() if rule == "ant" else automaton.cells


def _display(automaton, rule, scheme):
    cells = _cells(automaton, rule)
    return render_frame(
        cells=cells,
        rule=rule,
        scheme=scheme,
        generation=automaton.generation,
        population=automaton.population,
        density=automaton.density,
        delta=automaton.population_delta,
        is_stable=getattr(automaton, "is_stable", False),
        is_oscillating=getattr(automaton, "is_oscillating", False),
        width=automaton.width,
        height=automaton.height,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
def cli():
    """CelluVerse — A Multi-Rule Cellular Automata Playground."""


@cli.command()
@click.option("--rule", "-r", default="life",
              type=click.Choice(ALL_RULES), show_default=True,
              help="Cellular automaton rule engine.")
@click.option("--pattern", "-p", default="random", show_default=True,
              help="Starting pattern name or 'random'.")
@click.option("--width",   "-W", default=70,   show_default=True, help="Grid width.")
@click.option("--height",  "-H", default=35,   show_default=True, help="Grid height.")
@click.option("--density", "-d", default=0.30, show_default=True,
              help="Cell density for random start (0–1).")
@click.option("--generations", "-g", default=0, show_default=True,
              help="Max generations to run (0 = run until Ctrl-C or stable).")
@click.option("--speed",   "-s", default=0.07, show_default=True,
              help="Seconds between generations.")
@click.option("--scheme",  "-c", default="matrix",
              type=click.Choice(SCHEME_NAMES), show_default=True,
              help="Colour scheme.")
@click.option("--ants",          default=1,  show_default=True,
              help="Number of ants (only for --rule ant).")
@click.option("--seed",          default=None, type=int,
              help="Random seed for reproducible results.")
@click.option("--export",  "-e", default=None, type=click.Path(),
              help="Export animated GIF to this path.")
@click.option("--export-frames", default=80, show_default=True,
              help="Number of frames to capture for the GIF.")
@click.option("--export-png",    default=None, type=click.Path(),
              help="Export final state as PNG.")
def run(rule, pattern, width, height, density, generations, speed, scheme,
        ants, seed, export, export_frames, export_png):
    """Run a live cellular automata simulation."""
    console.print(Text(BANNER, style="bold cyan"), justify="center")

    automaton = _make_automaton(rule, width, height, pattern, density, seed, ants)
    rule_fn    = RULES.get(rule)
    frames: list = []

    try:
        with Live(_display(automaton, rule, scheme),
                  refresh_per_second=20, console=console) as live:
            gen = 0
            while True:
                if generations > 0 and gen >= generations:
                    break

                automaton.step(rule_fn)
                gen += 1

                # Capture frames for GIF export
                if export and gen <= export_frames:
                    frames.append(_cells(automaton, rule).copy())

                live.update(_display(automaton, rule, scheme))
                time.sleep(speed)

                # Auto-stop if stable (not applicable to ant)
                if rule != "ant" and getattr(automaton, "is_stable", False):
                    console.print("\n[bold green]Simulation reached a stable state.[/bold green]")
                    break

    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted.[/dim]")

    # ── Exports ─────────────────────────────────────────────────────────────
    if export and frames:
        console.print(f"[cyan]Saving GIF ({len(frames)} frames) → [bold]{export}[/bold]…[/cyan]")
        export_gif(frames, export, rule=rule)
        console.print("[green]GIF saved.[/green]")

    if export_png:
        console.print(f"[cyan]Saving PNG → [bold]{export_png}[/bold]…[/cyan]")
        export_png(_cells(automaton, rule), export_png, rule=rule)
        console.print("[green]PNG saved.[/green]")


@cli.command("list-rules")
def list_rules():
    """List all available CA rule engines."""
    t = Table(title="[bold cyan]Available Rules[/bold cyan]",
              border_style="cyan", show_header=True)
    t.add_column("Name",        style="bold yellow", no_wrap=True)
    t.add_column("Description", style="white")
    for name, desc in RULE_DESCRIPTIONS.items():
        t.add_row(name, desc)
    console.print(t)


@cli.command("list-patterns")
@click.option("--category", "-c", default=None,
              type=click.Choice(list(CATEGORIES.keys())),
              help="Filter by category.")
def list_patterns(category):
    """List all built-in starting patterns."""
    t = Table(title="[bold cyan]Pattern Library[/bold cyan]",
              border_style="cyan", show_header=True)
    t.add_column("Name",        style="bold yellow", no_wrap=True)
    t.add_column("Category",    style="magenta")
    t.add_column("Description", style="white")
    for name, pat in PATTERNS.items():
        if category and pat.category != category:
            continue
        t.add_row(name, CATEGORIES.get(pat.category, pat.category), pat.description)
    console.print(t)


@cli.command()
@click.argument("name")
def show(name):
    """Render a pattern as ASCII art in the terminal."""
    if name not in PATTERNS:
        console.print(f"[red]Pattern '[bold]{name}[/bold]' not found.[/red]")
        sys.exit(1)
    pat = PATTERNS[name]
    text = Text()
    for row in pat.cells:
        for val in row:
            if val:
                text.append("██", style="bright_green")
            else:
                text.append("  ")
        text.append("\n")
    console.print(
        Panel(
            text,
            title=f"[bold cyan]{name}[/bold cyan]  [dim]{pat.description}[/dim]",
            border_style="cyan",
        )
    )


@cli.command()
def demo():
    """Run a self-contained demonstration of several rules and patterns."""
    demos = [
        ("life",    "gosper_gun",  "matrix",  120),
        ("brain",   "random",      "ocean",    80),
        ("maze",    "random",      "gold",     60),
        ("ant",     "random",      "fire",    200),
    ]

    console.print(Text(BANNER, style="bold cyan"), justify="center")
    console.print(
        Panel("[bold]CelluVerse Demo Mode[/bold] — cycling through rules automatically",
              border_style="cyan")
    )

    for rule, pattern, scheme, steps in demos:
        console.rule(f"[bold cyan]{rule.upper()}[/bold cyan]")
        automaton = _make_automaton(rule, 60, 30, pattern, 0.35, 42, 1)
        rule_fn   = RULES.get(rule)

        with Live(_display(automaton, rule, scheme),
                  refresh_per_second=20, console=console) as live:
            for _ in range(steps):
                automaton.step(rule_fn)
                live.update(_display(automaton, rule, scheme))
                time.sleep(0.04)
                if rule != "ant" and getattr(automaton, "is_stable", False):
                    break

        console.print()


if __name__ == "__main__":
    cli()
