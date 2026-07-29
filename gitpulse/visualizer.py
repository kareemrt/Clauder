"""Rich-based visual rendering layer for GitPulse analytics."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.rule import Rule
from rich import box
from rich.align import Align
from rich.progress_bar import ProgressBar


console = Console()

# Heatmap intensity blocks (dark→light, rendered for terminal)
HEAT_BLOCKS = [" ", "░", "▒", "▓", "█"]
HEAT_COLORS = ["grey23", "dark_green", "green3", "green1", "bright_green"]

WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

TIME_LABELS = {
    range(5, 9): "🌅 Early Bird",
    range(9, 13): "☀️  Morning",
    range(13, 17): "🌤  Afternoon",
    range(17, 21): "🌆 Evening",
    range(21, 24): "🌙 Night Owl",
    range(0, 5): "🦉 Midnight",
}


def _time_label(hour: int) -> str:
    for r, label in TIME_LABELS.items():
        if hour in r:
            return label
    return "Unknown"


def print_header(repo_name: str, stats: dict) -> None:
    first = stats["first_date"].strftime("%b %d, %Y")
    last = stats["last_date"].strftime("%b %d, %Y")
    age = stats["age_days"]

    title = Text()
    title.append("⚡ GitPulse", style="bold bright_yellow")
    title.append(" — Repository Analytics Dashboard", style="bold white")

    subtitle = Text(justify="center")
    subtitle.append(f"  📁 {repo_name}", style="bold cyan")
    subtitle.append(f"   |   🗓 {first} → {last}", style="dim")
    subtitle.append(f"   |   ⏳ {age} days", style="dim")

    console.print()
    console.print(Panel(
        Align.center(f"[bold bright_yellow]⚡ GitPulse[/bold bright_yellow]  [bold white]— Repository Analytics Dashboard[/bold white]\n{subtitle}"),
        border_style="bright_yellow",
        padding=(0, 2),
    ))
    console.print()


def print_summary_cards(stats: dict) -> None:
    cards = [
        Panel(
            Align.center(
                f"[bold bright_cyan]{stats['total_commits']:,}[/bold bright_cyan]\n[dim]Total Commits[/dim]"
            ),
            border_style="cyan",
            width=22,
        ),
        Panel(
            Align.center(
                f"[bold bright_magenta]{stats['commits_per_day']}[/bold bright_magenta]\n[dim]Commits / Day[/dim]"
            ),
            border_style="magenta",
            width=22,
        ),
        Panel(
            Align.center(
                f"[bold bright_blue]{stats['branch_count']}[/bold bright_blue]\n[dim]Branches[/dim]"
            ),
            border_style="blue",
            width=22,
        ),
        Panel(
            Align.center(
                f"[bold bright_green]{stats['tag_count']}[/bold bright_green]\n[dim]Tags / Releases[/dim]"
            ),
            border_style="green",
            width=22,
        ),
    ]
    console.print(Columns(cards, equal=True, expand=False))
    console.print()


def print_heatmap(heatmap: dict[str, int], weeks: int = 52) -> None:
    console.print(Rule("[bold]📅  Commit Activity Heatmap  (last 52 weeks)[/bold]", style="bright_yellow"))
    console.print()

    today = datetime.now(tz=timezone.utc).date()
    # Align to the most recent Sunday
    start = today - timedelta(days=today.weekday() + 1 + (weeks - 1) * 7)

    # Build week × day grid
    grid: list[list[str]] = []
    month_labels: list[tuple[int, str]] = []  # (col_index, month_abbr)
    last_month = -1

    for week in range(weeks):
        col = []
        for day in range(7):
            d = start + timedelta(days=week * 7 + day)
            key = d.strftime("%Y-%m-%d")
            count = heatmap.get(key, 0)
            if count == 0:
                intensity = 0
            elif count == 1:
                intensity = 1
            elif count <= 3:
                intensity = 2
            elif count <= 6:
                intensity = 3
            else:
                intensity = 4
            col.append(HEAT_COLORS[intensity])

            if d.month != last_month and day == 0:
                month_labels.append((week, MONTH_NAMES[d.month - 1]))
                last_month = d.month
        grid.append(col)

    # Print month labels row
    month_row = Text()
    month_row.append("     ")  # day-label indent
    prev_col = 0
    for col_idx, month_name in month_labels:
        gap = col_idx - prev_col
        month_row.append(" " * (gap * 2))
        month_row.append(month_name[:3], style="dim")
        prev_col = col_idx + 2
    console.print(month_row)

    # Print rows (Mon=0 … Sun=6)
    for day in range(7):
        row = Text()
        label = WEEKDAY_NAMES[day] if day in (0, 2, 4) else "   "
        row.append(f"  {label}  ", style="dim")
        for week in range(weeks):
            color = grid[week][day]
            row.append("█ ", style=color)
        console.print(row)

    console.print()
    # Legend
    legend = Text("  Legend:  ", style="dim")
    for i, (block, color) in enumerate(zip(HEAT_BLOCKS, HEAT_COLORS)):
        labels = ["0", "1", "2-3", "4-6", "7+"]
        legend.append(f"█ {labels[i]}  ", style=color)
    console.print(legend)
    console.print()


def print_contributors(contributors: list[dict]) -> None:
    console.print(Rule("[bold]👥  Top Contributors[/bold]", style="bright_yellow"))
    console.print()

    table = Table(box=box.ROUNDED, border_style="dim", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("Author", min_width=20)
    table.add_column("Commits", justify="right", style="bold bright_cyan", width=10)
    table.add_column("Share", width=30)
    table.add_column("%", justify="right", style="bright_magenta", width=6)

    colors = ["gold1", "grey74", "dark_orange3"] + ["cyan"] * 20
    for i, c in enumerate(contributors):
        bar_len = int(c["pct"] / 100 * 25)
        bar = Text()
        bar.append("█" * bar_len, style=colors[min(i, len(colors) - 1)])
        bar.append("░" * (25 - bar_len), style="grey23")
        table.add_row(str(i + 1), c["name"], f"{c['commits']:,}", bar, f"{c['pct']}%")

    console.print(table)
    console.print()


def print_hourly_chart(dist: dict[int, int]) -> None:
    console.print(Rule("[bold]🕐  Commit Activity by Hour[/bold]", style="bright_yellow"))
    console.print()

    if not dist:
        console.print("[dim]No data.[/dim]")
        return

    max_val = max(dist.values()) or 1
    peak_hour = max(dist, key=lambda h: dist[h])

    rows: list[Text] = []
    for hour in range(24):
        count = dist.get(hour, 0)
        bar_len = int(count / max_val * 40)
        label = f"{hour:02d}:00"

        # color by time of day
        if 5 <= hour < 9:
            color = "gold1"
        elif 9 <= hour < 17:
            color = "bright_cyan"
        elif 17 <= hour < 21:
            color = "bright_magenta"
        else:
            color = "blue"

        row = Text()
        row.append(f"  {label} ", style="dim")
        row.append("█" * bar_len, style=color)
        row.append(f"  {count}", style="dim")
        if hour == peak_hour:
            row.append(" ← peak", style="bold bright_yellow")
        rows.append(row)

    for row in rows:
        console.print(row)

    peak_label = _time_label(peak_hour)
    console.print()
    console.print(f"  [dim]Peak coding time:[/dim] [bold bright_yellow]{peak_label}[/bold bright_yellow] (around [bold]{peak_hour:02d}:00[/bold])")
    console.print()


def print_weekday_chart(dist: dict[int, int]) -> None:
    console.print(Rule("[bold]📆  Activity by Day of Week[/bold]", style="bright_yellow"))
    console.print()

    if not dist:
        console.print("[dim]No data.[/dim]")
        return

    max_val = max(dist.values()) or 1
    for day in range(7):
        count = dist.get(day, 0)
        bar_len = int(count / max_val * 40)
        is_weekend = day >= 5
        color = "bright_magenta" if is_weekend else "bright_cyan"
        row = Text()
        row.append(f"  {WEEKDAY_NAMES[day]}  ", style="dim")
        row.append("█" * bar_len, style=color)
        row.append(f"  {count:,}", style="dim")
        console.print(row)

    console.print()


def print_file_hotspots(hotspots: list[dict]) -> None:
    console.print(Rule("[bold]🔥  File Hotspots (Most Changed)[/bold]", style="bright_yellow"))
    console.print()

    if not hotspots:
        console.print("[dim]No data.[/dim]")
        return

    max_changes = hotspots[0]["changes"] if hotspots else 1
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("#", width=3, justify="right", style="dim")
    table.add_column("File", min_width=35)
    table.add_column("Changes", justify="right", style="bold bright_red", width=10)
    table.add_column("Heat", width=22)

    heat_colors = ["bright_red", "red", "dark_orange3", "orange3", "yellow3",
                   "yellow4", "bright_green", "green3", "cyan3", "blue"]

    for i, h in enumerate(hotspots):
        bar_len = int(h["changes"] / max_changes * 18)
        color = heat_colors[min(i, len(heat_colors) - 1)]
        bar = Text()
        bar.append("█" * bar_len, style=color)
        bar.append("░" * (18 - bar_len), style="grey23")
        table.add_row(str(i + 1), h["file"], str(h["changes"]), bar)

    console.print(table)
    console.print()


def print_keywords(keywords: list[tuple[str, int]]) -> None:
    console.print(Rule("[bold]💬  Top Commit Keywords[/bold]", style="bright_yellow"))
    console.print()

    if not keywords:
        console.print("[dim]No data.[/dim]")
        return

    max_count = keywords[0][1] if keywords else 1
    cols_data: list[Text] = []
    for word, count in keywords:
        bar_len = int(count / max_count * 15)
        t = Text()
        t.append(f"  {word:<14}", style="bold bright_cyan")
        t.append("█" * bar_len, style="bright_yellow")
        t.append(f"  {count}", style="dim")
        cols_data.append(t)

    half = len(cols_data) // 2
    left = cols_data[:half]
    right = cols_data[half:]
    for l, r in zip(left, right):
        row = Text()
        row.append_text(l)
        row.append("     ")
        row.append_text(r)
        console.print(row)

    console.print()


def print_growth_timeline(timeline: list[dict]) -> None:
    console.print(Rule("[bold]📈  Monthly Commit Volume[/bold]", style="bright_yellow"))
    console.print()

    if not timeline:
        console.print("[dim]No data.[/dim]")
        return

    max_commits = max(m["commits"] for m in timeline) or 1
    for entry in timeline:
        bar_len = int(entry["commits"] / max_commits * 45)
        row = Text()
        row.append(f"  {entry['month']}  ", style="dim")
        row.append("█" * bar_len, style="bright_blue")
        row.append(f"  {entry['commits']}", style="dim")
        console.print(row)

    console.print()


def print_language_breakdown(langs: list[dict]) -> None:
    console.print(Rule("[bold]🧬  Language Breakdown (by file count)[/bold]", style="bright_yellow"))
    console.print()

    if not langs:
        console.print("[dim]No language data found.[/dim]\n")
        return

    lang_colors = [
        "bright_yellow", "bright_cyan", "bright_magenta", "bright_green",
        "bright_blue", "bright_red", "gold1", "orchid",
    ]

    for i, l in enumerate(langs):
        bar_len = int(l["pct"] / 100 * 35)
        color = lang_colors[i % len(lang_colors)]
        row = Text()
        row.append(f"  {l['lang']:<18}", style="bold " + color)
        row.append("█" * bar_len, style=color)
        row.append(f"  {l['files']} files  {l['pct']}%", style="dim")
        console.print(row)

    console.print()


def print_footer() -> None:
    console.print()
    console.print(Panel(
        Align.center(
            "[dim]Generated by [bold bright_yellow]GitPulse[/bold bright_yellow] — "
            "github.com/kareemrt/Clauder  |  [italic]Powered by Python + Rich[/italic][/dim]"
        ),
        border_style="dim",
        padding=(0, 2),
    ))
    console.print()
