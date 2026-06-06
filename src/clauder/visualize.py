"""Rich terminal visualizations for git data."""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.rule import Rule
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .git_analysis import RepoStats

# Heatmap colors: 0 = empty, 1-4 = intensity levels
HEAT_COLORS = ["#1e1e2e", "#003820", "#006400", "#34a853", "#57ff6e"]
HEAT_CHAR = "█"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

LOGO = r"""
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|
"""

LANG_COLORS: dict[str, str] = {
    ".py":   "#3572A5",
    ".js":   "#f1e05a",
    ".ts":   "#2b7489",
    ".rs":   "#dea584",
    ".go":   "#00ADD8",
    ".java": "#b07219",
    ".rb":   "#701516",
    ".cpp":  "#f34b7d",
    ".c":    "#555555",
    ".cs":   "#178600",
    ".html": "#e34c26",
    ".css":  "#563d7c",
    ".sh":   "#89e051",
    ".md":   "#083fa1",
    ".json": "#292929",
}

BAR_CHARS = "▏▎▍▌▋▊▉█"


def _bar(value: float, max_val: float, width: int = 20, color: str = "green") -> Text:
    if max_val == 0:
        frac = 0.0
    else:
        frac = min(value / max_val, 1.0)
    filled = int(frac * width)
    partial_idx = int((frac * width - filled) * len(BAR_CHARS))
    bar_str = "█" * filled
    if filled < width and partial_idx > 0:
        bar_str += BAR_CHARS[partial_idx - 1]
    bar_str = bar_str.ljust(width, "░")
    return Text(bar_str, style=Style(color=color))


def render_header(console: Console, stats: RepoStats) -> None:
    logo_text = Text(LOGO, style="bold cyan")
    subtitle = Text("  Git Repository Intelligence Dashboard", style="dim cyan")
    console.print(Align.center(logo_text))
    console.print(Align.center(subtitle))
    console.print()


def render_overview(console: Console, stats: RepoStats) -> None:
    console.print(Rule("[bold cyan]Repository Overview[/bold cyan]", style="cyan"))
    console.print()

    # Compute active days — derive span from actual daily_counts keys, not commit objects
    active_days = len(stats.daily_counts)
    if stats.daily_counts:
        dates = sorted(stats.daily_counts.keys())
        from datetime import date as _date
        d0 = _date.fromisoformat(dates[0])
        d1 = _date.fromisoformat(dates[-1])
        span = (d1 - d0).days + 1
        pct = round(active_days / max(span, 1) * 100, 1)
        age_str = f"{span:,} days"
    else:
        pct = 0.0
        age_str = "—"

    top_author = max(stats.authors, key=lambda a: stats.authors[a]) if stats.authors else "—"
    top_count = stats.authors.get(top_author, 0)

    cards = [
        ("📦", "Repository", stats.name, "bold white"),
        ("🔖", "Total Commits", f"{stats.total_commits:,}", "bold green"),
        ("👥", "Contributors", str(len(stats.authors)), "bold yellow"),
        ("📅", "Active Days", f"{active_days} ({pct}%)", "bold blue"),
        ("⏱  ", "Age", age_str, "bold magenta"),
        ("🌿", "Branches", str(stats.branch_count), "bold cyan"),
        ("🏷  ", "Tags", str(stats.tag_count), "bold red"),
        ("🏆", "Top Author", f"{top_author} ({top_count:,})", "bold white"),
    ]

    table = Table(box=box.ROUNDED, padding=(0, 1), show_header=False,
                  border_style="dim cyan")
    table.add_column(style="dim", width=3)
    table.add_column(style="bold dim white", width=16)
    table.add_column(width=28)

    for icon, label, value, style in cards:
        table.add_row(icon, label, Text(value, style=style))

    console.print(Align.center(table))
    console.print()


