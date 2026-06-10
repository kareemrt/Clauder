"""Command line interface for Fractal Garden."""

from __future__ import annotations

import argparse
import json
import sys

from .lsystem import LSystem, interpret
from .presets import PRESETS, get_preset
from .render import render_animation, render_image


def _load_custom_lsystem(path: str) -> LSystem:
    with open(path) as handle:
        data = json.load(handle)
    return LSystem(
        name=data.get("name", "Custom L-System"),
        description=data.get("description", ""),
        axiom=data["axiom"],
        rules=data["rules"],
        angle=data["angle"],
        draw_chars=data.get("draw_chars", "F"),
        start_heading=data.get("start_heading", 90.0),
        default_iterations=data.get("default_iterations", 4),
    )


def _resolve_lsystem(args: argparse.Namespace) -> LSystem:
    return _load_custom_lsystem(args.custom) if args.custom else get_preset(args.preset)


def cmd_list(args: argparse.Namespace) -> int:
    print(f"{'KEY':<22} {'NAME':<28} {'DEFAULT ITERS':<14} DESCRIPTION")
    for key, lsystem in sorted(PRESETS.items()):
        print(f"{key:<22} {lsystem.name:<28} {lsystem.default_iterations:<14} {lsystem.description}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    lsystem = _resolve_lsystem(args)
    iterations = args.iterations if args.iterations is not None else lsystem.default_iterations
    segments = render_image(
        lsystem,
        iterations,
        args.output,
        cmap=args.cmap,
        linewidth=args.linewidth,
        figsize=(args.size, args.size),
        dpi=args.dpi,
    )
    print(f"Rendered '{lsystem.name}' (iteration {iterations}, {len(segments)} segments) -> {args.output}")
    return 0


def cmd_animate(args: argparse.Namespace) -> int:
    lsystem = _resolve_lsystem(args)
    max_iterations = args.iterations if args.iterations is not None else lsystem.default_iterations
    render_animation(
        lsystem,
        max_iterations,
        args.output,
        cmap=args.cmap,
        linewidth=args.linewidth,
        figsize=(args.size, args.size),
        fps=args.fps,
    )
    print(f"Rendered growth animation for '{lsystem.name}' (0..{max_iterations}) -> {args.output}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    lsystem = _resolve_lsystem(args)
    iterations = args.iterations if args.iterations is not None else lsystem.default_iterations
    instructions = lsystem.expand(iterations)
    segments = interpret(instructions, lsystem)
    print(f"Name:        {lsystem.name}")
    print(f"Description: {lsystem.description}")
    print(f"Axiom:       {lsystem.axiom}")
    print(f"Rules:       {lsystem.rules}")
    print(f"Angle:       {lsystem.angle} degrees")
    print(f"Iterations:  {iterations}")
    print(f"String len:  {len(instructions)}")
    print(f"Segments:    {len(segments)}")
    return 0


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("preset", nargs="?", help="Preset key (see the 'list' command)")
    parser.add_argument("--custom", help="Path to a JSON file describing a custom L-system")
    parser.add_argument("--iterations", "-n", type=int, help="Number of rewrite iterations")
    parser.add_argument("--cmap", default="spring", help="Matplotlib colormap used for branch depth")
    parser.add_argument("--linewidth", type=float, default=0.8, help="Line width")
    parser.add_argument("--size", type=float, default=8.0, help="Figure size in inches (square)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fractal-garden",
        description="Grow and render Lindenmayer-system (L-system) fractals.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available fractal presets")
    list_parser.set_defaults(func=cmd_list)

    render_parser = subparsers.add_parser("render", help="Render a single fractal image")
    _add_common_arguments(render_parser)
    render_parser.add_argument("--output", "-o", default="fractal.png", help="Output image path")
    render_parser.add_argument("--dpi", type=int, default=150, help="Image DPI")
    render_parser.set_defaults(func=cmd_render)

    animate_parser = subparsers.add_parser("animate", help="Render a growth animation as a GIF")
    _add_common_arguments(animate_parser)
    animate_parser.add_argument("--output", "-o", default="fractal.gif", help="Output GIF path")
    animate_parser.add_argument("--fps", type=int, default=1, help="Frames per second")
    animate_parser.set_defaults(func=cmd_animate)

    info_parser = subparsers.add_parser("info", help="Print details about a preset's rules and size")
    _add_common_arguments(info_parser)
    info_parser.set_defaults(func=cmd_info)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "list" and not args.preset and not args.custom:
        parser.error("a preset name or --custom file is required (see 'fractal-garden list')")

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
