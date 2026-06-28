"""Command-line interface for running and rendering the murmuration simulation."""

from __future__ import annotations

import argparse

from murmuration.simulation import FlockSimulation, SimulationConfig
from murmuration.visualize import render_gif, render_trajectories


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulate and render an emergent boid flock.")
    parser.add_argument("--boids", type=int, default=120, help="number of boid agents")
    parser.add_argument("--predators", type=int, default=2, help="number of predator agents")
    parser.add_argument("--steps", type=int, default=300, help="number of simulation steps to render")
    parser.add_argument("--width", type=float, default=100.0)
    parser.add_argument("--height", type=float, default=100.0)
    parser.add_argument("--seed", type=int, default=None, help="seed shared by the GIF and trajectory renders")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--gif", type=str, default="assets/flock.gif", help="output path for the animated GIF")
    parser.add_argument(
        "--trajectories", type=str, default="assets/trajectories.png", help="output path for the static trajectory plot"
    )
    parser.add_argument("--skip-gif", action="store_true")
    parser.add_argument("--skip-trajectories", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    config = SimulationConfig(
        width=args.width,
        height=args.height,
        num_boids=args.boids,
        num_predators=args.predators,
        seed=args.seed,
    )

    if not args.skip_gif:
        render_gif(FlockSimulation(config), args.steps, args.gif, fps=args.fps)
        print(f"wrote {args.gif}")

    if not args.skip_trajectories:
        render_trajectories(FlockSimulation(config), args.steps, args.trajectories)
        print(f"wrote {args.trajectories}")


if __name__ == "__main__":
    main()
