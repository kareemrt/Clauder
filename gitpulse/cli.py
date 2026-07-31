"""Command-line interface for GitPulse."""

import argparse
import sys
import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from .analyzer import get_repo_name, parse_commits, parse_file_changes, compute_stats
from .reporter import generate_html

console = Console()

_DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _sparkline(counts: list[int], width: int = 20) -> str:
    blocks = "▁▂▃▄▅▆▇█"
    if not counts or max(counts) == 0:
        return "▁" * width
    m = max(counts)
    return "".join(blocks[min(7, int(v / m * 7))] for v in counts[-width:])


def print_summary(repo_name: str, stats: dict) -> None:
    if not stats:
        console.print("[red]No commits found.[/red]")
        return

    start_dt, end_dt = stats["date_range"]
    span_days = (end_dt - start_dt).days + 1

    console.print()
    console.print(
        Panel(
            f"[bold cyan]⚡ GitPulse[/bold cyan]  ·  [bold]{repo_name}[/bold]\n"
            f"[dim]{start_dt.strftime('%Y-%m-%d')} → {end_dt.strftime('%Y-%m-%d')}  "
            f"({span_days:,} days)[/dim]",
            border_style="cyan",
            padding=(0, 2),
        )
    )

    # ── Key stats ────────────────────────────────────────────────────────────
    stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    stats_table.add_column(style="dim")
    stats_table.add_column(style="bold green")
    stats_table.add_row("Total commits", f"{stats['total_commits']:,}")
    stats_table.add_row("Contributors", f"{stats['total_authors']:,}")
    stats_table.add_row("Active days", f"{len(stats['by_date']):,}")
    stats_table.add_row(
        "Avg commits/day", f"{stats['total_commits'] / max(span_days, 1):.2f}"
    )
    console.print(stats_table)

    # ── Top contributors ──────────────────────────────────────────────────────
    if stats["by_author"]:
        console.print("[bold]Top contributors[/bold]")
        top = stats["by_author"][:8]
        max_c = top[0][1]
        for author, count in top:
            bar_len = int(count / max_c * 28)
            bar = "█" * bar_len + "░" * (28 - bar_len)
            console.print(f"  [cyan]{author:<22}[/cyan] {bar} [dim]{count:>5}[/dim]")
        console.print()

    # ── Day-of-week sparkline ────────────────────────────────────────────────
    dow_vals = [stats["by_dow"].get(i, 0) for i in range(7)]
    spark = _sparkline(dow_vals, 7)
    dow_labels = "  ".join(_DOW)
    console.print(f"[bold]Activity by weekday[/bold]\n  {spark}\n  [dim]{dow_labels}[/dim]\n")

    # ── Hour-of-day sparkline ────────────────────────────────────────────────
    hour_vals = [stats["by_hour"].get(i, 0) for i in range(24)]
    hour_spark = _sparkline(hour_vals, 24)
    console.print(f"[bold]Activity by hour (UTC)[/bold]\n  {hour_spark}\n  [dim]00              12              23[/dim]\n")

    # ── Hottest files ─────────────────────────────────────────────────────────
    if stats["top_files"]:
        console.print("[bold]Hottest files[/bold]")
        for i, (f, v) in enumerate(stats["top_files"][:8], 1):
            short = f if len(f) <= 48 else "…" + f[-47:]
            console.print(f"  [dim]{i:>2}.[/dim] [yellow]{short:<50}[/yellow] [dim]{v:>4}x[/dim]")
        console.print()


def main():
    parser = argparse.ArgumentParser(
        prog="gitpulse",
        description="⚡ GitPulse — beautiful git repository analytics",
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write HTML report to this file (default: <repo>-gitpulse.html)",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML report; print summary only",
    )
    args = parser.parse_args()

    repo_path = str(Path(args.repo).resolve())

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        t = progress.add_task("Parsing git log …", total=None)
        commits = parse_commits(repo_path)
        progress.update(t, description="Analyzing file changes …")
        file_changes = parse_file_changes(repo_path)
        progress.update(t, description="Computing statistics …")
        stats = compute_stats(commits, file_changes)
        repo_name = get_repo_name(repo_path)

    print_summary(repo_name, stats)

    if not args.no_html and stats:
        out_path = args.output or f"{repo_name.replace('/', '-')}-gitpulse.html"
        html_content = generate_html(repo_name, stats)
        Path(out_path).write_text(html_content, encoding="utf-8")
        console.print(
            f"[bold green]✓[/bold green] HTML report saved → [cyan]{out_path}[/cyan]\n"
        )


if __name__ == "__main__":
    main()
