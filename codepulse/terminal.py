"""Rich terminal dashboard for CodePulse."""

from datetime import datetime, timezone, timedelta
from collections import defaultdict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich import box
from rich.padding import Padding
from rich.rule import Rule

from .metrics import RepoMetrics

console = Console()

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Block shading levels for heatmap
SHADES = [" ", "░", "▒", "▓", "█"]

LANG_COLORS = {
    ".py": "bright_blue",
    ".js": "bright_yellow",
    ".ts": "yellow",
    ".go": "cyan",
    ".rs": "red",
    ".java": "bright_red",
    ".rb": "bright_red",
    ".md": "bright_green",
    ".json": "bright_white",
    ".yaml": "bright_magenta",
    ".yml": "bright_magenta",
    ".sh": "green",
    ".html": "orange3",
    ".css": "bright_cyan",
    ".c": "white",
    ".cpp": "white",
}


def _shade(count: int, max_count: int) -> tuple[str, str]:
    if max_count == 0 or count == 0:
        return SHADES[0], "grey23"
    ratio = count / max_count
    idx = max(1, min(4, int(ratio * 4) + 1))
    colors = ["grey23", "dark_green", "green3", "green1", "bright_green"]
    return SHADES[idx], colors[idx]


def render_heatmap(heatmap: dict[str, int]) -> Text:
    """Render a 52-week GitHub-style contribution heatmap."""
    today = datetime.now(timezone.utc).date()
    # Start on Monday 52 weeks ago
    start = today - timedelta(weeks=52)
    # Rewind to nearest Monday
    start = start - timedelta(days=start.weekday())

    max_count = max(heatmap.values(), default=1)

    # Build grid: rows = weekdays (0..6), cols = weeks (0..52)
    grid: list[list[tuple[str, str]]] = [[("", "") for _ in range(53)] for _ in range(7)]
    current = start
    for week in range(53):
        for day in range(7):
            date_str = current.strftime("%Y-%m-%d")
            count = heatmap.get(date_str, 0)
            char, color = _shade(count, max_count)
            grid[day][week] = (char, color)
            current += timedelta(days=1)

    text = Text()
    # Month labels row
    month_labels = Text("     ")
    label_current = start
    prev_month = -1
    for week in range(53):
        if label_current.month != prev_month:
            month_labels.append(label_current.strftime("%b")[:3], style="dim")
            prev_month = label_current.month
        else:
            month_labels.append("   ")
        label_current += timedelta(weeks=1)
    text.append_text(month_labels)
    text.append("\n")

    for day in range(7):
        if day % 2 == 0:
            text.append(f"{WEEKDAYS[day]} ", style="dim")
        else:
            text.append("    ")
        for week in range(53):
            char, color = grid[day][week]
            if char == " ":
                text.append("·", style="grey23")
            else:
                text.append(char + char, style=color)
        text.append("\n")

    # Legend
    text.append("\n  Less ", style="dim")
    for i, (s, c) in enumerate(zip(SHADES[1:], ["dark_green", "green3", "green1", "bright_green"])):
        text.append(s + s, style=c)
    text.append(" More", style="dim")

    return text


def render_hour_chart(commits_by_hour: dict[int, int]) -> Text:
    max_val = max(commits_by_hour.values(), default=1)
    bar_max = 20
    text = Text()
    for hour in range(24):
        count = commits_by_hour.get(hour, 0)
        bar_len = int((count / max_val) * bar_max) if max_val else 0
        label = f"{hour:02d}h "
        if 6 <= hour < 12:
            color = "bright_yellow"
        elif 12 <= hour < 18:
            color = "bright_cyan"
        elif 18 <= hour < 22:
            color = "bright_magenta"
        else:
            color = "grey62"
        text.append(label, style="dim")
        text.append("█" * bar_len, style=color)
        text.append(f" {count}\n", style="dim")
    return text


def render_weekday_chart(commits_by_weekday: dict[int, int]) -> Text:
    max_val = max(commits_by_weekday.values(), default=1)
    bar_max = 25
    text = Text()
    for day in range(7):
        count = commits_by_weekday.get(day, 0)
        bar_len = int((count / max_val) * bar_max) if max_val else 0
        label = f"{WEEKDAYS[day]} "
        color = "cyan" if day < 5 else "yellow"
        text.append(label, style="dim")
        text.append("█" * bar_len, style=color)
        text.append(f" {count}\n", style="dim")
    return text


