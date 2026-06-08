"""Command-line interface for L-System Garden.

Examples:
    lsystem-garden list
    lsystem-garden grow fern -i 6 -o fern.svg
    lsystem-garden grow dragon-curve -i 12 --angle 90 -o dragon.svg
    lsystem-garden grow bush -i 5 --seed 7 -o bush.svg --start-heading 90
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

from . import presets
from .core import expand, stats_for
from .render import render_svg
from .turtle import walk

DEFAULT_ITERATIONS = {
    "fractal-plant": 5,
    "fern": 6,
    "bush": 5,
    "koch-snowflake": 4,
    "sierpinski": 6,
    "dragon-curve": 11,
    "hilbert-curve": 5,
    "levy-curve": 14,
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lsystem-garden",
        description="Grow fractal plants and curves from L-system grammars, rendered as SVG.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List the available presets.")
    list_p.set_defaults(func=_cmd_list)

    grow_p = sub.add_parser("grow", help="Grow a preset (or custom grammar) and render it to SVG.")
    grow_p.add_argument("preset", nargs="?", help="Preset name (see `lsystem-garden list`).")
    grow_p.add_argument("-i", "--iterations", type=int, default=None, help="Number of rewrite passes.")
    grow_p.add_argument("-o", "--output", type=Path, default=None, help="Output SVG path.")
    grow_p.add_argument("--angle", type=float, default=None, help="Override the turning angle, in degrees.")
    grow_p.add_argument("--step", type=float, default=6.0, help="Length of one forward move (default: 6).")
    grow_p.add_argument(
        "--start-heading", type=float, default=90.0, help="Initial heading in degrees (default: 90, i.e. up)."
    )
    grow_p.add_argument("--seed", type=int, default=None, help="Random seed, for reproducible stochastic systems.")
    grow_p.add_argument("--background", default=None, help="Override the canvas background color.")
    grow_p.add_argument("--trunk-color", default=None, help="Override the depth-0 stroke color.")
    grow_p.add_argument("--tip-color", default=None, help="Override the deepest-branch stroke color.")
    grow_p.add_argument("--stroke-width", type=float, default=1.4, help="Base stroke width (default: 1.4).")
    grow_p.add_argument("--no-taper", action="store_true", help="Disable width tapering toward branch tips.")
    grow_p.add_argument("--axiom", default=None, help="Custom axiom (overrides the preset, requires --rule).")
    grow_p.add_argument(
        "--rule",
        action="append",
        default=None,
        metavar="SYMBOL=REPLACEMENT",
        help="Custom production rule, e.g. --rule F=F+F--F+F. Repeatable.",
    )
    grow_p.set_defaults(func=_cmd_grow)

    return parser


def _cmd_list(_args: argparse.Namespace) -> int:
    print(f"{'preset':<16} {'angle':>6}  description")
    print("-" * 70)
    for name in presets.names():
        system = presets.get(name)
        print(f"{name:<16} {system.angle:>5.1f}°  {system.description}")
    return 0


def _parse_custom_rules(rule_args: list[str]) -> dict[str, str]:
    rules: dict[str, str] = {}
    for raw in rule_args:
        if "=" not in raw:
            raise ValueError(f"malformed --rule {raw!r}, expected SYMBOL=REPLACEMENT")
        symbol, replacement = raw.split("=", 1)
        symbol = symbol.strip()
        if len(symbol) != 1:
            raise ValueError(f"--rule symbol must be a single character, got {symbol!r}")
        rules[symbol] = replacement
    return rules


def _cmd_grow(args: argparse.Namespace) -> int:
    if args.axiom is not None or args.rule is not None:
        if not (args.axiom and args.rule and args.angle is not None):
            print("error: a custom grammar needs --axiom, at least one --rule, and --angle", file=sys.stderr)
            return 2
        system_name = "custom"
        axiom = args.axiom
        rules = _parse_custom_rules(args.rule)
        angle = args.angle
        background = args.background or "#0b1020"
        trunk_color = args.trunk_color or "#5d4037"
        tip_color = args.tip_color or "#a5d6a7"
        iterations = args.iterations if args.iterations is not None else 5
    else:
        if not args.preset:
            print("error: pass a preset name, or supply --axiom/--rule/--angle for a custom grammar", file=sys.stderr)
            return 2
        try:
            system = presets.get(args.preset)
        except KeyError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        system_name = system.name
        axiom = system.axiom
        rules = system.rules
        angle = args.angle if args.angle is not None else system.angle
        background = args.background or system.background
        trunk_color = args.trunk_color or system.seed_color
        tip_color = args.tip_color or "#e8f5e9"
        iterations = (
            args.iterations if args.iterations is not None else DEFAULT_ITERATIONS.get(system_name, 5)
        )

    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    grown = expand(axiom, rules, iterations, rng=rng)
    summary = stats_for(grown, iterations)

    segments = walk(grown, angle=angle, step=args.step, start_heading=args.start_heading)
    svg = render_svg(
        segments,
        background=background,
        trunk_color=trunk_color,
        tip_color=tip_color,
        stroke_width=args.stroke_width,
        taper=not args.no_taper,
        title=f"{system_name} (iterations={iterations})",
    )

    output = args.output or Path(f"{system_name}.svg")
    output.write_text(svg, encoding="utf-8")

    print(
        f"grew '{system_name}' for {summary.iterations} iteration(s): "
        f"{summary.length:,} symbols, {summary.draw_commands:,} line segments drawn"
    )
    print(f"wrote {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
