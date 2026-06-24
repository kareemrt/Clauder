"""Command-line interface for lsystemgarden."""

from __future__ import annotations

import argparse
import pathlib
import sys

from .lsystem import LSystem
from .presets import PRESETS
from .render_svg import render
from .turtle import interpret


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lsystemgarden",
        description="Grow botanical fractals from Lindenmayer-system grammars and render them to SVG.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list available presets")

    render_parser = sub.add_parser("render", help="render a preset to an SVG file")
    render_parser.add_argument("preset", choices=sorted(PRESETS))
    render_parser.add_argument("-o", "--output", type=pathlib.Path, required=True)
    render_parser.add_argument("--iterations", type=int, default=None, help="override the preset's default generation count")
    render_parser.add_argument("--seed", type=int, default=None, help="override the random seed (stochastic presets only)")
    render_parser.add_argument("--width", type=int, default=800)
    render_parser.add_argument("--height", type=int, default=800)
    render_parser.add_argument("--start-color", default=None)
    render_parser.add_argument("--end-color", default=None)

    return parser


def _render_preset(name: str, args: argparse.Namespace) -> tuple[str, int]:
    preset = PRESETS[name]
    iterations = preset.iterations if args.iterations is None else args.iterations
    seed = preset.seed if args.seed is None else args.seed

    system = LSystem(axiom=preset.axiom, rules=preset.rules, angle=preset.angle, seed=seed)
    commands = system.expand(iterations)
    segments = interpret(
        commands,
        angle=preset.angle,
        step=preset.step,
        start_heading=preset.start_heading,
        draw_chars=preset.draw_chars,
    )
    svg = render(
        segments,
        width=args.width,
        height=args.height,
        start_color=args.start_color or preset.start_color,
        end_color=args.end_color or preset.end_color,
    )
    return svg, len(segments)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "list":
        for name in sorted(PRESETS):
            preset = PRESETS[name]
            print(f"{name:22s} angle={preset.angle:<6g} iterations={preset.iterations:<3d} {preset.description}")
        return 0

    if args.command == "render":
        svg, segment_count = _render_preset(args.preset, args)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg)
        print(f"wrote {segment_count} segments to {args.output}", file=sys.stderr)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
