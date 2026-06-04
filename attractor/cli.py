"""
attractor CLI — generate strange attractor art from the command line.

Usage examples:
  attractor render clifford --theme plasma --output clifford.png
  attractor render lorenz --theme galaxy --width 2560 --height 1440
  attractor ascii dejong --theme ember --width 100 --height 35
  attractor list
"""

import sys
import time
import argparse

from .attractors import ATTRACTORS, get_attractor, compute_points, list_attractors
from .themes import THEMES, list_themes
from .renderer import render_image, render_ascii


def _print_banner():
    banner = r"""
  ___  _   _  _____  ____    _    ____  _____ ___  ____
 / _ \| | | ||_   _||  _ \  / \  / ___||_   _/ _ \|  _ \
| | | | | | |  | |  | |_) |/ _ \| |      | || | | | |_) |
| |_| | |_| |  | |  |  _ </ ___ \ |___   | || |_| |  _ <
 \___/ \___/   |_|  |_| \_/_/   \_\____|  |_| \___/|_| \_\

  Strange Attractor Art Engine  •  Chaos. Beauty. Mathematics.
"""
    print(banner)


def cmd_list(args):
    _print_banner()
    print(f"{'Attractor':<14} {'Type':<12} {'Description'}")
    print("─" * 72)
    for key, adef in ATTRACTORS.items():
        kind = f"[{adef.kind}]"
        desc = adef.description[:48] + "…" if len(adef.description) > 49 else adef.description
        print(f"  {key:<12} {kind:<12} {desc}")
    print()
    print(f"{'Theme':<14} {'Background'}")
    print("─" * 32)
    for key, (bg, cmap) in THEMES.items():
        print(f"  {key:<12} {bg}  ({cmap})")
    print()


def cmd_render(args):
    attractor_def = get_attractor(args.attractor)

    iterations = args.iterations or attractor_def.default_iterations
    print(f"[attractor]  Computing {attractor_def.name} ({iterations:,} iterations)…")
    t0 = time.perf_counter()
    pts = compute_points(attractor_def, iterations)
    elapsed = time.perf_counter() - t0
    print(f"[attractor]  Done in {elapsed:.2f}s  ({len(pts):,} points, {pts.nbytes / 1e6:.1f} MB)")

    output = args.output or f"{args.attractor}_{args.theme}.png"
    print(f"[attractor]  Rendering → {output}  ({args.width}×{args.height}, theme={args.theme})")
    t1 = time.perf_counter()
    path = render_image(
        pts,
        output_path=output,
        width=args.width,
        height=args.height,
        theme=args.theme,
        gamma=args.gamma,
    )
    elapsed2 = time.perf_counter() - t1
    print(f"[attractor]  Saved  {path}  in {elapsed2:.2f}s")


def cmd_ascii(args):
    attractor_def = get_attractor(args.attractor)
    iterations = args.iterations or min(attractor_def.default_iterations, 500_000)
    print(f"Computing {attractor_def.name} ({iterations:,} pts)…\n")
    pts = compute_points(attractor_def, iterations)
    art = render_ascii(pts, width=args.width, height=args.height, theme=args.theme, color=not args.nocolor)
    print(art)
    print(f"\n  {attractor_def.name}  |  theme: {args.theme}")
    for eq in attractor_def.equations:
        print(f"    {eq}")
    print()


def cmd_info(args):
    adef = get_attractor(args.attractor)
    print(f"\n  {adef.name}")
    print(f"  {'─' * len(adef.name)}")
    print(f"  {adef.description}\n")
    print(f"  Type       : {adef.kind}")
    print(f"  Projection : {adef.projection[0].upper()} vs {adef.projection[1].upper()}")
    print(f"  Default iterations: {adef.default_iterations:,}\n")
    print("  Equations:")
    for eq in adef.equations:
        print(f"    {eq}")
    print("\n  Default Parameters:")
    for k, v in adef.default_params.items():
        print(f"    {k} = {v}")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="attractor",
        description="Strange Attractor Art Engine — generate beautiful chaos art.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    sub.add_parser("list", help="List available attractors and themes")

    # render
    rp = sub.add_parser("render", help="Render a high-resolution PNG image")
    rp.add_argument("attractor", choices=list_attractors(), metavar="ATTRACTOR")
    rp.add_argument("--theme",  "-t", default="plasma", choices=list_themes())
    rp.add_argument("--output", "-o", default=None, metavar="FILE")
    rp.add_argument("--width",  "-W", type=int, default=1920)
    rp.add_argument("--height", "-H", type=int, default=1080)
    rp.add_argument("--iterations", "-n", type=int, default=None)
    rp.add_argument("--gamma", "-g", type=float, default=0.5,
                    help="Gamma correction (< 1 brightens dim areas, default 0.5)")

    # ascii
    ap = sub.add_parser("ascii", help="Render ASCII art preview in the terminal")
    ap.add_argument("attractor", choices=list_attractors(), metavar="ATTRACTOR")
    ap.add_argument("--theme",  "-t", default="plasma", choices=list(THEMES))
    ap.add_argument("--width",  "-W", type=int, default=110)
    ap.add_argument("--height", "-H", type=int, default=36)
    ap.add_argument("--iterations", "-n", type=int, default=None)
    ap.add_argument("--nocolor", action="store_true", help="Disable ANSI colors")

    # info
    ip = sub.add_parser("info", help="Show detailed info about an attractor")
    ip.add_argument("attractor", choices=list_attractors(), metavar="ATTRACTOR")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "list":   cmd_list,
        "render": cmd_render,
        "ascii":  cmd_ascii,
        "info":   cmd_info,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