def render_language_chart(language_lines: dict[str, int]) -> Text:
    if not language_lines:
        return Text("No files detected.", style="dim")
    sorted_langs = sorted(language_lines.items(), key=lambda x: x[1], reverse=True)[:10]
    total = sum(v for _, v in sorted_langs)
    bar_max = 20
    text = Text()
    for ext, lines in sorted_langs:
        pct = lines / total if total else 0
        bar_len = int(pct * bar_max)
        color = LANG_COLORS.get(ext, "white")
        label = f"{ext:<12}"
        text.append(label, style=color)
        text.append("█" * bar_len, style=color)
        text.append(f" {lines:,} lines ({pct:.0%})\n", style="dim")
    return text


def print_dashboard(m: RepoMetrics) -> None:
    console.print()
    console.print(
        Align.center(
            Text.from_markup(
                f"[bold bright_green]⚡ CodePulse[/] [bold white]— Git Repository Analytics[/]\n"
                f"[dim]{m.repo_name}[/]"
            )
        )
    )
    console.print(Rule(style="bright_green"))
    console.print()

    # --- Summary cards ---
    age = (m.last_commit - m.first_commit).days or 1
    velocity = round(m.total_commits / (age / 30), 1)

    cards = [
        Panel(
            Align.center(Text(str(m.total_commits), style="bold bright_green") + Text("\ncommits", style="dim")),
            box=box.ROUNDED,
            border_style="green",
        ),
        Panel(
            Align.center(Text(str(m.total_contributors), style="bold bright_cyan") + Text("\ncontributors", style="dim")),
            box=box.ROUNDED,
            border_style="cyan",
        ),
        Panel(
            Align.center(Text(str(m.active_days), style="bold bright_yellow") + Text("\nactive days", style="dim")),
            box=box.ROUNDED,
            border_style="yellow",
        ),
        Panel(
            Align.center(Text(str(m.total_files_changed), style="bold magenta") + Text("\nfile changes", style="dim")),
            box=box.ROUNDED,
            border_style="magenta",
        ),
        Panel(
            Align.center(Text(str(velocity), style="bold bright_red") + Text("\ncommits/month", style="dim")),
            box=box.ROUNDED,
            border_style="red",
        ),
    ]
    console.print(Columns(cards, equal=True, expand=True))
    console.print()

    # --- Contributor leaderboard ---
    console.print(Rule("[bold]Top Contributors[/]", style="dim"))
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold bright_white")
    table.add_column("#", style="dim", width=3)
    table.add_column("Author", style="bright_white")
    table.add_column("Commits", justify="right", style="bright_green")
    table.add_column("Files Touched", justify="right", style="cyan")
    table.add_column("First Commit", style="dim")
    table.add_column("Last Commit", style="dim")
    for i, c in enumerate(m.contributors[:10], 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f" {i}.")
        table.add_row(
            medal,
            c.name,
            str(c.commits),
            str(c.files_touched),
            c.first_commit.strftime("%Y-%m-%d"),
            c.last_commit.strftime("%Y-%m-%d"),
        )
    console.print(table)

    # --- Heatmap ---
    console.print(Rule("[bold]Commit Activity (Last 52 Weeks)[/]", style="dim"))
    console.print(Padding(render_heatmap(m.heatmap), (0, 2)))
    console.print()

    # --- Side by side: hour chart + weekday chart + language chart ---
    console.print(Rule("[bold]Patterns & Languages[/]", style="dim"))
    hour_panel = Panel(render_hour_chart(m.commits_by_hour), title="By Hour of Day", border_style="dim", box=box.ROUNDED)
    day_panel = Panel(render_weekday_chart(m.commits_by_weekday), title="By Weekday", border_style="dim", box=box.ROUNDED)
    lang_panel = Panel(render_language_chart(m.language_lines), title="Languages", border_style="dim", box=box.ROUNDED)
    console.print(Columns([hour_panel, day_panel, lang_panel], expand=True))

    # --- Hot files ---
    if m.hot_files:
        console.print()
        console.print(Rule("[bold]Hottest Files[/]", style="dim"))
        hot_table = Table(box=box.SIMPLE, show_header=True, header_style="bold bright_white")
        hot_table.add_column("File", style="bright_white")
        hot_table.add_column("Changes", justify="right", style="bright_red")
        hot_table.add_column("Heat", style="bright_yellow")
        max_changes = m.hot_files[0][1] if m.hot_files else 1
        for path, count in m.hot_files:
            bar = "█" * int((count / max_changes) * 20)
            hot_table.add_row(path, str(count), bar)
        console.print(hot_table)

    console.print()
    console.print(
        Align.center(
            Text.from_markup(
                f"[dim]Repository active from [bright_white]{m.first_commit.strftime('%b %Y')}[/] "
                f"to [bright_white]{m.last_commit.strftime('%b %Y')}[/] · "
                f"Generated by [bright_green]CodePulse[/][/]"
            )
        )
    )
    console.print()
