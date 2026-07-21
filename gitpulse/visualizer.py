"""Terminal visualizations using Rich."""

from __future__ import annotations

from datetime import date, timedelta

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from .analyzer import RepoStats

console = Console()

_WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_CALENDAR_BLOCKS = [" ", "░", "▒", "▓", "█"]
_HOUR_LABELS = [f"{h:02d}:00" for h in range(24)]
_PALETTE = {
    "header": "bold cyan",
    "accent": "bold magenta",
    "good": "bold green",
    "warn": "bold yellow",
    "dim": "dim white",
    "number": "bold white",
}


def render_all(stats: RepoStats) -> None:
    """Render complete analysis to terminal."""
    _render_header(stats)
    _render_summary_cards(stats)
    _render_commit_calendar(stats)
    _render_contributors(stats)
    _render_time_heatmap(stats)
    _render_weekday_chart(stats)
    _render_file_hotspots(stats)
    _render_word_cloud(stats)
    _render_footer(stats)


def _render_header(stats: RepoStats) -> None:
    banner = Text()
    banner.append("  ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗\n", style="bold cyan")
    banner.append("  ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝\n", style="bold cyan")
    banner.append("  ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗  \n", style="bold blue")
    banner.append("  ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  \n", style="bold blue")
    banner.append("  ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗\n", style="bold magenta")
    banner.append("   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝\n", style="bold magenta")
    banner.append(f"\n  Terminal Git Analytics Dashboard  •  {stats.repo_name}\n", style="dim white")
    console.print(Panel(banner, border_style="bright_blue", padding=(0, 2)))


def _render_summary_cards(stats: RepoStats) -> None:
    console.print(Rule("[bold cyan]Repository Overview[/bold cyan]", style="bright_blue"))

    duration = f"{stats.age_days:,} days" if stats.age_days else "—"
    freq = f"{stats.commit_frequency:.2f}/day" if stats.commit_frequency else "—"
    first = stats.first_commit.strftime("%b %d %Y") if stats.first_commit else "—"
    last = stats.last_commit.strftime("%b %d %Y") if stats.last_commit else "—"

    cards = [
        _stat_card("Total Commits", f"{stats.total_commits:,}", "🔖", "bold green"),
        _stat_card("Contributors", f"{len(stats.contributors):,}", "👥", "bold cyan"),
        _stat_card("Active Days", f"{stats.active_days:,}", "📅", "bold yellow"),
        _stat_card("Branches", f"{stats.total_branches:,}", "🌿", "bold magenta"),
        _stat_card("Commit Freq", freq, "⚡", "bold red"),
        _stat_card("Repo Age", duration, "⏳", "bold blue"),
        _stat_card("First Commit", first, "🌱", "dim cyan"),
        _stat_card("Last Commit", last, "🔥", "dim magenta"),
        _stat_card("Longest Streak", f"{stats.longest_streak} days", "🏆", "bold gold1"),
    ]
    console.print(Columns(cards, equal=True, expand=True))


def _stat_card(label: str, value: str, icon: str, color: str) -> Panel:
    content = Text(justify="center")
    content.append(f"{icon}\n", style="bold")
    content.append(f"{value}\n", style=color)
    content.append(label, style="dim white")
    return Panel(content, border_style="bright_black", padding=(0, 1))


def _render_commit_calendar(stats: RepoStats) -> None:
    console.print()
    console.print(Rule("[bold cyan]Commit Activity Calendar  (last 52 weeks)[/bold cyan]", style="bright_blue"))

    today = date.today()
    start = today - timedelta(weeks=52)
    # Align to Monday
    start -= timedelta(days=start.weekday())

    max_count = max(stats.calendar_data.values(), default=1)

    # Build week columns (7 rows × 52 columns)
    weeks: list[list[tuple[str, str]]] = []
    current = start
    while current <= today:
        week_col: list[tuple[str, str]] = []
        for _ in range(7):
            day_str = current.isoformat()
            count = stats.calendar_data.get(day_str, 0)
            if count == 0:
                block, color = "·", "grey23"
            else:
                idx = min(4, int(count / max_count * 4) + 1)
                block = _CALENDAR_BLOCKS[idx]
                colors = ["green4", "green3", "bright_green", "bold bright_green"]
                color = colors[idx - 1]
            week_col.append((block, color))
            current += timedelta(days=1)
        weeks.append(week_col)

    # Month labels
    month_row = Text()
    month_row.append("     ")
    current = start
    prev_month = -1
    for week in weeks:
        col_start = current
        current += timedelta(weeks=1)
        if col_start.month != prev_month:
            label = col_start.strftime("%b")
            month_row.append(f"{label:<2} ", style="dim white")
            prev_month = col_start.month
        else:
            month_row.append("   ")
    console.print(month_row)

    # Weekday labels + calendar grid
    for row in range(7):
        line = Text()
        if row % 2 == 0:
            line.append(f"  {_WEEKDAY_NAMES[row]} ", style="dim white")
        else:
            line.append("       ")
        for week in weeks:
            block, color = week[row]
            line.append(block + "  ", style=color)
        console.print(line)

    # Legend
    legend = Text("\n  Less  ")
    for i, (b, c) in enumerate(zip(_CALENDAR_BLOCKS[1:], ["green4", "green3", "bright_green", "bold bright_green"])):
        legend.append(b + " ", style=c)
    legend.append(" More", style="dim white")
    console.print(legend)


