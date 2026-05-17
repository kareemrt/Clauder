"""Rich-powered terminal renderer for TerraGen worlds."""

from __future__ import annotations

from collections import Counter

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .biomes import BIOME_DISPLAY, Biome

_WATER = {Biome.DEEP_OCEAN, Biome.OCEAN, Biome.SHALLOW_WATER}

_RIVER_CHAR   = "≀"
_CITY_CHAR    = "★"
_CAPITAL_CHAR = "⊕"

LOGO = r"""
 ████████╗███████╗██████╗ ██████╗  █████╗  ██████╗ ███████╗███╗   ██╗
    ██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║
    ██║   █████╗  ██████╔╝██████╔╝███████║██║  ███╗█████╗  ██╔██╗ ██║
    ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║██║   ██║██╔══╝  ██║╚██╗██║
    ██║   ███████╗██║  ██║██║  ██║██║  ██║╚██████╔╝███████╗██║ ╚████║
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
"""


def render_world(
    world,
    console: Console | None = None,
    show_legend: bool = True,
    show_stats: bool = True,
    show_cities: bool = True,
) -> None:
    if console is None:
        console = Console()

    # ── Header ──────────────────────────────────────────────────────────
    console.print(Text(LOGO, style="bold gold1"), justify="center")
    console.print(
        Align.center(f"[bold white]{world.world_name.upper()}[/]")
    )
    console.print(
        Align.center(
            f"[dim]Seed [bold]{world.seed}[/]  ·  "
            f"{world.width}×{world.height}  ·  "
            f"{len(world.rivers)} rivers  ·  "
            f"{len(world.cities)} settlements[/]"
        )
    )
    console.print()

    # ── Map ─────────────────────────────────────────────────────────────
    city_pos = {(y, x): (cap, name) for y, x, cap, name in world.cities}

    map_text = Text()
    for y in range(world.height):
        for x in range(world.width):
            biome = world.biome_map[y][x]
            bg = BIOME_DISPLAY[biome][2]

            if (y, x) in city_pos:
                is_cap, _ = city_pos[(y, x)]
                char = _CAPITAL_CHAR if is_cap else _CITY_CHAR
                style = f"bold bright_yellow on {bg}"
                map_text.append(char, style=style)
            elif (y, x) in world.river_cells:
                map_text.append(_RIVER_CHAR, style=f"bold bright_cyan on {bg}")
            else:
                char, fg, bg_b, _ = BIOME_DISPLAY[biome]
                map_text.append(char, style=f"{fg} on {bg_b}")
        map_text.append("\n")

    console.print(
        Panel(
            map_text,
            title=f"[bold gold1]  {world.world_name}  [/]",
            border_style="gold1",
            padding=(0, 1),
        )
    )

    # ── Legend ───────────────────────────────────────────────────────────
    if show_legend:
        _render_legend(console)

    # ── Stats ────────────────────────────────────────────────────────────
    if show_stats:
        _render_stats(world, console)

    # ── Cities ───────────────────────────────────────────────────────────
    if show_cities and world.cities:
        _render_cities(world, console)


# ── Helper panels ────────────────────────────────────────────────────────────

def _render_legend(console: Console) -> None:
    tbl = Table(title="[bold]Biome Legend[/]", box=box.ROUNDED, border_style="dim", padding=(0, 1))
    tbl.add_column("", justify="center", width=3, no_wrap=True)
    tbl.add_column("Biome",  width=18)
    tbl.add_column("", justify="center", width=3, no_wrap=True)
    tbl.add_column("Biome",  width=18)

    items = [(BIOME_DISPLAY[b], b) for b in Biome]
    for i in range(0, len(items), 2):
        (c1, f1, bg1, n1), _ = items[i]
        sym1 = Text(c1, style=f"{f1} on {bg1}")
        if i + 1 < len(items):
            (c2, f2, bg2, n2), _ = items[i + 1]
            tbl.add_row(sym1, n1, Text(c2, style=f"{f2} on {bg2}"), n2)
        else:
            tbl.add_row(sym1, n1, "", "")

    tbl.add_row(
        Text(_RIVER_CHAR, style="bold bright_cyan"), "River",
        Text(_CITY_CHAR,  style="bold bright_yellow"), "Settlement",
    )
    tbl.add_row(
        Text(_CAPITAL_CHAR, style="bold bright_yellow"), "Capital", "", "",
    )
    console.print()
    console.print(Align.center(tbl))


def _render_stats(world, console: Console) -> None:
    total = world.width * world.height
    counts: Counter = Counter()
    for row in world.biome_map:
        counts.update(row)

    water_cells = sum(v for b, v in counts.items() if b in _WATER)
    land_cells  = total - water_cells

    dominant_land = max(
        ((b, v) for b, v in counts.items() if b not in _WATER),
        key=lambda t: t[1],
        default=(Biome.GRASSLAND, 0),
    )
    dom_name = BIOME_DISPLAY[dominant_land[0]][3]

    tbl = Table(title="[bold]World Statistics[/]", box=box.ROUNDED, border_style="dim", padding=(0, 1))
    tbl.add_column("Stat",  width=20)
    tbl.add_column("Value", width=14)
    tbl.add_column("Stat",  width=20)
    tbl.add_column("Value", width=14)

    tbl.add_row("Dimensions",    f"{world.width} × {world.height}",
                "Total Cells",   f"{total:,}")
    tbl.add_row("Land Coverage", f"{land_cells / total * 100:.1f}%",
                "Ocean Coverage",f"{water_cells / total * 100:.1f}%")
    tbl.add_row("Rivers",        str(len(world.rivers)),
                "Settlements",   str(len(world.cities)))
    tbl.add_row("Dominant Biome", dom_name,
                "Seed",          str(world.seed))

    console.print()
    console.print(Align.center(tbl))


def _render_cities(world, console: Console) -> None:
    tbl = Table(title="[bold]Notable Settlements[/]", box=box.ROUNDED, border_style="dim", padding=(0, 1))
    tbl.add_column("Name",     width=16)
    tbl.add_column("Type",     width=10)
    tbl.add_column("Location", width=12)
    tbl.add_column("Biome",    width=20)

    for y, x, is_cap, name in sorted(world.cities, key=lambda c: not c[2]):
        biome = world.biome_map[y][x]
        bname = BIOME_DISPLAY.get(biome, ("?", "w", "b", "Unknown"))[3]
        ctype = "[bold yellow]Capital[/]" if is_cap else "Town"
        tbl.add_row(f"[bold]{name}[/]", ctype, f"({x}, {y})", bname)

    console.print()
    console.print(Align.center(tbl))
