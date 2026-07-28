"""
Rich terminal dashboard and HTML report renderer.
"""

from __future__ import annotations

import html
import math
from datetime import datetime
from typing import List, Tuple, Dict

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from .analyzer import RepoStats


# ──────────────────────────────────────────────────────────────────────────────
# Terminal renderer
# ──────────────────────────────────────────────────────────────────────────────

PALETTE = {
    "accent": "bold cyan",
    "warn": "bold yellow",
    "good": "bold green",
    "muted": "dim white",
    "title": "bold magenta",
    "header": "bold white on dark_blue",
}


def _bar(value: int, max_value: int, width: int = 30, char: str = "█") -> str:
    if max_value == 0:
        return ""
    filled = round((value / max_value) * width)
    return char * filled + "░" * (width - filled)


def _age(dt: datetime) -> str:
    if dt is None:
        return "N/A"
    delta = datetime.now(tz=dt.tzinfo) - dt
    days = delta.days
    if days < 1:
        return "today"
    if days < 30:
        return f"{days}d ago"
    if days < 365:
        return f"{days // 30}mo ago"
    return f"{days // 365}y {(days % 365) // 30}mo ago"


def render_terminal(stats: RepoStats, console: Console | None = None) -> None:
    c = console or Console()

    # ── Banner ──────────────────────────────────────────────────────────────
    banner = Text(justify="center")
    banner.append("\n  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗ ██████╗██╗     ███████╗\n", style="bold cyan")
    banner.append(" ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗  ██║██║██╔════╝██║     ██╔════╝\n", style="bold cyan")
    banner.append(" ██║     ███████║██████╔╝██║   ██║██╔██╗ ██║██║██║     ██║     █████╗  \n", style="bold magenta")
    banner.append(" ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╗██║██║██║     ██║     ██╔══╝  \n", style="bold magenta")
    banner.append(" ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚████║██║╚██████╗███████╗███████╗\n", style="bold blue")
    banner.append("  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝╚══════╝\n", style="bold blue")
    banner.append(f"           Git Repository Historian  •  {stats.repo_name}\n\n", style="dim cyan")
    c.print(banner)

    # ── Summary cards ───────────────────────────────────────────────────────
    def stat_card(label: str, value: str, color: str = "cyan") -> Panel:
        t = Text(value, style=f"bold {color}", justify="center")
        t.append(f"\n{label}", style="dim white")
        return Panel(t, box=box.ROUNDED, border_style=color, padding=(0, 2))

    first = stats.first_commit.strftime("%b %Y") if stats.first_commit else "N/A"
    last = stats.last_commit.strftime("%b %Y") if stats.last_commit else "N/A"
    age_str = _age(stats.first_commit) if stats.first_commit else "N/A"

    cards = Columns(
        [
            stat_card(f"Commits", str(stats.total_commits), "cyan"),
            stat_card("Authors", str(stats.total_authors), "magenta"),
            stat_card("Lines Added", f"+{stats.total_insertions:,}", "green"),
            stat_card("Lines Removed", f"-{stats.total_deletions:,}", "red"),
            stat_card("Born", first, "yellow"),
            stat_card("Last Active", _age(stats.last_commit) if stats.last_commit else "N/A", "blue"),
        ],
        equal=True,
        expand=True,
    )
    c.print(cards)
    c.print()

    # ── Commit timeline ──────────────────────────────────────────────────────
    c.print(Rule("[bold cyan]  Commit Timeline  ", style="cyan"))
    c.print()

    if stats.monthly_commits:
        max_val = max(stats.monthly_commits.values())
        months = list(stats.monthly_commits.items())
        # Show last 24 months max
        months = months[-24:]
        for month, count in months:
            bar = _bar(count, max_val, width=40)
            label = f"[dim]{month}[/dim]"
            count_str = f"[cyan]{count:3d}[/cyan]"
            bar_text = f"[{'cyan' if count < max_val else 'bold yellow'}]{bar}[/]"
            c.print(f"  {label}  {bar_text}  {count_str}")
    else:
        c.print("  [dim]No commit data available.[/dim]")

    c.print()

    # ── Top contributors ─────────────────────────────────────────────────────
    c.print(Rule("[bold magenta]  Top Contributors  ", style="magenta"))
    c.print()

    contrib_table = Table(
        box=box.SIMPLE_HEAD,
        show_edge=False,
        expand=True,
        padding=(0, 1),
    )
    contrib_table.add_column("Rank", style="dim", width=5, justify="right")
    contrib_table.add_column("Author", style="bold white", min_width=20)
    contrib_table.add_column("Commits", style="cyan", justify="right", width=8)
    contrib_table.add_column("Lines", style="green", justify="right", width=10)
    contrib_table.add_column("Activity", min_width=30)

    max_commits = max(stats.author_commits.values()) if stats.author_commits else 1
    medals = ["🥇", "🥈", "🥉"]

    for i, (author, cnt) in enumerate(list(stats.author_commits.items())[:10]):
        rank = medals[i] if i < 3 else f"#{i+1}"
        lines = stats.author_lines.get(author, 0)
        bar = _bar(cnt, max_commits, width=25)
        contrib_table.add_row(
            rank,
            author,
            str(cnt),
            f"{lines:,}",
            f"[{'yellow' if i == 0 else 'cyan'}]{bar}[/]",
        )

    c.print(contrib_table)
    c.print()

    # ── Hot files ────────────────────────────────────────────────────────────
    if stats.hot_files:
        c.print(Rule("[bold yellow]  Hottest Files  ", style="yellow"))
        c.print()

        max_changes = stats.hot_files[0][1] if stats.hot_files else 1
        heat_table = Table(box=box.SIMPLE_HEAD, show_edge=False, expand=True, padding=(0, 1))
        heat_table.add_column("File", style="white", min_width=30)
        heat_table.add_column("Changes", justify="right", style="bold yellow", width=8)
        heat_table.add_column("Heat", min_width=30)

        heat_chars = ["░", "▒", "▓", "█"]
        for fname, changes in stats.hot_files[:10]:
            ratio = changes / max_changes
            if ratio > 0.75:
                color = "bold red"
            elif ratio > 0.5:
                color = "yellow"
            elif ratio > 0.25:
                color = "cyan"
            else:
                color = "dim white"
            bar = _bar(changes, max_changes, width=25)
            heat_table.add_row(
                fname if len(fname) <= 45 else "…" + fname[-44:],
                str(changes),
                f"[{color}]{bar}[/]",
            )
        c.print(heat_table)
        c.print()

    # ── Language breakdown ───────────────────────────────────────────────────
    if stats.language_breakdown:
        c.print(Rule("[bold blue]  Language Breakdown  ", style="blue"))
        c.print()

        lang_table = Table(box=box.SIMPLE_HEAD, show_edge=False, padding=(0, 1))
        lang_table.add_column("Extension", style="bold white", width=12)
        lang_table.add_column("Files", justify="right", style="cyan", width=7)
        lang_table.add_column("Share", min_width=35)

        total_files = sum(stats.language_breakdown.values())
        max_files = max(stats.language_breakdown.values()) if stats.language_breakdown else 1
        ext_colors = ["cyan", "magenta", "green", "yellow", "blue", "red"]

        for idx, (ext, count) in enumerate(stats.language_breakdown.items()):
            pct = count / total_files * 100
            bar = _bar(count, max_files, width=30)
            color = ext_colors[idx % len(ext_colors)]
            lang_table.add_row(
                ext or "(no ext)",
                str(count),
                f"[{color}]{bar}[/] [dim]{pct:.1f}%[/dim]",
            )
        c.print(lang_table)
        c.print()

    # ── Fun facts / insights ─────────────────────────────────────────────────
    c.print(Rule("[bold green]  Project Insights  ", style="green"))
    c.print()

    insights = _generate_insights(stats)
    for icon, text in insights:
        c.print(f"  {icon}  {text}")
    c.print()