def _render_contributors(stats: RepoStats) -> None:
    console.print()
    console.print(Rule("[bold cyan]Top Contributors[/bold cyan]", style="bright_blue"))

    table = Table(box=box.ROUNDED, border_style="bright_black", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim white", width=4, justify="right")
    table.add_column("Name", style="bold white", min_width=20)
    table.add_column("Commits", style="bold green", justify="right", width=10)
    table.add_column("Additions", style="bold cyan", justify="right", width=12)
    table.add_column("Deletions", style="bold red", justify="right", width=12)
    table.add_column("Impact", style="bold yellow", width=30)

    top = stats.contributors[:15]
    max_commits = top[0].commits if top else 1

    for i, c in enumerate(top, 1):
        bar_len = int(c.commits / max_commits * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i:2d}")
        table.add_row(
            str(medal),
            c.name,
            f"{c.commits:,}",
            f"+{c.additions:,}" if c.additions else "—",
            f"-{c.deletions:,}" if c.deletions else "—",
            f"[green]{bar}[/green]",
        )

    console.print(table)


def _render_time_heatmap(stats: RepoStats) -> None:
    console.print()
    console.print(Rule("[bold cyan]Commits by Hour of Day[/bold cyan]", style="bright_blue"))

    max_val = max(stats.commits_by_hour.values(), default=1)
    line = Text("  ")
    bar_line = Text("  ")

    for h in range(24):
        count = stats.commits_by_hour.get(h, 0)
        height = int(count / max_val * 8) if max_val else 0
        label = f"{h:02d}"

        bars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        if height == 0:
            bar = " "
            color = "grey23"
        else:
            bar = bars[min(height - 1, 7)]
            color = "bold cyan" if 9 <= h <= 17 else "bold blue"

        bar_line.append(bar + " ", style=color)
        line.append(label[:1], style="dim white")

    console.print(bar_line)
    console.print(line)

    # Find peak hour
    if stats.commits_by_hour:
        peak_h = max(stats.commits_by_hour, key=stats.commits_by_hour.get)
        console.print(f"  Peak hour: [bold yellow]{peak_h:02d}:00[/bold yellow] "
                      f"({stats.commits_by_hour[peak_h]:,} commits)", style="dim white")


def _render_weekday_chart(stats: RepoStats) -> None:
    console.print()
    console.print(Rule("[bold cyan]Commits by Day of Week[/bold cyan]", style="bright_blue"))

    max_val = max(stats.commits_by_weekday.values(), default=1)
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Day", style="dim white", width=4)
    table.add_column("Bar", min_width=40)
    table.add_column("Count", style="bold white", justify="right", width=8)

    for wd in range(7):
        count = stats.commits_by_weekday.get(wd, 0)
        bar_len = int(count / max_val * 36) if max_val else 0
        bar = "█" * bar_len
        is_weekend = wd >= 5
        color = "dim cyan" if is_weekend else "bold cyan"
        table.add_row(_WEEKDAY_NAMES[wd], f"[{color}]{bar}[/{color}]", f"{count:,}")

    console.print(table)


def _render_file_hotspots(stats: RepoStats) -> None:
    if not stats.file_hotspots:
        return
    console.print()
    console.print(Rule("[bold cyan]File Hotspots  (most frequently changed)[/bold cyan]", style="bright_blue"))

    table = Table(box=box.SIMPLE_HEAVY, border_style="bright_black", show_header=True, header_style="bold cyan")
    table.add_column("File", style="white", min_width=40)
    table.add_column("Changes", style="bold red", justify="right", width=10)
    table.add_column("Churn", width=30)

    max_churn = stats.file_hotspots[0].change_count if stats.file_hotspots else 1

    for hs in stats.file_hotspots[:15]:
        bar_len = int(hs.change_count / max_churn * 24)
        bar = "[red]" + "█" * bar_len + "[/red]" + "[grey23]" + "░" * (24 - bar_len) + "[/grey23]"
        # Truncate long paths
        path = hs.path
        if len(path) > 42:
            path = "…" + path[-41:]
        table.add_row(path, f"{hs.change_count:,}", bar)

    console.print(table)


def _render_word_cloud(stats: RepoStats) -> None:
    if not stats.top_words:
        return
    console.print()
    console.print(Rule("[bold cyan]Commit Message Words[/bold cyan]", style="bright_blue"))

    colors = ["bold red", "bold yellow", "bold green", "bold cyan", "bold blue",
              "bold magenta", "red", "yellow", "green", "cyan"]
    max_count = stats.top_words[0][1] if stats.top_words else 1

    text = Text("  ")
    for i, (word, count) in enumerate(stats.top_words):
        size_factor = count / max_count
        if size_factor > 0.7:
            styled = word.upper()
        elif size_factor > 0.4:
            styled = word.title()
        else:
            styled = word
        color = colors[i % len(colors)]
        text.append(styled + "  ", style=color)
        if (i + 1) % 8 == 0:
            text.append("\n  ")

    console.print(text)


def _render_footer(stats: RepoStats) -> None:
    console.print()
    footer = Text(justify="center")
    footer.append("Generated by ", style="dim white")
    footer.append("GitPulse", style="bold cyan")
    footer.append(" • ", style="dim white")
    footer.append("github.com/kareemrt/clauder", style="dim cyan")
    console.print(Panel(footer, border_style="bright_black", padding=(0, 4)))
