#!/usr/bin/env python3
"""
Terrarium — Terminal Ecosystem Simulator
Run `python main.py --help` for options.
"""

import sys
import time
import argparse
import random

from terrarium.simulation import step
from terrarium.renderer import Renderer
from biomes import BIOMES


BANNER = r"""
  ╔══════════════════════════════════════╗
  ║  🌿  T E R R A R I U M  🌿          ║
  ║     Terminal Ecosystem Simulator     ║
  ╚══════════════════════════════════════╝
"""


def parse_args():
    parser = argparse.ArgumentParser(
        prog="terrarium",
        description="Terrarium — a living ecosystem in your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
biomes:
  forest       Dense woodland — many plants, steady herbivore population
  savanna      Open grassland — sparse cover, active predator-prey cycles
  sparse       Minimal seed — watch life bootstrap from almost nothing
  archipelago  Island chains — isolated pockets of evolving populations

examples:
  python main.py
  python main.py --biome savanna --speed 0.03
  python main.py --biome sparse --width 80 --height 32 --seed 42
        """,
    )
    parser.add_argument(
        "--biome",
        choices=list(BIOMES.keys()),
        default="forest",
        help="Starting biome (default: forest)",
    )
    parser.add_argument("--width",  type=int,   default=70,   help="World width  (default: 70)")
    parser.add_argument("--height", type=int,   default=28,   help="World height (default: 28)")
    parser.add_argument("--speed",  type=float, default=0.05, help="Tick delay seconds (default: 0.05)")
    parser.add_argument("--seed",   type=int,   default=None, help="Random seed for reproducibility")
    parser.add_argument("--plain",  action="store_true",      help="Use plain ASCII instead of Unicode")
    parser.add_argument("--ticks",  type=int,   default=None, help="Stop after N ticks (default: run forever)")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print(BANNER)
    print(f"  Biome : {args.biome}")
    print(f"  World : {args.width} × {args.height}")
    print(f"  Speed : {args.speed}s / tick")
    print(f"\n  Starting in 1 second … (Ctrl+C to exit)\n")
    time.sleep(1)

    world = BIOMES[args.biome](args.width, args.height)
    renderer = Renderer(world, fancy=not args.plain)

    tick = 0
    last_time = time.perf_counter()

    # Switch to alternate screen buffer
    sys.stdout.write("\033[?1049h")
    sys.stdout.flush()

    try:
        while True:
            now = time.perf_counter()
            fps = 1.0 / (now - last_time) if (now - last_time) > 0 else 0
            last_time = now

            step(world)
            renderer.render(tick, fps)
            tick += 1

            if args.ticks is not None and tick >= args.ticks:
                break

            plants, herbs, carns = world.counts()
            if herbs == 0 and carns == 0:
                # Ecosystem collapsed — plants won
                break

            time.sleep(args.speed)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore terminal
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()

    plants, herbs, carns = world.counts()
    print(f"\nSimulation ended at tick {tick}.")
    print(f"Final counts — Plants: {plants}  Herbivores: {herbs}  Carnivores: {carns}")
    if herbs == 0 and carns == 0:
        print("The ecosystem collapsed — plants reclaimed the world.")
    print()


if __name__ == "__main__":
    main()
