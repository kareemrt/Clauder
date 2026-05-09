"""Rich-powered terminal visualizations for git history."""

from __future__ import annotations

from collections import Counter

from rich.bar import Bar
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from .git_analyzer import RepoStats

BANNER = r"""
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|

       AI-Powered Git Storyteller
       Powered by Claude ✦ Anthropic
"""


def print_banner(console: Console) -> None:
    console.print(Text(BANNER, style="bold cyan"))


def print_repo_stats(stats: RepoStats, console: Console) -> None:
    """Print a rich stats table for the repository."""
    console.print(Rule(f"[bold yellow]  {stats.name}  [/bold yellow]"))
    console.print()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Total Commits", str(stats.total_commits))
    table.add_row(
        "Contributors",
        ", ".join(f"[bold]{n}[/bold] ({c})" for n, c in stats.contributors[:5]),
    )
    table.add_row("Lines Added", f"[green]+{stats.total_insertions:,}[/green]")
    table.add_row("Lines Removed", f"[red]-{stats.total_deletions:,}[/red]")
    table.add_row("Most Active Day", stats.most_active_day or "N/A")

    if stats.first_commit:
        table.add_row(
            "Born",
            f"{stats.first_commit.date.strftime('%b %d, %Y')} — {stats.first_commit.message[:50]}",
        )
    if stats.last_commit:
        table.add_row(
            "Latest",
            f"{stats.last_commit.date.strftime('%b %d, %Y')} — {stats.last_commit.message[:50]}",
        )

    console.print(Panel(table, title="[bold]Repository Profile[/bold]", border_style="cyan"))
    console.print()


def print_commit_timeline(stats: RepoStats, console: Console) -> None:
    """Print an ASCII bar chart of commits by month."""
    if not stats.commits_by_month:
        return

    console.print(Panel("[bold]Commit Timeline[/bold]", border_style="yellow"))
    max_val = max(stats.commits_by_month.values(), default=1)

    for month, count in list(stats.commits_by_month.items())[-18:]:
        bar_len = int((count / max_val) * 40)
        bar = "█" * bar_len
        label = f"{month}  "
        console.print(
            f"  [dim]{label}[/dim][cyan]{bar}[/cyan] [bold white]{count}[/bold white]"
        )
    console.print()


def print_contributor_chart(stats: RepoStats, console: Console) -> None:
    """Print a horizontal bar chart of top contributors."""
    if not stats.contributors:
        return

    console.print(Panel("[bold]Contributor Leaderboard[/bold]", border_style="magenta"))
    max_val = stats.contributors[0][1] if stats.contributors else 1
    colors = ["gold1", "silver", "tan", "cyan", "green", "blue", "magenta", "red"]

    for i, (name, count) in enumerate(stats.contributors[:8]):
        color = colors[i % len(colors)]
        bar_len = int((count / max_val) * 35)
        bar = "▓" * bar_len
        console.print(
            f"  [{color}]{name:<20}[/{color}] [{color}]{bar}[/{color}] "
            f"[bold]{count}[/bold] commits"
        )
    console.print()


def print_top_files(stats: RepoStats, console: Console) -> None:
    """Print most frequently changed files."""
    if not stats.top_files:
        return

    table = Table(title="Most-Touched Files", border_style="green", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("File", style="cyan")
    table.add_column("Changes", justify="right", style="bold yellow")

    for i, (filepath, count) in enumerate(stats.top_files[:8], 1):
        short = filepath if len(filepath) <= 55 else "..." + filepath[-52:]
        table.add_row(str(i), short, str(count))

    console.print(table)
    console.print()


def print_haiku(haiku: str, console: Console) -> None:
    console.print(
        Panel(
            Text(haiku, style="italic cyan", justify="center"),
            title="[bold yellow]Project Haiku[/bold yellow]",
            border_style="yellow",
            padding=(1, 4),
        )
    )
    console.print()


def print_tagline(tagline: str, console: Console) -> None:
    console.print(
        Panel(
            Text(f'"{tagline}"', style="bold white", justify="center"),
            title="[bold magenta]Project Tagline[/bold magenta]",
            border_style="magenta",
            padding=(0, 4),
        )
    )
    console.print()
