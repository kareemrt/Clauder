"""Command-line entry point for running and exporting boid simulations."""
from __future__ import annotations

import argparse

from boids.flock import Flock
from boids.render import render_gif, render_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vectorized boids flocking simulation")
    parser.add_argument("--boids", type=int, default=150, help="number of boids")
    parser.add_argument("--predators", type=int, default=2, help="number of predators")
    parser.add_argument("--width", type=float, default=640)
    parser.add_argument("--height", type=float, default=640)
    parser.add_argument("--frames", type=int, default=240, help="frames to simulate/export")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--gif", type=str, default=None, help="output path for an animated GIF")
    parser.add_argument("--png", type=str, default=None, help="output path for a single PNG snapshot")
    parser.add_argument(
        "--warmup", type=int, default=0, help="steps to simulate before taking a PNG snapshot"
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    flock = Flock(
        n_boids=args.boids,
        width=args.width,
        height=args.height,
        n_predators=args.predators,
        seed=args.seed,
    )

    if args.gif:
        render_gif(flock, args.gif, frames=args.frames, fps=args.fps)
        print(f"wrote {args.gif}")

    if args.png:
        render_snapshot(flock, args.png, warmup_steps=args.warmup)
        print(f"wrote {args.png}")

    if not args.gif and not args.png:
        print("nothing to do: pass --gif and/or --png to export a visualization")


if __name__ == "__main__":
    main()
