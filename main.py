#!/usr/bin/env python3
"""
Clauder — Git Time Machine
Usage:
  python main.py [REPO_PATH] [--html [OUTPUT.html]] [--weeks N] [--no-timeline]
"""

import argparse
import os
import sys

from clauder.analyzer import (
    get_author_stats,
    get_commit_date_map,
    get_commit_heatmap_by_hour,
    get_commits,
    get_file_hotspots,
    get_repo_info,
    get_weekly_velocity,
)
from clauder.visualizer import (
    render_author_bars,
    render_banner,
    render_heatmap,
    render_hotspots,
    render_hour_heatmap,
    render_timeline,
    render_weekly_velocity,
)
from clauder.reporter import generate_html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clauder — Git Time Machine: beautiful terminal dashboard for any git repo."
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    parser.add_argument(
        "--html",
        nargs="?",
        const="clauder-report.html",
        metavar="FILE",
        help="Export an HTML report (default filename: clauder-report.html)",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=52,
        help="Number of weeks to show in the heatmap (default: 52)",
    )
    parser.add_argument(
        "--no-timeline",
        action="store_true",
        help="Skip the commit timeline in terminal output",
    )
    parser.add_argument(
        "--no-hours",
        action="store_true",
        help="Skip the hourly activity chart",
    )
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"Error: '{repo_path}' is not a git repository.", file=sys.stderr)
        sys.exit(1)

    print("  Analyzing repository…", end="\r", flush=True)

    repo_info   = get_repo_info(repo_path)
    commits     = get_commits(repo_path)
    author_stats = get_author_stats(commits)
    date_map    = get_commit_date_map(commits)
    hotspots    = get_file_hotspots(repo_path)
    hour_map    = get_commit_heatmap_by_hour(commits)
    weekly      = get_weekly_velocity(commits, weeks=args.weeks)

    print(" " * 40, end="\r")  # clear "Analyzing…" line

    render_banner(repo_info, commits, author_stats)
    render_heatmap(date_map, weeks=args.weeks)
    render_weekly_velocity(weekly)
    render_author_bars(author_stats, repo_info.get("total_commits", len(commits)))
    render_hotspots(hotspots)

    if not args.no_hours:
        render_hour_heatmap(hour_map)

    if not args.no_timeline:
        render_timeline(commits)

    if args.html:
        html = generate_html(repo_info, commits, author_stats, date_map, hotspots, hour_map)
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  HTML report saved → {args.html}")


if __name__ == "__main__":
    main()
