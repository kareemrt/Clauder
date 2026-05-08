"""Entry point: animation loop and CLI argument parsing."""
from __future__ import annotations

import argparse
import time

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from .canvas import Canvas
from .solar_system import PLANETS


TITLE = "[bold cyan]✦  O R B I T  —  Solar System Simulator  ✦  [dim](Ctrl+C to quit)[/dim][/bold cyan]"


def _info_table(t: float) -> Table:
    tbl = Table(
        show_header=True,
        header_style="bold magenta",
        expand=True,
        show_edge=False,
        padding=(0, 1),
    )
    tbl.add_column("Planet",         style="bold", min_width=9)
    tbl.add_column("Symbol",         min_width=4)
    tbl.add_column("Orbital Period", justify="right", min_width=16)
    tbl.add_column("Orbits Elapsed", justify="right", min_width=14)
    tbl.add_column("Sim. Year",      justify="right", min_width=12)

    for p in PLANETS:
        orbits = t / p.period
        tbl.add_row(
            f"[{p.color}]{p.name}[/]",
            f"[{p.color}]{p.char}[/]",
            f"{p.period:.3f} yr",
            f"{orbits:.2f}",
            f"{t:.2f} yr",
        )
    return tbl


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="orbit",
        description="Orbit — Real-time solar system simulator in your terminal.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--speed",  type=float, default=2.0,
                        help="Simulation speed in Earth-years per real second")
    parser.add_argument("--fps",    type=int,   default=24,
                        help="Frames per second")
    parser.add_argument("--width",  type=int,   default=None,
                        help="Canvas width in columns (default: terminal width)")
    parser.add_argument("--height", type=int,   default=None,
                        help="Canvas height in rows")
    args = parser.parse_args()

    console = Console()
    width  = args.width  or max(80, console.width - 4)
    height = args.height or 34

    canvas = Canvas(width, height)
    dt = args.speed / args.fps   # years advanced per frame
    frame_s = 1.0 / args.fps

    layout = Layout()
    layout.split_column(
        Layout(name="sim",  ratio=5),
        Layout(name="data", ratio=1),
    )

    t = 0.0
    try:
        with Live(layout, refresh_per_second=args.fps, screen=True, console=console):
            while True:
                t0 = time.monotonic()

                layout["sim"].update(Panel(
                    canvas.render(PLANETS, t),
                    title=TITLE,
                    border_style="cyan",
                    padding=(0, 1),
                ))
                layout["data"].update(Panel(
                    _info_table(t),
                    title="[bold yellow]Planetary Data[/bold yellow]",
                    border_style="yellow",
                ))

                t += dt

                sleep = frame_s - (time.monotonic() - t0)
                if sleep > 0:
                    time.sleep(sleep)

    except KeyboardInterrupt:
        pass

    console.print("\n[dim]Simulation ended — thanks for exploring the cosmos![/dim]\n")


if __name__ == "__main__":
    main()
