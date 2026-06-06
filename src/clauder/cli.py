"""CLI entry point for Clauder."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

from .git_analysis import analyze
from .visualize import (
    render_authors,
    render_file_churn,
    render_full_report,
    render_heatmap,
    render_header,
    render_languages,
    render_overview,
    render_pulse,
    render_timeline,
)

console = Console()

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def _load(path: str):
    stats = analyze(path)
    if stats is None:
        console.print("[bold red]✗[/bold red] Not a git repository (or no git found).")
        sys.exit(1)
    if stats.total_commits == 0:
        console.print("[yellow]⚠[/yellow]  Repository has no commits yet.")
        sys.exit(0)
    return stats


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option("1.0.0", prog_name="clauder")
def cli():
    """
    Clauder — Git Repository Intelligence Dashboard.

    Analyse any git repo with beautiful terminal visualisations: heatmaps,
    author leaderboards, file churn, language breakdowns, and more.

    Run  clauder report  for the full dashboard, or use a sub-command.
    """


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def report(path: str):
    """Full dashboard — all panels in one view."""
    stats = _load(path)
    render_full_report(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def overview(path: str):
    """Repository overview card."""
    stats = _load(path)
    render_header(console, stats)
    render_overview(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def heatmap(path: str):
    """52-week GitHub-style contribution heatmap."""
    stats = _load(path)
    render_heatmap(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def authors(path: str):
    """Author leaderboard and contribution breakdown."""
    stats = _load(path)
    render_authors(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def churn(path: str):
    """File churn — the hottest (most-changed) files."""
    stats = _load(path)
    render_file_churn(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def langs(path: str):
    """Language activity breakdown by lines changed."""
    stats = _load(path)
    render_languages(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def pulse(path: str):
    """Recent commit activity feed."""
    stats = _load(path)
    render_pulse(console, stats)


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def timeline(path: str):
    """Sparkline commit activity for the last 30 days."""
    stats = _load(path)
    render_timeline(console, stats)


def main():
    cli()


if __name__ == "__main__":
    main()
