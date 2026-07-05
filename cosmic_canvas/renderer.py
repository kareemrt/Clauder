"""
Terminal renderer using Rich.

Builds a two-column layout:
  • Left  — ASCII canvas with orbital trails and body symbols
  • Right — live data panel (positions, velocities, simulation stats)
"""

import shutil
from typing import List, Tuple

from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from .bodies import CelestialBody
from .physics import total_energy

# Trail density decreases with age: newest → oldest
_TRAIL_SYMBOLS = ("·", ":", ";", ",", ".")
_TRAIL_THRESHOLDS = (0.85, 0.65, 0.45, 0.25)   # normalised age breakpoints


def _world_to_screen(
    x: float, y: float,
    scale: float,
    w: int, h: int,
) -> Tuple[int, int]:
    """
    Map world coordinates (AU) to terminal cell (col, row).

    Terminal characters are ≈2× taller than wide, so y is halved
    to produce visually circular orbits.
    """
    col = int((x / scale + 1.0) * w / 2.0)
    row = int((y / (scale * 0.5) + 1.0) * h / 2.0)
    return col, row


def _build_canvas(
    bodies: List[CelestialBody],
    scale: float,
    w: int, h: int,
) -> Text:
    """Rasterise bodies and their trails into a w×h character grid."""
    # grid[row][col] = (char, style)
    grid: List[List[Tuple[str, str]]] = [
        [(" ", "")] * w for _ in range(h)
    ]

    for body in bodies:
        n = len(body.trail)
        for i, (tx, ty) in enumerate(body.trail):
            col, row = _world_to_screen(tx, ty, scale, w, h)
            if not (0 <= col < w and 0 <= row < h):
                continue
            if grid[row][col][0] != " ":
                continue   # don't overwrite bodies or brighter trail points
            age = i / max(n, 1)   # 0 = oldest, 1 = newest
            if age > _TRAIL_THRESHOLDS[0]:
                sym, style = _TRAIL_SYMBOLS[0], body.color
            elif age > _TRAIL_THRESHOLDS[1]:
                sym, style = _TRAIL_SYMBOLS[1], f"dim {body.color}"
            elif age > _TRAIL_THRESHOLDS[2]:
                sym, style = _TRAIL_SYMBOLS[2], "dim white"
            elif age > _TRAIL_THRESHOLDS[3]:
                sym, style = _TRAIL_SYMBOLS[3], "dim white"
            else:
                sym, style = _TRAIL_SYMBOLS[4], "grey30"
            grid[row][col] = (sym, style)

    # Bodies drawn last so they always appear on top of trails
    for body in bodies:
        col, row = _world_to_screen(body.x, body.y, scale, w, h)
        if 0 <= col < w and 0 <= row < h:
            grid[row][col] = (body.symbol, f"bold {body.color}")

    text = Text(no_wrap=True)
    for row in grid:
        for char, style in row:
            text.append(char, style=style)
        text.append("\n")
    return text


def _build_info(
    bodies: List[CelestialBody],
    t: float,
    dt: float,
    substeps: int,
    initial_energy: float,
) -> Text:
    """Build the right-hand data panel."""
    info = Text()

    info.append("  BODIES\n", style="bold white underline")
    info.append("  ─────────────────\n", style="dim white")
    for body in bodies:
        info.append(f"  {body.symbol} ", style=f"bold {body.color}")
        info.append(f"{body.name}\n", style="bold white")
        info.append(f"    dist:  {body.distance:>7.3f} AU\n", style="dim white")
        info.append(f"    speed: {body.speed:>7.3f} AU/yr\n", style="dim white")

    info.append("\n  SIMULATION\n", style="bold white underline")
    info.append("  ─────────────────\n", style="dim white")

    years = int(t)
    days = (t - years) * 365.25
    info.append(f"  Time:  {t:>8.3f} yr\n", style="bright_cyan")
    info.append(f"         ({years}y {days:>5.1f}d)\n", style="dim cyan")
    info.append(f"  dt:    {dt:>8.5f} yr\n", style="dim white")
    info.append(f"  subs:  {substeps:>8d}×\n", style="dim white")

    e_now = total_energy(bodies)
    if initial_energy != 0.0:
        drift = abs((e_now - initial_energy) / initial_energy) * 100.0
        drift_str = f"{drift:.5f}%"
        drift_style = "green" if drift < 0.01 else ("yellow" if drift < 0.5 else "red")
    else:
        drift_str, drift_style = "N/A", "dim white"

    info.append(f"  ΔE:    ", style="white")
    info.append(f"{drift_str:>10}\n", style=drift_style)

    info.append("\n  [dim]Ctrl-C to exit[/dim]\n", style="dim")
    return info


class Renderer:
    """Manages layout dimensions and produces Rich renderables each frame."""

    INFO_WIDTH = 28   # fixed width of the data panel (chars)

    def __init__(self, scale: float = 6.0) -> None:
        self.scale = scale

    def render(
        self,
        bodies: List[CelestialBody],
        t: float,
        dt: float,
        substeps: int,
        initial_energy: float,
        title: str,
    ) -> Layout:
        term_w, term_h = shutil.get_terminal_size(fallback=(120, 40))

        canvas_w = max(20, term_w - self.INFO_WIDTH - 5)
        canvas_h = max(10, term_h - 4)

        canvas_text = _build_canvas(bodies, self.scale, canvas_w, canvas_h)
        info_text = _build_info(bodies, t, dt, substeps, initial_energy)

        layout = Layout()
        layout.split_row(
            Layout(
                Panel(canvas_text,
                      title=f"[bold blue]{title}[/bold blue]",
                      border_style="blue",
                      padding=(0, 0)),
                name="canvas",
            ),
            Layout(
                Panel(info_text,
                      title="[bold blue]Data[/bold blue]",
                      border_style="blue",
                      padding=(0, 0)),
                name="info",
                size=self.INFO_WIDTH + 2,
            ),
        )
        return layout
