#!/usr/bin/env python3
"""GitNarrator CLI — AI-powered repository storyteller."""

import os
import sys
import time

import click

from gitnarrator.git_analyzer import analyze_repo
from gitnarrator.visualizer import (
    console,
    print_banner,
    print_chapter_cards,
    print_contributor_chart,
    print_hot_files,
    print_activity_heatmap,
    print_language_breakdown,
    print_stats_overview,
    stream_narrative,
    spinner,
)


@click.group()
def cli():
    """GitNarrator — Turn your git history into a compelling story."""


@cli.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--max-commits", "-n", default=500, help="Max commits to analyze (default: 500)")
@click.option("--html", "html_output", default=None, help="Export HTML report to this path")
@click.option("--no-story", is_flag=True, default=False, help="Skip AI narrative generation")
def analyze(repo_path: str, max_commits: int, html_output: str | None, no_story: bool):
    """Analyze a git repository and tell its story.

    REPO_PATH defaults to the current directory.
    """
    print_banner()

    # 1. Analyze the repository
    console.print(f"[dim]Analyzing repository at:[/dim] [cyan]{os.path.abspath(repo_path)}[/cyan]\n")
    with spinner("Parsing git history..."):
        try:
            stats = analyze_repo(repo_path, max_commits)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    # 2. Print stats sections
    print_stats_overview(stats)
    print_contributor_chart(stats)
    print_language_breakdown(stats)
    print_activity_heatmap(stats)
    print_hot_files(stats)
    print_chapter_cards(stats.chapters)

    # 3. Stream the AI narrative
    narrative_text = ""
    if not no_story:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            console.print("[yellow]Warning:[/yellow] ANTHROPIC_API_KEY not set — skipping AI narrative.")
        else:
            console.print("[dim]Generating AI narrative (streaming)...[/dim]\n")
            from gitnarrator.claude_narrator import stream_full_story
            chunks = []
            stream_narrative(
                (c for c in _tee(stream_full_story(stats), chunks)),
                title="AI Story",
            )
            narrative_text = "".join(chunks)

    # 4. Export HTML
    if html_output:
        from gitnarrator.html_export import export_html
        path = export_html(stats, narrative_text or "(no narrative generated)", html_output)
        console.print(f"[green]HTML report saved:[/green] [cyan]{path}[/cyan]\n")


@cli.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--max-commits", "-n", default=500)
def story(repo_path: str, max_commits: int):
    """Generate only the AI narrative for a repository."""
    print_banner()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]Error:[/red] ANTHROPIC_API_KEY environment variable is required.")
        sys.exit(1)

    console.print("[dim]Parsing git history...[/dim]")
    stats = analyze_repo(repo_path, max_commits)

    from gitnarrator.claude_narrator import stream_full_story
    stream_narrative(stream_full_story(stats), title=f"The Story of {stats.name}")


@cli.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--max-commits", "-n", default=500)
def stats(repo_path: str, max_commits: int):
    """Show statistics for a repository without AI generation."""
    print_banner()
    data = analyze_repo(repo_path, max_commits)
    print_stats_overview(data)
    print_contributor_chart(data)
    print_language_breakdown(data)
    print_activity_heatmap(data)
    print_hot_files(data)
    print_chapter_cards(data.chapters)


def _tee(iterator, accumulator: list):
    """Tee an iterator into a list while yielding each item."""
    for item in iterator:
        accumulator.append(item)
        yield item


if __name__ == "__main__":
    cli()
