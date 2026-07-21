"""CLI entry point for GitPulse."""

from __future__ import annotations

import sys

import click
from rich.console import Console

from .analyzer import analyze
from .reporter import generate_html_report
from .visualizer import render_all

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="gitpulse")
def main() -> None:
    """GitPulse — Terminal Git Analytics Dashboard.

    Analyze any git repository and visualize its history as beautiful
    terminal output or a standalone HTML report.
    """


@main.command()
@click.argument("repo", default=".", type=click.Path(exists=True))
@click.option("--max-commits", "-n", default=5000, show_default=True,
              help="Maximum number of commits to analyze.")
@click.option("--report", "-r", is_flag=True, help="Also generate an HTML report.")
@click.option("--output", "-o", default="gitpulse-report.html", show_default=True,
              help="HTML report output path (used with --report).")
def analyze_cmd(repo: str, max_commits: int, report: bool, output: str) -> None:
    """Analyze REPO and display rich terminal statistics.

    REPO defaults to the current directory.

    Examples:

        gitpulse analyze

        gitpulse analyze ~/projects/myrepo --report

        gitpulse analyze . -n 1000 --report -o report.html
    """
    with console.status("[bold cyan]Analyzing repository…[/bold cyan]", spinner="dots"):
        try:
            stats = analyze(repo, max_commits=max_commits)
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            sys.exit(1)

    render_all(stats)

    if report:
        with console.status("[bold cyan]Generating HTML report…[/bold cyan]", spinner="dots"):
            path = generate_html_report(stats, output)
        console.print(f"\n[bold green]✓[/bold green] Report saved to [bold cyan]{path}[/bold cyan]")


@main.command()
@click.argument("repo", default=".", type=click.Path(exists=True))
@click.option("--output", "-o", default="gitpulse-report.html", show_default=True,
              help="Output path for the HTML report.")
@click.option("--max-commits", "-n", default=5000, show_default=True,
              help="Maximum number of commits to analyze.")
def report(repo: str, output: str, max_commits: int) -> None:
    """Generate an HTML report for REPO without terminal output.

    REPO defaults to the current directory.

    Examples:

        gitpulse report

        gitpulse report ~/projects/myrepo -o myreport.html
    """
    with console.status("[bold cyan]Analyzing repository…[/bold cyan]", spinner="dots"):
        try:
            stats = analyze(repo, max_commits=max_commits)
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            sys.exit(1)

    with console.status("[bold cyan]Generating HTML report…[/bold cyan]", spinner="dots"):
        path = generate_html_report(stats, output)

    console.print(f"[bold green]✓[/bold green] Report saved to [bold cyan]{path}[/bold cyan]")


# Register 'analyze' as the default command alias
main.add_command(analyze_cmd, name="analyze")

if __name__ == "__main__":
    main()
