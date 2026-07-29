"""GitPulse CLI entry point."""

import sys
import os
import argparse

from rich.console import Console

from . import analyzer
from . import visualizer

console = Console()


def run(repo_path: str = ".", sections: set[str] | None = None) -> None:
    # Resolve and validate
    repo_path = os.path.abspath(repo_path)
    try:
        repo_root = analyzer.validate_repo(repo_path)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    all_sections = sections is None

    with console.status("[bold bright_yellow]Analyzing repository…[/bold bright_yellow]", spinner="dots"):
        repo_name = analyzer.get_repo_name(repo_root)
        stats = analyzer.get_basic_stats(repo_root)
        contributors = analyzer.get_contributor_stats(repo_root)
        heatmap = analyzer.get_commit_heatmap(repo_root)
        hourly = analyzer.get_hourly_distribution(repo_root)
        weekday = analyzer.get_weekday_distribution(repo_root)
        hotspots = analyzer.get_file_hotspots(repo_root)
        keywords = analyzer.get_commit_keywords(repo_root)
        timeline = analyzer.get_growth_timeline(repo_root)
        langs = analyzer.get_language_breakdown(repo_root)

    visualizer.print_header(repo_name, stats)
    visualizer.print_summary_cards(stats)

    if all_sections or "heatmap" in sections:
        visualizer.print_heatmap(heatmap)

    if all_sections or "contributors" in sections:
        visualizer.print_contributors(contributors)

    if all_sections or "hours" in sections:
        visualizer.print_hourly_chart(hourly)

    if all_sections or "weekdays" in sections:
        visualizer.print_weekday_chart(weekday)

    if all_sections or "hotspots" in sections:
        visualizer.print_file_hotspots(hotspots)

    if all_sections or "keywords" in sections:
        visualizer.print_keywords(keywords)

    if all_sections or "timeline" in sections:
        visualizer.print_growth_timeline(timeline)

    if all_sections or "langs" in sections:
        visualizer.print_language_breakdown(langs)

    visualizer.print_footer()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gitpulse",
        description="⚡ GitPulse — Terminal Git Repository Analytics Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sections:  heatmap  contributors  hours  weekdays  hotspots  keywords  timeline  langs

Examples:
  gitpulse                          # analyze current directory
  gitpulse /path/to/repo            # analyze a specific repo
  gitpulse . --only heatmap hours   # show only selected sections
        """,
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="SECTION",
        help="Show only these sections",
    )

    args = parser.parse_args()
    sections = set(args.only) if args.only else None
    run(args.repo, sections)


if __name__ == "__main__":
    main()
