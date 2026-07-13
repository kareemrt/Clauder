"""Command-line interface for LifeSim."""

import argparse
import sys

from .automata import GameOfLife, BriansBrain, LangtonsAnt
from .patterns import PATTERNS, place_pattern, patterns_by_category
from .renderer import CursesRenderer, SimpleRenderer

MODES = {
    "life":  GameOfLife,
    "brain": BriansBrain,
    "ant":   LangtonsAnt,
}

BANNER = r"""
  _     _  __      _____ _
 | |   (_)/ _|    / ____(_)
 | |    _| |_ ___| (___  _ _ __ ___
 | |   | |  _/ _ \\___ \| | '_ ` _ \
 | |___| | ||  __/____) | | | | | | |
 |_____|_|_| \___|_____/|_|_| |_| |_|

 Interactive Cellular Automata Simulator
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lifesim",
        description="LifeSim — Interactive Cellular Automata Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Keyboard Controls (interactive mode):
  Space        Pause / Resume
  R            Randomize grid
  C            Clear grid
  S            Single step (when paused)
  + / -        Increase / decrease speed
  Arrow keys   Pan the viewport
  Q / Esc      Quit

Examples:
  python main.py                              Random Game of Life
  python main.py --mode brain                 Brian's Brain simulation
  python main.py --mode ant                   Langton's Ant
  python main.py --pattern gosper_glider_gun  Load a specific pattern
  python main.py --list-patterns              Show all available patterns
  python main.py --demo                       Quick non-interactive demo
        """,
    )

    p.add_argument(
        "--mode", "-m",
        choices=list(MODES.keys()),
        default="life",
        metavar="MODE",
        help="Simulation mode: life | brain | ant  (default: life)",
    )
    p.add_argument(
        "--width", "-W",
        type=int, default=200,
        help="Grid width in cells (default: 200)",
    )
    p.add_argument(
        "--height", "-H",
        type=int, default=80,
        help="Grid height in cells (default: 80)",
    )
    p.add_argument(
        "--density", "-d",
        type=float, default=0.30,
        help="Random seed density 0.0–1.0 (default: 0.30)",
    )
    p.add_argument(
        "--speed", "-s",
        type=int, default=10,
        help="Initial simulation speed in steps/sec (default: 10)",
    )
    p.add_argument(
        "--pattern", "-p",
        metavar="NAME",
        help="Load a named pattern (Game of Life only); use --list-patterns to see names",
    )
    p.add_argument(
        "--style",
        choices=["block", "shade", "dot", "square", "hash", "cross"],
        default="block",
        help="Cell rendering style (default: block)",
    )
    p.add_argument(
        "--no-wrap",
        action="store_true",
        help="Disable toroidal (wrapping) boundary",
    )
    p.add_argument(
        "--list-patterns",
        action="store_true",
        help="Print available patterns and exit",
    )
    p.add_argument(
        "--demo",
        action="store_true",
        help="Run a 3-second non-interactive demo and exit",
    )

    return p


def cmd_list_patterns() -> None:
    print("\n  LifeSim Pattern Library")
    print("  " + "─" * 46)
    by_cat = patterns_by_category()
    for category in sorted(by_cat):
        print(f"\n  ◆ {category}")
        for name in sorted(by_cat[category]):
            info = PATTERNS[name]
            desc = info.get("description", "")
            extra = ""
            if "period" in info:
                extra = f"  [period {info['period']}]"
            elif "speed" in info:
                extra = f"  [{info['speed']}]"
            elif "lifespan" in info:
                extra = f"  [dies at gen {info['lifespan']}]"
            print(f"    {name:<26} {desc}{extra}")
    print()


def cmd_demo() -> None:
    print(BANNER)
    print("  Running demo: Conway's Game of Life")
    print("  Starting from the Gosper Glider Gun...\n")

    sim = GameOfLife(70, 22)
    place_pattern(sim, "gosper_glider_gun", 20, 10)

    r = SimpleRenderer(sim, on_char="█", off_char=" ")
    r.animate(steps=60, width=68, height=20, fps=10.0)

    print(f"\n  Done — {sim.generation} generations simulated.")
    print("  Run without --demo for the full interactive experience.\n")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_patterns:
        cmd_list_patterns()
        return 0

    if args.demo:
        cmd_demo()
        return 0

    AutomatonClass = MODES[args.mode]
    sim = AutomatonClass(args.width, args.height, wrap=not args.no_wrap)

    # Initialise grid
    if args.pattern:
        if args.mode != "life":
            print("Error: --pattern only applies to --mode life", file=sys.stderr)
            return 1
        if args.pattern not in PATTERNS:
            print(
                f"Error: unknown pattern '{args.pattern}'. "
                "Run with --list-patterns to see options.",
                file=sys.stderr,
            )
            return 1
        place_pattern(sim, args.pattern, args.width // 2, args.height // 2)
    else:
        sim.randomize(args.density)

    renderer = CursesRenderer(sim, style=args.style, speed=args.speed)
    try:
        renderer.run()
    except KeyboardInterrupt:
        pass

    print(
        f"\nLifeSim session ended — "
        f"Gen {sim.generation:,}, final pop {sim.population():,}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
