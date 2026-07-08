"""CLI entry point for Pulsar."""

import argparse
import sys
import os
from pathlib import Path

from .analyzer import analyze
from .renderer import render
from . import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="pulsar",
        description="⚡ Pulsar — Git Repository Heartbeat Visualizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pulsar .                          analyse current directory
  pulsar /path/to/repo --days 180   analyse last 180 days
  pulsar . --report report.html     also generate an HTML report
  pulsar . --no-color               plain text output
        """,
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        metavar="REPO",
        help="path to the git repository (default: current directory)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        metavar="N",
        help="number of days to look back (default: 90)",
    )
    parser.add_argument(
        "--report",
        metavar="FILE",
        help="write a standalone HTML report to FILE",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI colour output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pulsar {__version__}",
    )

    args = parser.parse_args(argv)

    repo_path = Path(args.path).resolve()
    if not (repo_path / ".git").exists():
        # try parent dirs
        check = repo_path
        found = False
        for _ in range(5):
            if (check / ".git").exists():
                repo_path = check
                found = True
                break
            check = check.parent
        if not found:
            print(f"error: no git repository found at {args.path}", file=sys.stderr)
            sys.exit(1)

    if args.no_color:
        os.environ["NO_COLOR"] = "1"

    print(f"\n  Analysing {repo_path} …\n")
    try:
        stats = analyze(str(repo_path), days=args.days)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.no_color:
        # strip ANSI from output
        import re
        ansi_escape = re.compile(r"\033\[[0-9;]*m")
        output = ansi_escape.sub("", render(stats))
    else:
        output = render(stats)

    print(output)

    if args.report:
        from .report import generate
        generate(stats, args.report)
        print(f"  HTML report written to: {args.report}\n")


if __name__ == "__main__":
    main()
