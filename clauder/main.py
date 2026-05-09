"""Clauder CLI — AI-powered Git Storyteller."""

from __future__ import annotations

import os
import sys

import anthropic
import click
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.text import Text

from .git_analyzer import analyze_repo
from .report import save_report
from .storyteller import generate_commit_haiku, generate_one_line_tagline, stream_story
from .visualizer import (
    print_banner,
    print_commit_timeline,
    print_contributor_chart,
    print_haiku,
    print_repo_stats,
    print_tagline,
    print_top_files,
)

console = Console()


@click.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--max-commits", default=200, show_default=True, help="Max commits to analyze")
@click.option("--save", is_flag=True, help="Save a Markdown report to disk")
@click.option("--output", default="clauder_report.md", help="Output file path for --save")
@click.option("--no-story", is_flag=True, help="Skip AI story generation (stats only)")
def main(
    repo_path: str,
    max_commits: int,
    save: bool,
    output: str,
    no_story: bool,
) -> None:
    """Clauder — Turn your git history into a living story.

    Analyzes REPO_PATH (default: current directory) and generates
    beautiful stats, visualizations, and an AI-narrated developer diary.
    """
    print_banner(console)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not no_story:
        console.print(
            "[yellow]Warning:[/yellow] ANTHROPIC_API_KEY not set. "
            "Running in stats-only mode (use --no-story to suppress this warning)."
        )
        no_story = True

    # ── Analyze ──────────────────────────────────────────────────────────────
    with console.status("[cyan]Scanning git history...[/cyan]", spinner="dots"):
        try:
            stats = analyze_repo(repo_path, max_commits=max_commits)
        except Exception as exc:
            console.print(f"[red]Error:[/red] {exc}")
            sys.exit(1)

    print_repo_stats(stats, console)
    print_commit_timeline(stats, console)
    print_contributor_chart(stats, console)
    print_top_files(stats, console)

    story = ""
    haiku = ""
    tagline = ""

    if not no_story:
        client = anthropic.Anthropic(api_key=api_key)

        # ── Tagline ───────────────────────────────────────────────────────────
        with console.status("[magenta]Crafting tagline...[/magenta]", spinner="aesthetic"):
            tagline = generate_one_line_tagline(stats, client)
        print_tagline(tagline, console)

        # ── Haiku ─────────────────────────────────────────────────────────────
        with console.status("[yellow]Writing haiku...[/yellow]", spinner="aesthetic"):
            haiku = generate_commit_haiku(stats, client)
        print_haiku(haiku, console)

        # ── Story ─────────────────────────────────────────────────────────────
        console.print(Rule("[bold cyan]  The Developer Diary  [/bold cyan]"))
        console.print()

        full_story_parts: list[str] = []
        with Live(console=console, refresh_per_second=15) as live:
            for chunk in stream_story(stats, client):
                full_story_parts.append(chunk)
                story_so_far = "".join(full_story_parts)
                live.update(Markdown(story_so_far))

        story = "".join(full_story_parts)
        console.print()

    if save:
        path = save_report(stats, story, haiku, tagline, output_path=output)
        console.print(f"[green]Report saved to:[/green] {path}")

    console.print(Rule("[bold green] Clauder complete [/bold green]"))


if __name__ == "__main__":
    main()
