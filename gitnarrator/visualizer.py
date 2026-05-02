"""Rich terminal UI for GitNarrator — ASCII timelines, heatmaps, tables."""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime

from rich.align import Align
from rich.bar import Bar
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .git_analyzer import RepoStats

console = Console()

BANNER = r"""
  ██████╗ ██╗████████╗███╗   ██╗ █████╗ ██████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗
 ██╔════╝ ██║╚══██╔══╝████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
 ██║  ███╗██║   ██║   ██╔██╗ ██║███████║██████╔╝██████╔╝███████║   ██║   ██║   ██║██████╔╝
 ██║   ██║██║   ██║   ██║╚██╗██║██╔══██║██╔══██╗██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
 ╚██████╔╝██║   ██║   ██║ ╚████║██║  ██║██║  ██║██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
  ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""

COLORS = ["bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta"]


def print_banner():
    console.print(Text(BANNER, style="bold bright_cyan"), justify="center")
    console.print(
        Align.center(Text("  AI-Powered Repository Storyteller  ", style="bold white on dark_blue")),
    )
    console.print()


def print_stats_overview(stats: RepoStats):
    console.print(Rule(f"[bold cyan] {stats.name} — Repository Overview [/bold cyan]"))
    console.print()

    duration = (stats.last_commit - stats.first_commit).days
    years = duration / 365

    grid = Table.grid(expand=True, padding=(0, 4))
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")

    def stat_panel(label: str, value: str, color: str) -> Panel:
        return Panel(
            Align.center(Text(value, style=f"bold {color}") + Text(f"\n{label}", style="dim")),
            border_style=color,
            padding=(0, 2),
        )

    grid.add_row(
        stat_panel("Total Commits", str(stats.total_commits), "bright_cyan"),
        stat_panel("Contributors", str(len(stats.authors)), "bright_green"),
        stat_panel("Days Active", str(duration), "bright_yellow"),
        stat_panel("Files Touched", str(len(stats.file_heatmap)), "bright_magenta"),
    )
    console.print(grid)
    console.print()


def print_contributor_chart(stats: RepoStats):
    console.print(Rule("[bold green] Contributors [/bold green]"))
    console.print()

    sorted_authors = sorted(stats.authors.items(), key=lambda x: x[1], reverse=True)[:10]
    total = sum(n for _, n in sorted_authors)

    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    table.add_column("Author", style="cyan", min_width=20)
    table.add_column("Commits", justify="right", style="bright_white", min_width=8)
    table.add_column("Share", min_width=40)
    table.add_column("%", justify="right", style="dim")

    for i, (author, count) in enumerate(sorted_authors):
        pct = count / total
        bar_width = max(1, int(pct * 40))
        color = COLORS[i % len(COLORS)]
        bar = Text("█" * bar_width, style=color)
        table.add_row(author, str(count), bar, f"{pct:.0%}")

    console.print(table)
    console.print()


def print_language_breakdown(stats: RepoStats):
    console.print(Rule("[bold yellow] Language Breakdown [/bold yellow]"))
    console.print()

    sorted_langs = sorted(stats.primary_languages.items(), key=lambda x: x[1], reverse=True)[:10]
    total = sum(n for _, n in sorted_langs)

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Ext", style="bold yellow", min_width=12)
    table.add_column("Bar", min_width=30)
    table.add_column("Files", justify="right", style="dim")

    for i, (ext, count) in enumerate(sorted_langs):
        pct = count / total
        bar_width = max(1, int(pct * 30))
        color = COLORS[i % len(COLORS)]
        bar = Text("▓" * bar_width + "░" * (30 - bar_width), style=color)
        table.add_row(ext or "(none)", bar, str(count))

    console.print(table)
    console.print()


def print_activity_heatmap(stats: RepoStats):
    """Print a simple ASCII commit-frequency heatmap by week."""
    console.print(Rule("[bold magenta] Commit Activity Timeline [/bold magenta]"))
    console.print()

    if not stats.weekly_activity:
        return

    weeks = sorted(stats.weekly_activity.keys())
    max_val = max(stats.weekly_activity.values())

    # Group into rows of 26 weeks (6 months)
    chunk = 26
    blocks = " ░▒▓█"

    for start in range(0, len(weeks), chunk):
        row_weeks = weeks[start:start + chunk]
        line = Text()
        for w in row_weeks:
            val = stats.weekly_activity.get(w, 0)
            intensity = int((val / max_val) * (len(blocks) - 1)) if max_val else 0
            char = blocks[intensity]
            if intensity == 0:
                line.append(char, style="dim")
            elif intensity < 2:
                line.append(char, style="green")
            elif intensity < 4:
                line.append(char, style="bright_green")
            else:
                line.append(char, style="bold bright_green")

        label = row_weeks[0].replace("-W", " W")
        console.print(f"  {label:12s} ", end="")
        console.print(line)

    console.print()
    console.print(f"  Legend:  [dim]░[/dim] low  [green]▒[/green] medium  [bright_green]▓[/bright_green] high  [bold bright_green]█[/bold bright_green] peak")
    console.print()


def print_hot_files(stats: RepoStats):
    console.print(Rule("[bold red] Most-Changed Files [/bold red]"))
    console.print()

    top = sorted(stats.file_heatmap.items(), key=lambda x: x[1], reverse=True)[:12]
    max_val = top[0][1] if top else 1

    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    table.add_column("#", style="dim", width=3)
    table.add_column("File", style="cyan")
    table.add_column("Changes", justify="right", style="bright_white", width=8)
    table.add_column("Heat", min_width=20)

    for i, (filepath, count) in enumerate(top):
        pct = count / max_val
        heat_len = max(1, int(pct * 20))
        heat = Text("🔥" * min(3, heat_len) + "█" * max(0, heat_len - 3), style="bright_red")
        short = filepath if len(filepath) <= 45 else "…" + filepath[-44:]
        table.add_row(str(i + 1), short, str(count), heat)

    console.print(table)
    console.print()


def stream_narrative(story_iterator, title: str = "The Story"):
    console.print(Rule(f"[bold bright_yellow] {title} [/bold bright_yellow]"))
    console.print()
    for chunk in story_iterator:
        console.print(chunk, end="", highlight=False)
    console.print()
    console.print()


def print_chapter_cards(chapters: list[dict]):
    console.print(Rule("[bold cyan] Chapter Overview [/bold cyan]"))
    console.print()

    cards = []
    for ch in chapters:
        duration = ch["duration_days"]
        start = ch["start_date"].strftime("%b %Y")
        end = ch["end_date"].strftime("%b %Y")
        top_author = max(ch["authors"].items(), key=lambda x: x[1])[0] if ch["authors"] else "?"
        color = COLORS[(ch["number"] - 1) % len(COLORS)]

        text = (
            f"[bold {color}]Ch. {ch['number']}[/bold {color}]\n"
            f"[dim]{start} → {end}[/dim]\n"
            f"{ch['commit_count']} commits\n"
            f"[cyan]{top_author}[/cyan]\n"
            f"[green]+{ch['insertions']}[/green] [red]-{ch['deletions']}[/red]"
        )
        cards.append(Panel(text, border_style=color, width=22))

    console.print(Columns(cards))
    console.print()


def spinner(message: str):
    return Progress(SpinnerColumn(), TextColumn(message), transient=True)
