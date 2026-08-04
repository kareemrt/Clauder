#!/usr/bin/env python3
"""
GitPulse — Beautiful git repository analytics.

Usage:
    python main.py [REPO_PATH] [--report] [--output FILE]

Arguments:
    REPO_PATH   Path to git repository (default: current directory)

Options:
    --report    Generate an HTML report in addition to terminal output
    --output    Output path for the HTML report (default: gitpulse_report.html)
    --no-color  Disable ANSI color output
    --help      Show this help message
"""
import sys
import os

# Allow running from outside the package directory
sys.path.insert(0, os.path.dirname(__file__))

from gitpulse.core import GitAnalyzer
from gitpulse.terminal import (
    print_banner,
    print_summary,
    print_commit_calendar,
    print_monthly_trend,
    print_leaderboard,
    print_hotspots,
    print_languages,
    print_recent_commits,
    print_footer,
)
from gitpulse.report import generate_html


def parse_args(argv):
    args = {
        "repo": ".",
        "report": False,
        "output": "gitpulse_report.html",
        "no_color": False,
    }
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        elif arg == "--report":
            args["report"] = True
        elif arg == "--no-color":
            args["no_color"] = True
        elif arg == "--output":
            i += 1
            if i < len(argv):
                args["output"] = argv[i]
        elif not arg.startswith("-"):
            args["repo"] = arg
        i += 1
    return args


def main():
    args = parse_args(sys.argv)

    if args["no_color"]:
        # Strip all ANSI codes from terminal output
        import gitpulse.terminal as term
        term.C = {k: "" for k in term.C}

    repo_path = args["repo"]
    if not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"\n  Analyzing repository at: {os.path.abspath(repo_path)} …\n")

    try:
        analyzer = GitAnalyzer(repo_path)
        data = analyzer.analyze()
    except Exception as e:
        print(f"Error analyzing repository: {e}", file=sys.stderr)
        sys.exit(1)

    info = data["repo_info"]

    print_banner(info["name"])
    print_summary(data)
    print_commit_calendar(data["calendar"])
    print_monthly_trend(data["monthly_commits"])
    print_leaderboard(data["author_stats"])
    print_hotspots(data["file_stats"])
    print_languages(data["language_breakdown"])
    print_recent_commits(data["commits"])
    print_footer()

    if args["report"]:
        out = generate_html(data, args["output"])
        print(f"\n  HTML report saved to: {out}\n")


if __name__ == "__main__":
    main()
