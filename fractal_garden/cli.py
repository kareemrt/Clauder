"""Command-line interface for Fractal Garden."""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

from . import garden, palette, svgrender
from .species import SPECIES


def _write(output: Path | None, svg: str) -> None:
    if output is None:
        sys.stdout.write(svg)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(svg)
        print(f"wrote {output} ({len(svg):,} bytes)")


def _cmd_list(_args: argparse.Namespace) -> None:
    width = max(len(key) for key in SPECIES)
    for key, sp in SPECIES.items():
        print(f"{key.ljust(width)}  {sp.name} — {sp.description}")


def _cmd_grow(args: argparse.Namespace) -> None:
    segments = garden.grow(
        args.species,
        iterations=args.iterations,
        seed=args.seed,
        angle_jitter=args.angle_jitter,
    )
    pal = palette.resolve(args.palette)
    sp = SPECIES[args.species]
    svg = svgrender.render_svg(
        segments,
        palette=pal,
        background=args.background or sp.background,
        width_px=args.width,
        color_by=args.color_by,
    )
    _write(args.output, svg)


def _cmd_garden(args: argparse.Namespace) -> None:
    rng = random.Random(args.seed)
    species_keys = args.species or list(SPECIES)
    palette_names = list(palette.PALETTES)

    plants = []
    for key in species_keys:
        plant_seed = rng.randrange(2**32)
        segments = garden.grow(key, seed=plant_seed)
        pal_name = palette_names[rng.randrange(len(palette_names))]
        plants.append(svgrender.GardenPlant(segments, palette.resolve(pal_name)))

    svg = svgrender.render_garden(plants, width_px=args.width)
    _write(args.output, svg)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fractal-garden",
        description="Grow fractal plants and curves as SVG art using L-systems.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="list available species")
    list_parser.set_defaults(func=_cmd_list)

    grow_parser = sub.add_parser("grow", help="grow a single species into an SVG")
    grow_parser.add_argument("species", choices=sorted(SPECIES), help="species to grow")
    grow_parser.add_argument("-o", "--output", type=Path, default=None, help="output SVG path (default: stdout)")
    grow_parser.add_argument("--seed", type=int, default=None, help="random seed")
    grow_parser.add_argument("--iterations", type=int, default=None, help="override L-system iteration count")
    grow_parser.add_argument("--angle-jitter", type=float, default=None, help="override angle jitter in degrees")
    grow_parser.add_argument("--palette", choices=sorted(palette.PALETTES), default=palette.DEFAULT_PALETTE)
    grow_parser.add_argument("--background", default=None, help="override background colour (e.g. #101418)")
    grow_parser.add_argument("--width", type=int, default=900, help="output width in pixels")
    grow_parser.add_argument(
        "--color-by", choices=["auto", "depth", "position", "solid"], default="auto", help="colour gradient mode"
    )
    grow_parser.set_defaults(func=_cmd_grow)

    garden_parser = sub.add_parser("garden", help="grow several species into one scene")
    garden_parser.add_argument(
        "--species", nargs="+", choices=sorted(SPECIES), default=None, help="species to include (default: all)"
    )
    garden_parser.add_argument("-o", "--output", type=Path, default=None, help="output SVG path (default: stdout)")
    garden_parser.add_argument("--seed", type=int, default=None, help="random seed for the whole scene")
    garden_parser.add_argument("--width", type=int, default=1600, help="output width in pixels")
    garden_parser.set_defaults(func=_cmd_garden)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