def render_heatmap(console: Console, stats: RepoStats) -> None:
    """Render a 52-week GitHub-style contribution heatmap."""
    console.print(Rule("[bold cyan]Contribution Heatmap[/bold cyan]", style="cyan"))
    console.print()

    if not stats.daily_counts:
        console.print("  [dim]No commits to display.[/dim]")
        return

    today = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    # Start on the Monday 52 weeks ago
    start = today - timedelta(weeks=52)
    start -= timedelta(days=start.weekday())  # back to Monday

    # Bucket commits per day
    counts = stats.daily_counts  # str(YYYY-MM-DD) -> count

    max_count = max(counts.values()) if counts else 1

    def intensity(count: int) -> int:
        if count == 0:
            return 0
        q = count / max_count
        if q < 0.25:
            return 1
        elif q < 0.5:
            return 2
        elif q < 0.75:
            return 3
        return 4

    # Build grid: rows=7 (Mon-Sun), cols=53 weeks
    grid: list[list[int]] = [[0] * 53 for _ in range(7)]
    month_labels: dict[int, str] = {}

    cur = start
    for col in range(53):
        for row in range(7):
            day_str = cur.strftime("%Y-%m-%d")
            count = counts.get(day_str, 0)
            grid[row][col] = intensity(count)
            if row == 0 and cur.day <= 7:
                month_labels[col] = cur.strftime("%b")
            cur += timedelta(days=1)

    # Show only 26 most-recent weeks to fit standard 80-col terminal
    SHOW_WEEKS = 26
    offset = max(0, 53 - SHOW_WEEKS)

    # Month header (1 char per week column)
    month_line = Text("      ")
    prev_label = ""
    for col in range(offset, 53):
        label = month_labels.get(col, "")
        if label and label != prev_label:
            month_line.append(label[:1], style="dim white")
            prev_label = label
        else:
            month_line.append(" ", style="dim white")
    console.print(month_line)

    for row in range(7):
        day_abbr = DAYS[row][:2]
        day_label = Text(f"  {day_abbr}   ", style="dim white")
        row_text = Text()
        row_text.append_text(day_label)
        for col in range(offset, 53):
            lvl = grid[row][col]
            color = HEAT_COLORS[lvl]
            row_text.append(HEAT_CHAR, style=f"bold {color}")
        console.print(row_text)

    # Legend
    legend = Text("\n  Less  ")
    for lvl in range(5):
        legend.append(HEAT_CHAR, style=f"bold {HEAT_COLORS[lvl]}")
    legend.append("  More", style="dim white")
    console.print(legend)
    console.print()


def render_authors(console: Console, stats: RepoStats) -> None:
    """Render author leaderboard."""
    console.print(Rule("[bold cyan]Author Leaderboard[/bold cyan]", style="cyan"))
    console.print()

    if not stats.authors:
        console.print("  [dim]No author data.[/dim]")
        return

    table = Table(box=box.SIMPLE_HEAD, padding=(0, 1), border_style="dim cyan",
                  show_header=True, header_style="bold cyan")
    table.add_column("  #", style="dim", width=3, justify="right", no_wrap=True)
    table.add_column("Author", width=20, no_wrap=True)
    table.add_column("Commits", width=8, justify="right", no_wrap=True)
    table.add_column("Share", width=7, justify="right", no_wrap=True)
    table.add_column("Contribution", width=28, no_wrap=True)

    total = sum(stats.authors.values())
    palette = ["#57ff6e", "#34a853", "#006400", "#003820", "#001a0e"]

    for i, (author, count) in enumerate(
        sorted(stats.authors.items(), key=lambda x: x[1], reverse=True)[:15]
    ):
        pct = count / total * 100
        color = palette[min(i, len(palette) - 1)]
        rank_style = "bold yellow" if i < 3 else "dim white"
        bar = _bar(count, total * 0.6, width=24, color=color)
        short_author = author if len(author) <= 18 else author[:17] + "…"
        table.add_row(
            Text(f"{i+1}", style=rank_style),
            Text(short_author, style=f"bold {color}"),
            Text(f"{count:,}", style="bold white"),
            Text(f"{pct:.1f}%", style="dim white"),
            bar,
        )

    console.print(table)
    console.print()