def _generate_insights(stats: RepoStats) -> List[Tuple[str, str]]:
    insights = []

    if stats.total_commits == 0:
        return [("📭", "No commits found in this repository.")]

    # Age
    if stats.first_commit and stats.last_commit:
        age_days = (stats.last_commit - stats.first_commit).days
        if age_days > 365:
            insights.append(("📅", f"This project spans [bold]{age_days // 365}y {(age_days % 365) // 30}mo[/bold] of development."))
        elif age_days > 30:
            insights.append(("📅", f"This project is [bold]{age_days // 30} months[/bold] old."))
        else:
            insights.append(("🆕", f"A fresh project — only [bold]{age_days} days[/bold] old!"))

    # Commit velocity
    if stats.avg_commits_per_month > 50:
        insights.append(("🚀", f"[bold green]High velocity![/bold green] Averaging {stats.avg_commits_per_month:.0f} commits/month."))
    elif stats.avg_commits_per_month > 10:
        insights.append(("⚡", f"Active codebase — averaging {stats.avg_commits_per_month:.1f} commits/month."))
    else:
        insights.append(("🌱", f"Steady pace — averaging {stats.avg_commits_per_month:.1f} commits/month."))

    # Streak
    if stats.longest_streak_days > 30:
        insights.append(("🔥", f"Longest active streak: [bold yellow]{stats.longest_streak_days} consecutive days[/bold yellow]!"))
    elif stats.longest_streak_days > 7:
        insights.append(("⚡", f"Best streak: [bold]{stats.longest_streak_days} consecutive days[/bold] of commits."))

    # Churn ratio
    total_lines = stats.total_insertions + stats.total_deletions
    if total_lines > 0:
        churn = stats.total_deletions / total_lines
        if churn > 0.45:
            insights.append(("♻️", f"Heavy refactoring culture — {churn*100:.0f}% of line changes were deletions."))
        elif churn > 0.3:
            insights.append(("🔧", f"Healthy churn ratio — {churn*100:.0f}% of changes are removals (good sign!)."))
        else:
            insights.append(("📈", f"Growth-focused — mostly additive changes ({(1-churn)*100:.0f}% additions)."))

    # Team dynamics
    if stats.total_authors == 1:
        insights.append(("🧑‍💻", f"Solo project — all [bold]{stats.total_commits}[/bold] commits from one developer."))
    elif stats.total_authors <= 3:
        insights.append(("👥", f"Small, tight team of [bold]{stats.total_authors}[/bold] contributors."))
    else:
        insights.append(("🏢", f"Team project with [bold]{stats.total_authors}[/bold] contributors."))

    # Peak month
    if stats.peak_month and stats.peak_month != "N/A":
        peak_count = stats.monthly_commits.get(stats.peak_month, 0)
        insights.append(("📊", f"Peak productivity: [bold cyan]{stats.peak_month}[/bold cyan] with {peak_count} commits."))

    return insights


