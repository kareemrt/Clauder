#!/usr/bin/env python3
"""
Cosmosim — Real-time N-Body Gravitational Simulator
"""
from __future__ import annotations
import sys
import time
import argparse

from .physics import Simulation
from .renderer import Renderer
from .scenarios import SCENARIOS


def run(scenario_key: str, fps: float, spf: int, view_scale: float | None) -> None:
    factory, name, dt, default_scale, default_spf = SCENARIOS[scenario_key]
    bodies  = factory()
    spf     = spf if spf > 0 else default_spf
    scale   = view_scale if view_scale else default_scale

    sim      = Simulation(bodies, dt=dt)
    renderer = Renderer(scale=scale)

    # Hide cursor, clear screen once
    sys.stdout.write('\033[?25l\033[2J')
    sys.stdout.flush()

    frame_period = 1.0 / fps

    try:
        while True:
            t0 = time.perf_counter()

            for _ in range(spf):
                sim.step()

            com    = sim.center_of_mass()
            energy = sim.total_energy()
            renderer.render(bodies, sim.step_count, sim.time, name, com, energy)

            dt_frame = time.perf_counter() - t0
            slack    = frame_period - dt_frame
            if slack > 0:
                time.sleep(slack)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\033[?25h\033[0m\n')
        print(f"\nSimulation stopped — step {sim.step_count}, t = {sim.time:.3f}")


def main() -> None:
    p = argparse.ArgumentParser(
        prog='cosmosim',
        description='Cosmosim — Real-time N-Body Gravitational Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='\n'.join(
            f'  {k:10}  {v[1]}' for k, v in SCENARIOS.items()
        ),
    )
    p.add_argument(
        'scenario', nargs='?', default='solar',
        choices=list(SCENARIOS.keys()),
        metavar='SCENARIO',
        help=f'One of: {", ".join(SCENARIOS)} (default: solar)',
    )
    p.add_argument('--fps',   type=float, default=30,  help='Target FPS (default 30)')
    p.add_argument('--spf',   type=int,   default=0,   help='Sim steps per frame (0=auto)')
    p.add_argument('--scale', type=float, default=None, help='View scale (default per-scenario)')
    p.add_argument('--list',  action='store_true',     help='List scenarios and exit')

    args = p.parse_args()

    if args.list:
        print("Available scenarios:")
        for k, (_, name, dt, scale, spf) in SCENARIOS.items():
            print(f"  {k:10}  {name}")
        return

    run(args.scenario, args.fps, args.spf, args.scale)


if __name__ == '__main__':
    main()
