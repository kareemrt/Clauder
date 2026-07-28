"""
Chronicle CLI entry point.
"""

import sys
from pathlib import Path

import click
from rich.console import Console

from .analyzer import analyze
from .renderer import render_terminal, render_html


@click.command()
@click.argument("repo_path", default=".", metavar="[REPO]")
@click.option("--html", "output_html", is_flag=True, help="Generate an HTML report.")
@click.option("--out", "-o", default=None, help="Output path for HTML report (default: chronicle_report.html).")
@click.option("--no-color", is_flag=True, help="Disable color output.")
def main(repo_path: str, output_html: bool, out: str | None, no_color: bool) -> None:
    """Chronicle — Turn your git history into a beautiful story.

    Analyzes REPO (default: current directory) and renders a rich terminal dashboard.
    Pass --html to also generate a self-contained HTML report.
    """
    path = Path(repo_path).resolve()

    if not (path / ".git").exists() and not (path / ".git").is_file():
        # Try looking for a .git anywhere up the tree
        check = path
        found = False
        for _ in range(5):
            if (check / ".git").exists():
                path = check
                found = True
                break
            check = check.parent
        if not found:
            click.echo(f"Error: '{repo_path}' does not appear to be a git repository.", err=True)
            sys.exit(1)

    console = Console(no_color=no_color, force_terminal=not no_color)
    console.print(f"\n[dim]Analyzing [bold]{path}[/bold]...[/dim]\n")

    stats = analyze(str(path))
    render_terminal(stats, console)

    if output_html:
        report_path = out or "chronicle_report.html"
        html_content = render_html(stats)
        Path(report_path).write_text(html_content, encoding="utf-8")
        console.print(f"\n[bold green]HTML report saved:[/bold green] [cyan]{report_path}[/cyan]\n")


if __name__ == "__main__":
    main()
