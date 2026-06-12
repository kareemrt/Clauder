"""Command line interface for Particle Life."""

import argparse
import sys

from .presets import PRESETS, get_preset
from .render import render_gif
from .simulation import ParticleSystem, SimulationConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="particle-life",
        description="Simulate and render a Particle Life world as an animated GIF.",
    )
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="cells",
        help="Rule set to simulate (default: %(default)s).",
    )
    parser.add_argument(
        "--particles", type=int, default=500, help="Number of particles (default: %(default)s)."
    )
    parser.add_argument(
        "--frames", type=int, default=150, help="Number of GIF frames (default: %(default)s)."
    )
    parser.add_argument(
        "--steps-per-frame",
        type=int,
        default=2,
        help="Simulation steps per rendered frame (default: %(default)s).",
    )
    parser.add_argument(
        "--size", type=int, default=360, help="Output image size in pixels (default: %(default)s)."
    )
    parser.add_argument(
        "--output", default="output.gif", help="Output GIF path (default: %(default)s)."
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument("--list-presets", action="store_true", help="List available presets and exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_presets:
        for preset in sorted(PRESETS.values(), key=lambda p: p.name):
            print(f"{preset.name}: {preset.description}")
        return 0

    preset = get_preset(args.preset)
    config = SimulationConfig(
        num_particles=args.particles,
        attraction_matrix=preset.matrix,
        r_max=preset.r_max,
        force_factor=preset.force_factor,
        friction=preset.friction,
    )
    system = ParticleSystem(config, seed=args.seed)

    print(f"Simulating preset '{preset.name}' ({args.particles} particles, {args.frames} frames)...")
    output_path = render_gif(
        system,
        preset.colors,
        args.output,
        frames=args.frames,
        steps_per_frame=args.steps_per_frame,
        size=args.size,
    )
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
