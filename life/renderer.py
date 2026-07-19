"""Terminal rendering via Rich."""
from __future__ import annotations

import numpy as np
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich import box
from rich.style import Style

console = Console()

# Colour gradient for population age (cells that have been alive longest shine brightest)
ALIVE_STYLES = [
    "bold bright_cyan",
    "bold bright_green",
    "bold bright_yellow",
    "bold yellow",
    "bold bright_magenta",
]

DEAD_CHAR   = "  "
ALIVE_CHARS = ["██", "▓▓", "▒▒", "░░", "▪▪"]


def _cell_style(age: int, style_idx: int = 0) -> str:
    return ALIVE_STYLES[min(style_idx, len(ALIVE_STYLES) - 1)]


def render_board_simple(
    grid: np.ndarray,
    title: str = "",
    color: str = "bright_cyan",
    char: str = "██",
) -> Panel:
    lines = []
    for row in grid:
        line = Text()
        for cell in row:
            if cell:
                line.append(char, style=f"bold {color}")
            else:
                line.append(DEAD_CHAR)
        lines.append(line)

    content = Text("\n").join(lines)
    return Panel(content, title=title, border_style="dim cyan", padding=(0, 1))


def render_board_gradient(
    grid: np.ndarray,
    prev_grid: np.ndarray | None = None,
    age_grid: np.ndarray | None = None,
    title: str = "",
) -> Panel:
    """Render with per-cell age colouring."""
    h, w = grid.shape

    if age_grid is None:
        age_grid = grid.copy().astype(np.int32)
    if prev_grid is None:
        prev_grid = grid.copy()

    lines = []
    for r in range(h):
        line = Text()
        for c in range(w):
            if grid[r, c]:
                age = int(age_grid[r, c])
                bucket = min(age // 5, len(ALIVE_STYLES) - 1)
                line.append("██", style=ALIVE_STYLES[bucket])
            else:
                line.append(DEAD_CHAR)
        lines.append(line)

    content = Text("\n").join(lines)
    return Panel(content, title=title, border_style="dim", padding=(0, 1))


def render_stats(
    generation: int,
    population: int,
    fitness: float | None = None,
    alive_gens: int | None = None,
    unique_states: int | None = None,
    extra: dict | None = None,
) -> Table:
    t = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    t.add_column("key",   style="dim")
    t.add_column("value", style="bold bright_white")

    t.add_row("Generation", str(generation))
    t.add_row("Population", str(population))
    if fitness is not None:
        t.add_row("Fitness",    f"{fitness:.4f}")
    if alive_gens is not None:
        t.add_row("Alive gens", str(alive_gens))
    if unique_states is not None:
        t.add_row("Uniq states", str(unique_states))
    if extra:
        for k, v in extra.items():
            t.add_row(k, str(v))
    return t


def render_evolution_bar(generation: int, total: int, best_fitness: float, mean_fitness: float) -> str:
    frac  = generation / max(total, 1)
    width = 30
    filled = int(frac * width)
    bar   = "█" * filled + "░" * (width - filled)
    return (
        f"[dim]Gen [bold]{generation:3d}[/bold]/{total}[/dim]  "
        f"[cyan]{bar}[/cyan]  "
        f"best=[bold bright_green]{best_fitness:.4f}[/bold bright_green]  "
        f"mean=[yellow]{mean_fitness:.4f}[/yellow]"
    )


def print_header() -> None:
    console.print()
    console.print(
        "[bold bright_cyan]"
        "  ██████╗ █████╗ ███╗   ███╗███████╗     ██████╗ ███████╗    ██╗     ██╗███████╗███████╗\n"
        " ██╔════╝██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██╔════╝    ██║     ██║██╔════╝██╔════╝\n"
        " ██║     ███████║██╔████╔██║█████╗      ██║   ██║█████╗      ██║     ██║█████╗  █████╗  \n"
        " ██║     ██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██╔══╝      ██║     ██║██╔══╝  ██╔══╝  \n"
        " ╚██████╗██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝██║         ███████╗██║██║     ███████╗\n"
        "  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝         ╚══════╝╚═╝╚═╝     ╚══════╝[/bold bright_cyan]"
    )
    console.print(
        "  [dim]Conway's Game of Life  ·  Evolutionary Pattern Discovery[/dim]\n"
    )
