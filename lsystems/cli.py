"""Command-line interface for expanding and rendering L-systems."""

import argparse
import sys

from .core import LSystem
from .presets import PRESETS, get
from .svg import segments_to_svg
from .turtle import TurtleInterpreter


def _render(
    lsystem: LSystem,
    angle: float,
    iterations: int,
    start_heading: float,
    width: int,
    draw_chars: str = "FG",
) -> str:
    instructions = lsystem.expand(iterations)
    segments = TurtleInterpreter(
        angle=angle, start_heading=start_heading, draw_chars=draw_chars
    ).interpret(instructions)
    return segments_to_svg(segments, width=width)


def cmd_list(_: argparse.Namespace) -> int:
    for name in sorted(PRESETS):
        preset = PRESETS[name]
        print(f"{name:<20} {preset.description}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    preset = get(args.preset)
    iterations = args.iterations if args.iterations is not None else preset.iterations
    svg = _render(
        preset.lsystem,
        angle=preset.angle,
        iterations=iterations,
        start_heading=preset.start_heading,
        width=args.width,
        draw_chars=preset.draw_chars,
    )
    if args.output:
        with open(args.output, "w") as f:
            f.write(svg)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(svg)
    return 0


def cmd_custom(args: argparse.Namespace) -> int:
    rules = dict(rule.split("=", 1) for rule in args.rule)
    lsystem = LSystem(axiom=args.axiom, rules=rules)
    svg = _render(
        lsystem,
        angle=args.angle,
        iterations=args.iterations,
        start_heading=args.start_heading,
        width=args.width,
        draw_chars=args.draw_chars,
    )
    if args.output:
        with open(args.output, "w") as f:
            f.write(svg)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(svg)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lsystems", description="Generate fractal SVGs from L-systems.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list available presets")
    list_parser.set_defaults(func=cmd_list)

    render_parser = subparsers.add_parser("render", help="render a named preset to SVG")
    render_parser.add_argument("preset", choices=sorted(PRESETS))
    render_parser.add_argument("-o", "--output", help="output SVG path (defaults to stdout)")
    render_parser.add_argument("--iterations", type=int, default=None, help="override preset's default iteration count")
    render_parser.add_argument("--width", type=int, default=600, help="output SVG width in pixels")
    render_parser.set_defaults(func=cmd_render)

    custom_parser = subparsers.add_parser("custom", help="render a user-defined L-system to SVG")
    custom_parser.add_argument("--axiom", required=True)
    custom_parser.add_argument(
        "--rule",
        action="append",
        required=True,
        metavar="SYMBOL=REPLACEMENT",
        help="a production rule, e.g. F=F+F-F-F+F; repeat for multiple rules",
    )
    custom_parser.add_argument("--angle", type=float, required=True)
    custom_parser.add_argument("--iterations", type=int, required=True)
    custom_parser.add_argument("--start-heading", type=float, default=90.0)
    custom_parser.add_argument("--draw-chars", default="FG", help="symbols that draw a line when moved forward")
    custom_parser.add_argument("--width", type=int, default=600)
    custom_parser.add_argument("-o", "--output", help="output SVG path (defaults to stdout)")
    custom_parser.set_defaults(func=cmd_custom)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
