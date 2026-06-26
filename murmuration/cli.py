"""Command-line interface for murmuration."""

from __future__ import annotations

import argparse
import sys

from .ascii_render import run_live
from .flock import Flock, FlockConfig
from .svg_render import render_snapshot, render_trail


def _build_flock(args: argparse.Namespace) -> Flock:
    config = FlockConfig(width=args.width, height=args.height)
    return Flock(n_boids=args.boids, n_predators=args.predators, config=config, seed=args.seed)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--boids", type=int, default=80, help="number of prey boids")
    parser.add_argument("--predators", type=int, default=0, help="number of predator boids")
    parser.add_argument("--width", type=float, default=120.0, help="world width")
    parser.add_argument("--height", type=float, default=60.0, help="world height")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="murmuration", description="A from-scratch boids flocking simulation.")
    sub = parser.add_subparsers(dest="command", required=True)

    live = sub.add_parser("live", help="watch a live ASCII animation in the terminal")
    _add_common_args(live)
    live.add_argument("--frames", type=int, default=300)
    live.add_argument("--cols", type=int, default=80)
    live.add_argument("--rows", type=int, default=30)
    live.add_argument("--fps", type=float, default=15.0)

    snapshot = sub.add_parser("snapshot", help="render a single SVG frame after N steps")
    _add_common_args(snapshot)
    snapshot.add_argument("--steps", type=int, default=200)
    snapshot.add_argument("--scale", type=float, default=8.0)
    snapshot.add_argument("--out", required=True, help="output .svg path")

    trail = sub.add_parser("trail", help="render an SVG of fading motion trails over N steps")
    _add_common_args(trail)
    trail.add_argument("--steps", type=int, default=400)
    trail.add_argument("--scale", type=float, default=8.0)
    trail.add_argument("--sample-every", type=int, default=2)
    trail.add_argument("--out", required=True, help="output .svg path")

    args = parser.parse_args(argv)
    flock = _build_flock(args)

    if args.command == "live":
        run_live(flock, frames=args.frames, cols=args.cols, rows=args.rows, fps=args.fps)
        return 0

    if args.command == "snapshot":
        for _ in range(args.steps):
            flock.step()
        svg = render_snapshot(flock, scale=args.scale)
        with open(args.out, "w") as f:
            f.write(svg)
        print(f"wrote {args.out}")
        return 0

    if args.command == "trail":
        svg = render_trail(flock, steps=args.steps, scale=args.scale, sample_every=args.sample_every)
        with open(args.out, "w") as f:
            f.write(svg)
        print(f"wrote {args.out}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
