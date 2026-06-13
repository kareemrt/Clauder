"""Command-line interface for WorldForge."""

from __future__ import annotations

import argparse
import sys

from .render import render_ascii, render_png
from .worldgen import generate_world


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="worldforge",
        description="Generate a procedural fantasy world map.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed (default: random)")
    parser.add_argument("--width", type=int, default=256, help="Map width in cells")
    parser.add_argument("--height", type=int, default=256, help="Map height in cells")
    parser.add_argument("--output", type=str, default="world.png", help="Output PNG path")
    parser.add_argument("--scale-factor", type=int, default=2, help="PNG upscale factor (pixels per cell)")
    parser.add_argument("--octaves", type=int, default=6, help="Noise octaves for terrain detail")
    parser.add_argument("--noise-scale", type=float, default=4.0, help="Number of noise periods across the map")
    parser.add_argument("--island-strength", type=float, default=0.9, help="0 = no island falloff, higher = smaller landmass")
    parser.add_argument("--rivers", type=int, default=10, help="Number of rivers to carve")
    parser.add_argument("--ascii", action="store_true", help="Print an ASCII preview of the map")
    parser.add_argument("--ascii-step", type=int, default=4, help="Sampling step for the ASCII preview")
    parser.add_argument("--no-png", action="store_true", help="Skip writing the PNG file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    world = generate_world(
        seed=args.seed,
        width=args.width,
        height=args.height,
        octaves=args.octaves,
        scale=args.noise_scale,
        island_strength=args.island_strength,
        river_count=args.rivers,
    )

    print(f"World: {world.name}")
    print(f"Seed:  {world.seed}")
    print(f"Size:  {world.width} x {world.height}")

    counts = world.biome_counts()
    total_cells = world.width * world.height
    print("\nBiome distribution:")
    for biome, count in counts.items():
        if biome == "river":
            print(f"  {biome:<10} {count} cells")
            continue
        pct = 100.0 * count / total_cells
        print(f"  {biome:<10} {pct:5.1f}%")

    if not args.no_png:
        render_png(world, args.output, scale_factor=args.scale_factor)
        print(f"\nSaved map to {args.output}")

    if args.ascii:
        print("\n" + render_ascii(world, step=args.ascii_step))

    return 0


if __name__ == "__main__":
    sys.exit(main())
