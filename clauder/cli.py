"""Clauder CLI — AI-powered code review in your terminal."""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import ReviewConfig
from .formatter import render_terminal, render_markdown, render_json
from .git_utils import (
    GitError,
    get_staged_diff,
    get_all_diff,
    get_commit_diff,
    get_branch_diff,
    get_current_branch,
    get_recent_commits,
)
from .reviewer import review_diff, review_files

console = Console()
err_console = Console(stderr=True)


def _run_review(diff_or_files, is_files: bool, config: ReviewConfig, output: str, save: str | None, context: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=err_console,
        transient=True,
    ) as progress:
        progress.add_task("Reviewing with Claude...", total=None)
        if is_files:
            result = review_files(diff_or_files, config, context)
        else:
            result = review_diff(diff_or_files, config, context)

    if output == "terminal":
        render_terminal(result, console)
    elif output == "markdown":
        md = render_markdown(result)
        console.print(md)
    elif output == "json":
        console.print(render_json(result))

    if save:
        ext = Path(save).suffix.lower()
        if ext == ".json":
            content = render_json(result)
        else:
            content = render_markdown(result)
        Path(save).write_text(content, encoding="utf-8")
        console.print(f"\n[dim]Report saved to[/] [bold]{save}[/]")

    sys.exit(1 if result.critical_count > 0 or result.high_count > 0 else 0)


@click.group()
@click.version_option(package_name="clauder")
def main():
    """Clauder ☁  — AI-powered code review powered by Claude."""


@main.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--staged/--no-staged", default=False, help="Review only staged git changes.")
@click.option("--all", "all_changes", is_flag=True, help="Review all changes (staged + unstaged).")
@click.option("--commit", metavar="SHA", help="Review a specific commit.")
@click.option("--branch", metavar="BASE", help="Review changes vs a base branch (default: main).")
@click.option("--output", "-o", type=click.Choice(["terminal", "markdown", "json"]), default="terminal")
@click.option("--save", "-s", metavar="FILE", help="Save report to a file (.md or .json).")
@click.option("--context", "-c", metavar="TEXT", default="", help="Optional context about what this change is for.")
@click.option("--model", default=None, help="Override Claude model (e.g. claude-opus-4-8).")
def review(files, staged, all_changes, commit, branch, output, save, context, model):
    """Review code changes with Claude AI.

    \b
    Examples:
      clauder review                    # review staged changes
      clauder review --all              # review all changes
      clauder review --commit abc123    # review a specific commit
      clauder review --branch main      # review changes vs main branch
      clauder review src/app.py         # review specific files
      clauder review --output markdown  # output as markdown
      clauder review --save report.md   # save report to file
    """
    config = ReviewConfig.from_env()
    if model:
        config.model = model

    try:
        config.validate()
    except ValueError as e:
        err_console.print(f"[bold red]Error:[/] {e}")
        sys.exit(2)

    try:
        if files:
            _run_review(list(files), is_files=True, config=config, output=output, save=save, context=context)
        elif commit:
            diff = get_commit_diff(commit)
            _run_review(diff, is_files=False, config=config, output=output, save=save, context=context)
        elif branch:
            diff = get_branch_diff(branch)
            _run_review(diff, is_files=False, config=config, output=output, save=save, context=context)
        elif all_changes:
            diff = get_all_diff()
            _run_review(diff, is_files=False, config=config, output=output, save=save, context=context)
        else:
            diff = get_staged_diff()
            if not diff.strip():
                console.print("[yellow]No staged changes found.[/] Try [bold]--all[/] to review all changes, or stage some files first.")
                sys.exit(0)
            _run_review(diff, is_files=False, config=config, output=output, save=save, context=context)

    except GitError as e:
        err_console.print(f"[bold red]Git error:[/] {e}")
        sys.exit(2)
    except Exception as e:
        err_console.print(f"[bold red]Error:[/] {e}")
        sys.exit(2)


@main.command()
def status():
    """Show recent commits and current branch."""
    try:
        branch = get_current_branch()
        commits = get_recent_commits(5)
    except GitError as e:
        err_console.print(f"[bold red]Git error:[/] {e}")
        sys.exit(1)

    console.print()
    console.print(f"[bold cyan]Branch:[/] [bold]{branch}[/]")
    console.print()
    console.print("[bold]Recent commits:[/]")
    for c in commits:
        console.print(f"  [dim]{c['sha']}[/]  [bold]{c['message']}[/]  [dim]{c['author']} · {c['when']}[/]")
    console.print()


if __name__ == "__main__":
    main()
