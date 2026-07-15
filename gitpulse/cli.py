"""CLI entry point for GitPulse."""

import argparse
import sys
import os

from .analyzer import analyze
from .dashboard import render


def main():
    parser = argparse.ArgumentParser(
        prog="gitpulse",
        description="Repository Vital Signs Dashboard",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=2000,
        metavar="N",
        help="Maximum commits to analyse (default: 2000)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colour output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="GitPulse 1.0.0",
    )
    args = parser.parse_args()

    if args.no_color:
        # Strip ANSI by monkey-patching the module
        import gitpulse.charts as ch
        for attr in [a for a in dir(ch) if a.isupper()]:
            val = getattr(ch, attr)
            if isinstance(val, str) and "\033" in val:
                setattr(ch, attr, "")

    path = os.path.abspath(args.path)
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    print("  Analysing repository…", end="\r", flush=True)
    stats = analyze(path, max_commits=args.max_commits)
    print(" " * 40, end="\r")  # clear the "Analysing…" line
    print(render(stats))


if __name__ == "__main__":
    main()
