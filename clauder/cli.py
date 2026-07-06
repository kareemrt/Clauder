"""Command-line interface for Clauder."""

import os
import sys
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from .github_client import GitHubClient
from .storyteller import Storyteller
from .renderer import StoryRenderer
from .report import generate_html_report


console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="clauder")
def cli():
    """Clauder — AI-powered GitHub Repository Storyteller.

    Analyzes any GitHub repository and generates a captivating documentary-style
    narrative using Claude AI.
    """


@cli.command()
@click.argument("repo", metavar="OWNER/REPO")
@click.option(
    "--output", "-o",
    default=None,
    metavar="FILE",
    help="Save HTML report to FILE (e.g. story.html)",
)
@click.option(
    "--github-token", envvar="GITHUB_TOKEN",
    default=None,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
@click.option(
    "--anthropic-key", envvar="ANTHROPIC_API_KEY",
    default=None,
    help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
)
@click.option(
    "--no-terminal", is_flag=True, default=False,
    help="Skip terminal rendering (useful when only --output is needed)",
)
def story(repo, output, github_token, anthropic_key, no_terminal):
    """Generate an AI-powered story for a GitHub repository.

    \b
    Examples:
      clauder story torvalds/linux
      clauder story kareemrt/clauder --output clauder_story.html
      clauder story microsoft/vscode -o vscode.html --no-terminal
    """
    if "/" not in repo:
        console.print("[red]Error:[/red] REPO must be in OWNER/REPO format (e.g. torvalds/linux)")
        sys.exit(1)

    owner, _, repo_name = repo.partition("/")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task1 = progress.add_task("[cyan]Fetching repository data from GitHub…", total=None)
        try:
            client = GitHubClient(token=github_token)
            data = client.fetch_repo_data(owner, repo_name)
        except Exception as e:
            console.print(f"[red]Failed to fetch repository:[/red] {e}")
            sys.exit(1)
        progress.update(task1, description="[green]✓ Repository data fetched")
        progress.stop_task(task1)

        task2 = progress.add_task("[cyan]Generating tagline with Claude…", total=None)
        try:
            storyteller = Storyteller(api_key=anthropic_key)
            tagline = storyteller.generate_tagline(data)
        except Exception as e:
            console.print(f"[red]Failed to generate tagline:[/red] {e}")
            tagline = data.stats.description or "A repository worth exploring."
        progress.update(task2, description="[green]✓ Tagline generated")
        progress.stop_task(task2)

        task3 = progress.add_task("[cyan]Writing repository story with Claude…", total=None)
        try:
            story_text = storyteller.generate_story(data)
        except Exception as e:
            console.print(f"[red]Failed to generate story:[/red] {e}")
            sys.exit(1)
        progress.update(task3, description="[green]✓ Story written")
        progress.stop_task(task3)

    if not no_terminal:
        renderer = StoryRenderer(console=console)
        renderer.render_full(data, story_text, tagline)

    if output:
        try:
            path = generate_html_report(data, story_text, tagline, output)
            console.print(
                Panel(
                    f"[green]✓[/green] HTML report saved to [bold cyan]{path}[/bold cyan]",
                    border_style="green dim",
                    padding=(0, 2),
                )
            )
        except Exception as e:
            console.print(f"[red]Failed to write HTML report:[/red] {e}")
            sys.exit(1)


@cli.command()
@click.argument("repo", metavar="OWNER/REPO")
@click.option("--github-token", envvar="GITHUB_TOKEN", default=None)
def stats(repo, github_token):
    """Show quick statistics for a repository without generating a story."""
    if "/" not in repo:
        console.print("[red]Error:[/red] REPO must be in OWNER/REPO format")
        sys.exit(1)

    owner, _, repo_name = repo.partition("/")

    with Progress(
        SpinnerColumn(), TextColumn("{task.description}"), console=console, transient=True
    ) as progress:
        t = progress.add_task("[cyan]Fetching…", total=None)
        try:
            client = GitHubClient(token=github_token)
            data = client.fetch_repo_data(owner, repo_name)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)
        progress.stop_task(t)

    from rich.table import Table
    from rich import box as rbox

    s = data.stats
    table = Table(title=f"[bold]{s.full_name}[/bold]", box=rbox.ROUNDED, border_style="bright_cyan dim")
    table.add_column("Metric", style="bright_cyan")
    table.add_column("Value", style="bold")
    table.add_row("Description", s.description or "—")
    table.add_row("Stars", f"{s.stars:,}")
    table.add_row("Forks", f"{s.forks:,}")
    table.add_row("Open Issues", str(s.open_issues))
    table.add_row("Language", s.language or "—")
    table.add_row("License", s.license or "—")
    table.add_row("Created", s.created_at[:10])
    table.add_row("Last Updated", s.updated_at[:10])
    if s.topics:
        table.add_row("Topics", ", ".join(s.topics[:8]))
    console.print()
    console.print(table)
    console.print()


def main():
    cli()


if __name__ == "__main__":
    main()
