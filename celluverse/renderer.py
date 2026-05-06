"""Terminal rendering with Rich — live panels, colour schemes, stats."""

from __future__ import annotations

import numpy as np
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# ---------------------------------------------------------------------------
# Colour schemes — map cell state value → Rich colour name
# ---------------------------------------------------------------------------

_SCHEMES: dict[str, dict[int, str]] = {
    "matrix":    {1: "bright_green",  2: "green"},
    "ocean":     {1: "bright_cyan",   2: "cyan"},
    "fire":      {1: "bright_red",    2: "yellow"},
    "ghost":     {1: "bright_white",  2: "white"},
    "aurora":    {1: "bright_magenta",2: "magenta"},
    "gold":      {1: "bright_yellow", 2: "yellow"},
    "mono":      {1: "white",         2: "bright_white"},
}

# Per-rule state colour overrides (for multi-state CAs like Brian's Brain)
_RULE_COLOURS: dict[str, dict[int, str]] = {
    "brain": {1: "bright_white", 2: "cyan"},
    "ant":   {1: "bright_yellow", 2: "bright_red"},
}

_LIVE  = "██"
_DEAD  = "  "


def _colour(rule: str, val: int, scheme: str) -> str:
    if rule in _RULE_COLOURS and val in _RULE_COLOURS[rule]:
        return _RULE_COLOURS[rule][val]
    palette = _SCHEMES.get(scheme, _SCHEMES["matrix"])
    return palette.get(val, "")


def render_grid(
    cells: np.ndarray,
    rule: str = "life",
    scheme: str = "matrix",
    max_w: int = 80,
    max_h: int = 38,
) -> Text:
    """Convert a grid array to a coloured Rich Text block."""
    h, w = cells.shape
    sx = max(1, -(-w // max_w))   # ceil division for downscaling
    sy = max(1, -(-h // max_h))

    text = Text(overflow="fold")
    for y in range(0, h, sy):
        for x in range(0, w, sx):
            val = int(np.max(cells[y : y + sy, x : x + sx]))
            if val:
                text.append(_LIVE, style=_colour(rule, val, scheme))
            else:
                text.append(_DEAD)
        text.append("\n")
    return text


def render_stats(
    rule: str,
    generation: int,
    population: int,
    density: float,
    delta: int,
    is_stable: bool,
    is_oscillating: bool,
    width: int,
    height: int,
) -> Panel:
    """Build a stats panel to sit beside the grid."""
    t = Table.grid(padding=(0, 2))
    t.add_column(style="bold cyan", no_wrap=True)
    t.add_column(style="white")

    t.add_row("Rule",       rule)
    t.add_row("Grid",       f"{width}×{height}")
    t.add_row("Generation", f"{generation:,}")
    t.add_row("Population", f"{population:,}")
    t.add_row("Density",    f"{density:.2%}")

    sign   = "+" if delta > 0 else ""
    colour = "green" if delta > 0 else ("red" if delta < 0 else "white")
    t.add_row("Δ Pop", f"[{colour}]{sign}{delta}[/{colour}]")

    if is_stable:
        status = "[bold green]stable ✓[/bold green]"
    elif is_oscillating:
        status = "[bold cyan]oscillating ↺[/bold cyan]"
    else:
        status = "[yellow]evolving …[/yellow]"
    t.add_row("Status", status)

    return Panel(t, title="[bold]Stats[/bold]", border_style="cyan", width=24)


def render_frame(
    cells: np.ndarray,
    rule: str,
    scheme: str,
    generation: int,
    population: int,
    density: float,
    delta: int,
    is_stable: bool,
    is_oscillating: bool,
    width: int,
    height: int,
) -> Columns:
    """Full side-by-side display: grid panel + stats panel."""
    grid_text = render_grid(cells, rule=rule, scheme=scheme)
    grid_panel = Panel(
        grid_text,
        title=f"[bold cyan]CelluVerse[/bold cyan]  [dim]{rule}[/dim]",
        border_style="bright_black",
        padding=(0, 1),
    )
    stats_panel = render_stats(
        rule=rule,
        generation=generation,
        population=population,
        density=density,
        delta=delta,
        is_stable=is_stable,
        is_oscillating=is_oscillating,
        width=width,
        height=height,
    )
    return Columns([grid_panel, stats_panel], equal=False)


SCHEME_NAMES = list(_SCHEMES.keys())