# ──────────────────────────────────────────────────────────────────────────────
# HTML report renderer
# ──────────────────────────────────────────────────────────────────────────────


def _svg_bar_chart(data: Dict[str, int], width: int = 700, height: int = 200) -> str:
    if not data:
        return ""
    keys = list(data.keys())
    values = list(data.values())
    max_val = max(values) or 1
    n = len(keys)
    bar_width = max(4, (width - 80) // n - 2)
    padding = 40

    bars = []
    for i, (k, v) in enumerate(zip(keys, values)):
        x = padding + i * (bar_width + 2)
        bar_h = max(2, int((v / max_val) * (height - 60)))
        y = height - 30 - bar_h
        color = f"hsl({200 + i * 5}, 70%, 55%)"
        bars.append(
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_h}" '
            f'fill="{color}" rx="2" opacity="0.9">'
            f'<title>{html.escape(str(k))}: {v}</title></rect>'
        )
        # X label (rotated, show every nth)
        step = max(1, n // 12)
        if i % step == 0:
            short_k = str(k)[-7:]  # last 7 chars (YYYY-MM)
            bars.append(
                f'<text x="{x + bar_width//2}" y="{height - 5}" '
                f'text-anchor="middle" font-size="9" fill="#888" '
                f'transform="rotate(-45, {x + bar_width//2}, {height - 5})">'
                f'{html.escape(short_k)}</text>'
            )

    # Y axis label
    bars.append(f'<text x="8" y="{height//2}" fill="#888" font-size="10" text-anchor="middle" transform="rotate(-90, 8, {height//2})">commits</text>')
    bars.append(f'<text x="{padding}" y="{height - 30 - int((max_val/max_val)*(height-60)) - 5}" fill="#aaa" font-size="9">{max_val}</text>')

    return (
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;max-width:{width}px;background:#1a1a2e;border-radius:8px">'
        + "".join(bars)
        + "</svg>"
    )


def _svg_donut(data: Dict[str, int], size: int = 200) -> str:
    if not data:
        return ""
    total = sum(data.values())
    if total == 0:
        return ""
    colors = ["#00d4ff", "#c724b1", "#00c896", "#f59e0b", "#6366f1", "#ef4444", "#8b5cf6", "#ec4899"]
    cx = cy = size // 2
    r_outer = size // 2 - 10
    r_inner = r_outer * 0.55

    slices = []
    start_angle = -90.0

    for idx, (label, value) in enumerate(list(data.items())[:8]):
        angle = (value / total) * 360
        end_angle = start_angle + angle

        def polar(angle_deg: float, radius: float):
            import math
            rad = math.radians(angle_deg)
            return cx + radius * math.cos(rad), cy + radius * math.sin(rad)

        x1, y1 = polar(start_angle, r_outer)
        x2, y2 = polar(end_angle, r_outer)
        x3, y3 = polar(end_angle, r_inner)
        x4, y4 = polar(start_angle, r_inner)
        large = 1 if angle > 180 else 0
        color = colors[idx % len(colors)]
        path = (
            f'M {x1:.1f} {y1:.1f} '
            f'A {r_outer} {r_outer} 0 {large} 1 {x2:.1f} {y2:.1f} '
            f'L {x3:.1f} {y3:.1f} '
            f'A {r_inner} {r_inner} 0 {large} 0 {x4:.1f} {y4:.1f} Z'
        )
        slices.append(
            f'<path d="{path}" fill="{color}" opacity="0.9">'
            f'<title>{html.escape(str(label))}: {value} ({value/total*100:.1f}%)</title>'
            f'</path>'
        )
        start_angle = end_angle

    # Center text
    slices.append(f'<text x="{cx}" y="{cy - 8}" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{total}</text>')
    slices.append(f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" fill="#aaa" font-size="9">files</text>')

    return (
        f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:{size}px;height:{size}px">'
        + "".join(slices)
        + "</svg>"
    )


def render_html(stats: RepoStats) -> str:
    """Generate a self-contained HTML report."""
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    first_str = stats.first_commit.strftime("%b %d, %Y") if stats.first_commit else "N/A"
    last_str = stats.last_commit.strftime("%b %d, %Y") if stats.last_commit else "N/A"

    timeline_svg = _svg_bar_chart(stats.monthly_commits)
    lang_svg = _svg_donut(stats.language_breakdown)

    # Build contributor rows
    contrib_rows = ""
    medals = ["🥇", "🥈", "🥉"]
    max_commits = max(stats.author_commits.values()) if stats.author_commits else 1
    for i, (author, cnt) in enumerate(list(stats.author_commits.items())[:10]):
        pct = cnt / max_commits * 100
        medal = medals[i] if i < 3 else f"#{i+1}"
        lines = stats.author_lines.get(author, 0)
        contrib_rows += f"""
        <tr>
          <td>{medal}</td>
          <td>{html.escape(author)}</td>
          <td>{cnt}</td>
          <td>{lines:,}</td>
          <td><div class="bar-bg"><div class="bar-fill" style="width:{pct:.1f}%"></div></div></td>
        </tr>"""

    # Build hot files rows
    hot_rows = ""
    max_changes = stats.hot_files[0][1] if stats.hot_files else 1
    for fname, changes in stats.hot_files[:10]:
        pct = changes / max_changes * 100
        heat = "🔴" if pct > 75 else "🟡" if pct > 50 else "🟢"
        hot_rows += f"""
        <tr>
          <td>{heat}</td>
          <td class="file-name">{html.escape(fname)}</td>
          <td>{changes}</td>
          <td><div class="bar-bg"><div class="bar-fill" style="width:{pct:.1f}%"></div></div></td>
        </tr>"""

    # Insights
    insights_html = ""
    for icon, text in _generate_insights(stats):
        # Strip rich markup for HTML
        clean = re.sub(r"\[/?[^\]]*\]", "", text)
        insights_html += f'<div class="insight"><span class="insight-icon">{icon}</span><span>{clean}</span></div>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chronicle Report — {html.escape(stats.repo_name)}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0d0d1a;
      --surface: #13132b;
      --surface2: #1a1a35;
      --border: #2a2a4a;
      --text: #e2e2f0;
      --muted: #8888aa;
      --accent: #00d4ff;
      --magenta: #c724b1;
      --green: #00c896;
      --yellow: #f59e0b;
      --red: #ef4444;
    }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; }}
    a {{ color: var(--accent); }}
    .hero {{
      background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0a1a2e 100%);
      padding: 3rem 2rem 2rem;
      text-align: center;
      border-bottom: 1px solid var(--border);
    }}
    .hero pre {{
      font-family: monospace;
      font-size: 0.65rem;
      line-height: 1.2;
      color: #00d4ff;
      display: inline-block;
      text-align: left;
    }}
    .hero h1 {{ font-size: 1.8rem; margin-top: 1rem; color: var(--text); }}
    .hero .subtitle {{ color: var(--muted); font-size: 0.9rem; margin-top: 0.25rem; }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 1rem;
      padding: 2rem;
      max-width: 1100px;
      margin: 0 auto;
    }}
    .stat-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem;
      text-align: center;
      transition: transform 0.2s;
    }}
    .stat-card:hover {{ transform: translateY(-2px); }}
    .stat-card .val {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
    .stat-card .val.green {{ color: var(--green); }}
    .stat-card .val.red {{ color: var(--red); }}
    .stat-card .val.yellow {{ color: var(--yellow); }}
    .stat-card .val.magenta {{ color: var(--magenta); }}
    .stat-card .lbl {{ font-size: 0.8rem; color: var(--muted); margin-top: 0.25rem; }}
    .section {{ max-width: 1100px; margin: 0 auto 2rem; padding: 0 2rem; }}
    .section-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--accent);
      border-left: 3px solid var(--accent);
      padding-left: 0.75rem;
      margin-bottom: 1.25rem;
    }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    th {{ color: var(--muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; padding: 0.5rem; text-align: left; border-bottom: 1px solid var(--border); }}
    td {{ padding: 0.6rem 0.5rem; border-bottom: 1px solid var(--border); vertical-align: middle; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: var(--surface2); }}
    .bar-bg {{ background: var(--border); border-radius: 4px; height: 8px; min-width: 60px; }}
    .bar-fill {{ background: linear-gradient(90deg, var(--accent), var(--magenta)); height: 100%; border-radius: 4px; }}
    .file-name {{ font-family: monospace; font-size: 0.82rem; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
    @media (max-width: 700px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
    .insights-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
    .insight {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; display: flex; gap: 0.75rem; align-items: flex-start; }}
    .insight-icon {{ font-size: 1.4rem; flex-shrink: 0; }}
    .footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.8rem; border-top: 1px solid var(--border); margin-top: 2rem; }}
    .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
    .badge-green {{ background: rgba(0,200,150,0.2); color: var(--green); }}
    .badge-red {{ background: rgba(239,68,68,0.2); color: var(--red); }}
  </style>
</head>
<body>

<div class="hero">
  <pre>
  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗ ██████╗██╗     ███████╗
 ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗  ██║██║██╔════╝██║     ██╔════╝
 ██║     ███████║██████╔╝██║   ██║██╔██╗ ██║██║██║     ██║     █████╗
 ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╗██║██║██║     ██║     ██╔══╝
 ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚████║██║╚██████╗███████╗███████╗
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝╚══════╝</pre>
  <h1>{html.escape(stats.repo_name)}</h1>
  <p class="subtitle">Repository Analysis Report &nbsp;•&nbsp; Generated {generated_at}</p>
</div>

<div class="stats-grid">
  <div class="stat-card"><div class="val">{stats.total_commits:,}</div><div class="lbl">Total Commits</div></div>
  <div class="stat-card"><div class="val magenta">{stats.total_authors}</div><div class="lbl">Contributors</div></div>
  <div class="stat-card"><div class="val green">+{stats.total_insertions:,}</div><div class="lbl">Lines Added</div></div>
  <div class="stat-card"><div class="val red">-{stats.total_deletions:,}</div><div class="lbl">Lines Removed</div></div>
  <div class="stat-card"><div class="val yellow">{stats.avg_commits_per_month:.1f}</div><div class="lbl">Commits / Month</div></div>
  <div class="stat-card"><div class="val">{stats.longest_streak_days}</div><div class="lbl">Best Streak (days)</div></div>
  <div class="stat-card"><div class="val">{first_str}</div><div class="lbl">First Commit</div></div>
  <div class="stat-card"><div class="val">{last_str}</div><div class="lbl">Last Commit</div></div>
</div>

<div class="section">
  <div class="section-title">Commit Timeline</div>
  <div class="card">
    {timeline_svg}
  </div>
</div>

<div class="section">
  <div class="two-col">
    <div>
      <div class="section-title">Top Contributors</div>
      <div class="card">
        <table>
          <thead><tr><th></th><th>Author</th><th>Commits</th><th>Lines</th><th>Activity</th></tr></thead>
          <tbody>{contrib_rows}</tbody>
        </table>
      </div>
    </div>
    <div>
      <div class="section-title">Language Breakdown</div>
      <div class="card" style="display:flex;align-items:center;justify-content:center;gap:2rem;flex-wrap:wrap">
        {lang_svg}
        <div>
          {"".join(f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem"><div style="width:12px;height:12px;border-radius:50%;background:hsl({200+i*25},70%,55%)"></div><span style="font-size:0.85rem">{html.escape(ext)}</span><span style="color:#888;font-size:0.8rem">{cnt}</span></div>' for i,(ext,cnt) in enumerate(list(stats.language_breakdown.items())[:8]))}
        </div>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <div class="section-title">Hottest Files</div>
  <div class="card">
    <table>
      <thead><tr><th></th><th>File</th><th>Changes</th><th>Churn</th></tr></thead>
      <tbody>{hot_rows}</tbody>
    </table>
  </div>
</div>

<div class="section">
  <div class="section-title">Project Insights</div>
  <div class="insights-grid">
    {insights_html}
  </div>
</div>

<div class="footer">
  Generated by <strong>Chronicle</strong> — Git Repository Historian
</div>

</body>
</html>"""


import re  # needed by render_html for stripping rich markup
