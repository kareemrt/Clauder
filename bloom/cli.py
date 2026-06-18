"""Command-line interface for running and rendering Bloom simulations."""

from __future__ import annotations

import argparse
import sys

from .creatures import PRESETS, list_presets
from .render import save_gif, save_png
from .world import World


def _build_world(preset_name: str, size: int, seed: int) -> World:
    preset = PRESETS[preset_name]
    world = World(
        size,
        size,
        radius=preset.radius,
        shells=preset.shells,
        mu=preset.mu,
        sigma=preset.sigma,
        dt=preset.dt,
        seed=seed,
    )
    if preset.seed_kind == "random":
        world.seed_random(density=preset.density, patch=int(size * 0.6))
    else:
        world.place(preset.pattern, size // 2, size // 2)
    return world


def cmd_list(_args: argparse.Namespace) -> None:
    for name in list_presets():
        print(f"{name}: {PRESETS[name].description}")


def cmd_run(args: argparse.Namespace) -> None:
    if args.preset not in PRESETS:
        sys.exit(f"unknown preset {args.preset!r}; choices: {', '.join(list_presets())}")

    world = _build_world(args.preset, args.size, args.seed)
    frames = [world.state.copy()]
    for step in range(args.steps):
        world.step()
        if step % args.stride == 0:
            frames.append(world.state.copy())

    save_gif(frames, args.out, scale=args.scale, fps=args.fps)
    print(f"wrote {len(frames)} frames to {args.out} (final mass={world.mass():.1f})")


def cmd_snapshot(args: argparse.Namespace) -> None:
    if args.preset not in PRESETS:
        sys.exit(f"unknown preset {args.preset!r}; choices: {', '.join(list_presets())}")

    world = _build_world(args.preset, args.size, args.seed)
    for _ in range(args.steps):
        world.step()

    save_png(world.state, args.out, scale=args.scale)
    print(f"wrote step {args.steps} to {args.out} (mass={world.mass():.1f})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bloom", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list available creature presets").set_defaults(func=cmd_list)

    run = sub.add_parser("run", help="simulate a preset and save an animated GIF")
    run.add_argument("--preset", default="mitosis", choices=list_presets())
    run.add_argument("--size", type=int, default=120, help="grid side length")
    run.add_argument("--steps", type=int, default=220, help="number of simulation steps")
    run.add_argument("--stride", type=int, default=2, help="steps between captured frames")
    run.add_argument("--scale", type=int, default=3, help="pixel scale factor for output")
    run.add_argument("--fps", type=int, default=20)
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--out", default="bloom.gif")
    run.set_defaults(func=cmd_run)

    snap = sub.add_parser("snapshot", help="simulate a preset and save a single PNG")
    snap.add_argument("--preset", default="mitosis", choices=list_presets())
    snap.add_argument("--size", type=int, default=120)
    snap.add_argument("--steps", type=int, default=150)
    snap.add_argument("--scale", type=int, default=3)
    snap.add_argument("--seed", type=int, default=0)
    snap.add_argument("--out", default="bloom.png")
    snap.set_defaults(func=cmd_snapshot)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
