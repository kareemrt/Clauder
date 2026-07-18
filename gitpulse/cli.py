"""GitPulse CLI entry point."""

import sys
import os
from pathlib import Path

import click
from rich.console import Console
from rich.text import Text

from .analyzer import (
    get_repo_name,
    get_commits,
    get_file_churn,
    get_file_stats,
    get_co_change_pairs,
    build_heatmap,
    build_velocity,
    author_stats,
    peak_hours,
    summary_stats,
)
from .charts import (
    render_summary_panel,
    render_heatmap,
    render_velocity_chart,
    render_bar_chart,
    render_author_table,
    render_peak_hours,
    render_language_pie,
    render_co_change,
)
from .report import generate_html_report


BANNER = r"""
  ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
 ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
 ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
 ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
 ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
  ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
        Terminal Analytics Dashboard for Git Repositories
"""


@click.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--limit", "-l", default=2000, show_default=True, help="Max commits to analyse.")
@click.option("--weeks", "-w", default=52, show_default=True, help="Heatmap weeks to display.")
@click.option("--export", "-e", is_flag=True, help="Export HTML report.")
@click.option("--output", "-o", default="gitpulse_report.html", show_default=True, help="HTML output path.")
@click.option("--no-banner", is_flag=True, help="Skip the ASCII banner.")
def main(repo_path, limit, weeks, export, output, no_banner):
    """Analyse a git repository and render a beautiful terminal dashboard.

    REPO_PATH defaults to the current directory.
    """
    console = Console()

    if not no_banner:
        console.print(Text(BANNER, style="bold bright_cyan"))

    repo_path = str(Path(repo_path).resolve())

    # Verify it's a git repo
    git_dir = os.path.join(repo_path, ".git")
    if not os.path.exists(git_dir):
        console.print(f"[red]✗ Not a git repository:[/red] {repo_path}")
        sys.exit(1)

    with console.status("[cyan]Mining git history…[/cyan]", spinner="dots"):
        repo_name = get_repo_name(repo_path)
        commits = get_commits(repo_path, limit=limit)

    if not commits:
        console.print("[yellow]⚠ No commits found (or repository is empty).[/yellow]")
        sys.exit(0)

    with console.status("[cyan]Analysing file churn…[/cyan]", spinner="dots"):
        churn = get_file_churn(repo_path, limit=limit)
        ext_counter = get_file_stats(repo_path)

    with console.status("[cyan]Computing statistics…[/cyan]", spinner="dots"):
        stats = summary_stats(commits, churn, repo_path)
        authors = author_stats(commits)
        hours = peak_hours(commits)
        grid, w, grid_start = build_heatmap(commits, weeks=weeks)
        vel_counts, vel_labels = build_velocity(commits)

    with console.status("[cyan]Computing co-change pairs…[/cyan]", spinner="dots"):
        pairs = get_co_change_pairs(repo_path, limit=min(limit, 1000))

    # ── Render ──────────────────────────────────────────────────────────
    render_summary_panel(console, stats, repo_name)

    console.print("\n[bold cyan]Contribution Heatmap (last 52 weeks)[/bold cyan]")
    render_heatmap(console, grid, weeks, grid_start)

    render_velocity_chart(console, vel_counts, vel_labels, title="Commit Velocity Over Time")
    render_bar_chart(console, churn.most_common(15), "🔥 Most Changed Files", color="bright_red", unit="changes")
    render_author_table(console, authors)
    render_language_pie(console, ext_counter)
    render_peak_hours(console, hours)
    render_co_change(console, pairs)

    # ── HTML Export ──────────────────────────────────────────────────────
    if export:
        with console.status(f"[cyan]Writing HTML report → {output}…[/cyan]"):
            html = generate_html_report(
                repo_name=repo_name,
                stats=stats,
                commits=commits,
                churn=churn,
                author_data=authors,
                ext_counter=ext_counter,
                grid=grid,
                weeks=weeks,
                grid_start=grid_start,
                velocity_counts=vel_counts,
                velocity_labels=vel_labels,
                pairs=pairs,
            )
            with open(output, "w", encoding="utf-8") as f:
                f.write(html)
        console.print(f"\n[bold green]✓ HTML report saved:[/bold green] [link]{output}[/link]")

    console.print("\n[dim]⚡ GitPulse complete.[/dim]\n")
