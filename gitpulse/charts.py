"""ASCII and rich-rendered chart generation for GitPulse."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.bar import Bar
from rich import box
from datetime import datetime


HEATMAP_CHARS = [" ", "░", "▒", "▓", "█"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS_ABBR = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"
HORIZON_CHARS = ["⣀", "⣤", "⣶", "⣿"]


def _spark_char(val, max_val):
    if max_val == 0:
        return " "
    idx = int((val / max_val) * (len(SPARKLINE_CHARS) - 1))
    return SPARKLINE_CHARS[idx]


def _heat_char(val, max_val):
    if max_val == 0 or val == 0:
        return HEATMAP_CHARS[0]
    idx = max(1, int((val / max_val) * (len(HEATMAP_CHARS) - 1)))
    return HEATMAP_CHARS[min(idx, len(HEATMAP_CHARS) - 1)]


def _heat_color(val, max_val):
    if val == 0 or max_val == 0:
        return "grey19"
    ratio = val / max_val
    if ratio < 0.25:
        return "dark_green"
    if ratio < 0.5:
        return "green3"
    if ratio < 0.75:
        return "green1"
    return "bright_green"


def render_heatmap(console: Console, grid, weeks, grid_start):
    """Render a GitHub-style contribution heatmap."""
    max_val = max(grid.values()) if grid else 1

    # Month labels row
    month_labels = []
    prev_month = None
    label_row = []
    for w in range(weeks):
        from datetime import timedelta
        dt = grid_start + timedelta(weeks=w)
        m = dt.month
        if m != prev_month:
            label_row.append(f"[dim]{MONTHS[m-1]}[/dim]")
            prev_month = m
        else:
            label_row.append("   ")

    header = Text()
    header.append("     ", style="")
    for chunk in label_row:
        # chunk is either a 3-char month abbreviation or 3 spaces
        raw = chunk.replace("[dim]", "").replace("[/dim]", "")
        header.append(raw[:3] + " ", style="dim")
    console.print(header)

    for dow in range(7):
        row = Text()
        row.append(f"{DAYS_ABBR[dow]} ", style="dim")
        for w in range(weeks):
            val = grid.get((w, dow), 0)
            ch = _heat_char(val, max_val)
            color = _heat_color(val, max_val)
            row.append(ch + " ", style=color)
        console.print(row)

    legend = Text("\n    Less ")
    for i, ch in enumerate(HEATMAP_CHARS):
        colors = ["grey19", "dark_green", "green3", "green1", "bright_green"]
        legend.append(ch + " ", style=colors[i])
    legend.append("More", style="dim")
    console.print(legend)


def render_velocity_chart(console: Console, counts, labels, title="Commit Velocity"):
    """Render a sparkline-style velocity chart."""
    if not counts:
        console.print("[dim]No data[/dim]")
        return

    max_val = max(counts) if counts else 1
    height = 8

    rows = []
    for row_idx in range(height, 0, -1):
        threshold = (row_idx / height) * max_val
        line = Text()
        y_label = f"{int(threshold):>4} │ "
        line.append(y_label, style="dim")
        for val in counts:
            if val >= threshold:
                line.append("█", style="cyan")
            elif val >= threshold - (max_val / height / 2):
                line.append("▄", style="cyan")
            else:
                line.append(" ")
        rows.append(line)

    # Bottom axis
    axis = Text()
    axis.append("     └" + "─" * len(counts), style="dim")

    # Time labels
    label_line = Text("      ")
    step = max(1, len(labels) // 6)
    for i, lbl in enumerate(labels):
        if i % step == 0:
            lstr = lbl.strftime("%b'%y")
            label_line.append(lstr[:6].ljust(max(1, step)), style="dim")

    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    for r in rows:
        console.print(r)
    console.print(axis)
    console.print(label_line)


def render_bar_chart(console: Console, items, title, color="cyan", max_items=15, unit="commits"):
    """Render a horizontal bar chart from (name, value) pairs."""
    if not items:
        console.print("[dim]No data[/dim]")
        return

    items = items[:max_items]
    max_val = max(v for _, v in items) if items else 1
    bar_width = 40

    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    table = Table(box=None, padding=(0, 1), show_header=False)
    table.add_column("name", style="", no_wrap=True, min_width=25, max_width=35)
    table.add_column("bar", no_wrap=True)
    table.add_column("val", style="dim", justify="right")

    for name, val in items:
        filled = int((val / max_val) * bar_width)
        bar_str = "█" * filled + "░" * (bar_width - filled)
        bar_text = Text(bar_str[:bar_width], style=color)
        display_name = name[-33:] if len(name) > 35 else name
        table.add_row(display_name, bar_text, f"{val} {unit}")

    console.print(table)


def render_author_table(console: Console, author_data):
    """Render author contribution table with sparkline-style share bar."""
    if not author_data:
        return

    total = sum(v for _, v in author_data)
    console.print("\n[bold cyan]Author Contributions[/bold cyan]")

    table = Table(box=box.SIMPLE, padding=(0, 1))
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Author", style="bold", min_width=20)
    table.add_column("Commits", justify="right", style="cyan")
    table.add_column("Share", justify="right", style="dim")
    table.add_column("Distribution", min_width=30)

    colors = ["bright_green", "green3", "cyan", "blue", "magenta", "yellow", "red"]
    for i, (author, count) in enumerate(author_data[:10]):
        pct = count / total * 100
        bar_len = int(pct / 2)
        color = colors[i % len(colors)]
        bar = Text("█" * bar_len + "░" * (20 - bar_len), style=color)
        table.add_row(str(i + 1), author[:30], str(count), f"{pct:.1f}%", bar)

    console.print(table)


def render_peak_hours(console: Console, hours_data):
    """Render commit activity by hour of day."""
    max_val = max(hours_data) if hours_data else 1
    height = 6

    console.print("\n[bold cyan]Peak Commit Hours (UTC)[/bold cyan]")

    for row_idx in range(height, 0, -1):
        threshold = (row_idx / height) * max_val
        line = Text()
        for val in hours_data:
            if val >= threshold:
                line.append("▓", style="yellow")
            else:
                line.append(" ")
        console.print(line)

    # Hour labels
    hour_labels = Text()
    for h in range(24):
        if h % 3 == 0:
            hour_labels.append(f"{h:02d}", style="dim")
        else:
            hour_labels.append(" ")
    console.print(hour_labels)
    console.print(Text("─" * 24, style="dim"))

    peak_h = hours_data.index(max(hours_data))
    console.print(f"  [dim]Peak hour: [bold yellow]{peak_h:02d}:00 UTC[/bold yellow][/dim]")


def render_language_pie(console: Console, ext_counter):
    """Render language distribution as a horizontal stacked bar."""
    if not ext_counter:
        return

    top = ext_counter.most_common(8)
    total = sum(v for _, v in top)
    if total == 0:
        return

    colors = [
        "bright_cyan", "bright_green", "bright_yellow", "bright_magenta",
        "bright_blue", "bright_red", "cyan", "green",
    ]
    bar_width = 60

    console.print("\n[bold cyan]Language Distribution[/bold cyan]")

    bar = Text()
    for i, (ext, count) in enumerate(top):
        seg_len = max(1, int((count / total) * bar_width))
        bar.append("█" * seg_len, style=colors[i % len(colors)])

    console.print(bar)

    legend_cols = []
    for i, (ext, count) in enumerate(top):
        pct = count / total * 100
        label = Text(f"  {ext} {pct:.0f}%", style=colors[i % len(colors)])
        legend_cols.append(label)

    console.print(Columns(legend_cols))


def render_summary_panel(console: Console, stats, repo_name):
    """Render the top summary stats panel."""
    if not stats:
        return

    first = stats["first_commit"].strftime("%Y-%m-%d") if stats.get("first_commit") else "N/A"
    last = stats["last_commit"].strftime("%Y-%m-%d") if stats.get("last_commit") else "N/A"

    grid = Table.grid(padding=(0, 4))
    grid.add_column(justify="left")
    grid.add_column(justify="left")
    grid.add_column(justify="left")
    grid.add_column(justify="left")

    grid.add_row(
        f"[dim]Commits[/dim]\n[bold bright_cyan]{stats['total_commits']:,}[/bold bright_cyan]",
        f"[dim]Authors[/dim]\n[bold bright_green]{stats['total_authors']}[/bold bright_green]",
        f"[dim]Files[/dim]\n[bold bright_yellow]{stats['total_files']:,}[/bold bright_yellow]",
        f"[dim]Age[/dim]\n[bold bright_magenta]{stats['age_days']} days[/bold bright_magenta]",
    )
    grid.add_row(
        f"[dim]Lines Added[/dim]\n[bold green]+{stats['lines_added']:,}[/bold green]",
        f"[dim]Lines Removed[/dim]\n[bold red]-{stats['lines_deleted']:,}[/bold red]",
        f"[dim]Commits/Day[/dim]\n[bold cyan]{stats['commits_per_day']}[/bold cyan]",
        f"[dim]Active[/dim]\n[bold dim]{first} → {last}[/bold dim]",
    )

    panel = Panel(
        grid,
        title=f"[bold bright_white] ⚡ GitPulse — {repo_name} [/bold bright_white]",
        border_style="bright_cyan",
        padding=(1, 2),
    )
    console.print(panel)


def render_co_change(console: Console, pairs, top_n=10):
    """Render co-change pairs — files that often change together."""
    if not pairs:
        return

    top = pairs.most_common(top_n)
    if not top:
        return

    console.print("\n[bold cyan]Co-Change Pairs (files that change together)[/bold cyan]")
    table = Table(box=box.SIMPLE, padding=(0, 1))
    table.add_column("File A", style="dim", min_width=25)
    table.add_column("↔", style="bold cyan", justify="center", width=3)
    table.add_column("File B", style="dim", min_width=25)
    table.add_column("Times", style="cyan", justify="right")

    for (f1, f2), count in top:
        a = f1[-30:] if len(f1) > 30 else f1
        b = f2[-30:] if len(f2) > 30 else f2
        table.add_row(a, "↔", b, str(count))

    console.print(table)
