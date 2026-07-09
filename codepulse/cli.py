"""
CodePulse CLI entry point.
"""
import sys
from datetime import datetime
from pathlib import Path

try:
    import click
except ImportError:
    print("CodePulse requires 'click'. Install with: pip install click")
    sys.exit(1)

from .analyzer import GitAnalyzer
from . import visualizer as viz
from .reporter import generate_markdown_report


@click.command()
@click.argument("repo_path", default=".", metavar="[REPO_PATH]")
@click.option("-n", "--max-commits", default=500, show_default=True,
              help="Maximum number of commits to analyze.")
@click.option("--top-files", default=15, show_default=True,
              help="Number of top-churned files to show.")
@click.option("--report", is_flag=True, default=False,
              help="Also write a Markdown report to CODEPULSE_REPORT.md.")
@click.option("--report-path", default="CODEPULSE_REPORT.md", show_default=True,
              help="Path for the Markdown report output.")
@click.option("--no-color", is_flag=True, default=False,
              help="Disable ANSI colors (useful for piping).")
@click.version_option("1.0.0", prog_name="codepulse")
def main(repo_path, max_commits, top_files, report, report_path, no_color):
    """
    💓 CodePulse — Git Repository Health Visualizer

    Analyzes a git repository and renders beautiful terminal visualizations
    of code health: commit patterns, file churn hotspots, contributor stats,
    activity heatmaps, and more.

    REPO_PATH defaults to the current directory.

    Examples:

    \b
      codepulse .
      codepulse /path/to/my/repo --report
      codepulse . --max-commits 1000 --top-files 20
    """
    if no_color:
        import os
        os.environ["NO_COLOR"] = "1"

    # ── Load and analyze ──────────────────────────────────────────────────
    try:
        analyzer = GitAnalyzer(repo_path)
    except ValueError as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)
        sys.exit(1)

    repo_name = analyzer.get_repo_name()
    click.echo(f"\n{viz.bold(viz.cyan('💓 CodePulse'))} — analyzing {viz.bold(repo_name)} …\n")

    commits = analyzer.get_commits(max_commits=max_commits)
    if not commits:
        click.echo(viz.yellow("  No commits found in this repository."))
        sys.exit(0)

    file_stats    = analyzer.get_file_stats(commits)
    contributors  = analyzer.get_contributor_stats(commits)
    monthly       = analyzer.get_activity_by_month(commits)
    hourly        = analyzer.get_activity_by_hour(commits)
    weekday       = analyzer.get_activity_by_weekday(commits)

    # ── Compute summary stats ─────────────────────────────────────────────
    dates = sorted(c.date for c in commits)
    first, last = dates[0], dates[-1]
    delta = last - first
    years  = delta.days // 365
    months = (delta.days % 365) // 30
    age_str = (f"{years}y {months}m" if years else f"{months}m {delta.days % 30}d") if delta.days else "< 1 day"

    active_days = len({c.date.date() for c in commits})

    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        peak_wd = max(weekday, key=weekday.get)
        most_active_day = weekday_names[peak_wd]
    except (ValueError, KeyError):
        most_active_day = "N/A"

    summary = {
        "total_commits": len(commits),
        "contributors":  len(contributors),
        "files_changed": len(file_stats),
        "insertions":    sum(c.insertions for c in commits),
        "deletions":     sum(c.deletions for c in commits),
        "active_days":   active_days,
        "age":           age_str,
        "most_active_day": most_active_day,
    }

    # ── Render sections ───────────────────────────────────────────────────
    click.echo(viz.header("REPOSITORY OVERVIEW"))
    click.echo(viz.summary_box(summary))

    click.echo(viz.header("CONTRIBUTION HEATMAP"))
    click.echo(viz.activity_heatmap(commits))

    click.echo(viz.header("HOURLY ACTIVITY PATTERN"))
    click.echo(viz.hourly_chart(hourly))

    click.echo(viz.header("WEEKLY RHYTHM"))
    click.echo(viz.weekday_chart(weekday))

    click.echo(viz.header("COMMIT TYPE BREAKDOWN"))
    click.echo(viz.commit_type_breakdown(commits))

    click.echo(viz.header("TOP CONTRIBUTORS"))
    click.echo(viz.contributor_table(contributors))

    click.echo(viz.header(f"🔥 HOTSPOT FILES (top {top_files})"))
    click.echo(viz.top_files_table(file_stats, top_n=top_files))

    click.echo(viz.header("LANGUAGE BREAKDOWN (by churn)"))
    lang_data = analyzer.get_language_breakdown(file_stats)
    click.echo(viz.bar_chart(lang_data, top_n=12, color_fn=viz.yellow))

    click.echo(viz.header("MONTHLY COMMIT TREND"))
    monthly_vals = list(monthly.values())
    months_list  = list(monthly.keys())
    spark = viz.sparkline(monthly_vals, width=60)
    click.echo(f"  {months_list[0] if months_list else ''}  {spark}  {months_list[-1] if months_list else ''}")
    peak_month = max(monthly, key=monthly.get) if monthly else "N/A"
    click.echo(f"\n  Peak month: {viz.bold(peak_month)} ({viz.green(str(monthly.get(peak_month, 0)))} commits)\n")

    # ── Optional Markdown report ──────────────────────────────────────────
    if report:
        generate_markdown_report(
            repo_name=repo_name,
            commits=commits,
            file_stats=file_stats,
            contributors=contributors,
            monthly=monthly,
            summary=summary,
            output_path=report_path,
        )
        click.echo(viz.green(f"\n  ✅ Markdown report written to: {report_path}\n"))

    click.echo(viz.dim(f"\n  Analyzed {len(commits)} commits across {active_days} active days.\n"))
