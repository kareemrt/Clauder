"""
cosmos — Real-time solar system visualizer

Usage:
  python -m cosmos [options]

Options:
  --static          Print a single frame and exit (default)
  --animate         Run animated time-lapse in the terminal
  --fps N           Frames per second [default: 12]
  --speed N         Time scale — days per second of wall time [default: 30]
  --view N          Radius in AU visible on screen [default: 32]
  --inner           Zoom to inner solar system (view: 2 AU)
  --date YYYY-MM-DD Start from this date instead of now
  --svg [PATH]      Export an SVG snapshot (default: cosmos.svg)
  --help, -h        Show this help
"""

import sys
import argparse
from datetime import datetime, timezone

from src.renderer import full_render, CANVAS_W, CANVAS_H, VIEW_AU, INNER_AU
from src.exporter import export_svg
from src.animate import run_animation


def parse_args():
    p = argparse.ArgumentParser(
        prog="cosmos",
        description="Real-time solar system visualizer using Keplerian orbital mechanics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--static",   action="store_true", help="Print a static frame and exit")
    p.add_argument("--animate",  action="store_true", help="Run animation loop")
    p.add_argument("--fps",      type=float, default=12, metavar="N")
    p.add_argument("--speed",    type=float, default=30, metavar="N",
                   help="Days per second of wall time (animation)")
    p.add_argument("--view",     type=float, default=VIEW_AU, metavar="N")
    p.add_argument("--inner",    action="store_true", help="Zoom to inner planets")
    p.add_argument("--date",     type=str, default=None, metavar="YYYY-MM-DD")
    p.add_argument("--svg",      nargs="?", const="cosmos.svg", metavar="PATH",
                   help="Export SVG snapshot")
    return p.parse_args()


def main():
    args = parse_args()

    dt: datetime | None = None
    if args.date:
        dt = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    view = INNER_AU if args.inner else args.view

    if args.svg is not None:
        path = export_svg(dt=dt, path=args.svg)
        print(f"  \033[1;92m✓ SVG exported → {path}\033[0m")
        return

    if args.animate:
        run_animation(
            fps=args.fps,
            time_scale=args.speed * 86400,
            start_dt=dt,
            view_au=view,
        )
        return

    # Default: static frame
    frame = full_render(dt=dt, view_au=view)
    print(frame)


if __name__ == "__main__":
    main()
