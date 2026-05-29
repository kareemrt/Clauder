#!/usr/bin/env python3
"""WorldForge CLI — generate and render procedural ASCII worlds."""

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="worldforge",
        description="WorldForge — Procedural ASCII World Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python generate.py                             # default (seed=42, 65×65)
  python generate.py --seed 1337                 # different seed
  python generate.py --size 129                  # larger world
  python generate.py --no-color                  # plain text
  python generate.py --output my_world.txt       # save to file
  python generate.py --legend --stats            # show legend + stats
        """,
    )
    parser.add_argument("--seed",    type=int, default=42,
                        help="world generation seed (default: 42)")
    parser.add_argument("--size",    type=int, default=65,
                        choices=[33, 65, 129, 257],
                        help="map edge length — must be 2^k+1 (default: 65)")
    parser.add_argument("--rivers",  type=int, default=12,
                        help="target number of rivers (default: 12)")
    parser.add_argument("--cities",  type=int, default=8,
                        help="target number of cities (default: 8)")
    parser.add_argument("--no-color", action="store_true",
                        help="disable ANSI colour")
    parser.add_argument("--output", "-o", type=str,
                        help="save plain-text map to this file")
    parser.add_argument("--legend", action="store_true",
                        help="print biome legend")
    parser.add_argument("--stats",  action="store_true",
                        help="print biome coverage statistics")
    args = parser.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()

    from worldforge.world import World
    from worldforge.renderer import render_terminal, render_plain, render_legend

    w = args.size
    border = "═" * (w + 2)
    header_text = "W O R L D F O R G E"
    sub_text    = f"Seed: {args.seed}   Size: {w}×{w}"
    print(f"╔{border}╗")
    print(f"║{header_text:^{w + 2}}║")
    print(f"║{sub_text:^{w + 2}}║")
    print(f"╚{border}╝\n")

    world = World(
        size=args.size,
        seed=args.seed,
        num_rivers=args.rivers,
        num_cities=args.cities,
        verbose=True,
    )

    print()
    render_terminal(world, use_color=use_color)

    if args.legend:
        print("\nLEGEND")
        print("──────")
        print(render_legend(use_color=use_color))

    if args.stats:
        print("\nBIOME COVERAGE")
        print("──────────────")
        for biome, pct in world.stats().items():
            bar = "█" * int(pct / 2)
            print(f"  {biome:<20} {pct:>5.1f}%  {bar}")

    print()

    if args.output:
        plain = render_plain(world)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(plain)
        print(f"Map saved → {args.output}")


if __name__ == "__main__":
    main()
