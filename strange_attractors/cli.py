"""Command-line interface for the Strange Attractors Explorer."""

from __future__ import annotations

import argparse
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .systems import SYSTEMS
from .integrator import integrate
from .render import render_attractor, save_fig, _add_glow, _segments_2d
from .divergence import plot_divergence
from .animate import make_rotation_gif


def cmd_list(args):
    for key, system in SYSTEMS.items():
        print(f"{key:12s}  {system.name:12s} {system.description}")


def cmd_render(args):
    system = SYSTEMS[args.system]
    traj = integrate(system, steps=args.steps, dt=args.dt)
    projection = tuple(args.projection) if args.projection else None
    fig, _ = render_attractor(traj, system, projection=projection, cmap=args.cmap)
    save_fig(fig, args.output)
    print(f"wrote {args.output}")


def cmd_gallery(args):
    keys = list(SYSTEMS.keys())
    cols = 3
    rows = (len(keys) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows), dpi=130, facecolor="black")
    axes = np.atleast_1d(axes).flatten()

    for ax, key in zip(axes, keys):
        system = SYSTEMS[key]
        traj = integrate(system)
        segments = _segments_2d(traj, system.projection)
        ax.set_facecolor("black")
        _add_glow(ax, segments, args.cmap, layers=3)
        i, j = "xyz".index(system.projection[0]), "xyz".index(system.projection[1])
        ax.set_xlim(traj[:, i].min(), traj[:, i].max())
        ax.set_ylim(traj[:, j].min(), traj[:, j].max())
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(system.name, color="white", fontfamily="monospace", fontsize=12)

    for ax in axes[len(keys):]:
        ax.axis("off")

    fig.tight_layout()
    save_fig(fig, args.output)
    print(f"wrote {args.output}")


def cmd_chaos(args):
    system = SYSTEMS[args.system]
    fig, _, lyap = plot_divergence(system, eps=args.eps, steps=args.steps)
    save_fig(fig, args.output)
    print(f"wrote {args.output}  (lambda ~ {lyap:.4f})")


def cmd_animate(args):
    system = SYSTEMS[args.system]
    traj = integrate(system, steps=args.steps, dt=args.dt)
    path = make_rotation_gif(traj, system, args.output, n_frames=args.frames, cmap=args.cmap)
    print(f"wrote {path}")


def build_parser():
    p = argparse.ArgumentParser(prog="strange-attractors", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("list", help="list available attractor systems")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("render", help="render a static glow-style image of one attractor")
    sp.add_argument("system", choices=SYSTEMS.keys())
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--steps", type=int, default=None)
    sp.add_argument("--dt", type=float, default=None)
    sp.add_argument("--projection", nargs=2, metavar=("AXIS1", "AXIS2"), default=None)
    sp.add_argument("--cmap", default="plasma")
    sp.set_defaults(func=cmd_render)

    sp = sub.add_parser("gallery", help="render a grid of every attractor")
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--cmap", default="plasma")
    sp.set_defaults(func=cmd_gallery)

    sp = sub.add_parser("chaos", help="plot exponential divergence of two nearby trajectories")
    sp.add_argument("system", choices=SYSTEMS.keys())
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--eps", type=float, default=1e-8)
    sp.add_argument("--steps", type=int, default=None)
    sp.set_defaults(func=cmd_chaos)

    sp = sub.add_parser("animate", help="render a rotating GIF of one attractor")
    sp.add_argument("system", choices=SYSTEMS.keys())
    sp.add_argument("-o", "--output", required=True)
    sp.add_argument("--steps", type=int, default=None)
    sp.add_argument("--dt", type=float, default=None)
    sp.add_argument("--frames", type=int, default=60)
    sp.add_argument("--cmap", default="plasma")
    sp.set_defaults(func=cmd_animate)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
