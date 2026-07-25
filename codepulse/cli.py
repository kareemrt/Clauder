"""CLI entry point for CodePulse."""

import sys
import os
import click
from rich.console import Console

from .git_data import get_repo_name, get_all_commits, get_file_extensions
from .metrics import build_metrics
from .terminal import print_dashboard
from .html_report import generate_html

console = Console()


@click.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--html", "html_output", default=None, metavar="FILE",
              help="Export an interactive HTML report to FILE.")
@click.option("--no-terminal", is_flag=True, default=False,
              help="Skip the terminal dashboard (use with --html).")
def main(repo_path: str, html_output: str | None, no_terminal: bool) -> None:
    """
    ⚡ CodePulse — Instant git repository analytics.

    Analyze REPO_PATH (defaults to current directory) and display
    a rich terminal dashboard of contributor stats, activity heatmaps,
    commit patterns, and hot files.
    """
    repo_path = os.path.abspath(repo_path)

    with console.status("[bold green]Collecting git history...[/]"):
        repo_name = get_repo_name(repo_path)
        commits = get_all_commits(repo_path)

    if not commits:
        console.print("[bold red]No commits found.[/] Is this a git repository?")
        sys.exit(1)

    with console.status("[bold green]Analyzing codebase...[/]"):
        language_lines = get_file_extensions(repo_path)

    with console.status("[bold green]Building metrics...[/]"):
        metrics = build_metrics(repo_name, commits, language_lines)

    if not no_terminal:
        print_dashboard(metrics)

    if html_output:
        with console.status(f"[bold green]Writing HTML report to {html_output}...[/]"):
            generate_html(metrics, html_output)
        console.print(f"[bold green]✓[/] HTML report saved to [bright_white]{html_output}[/]")
