"""Command-line interface for Nebula."""
from __future__ import annotations

import argparse
import sys
import time

from .renderer import Renderer
from .scenarios import SCENARIOS, SCENARIO_DESCRIPTIONS


BANNER = r"""
  ███╗   ██╗███████╗██████╗ ██╗   ██╗██╗      █████╗
  ████╗  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔══██╗
  ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ███████║
  ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██╔══██║
  ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗██║  ██║
  ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
        N - B o d y   G r a v i t a t i o n a l
"""


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="nebula",
        description="Terminal N-body gravitational simulator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py figure8\n"
            "  python main.py solar --fps 60 --steps 10\n"
            "  python main.py random --n 8 --seed 7\n"
            "  python main.py galaxy --fps 20\n"
        ),
    )
    p.add_argument(
        "scenario", nargs="?", default="figure8",
        choices=list(SCENARIOS.keys()),
        metavar="SCENARIO",
        help=f"Preset to run. Choices: {', '.join(SCENARIOS)} (default: figure8)",
    )
    p.add_argument("--fps",    type=float, default=30.0,  help="Target frames per second (default: 30)")
    p.add_argument("--steps",  type=int,   default=5,     help="Physics substeps per frame (default: 5)")
    p.add_argument("--width",  type=int,   default=None,  help="Override terminal width")
    p.add_argument("--height", type=int,   default=None,  help="Override terminal height")
    p.add_argument("--n",      type=int,   default=6,     help="Body count for 'random' scenario (default: 6)")
    p.add_argument("--seed",   type=int,   default=0,     help="RNG seed for 'random' scenario (default: 0)")
    p.add_argument("--list",   action="store_true",       help="List all scenarios and exit")
    return p


def main():
    args = _build_parser().parse_args()

    if args.list:
        print(BANNER)
        print("Available scenarios:\n")
        for name, desc in SCENARIO_DESCRIPTIONS.items():
            print(f"  {name:<10s}  {desc}")
        print()
        return

    factory = SCENARIOS[args.scenario]
    sim     = factory(n=args.n, seed=args.seed) if args.scenario == "random" else factory()
    renderer  = Renderer(width=args.width, height=args.height)
    frame_dt  = 1.0 / max(args.fps, 1.0)

    print(BANNER)
    print(f"  Scenario : {args.scenario}")
    print(f"  Bodies   : {len(sim.bodies)}")
    print(f"  Target   : {args.fps} fps  ×  {args.steps} steps/frame")
    print("  Starting in 1 s … (Ctrl-C to quit)\n")
    time.sleep(1.0)

    try:
        while True:
            t0 = time.perf_counter()

            for _ in range(args.steps):
                sim.step()

            elapsed    = time.perf_counter() - t0
            fps_actual = 1.0 / max(elapsed, 1e-9)
            renderer.render(sim, fps_actual)

            remaining = frame_dt - (time.perf_counter() - t0)
            if remaining > 0:
                time.sleep(remaining)

    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h")  # restore cursor
        print("\n\n  Simulation stopped. Goodbye! ✦\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
