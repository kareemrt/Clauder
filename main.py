#!/usr/bin/env python3
"""
CosmicCanvas — Real-time N-Body Gravitational Simulator

Usage:
  python main.py [preset] [options]

Presets:
  solar    Inner solar system + Jupiter  (default)
  binary   Binary star with circumbinary planet
  figure8  Choreographic figure-8 three-body orbit
  chaos    Seven-body unstable ring → gravitational chaos
"""

import argparse
import signal
import sys
import time

from rich.console import Console

try:
    from rich.live import Live
except ImportError:
    print("Rich is required: pip install rich>=13.0.0")
    sys.exit(1)

from cosmic_canvas import presets
from cosmic_canvas.physics import step, total_energy
from cosmic_canvas.renderer import Renderer

PRESETS = {
    "solar":   ("Inner Solar System",            presets.solar_system,  6.0,  0.0010, 20),
    "binary":  ("Binary Star + Tatooine",        presets.binary_star,   4.5,  0.0010, 20),
    "figure8": ("Figure-8 Three-Body Orbit",     presets.figure_eight,  1.8,  0.0005, 10),
    "chaos":   ("Seven-Body Gravitational Chaos", presets.chaotic_cluster, 4.0, 0.0005, 10),
}
# PRESETS[key] = (title, factory, default_scale, default_dt, default_substeps)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="CosmicCanvas — N-Body Gravitational Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Presets:\n" +
            "\n".join(f"  {k:10s}  {v[0]}" for k, v in PRESETS.items())
        ),
    )
    p.add_argument("preset", nargs="?", default="solar",
                   choices=list(PRESETS.keys()),
                   help="Scene preset (default: solar)")
    p.add_argument("--dt", type=float, default=None,
                   help="Time step in years (default varies by preset)")
    p.add_argument("--speed", type=int, default=None,
                   help="Physics substeps per display frame (default varies)")
    p.add_argument("--scale", type=float, default=None,
                   help="Viewport half-width in AU (default varies)")
    p.add_argument("--fps", type=float, default=24.0,
                   help="Target frames per second (default: 24)")
    p.add_argument("--years", type=float, default=None,
                   help="Stop after this many simulated years")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    title, factory, default_scale, default_dt, default_substeps = PRESETS[args.preset]
    scale    = args.scale  if args.scale  is not None else default_scale
    dt       = args.dt     if args.dt     is not None else default_dt
    substeps = args.speed  if args.speed  is not None else default_substeps

    bodies = factory()
    renderer = Renderer(scale=scale)
    console = Console()

    initial_energy = total_energy(bodies)
    t = 0.0
    frame_interval = 1.0 / args.fps

    running = True

    def _stop(sig, frame):   # noqa: ANN001
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    console.print(
        f"\n[bold blue]CosmicCanvas[/bold blue]  ✦  [white]{title}[/white]\n"
        f"[dim]scale={scale} AU  dt={dt} yr  substeps={substeps}  "
        f"Press Ctrl-C to exit[/dim]\n"
    )
    time.sleep(0.4)

    with Live(console=console, refresh_per_second=args.fps, screen=True) as live:
        while running:
            frame_start = time.perf_counter()

            for _ in range(substeps):
                step(bodies, dt)
            t += dt * substeps

            if args.years is not None and t >= args.years:
                running = False

            renderable = renderer.render(
                bodies, t, dt, substeps, initial_energy, title
            )
            live.update(renderable)

            elapsed = time.perf_counter() - frame_start
            wait = frame_interval - elapsed
            if wait > 0:
                time.sleep(wait)

    console.print(
        f"\n[bold blue]CosmicCanvas[/bold blue] — simulation ended.\n"
        f"[dim]Simulated {t:.3f} years across {len(bodies)} bodies.[/dim]\n"
    )


if __name__ == "__main__":
    main()
