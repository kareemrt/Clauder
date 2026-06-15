"""Command-line interface for Primordia.

Examples
--------
    python -m primordia list
    python -m primordia run chase --frames 200 --output chase.gif
    python -m primordia run cells --snapshot cells.png --steps 500
"""

from __future__ import annotations

import argparse
import sys

from primordia.presets import PRESETS, get_preset
from primordia.render import save_animation, save_snapshot
from primordia.simulation import ParticleLife


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="primordia", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available presets")

    run_parser = subparsers.add_parser("run", help="Run a simulation")
    run_parser.add_argument("preset", choices=sorted(PRESETS), help="Preset name")
    run_parser.add_argument("--seed", type=int, default=None, help="Override the random seed")
    run_parser.add_argument(
        "--output", default=None, help="Path to write an animated GIF (e.g. out.gif)"
    )
    run_parser.add_argument(
        "--snapshot", default=None, help="Path to write a single PNG snapshot instead"
    )
    run_parser.add_argument(
        "--frames", type=int, default=200, help="Number of frames in the GIF (default: 200)"
    )
    run_parser.add_argument(
        "--steps-per-frame", type=int, default=2, help="Simulation steps per GIF frame (default: 2)"
    )
    run_parser.add_argument(
        "--warmup", type=int, default=100, help="Steps to run before recording (default: 100)"
    )
    run_parser.add_argument(
        "--steps", type=int, default=300, help="Steps to run before a --snapshot (default: 300)"
    )
    run_parser.add_argument("--fps", type=int, default=30, help="GIF frames per second (default: 30)")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        for name, builder in sorted(PRESETS.items()):
            doc = (builder.__doc__ or "").strip().splitlines()[0]
            print(f"{name:12s} {doc}")
        return 0

    if args.command == "run":
        config = get_preset(args.preset, seed=args.seed)
        sim = ParticleLife(config)

        if args.snapshot:
            sim.run(args.steps)
            save_snapshot(sim, args.snapshot)
            print(f"Wrote snapshot after {args.steps} steps to {args.snapshot}")
            return 0

        output = args.output or f"{args.preset}.gif"
        save_animation(
            sim,
            output,
            frames=args.frames,
            steps_per_frame=args.steps_per_frame,
            fps=args.fps,
            warmup_steps=args.warmup,
        )
        print(f"Wrote {args.frames}-frame animation to {output}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