def render_file_churn(console: Console, stats: RepoStats) -> None:
    """Render hottest files by churn."""
    console.print(Rule("[bold cyan]File Churn — Hottest Files[/bold cyan]", style="cyan"))
    console.print()

    if not stats.file_churn:
        console.print("  [dim]No file churn data.[/dim]")
        return

    top = sorted(stats.file_churn.items(), key=lambda x: x[1], reverse=True)[:20]
    max_churn = top[0][1]

    table = Table(box=box.SIMPLE_HEAD, padding=(0, 1), border_style="dim cyan",
                  show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("File", width=36)
    table.add_column("Changes", width=9, justify="right")
    table.add_column("Heat", width=28)

    for i, (path, count) in enumerate(top):
        heat_frac = count / max_churn
        if heat_frac > 0.75:
            color = "#ff4444"
        elif heat_frac > 0.5:
            color = "#ff8800"
        elif heat_frac > 0.25:
            color = "#ffcc00"
        else:
            color = "#34a853"
        bar = _bar(count, max_churn, width=24, color=color)
        short_path = path if len(path) <= 34 else "…" + path[-33:]
        table.add_row(
            str(i + 1),
            Text(short_path, style=f"bold {color}"),
            Text(str(count), style="bold white"),
            bar,
        )

    console.print(table)
    console.print()


def render_languages(console: Console, stats: RepoStats) -> None:
    """Render language breakdown."""
    console.print(Rule("[bold cyan]Language Activity[/bold cyan]", style="cyan"))
    console.print()

    if not stats.language_bytes:
        console.print("  [dim]No language data.[/dim]")
        return

    top = sorted(stats.language_bytes.items(), key=lambda x: x[1], reverse=True)[:12]
    total_lines = sum(v for _, v in top)
    max_lines = top[0][1]

    table = Table(box=box.SIMPLE_HEAD, padding=(0, 1), border_style="dim cyan",
                  show_header=True, header_style="bold cyan")
    table.add_column("Ext", width=8)
    table.add_column("Lines Δ", width=10, justify="right")
    table.add_column("Share", width=7, justify="right")
    table.add_column("Activity", width=36)

    for ext, lines in top:
        pct = lines / total_lines * 100
        color = LANG_COLORS.get(ext, "#aaaaaa")
        bar = _bar(lines, max_lines, width=32, color=color)
        table.add_row(
            Text(ext or "other", style=f"bold {color}"),
            Text(f"{lines:,}", style="bold white"),
            Text(f"{pct:.1f}%", style="dim white"),
            bar,
        )

    console.print(table)
    console.print()


def render_timeline(console: Console, stats: RepoStats) -> None:
    """Render recent commit activity as a sparkline timeline."""
    console.print(Rule("[bold cyan]Commit Activity — Last 30 Days[/bold cyan]", style="cyan"))
    console.print()

    if not stats.daily_counts:
        console.print("  [dim]No commit data.[/dim]")
        return

    today = datetime.now(tz=timezone.utc).date()
    days_30 = [(today - timedelta(days=29 - i)) for i in range(30)]
    counts = [stats.daily_counts.get(d.strftime("%Y-%m-%d"), 0) for d in days_30]
    max_c = max(counts) if counts else 1

    bars = " ▁▂▃▄▅▆▇█"
    spark = Text("  ")
    for i, c in enumerate(counts):
        frac = c / max_c if max_c else 0
        bar_idx = int(frac * (len(bars) - 1))
        char = bars[bar_idx]
        # Color gradient: low=dim, high=bright green
        if frac == 0:
            style = "dim #333333"
        elif frac < 0.3:
            style = "bold #003820"
        elif frac < 0.6:
            style = "bold #006400"
        elif frac < 0.85:
            style = "bold #34a853"
        else:
            style = "bold #57ff6e"
        spark.append(char, style=style)

    console.print(spark)
    console.print()

    # Dates on x-axis (every 5 days)
    date_line = Text("  ")
    for i, d in enumerate(days_30):
        if i % 5 == 0:
            label = d.strftime("%d %b")
            date_line.append(f"{label:<5}", style="dim white")
        elif (i - (i % 5)) % 5 != 0:
            pass

    console.print(date_line)
    console.print()


def render_pulse(console: Console, stats: RepoStats) -> None:
    """Render recent commits as a scrollable activity feed."""
    console.print(Rule("[bold cyan]Recent Commits — Activity Pulse[/bold cyan]", style="cyan"))
    console.print()

    if not stats.commits:
        console.print("  [dim]No commits.[/dim]")
        return

    table = Table(box=box.SIMPLE, padding=(0, 1), border_style="dim cyan",
                  show_header=True, header_style="bold cyan")
    table.add_column("When", width=9, style="dim white", no_wrap=True)
    table.add_column("Author", width=16, no_wrap=True)
    table.add_column("Message", width=50, no_wrap=True)

    now = datetime.now(tz=timezone.utc)
    palette = ["#57ff6e", "#34a853", "#006400", "#aaaaaa"]
    author_colors: dict[str, str] = {}
    color_idx = 0

    for commit in stats.commits[:20]:
        author = commit.author
        if author not in author_colors:
            author_colors[author] = palette[color_idx % len(palette)]
            color_idx += 1
        color = author_colors[author]

        delta = now - commit.timestamp
        if delta.days > 365:
            when = f"{delta.days // 365}y ago"
        elif delta.days > 30:
            when = f"{delta.days // 30}mo ago"
        elif delta.days > 0:
            when = f"{delta.days}d ago"
        elif delta.seconds > 3600:
            when = f"{delta.seconds // 3600}h ago"
        else:
            when = f"{delta.seconds // 60}m ago"

        subject = commit.subject
        if len(subject) > 48:
            subject = subject[:45] + "..."

        short_author = author if len(author) <= 14 else author[:13] + "…"
        table.add_row(when, Text(short_author, style=f"bold {color}"), subject)

    console.print(table)
    console.print()


def render_full_report(console: Console, stats: RepoStats) -> None:
    render_header(console, stats)
    render_overview(console, stats)
    render_timeline(console, stats)
    render_heatmap(console, stats)
    render_authors(console, stats)
    render_languages(console, stats)
    render_file_churn(console, stats)
    render_pulse(console, stats)
    console.print(Rule(style="dim cyan"))
    console.print(Align.center(Text(
        "Clauder — Git Intelligence Dashboard  ✦  github.com/kareemrt/clauder",
        style="dim cyan"
    )))
    console.print()
