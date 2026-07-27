"""CLI entry point for Clauder."""

import os
import sys
from pathlib import Path

import click

from .config import ReviewConfig
from .diff_parser import parse_diff
from .git_utils import (
    diff_branch,
    diff_commit,
    diff_last_n,
    diff_staged,
    get_pr_diff_from_github,
)
from .renderer import render_json, render_markdown, render_terminal
from .reviewer import review_diff


BANNER = r"""
   ______ __    ___   __  ______  ______  ____
  / ____// /   /   | / / / / __ \/ ____/ / __ \
 / /    / /   / /| |/ / / / / / / __/   / /_/ /
/ /___ / /___/ ___ / /_/ / /_/ / /___  / _, _/
\____//_____/_/  |_\____/_____/_____/ /_/ |_|
                                     AI Code Reviewer
"""


def _get_github_token() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


@click.group()
@click.version_option(package_name="clauder")
def cli() -> None:
    """Clauder — AI-powered code review using Claude."""


@cli.command()
@click.option("--mode", "-m", default="full",
              type=click.Choice(["full", "security", "performance", "style", "bugs"]),
              help="Review focus mode.")
@click.option("--model", default="claude-opus-5", help="Claude model to use.")
@click.option("--format", "-f", "output_format",
              default="terminal",
              type=click.Choice(["terminal", "markdown", "json"]),
              help="Output format.")
@click.option("--output", "-o", type=click.Path(), help="Write output to file.")
@click.option("--min-severity", default="info",
              type=click.Choice(["critical", "high", "medium", "low", "info"]),
              help="Minimum severity level to report.")
@click.argument("diff_file", type=click.Path(exists=True), required=False)
def review(mode, model, output_format, output, min_severity, diff_file):
    """Review a diff file, or read from stdin.

    Examples:\n
      clauder review changes.diff\n
      git diff main | clauder review\n
      clauder review --mode security --format markdown
    """
    _print_banner()

    if diff_file:
        raw_diff = Path(diff_file).read_text()
    elif not sys.stdin.isatty():
        raw_diff = sys.stdin.read()
    else:
        click.echo("Error: provide a diff file or pipe diff via stdin.", err=True)
        sys.exit(1)

    config = ReviewConfig(
        mode=mode,
        model=model,
        output_format=output_format,
        min_severity=min_severity,
    )

    _run_review(raw_diff, config, output)


@cli.command()
@click.argument("base", default="main")
@click.argument("head", default="HEAD")
@click.option("--mode", "-m", default="full",
              type=click.Choice(["full", "security", "performance", "style", "bugs"]))
@click.option("--model", default="claude-opus-5")
@click.option("--format", "-f", "output_format", default="terminal",
              type=click.Choice(["terminal", "markdown", "json"]))
@click.option("--output", "-o", type=click.Path())
@click.option("--repo", "-r", default=".", help="Path to git repository.")
def branch(base, head, mode, model, output_format, output, repo):
    """Review changes between two git branches.

    Examples:\n
      clauder branch main feature/my-change\n
      clauder branch develop HEAD --mode security
    """
    _print_banner()
    raw_diff = diff_branch(base, head, repo_path=repo)
    config = ReviewConfig(mode=mode, model=model, output_format=output_format)
    _run_review(raw_diff, config, output)


@cli.command()
@click.argument("repo")
@click.argument("pr_number", type=int)
@click.option("--mode", "-m", default="full",
              type=click.Choice(["full", "security", "performance", "style", "bugs"]))
@click.option("--model", default="claude-opus-5")
@click.option("--format", "-f", "output_format", default="terminal",
              type=click.Choice(["terminal", "markdown", "json"]))
@click.option("--output", "-o", type=click.Path())
@click.option("--token", envvar="GITHUB_TOKEN", default=None,
              help="GitHub personal access token.")
def pr(repo, pr_number, mode, model, output_format, output, token):
    """Review a GitHub pull request.

    Examples:\n
      clauder pr owner/repo 42\n
      clauder pr owner/repo 42 --mode bugs --format markdown
    """
    _print_banner()
    token = token or _get_github_token()
    click.echo(f"Fetching PR #{pr_number} from {repo}...")
    raw_diff = get_pr_diff_from_github(repo, pr_number, token)
    config = ReviewConfig(
        mode=mode,
        model=model,
        output_format=output_format,
        github_token=token,
    )
    _run_review(raw_diff, config, output)


@cli.command()
@click.option("--mode", "-m", default="full",
              type=click.Choice(["full", "security", "performance", "style", "bugs"]))
@click.option("--model", default="claude-opus-5")
@click.option("--format", "-f", "output_format", default="terminal",
              type=click.Choice(["terminal", "markdown", "json"]))
@click.option("--output", "-o", type=click.Path())
@click.option("--repo", "-r", default=".", help="Path to git repository.")
def staged(mode, model, output_format, output, repo):
    """Review currently staged changes (git diff --cached).

    Examples:\n
      git add -p && clauder staged\n
      clauder staged --mode security
    """
    _print_banner()
    raw_diff = diff_staged(repo_path=repo)
    if not raw_diff.strip():
        click.echo("No staged changes found. Run 'git add' first.")
        sys.exit(0)
    config = ReviewConfig(mode=mode, model=model, output_format=output_format)
    _run_review(raw_diff, config, output)


@cli.command()
@click.argument("commit", required=False)
@click.option("-n", "last_n", default=1, help="Review last N commits.")
@click.option("--mode", "-m", default="full",
              type=click.Choice(["full", "security", "performance", "style", "bugs"]))
@click.option("--model", default="claude-opus-5")
@click.option("--format", "-f", "output_format", default="terminal",
              type=click.Choice(["terminal", "markdown", "json"]))
@click.option("--output", "-o", type=click.Path())
@click.option("--repo", "-r", default=".")
def commit(commit, last_n, mode, model, output_format, output, repo):
    """Review a specific commit or the last N commits.

    Examples:\n
      clauder commit abc123f\n
      clauder commit -n 3
    """
    _print_banner()
    if commit:
        raw_diff = diff_commit(commit, repo_path=repo)
    else:
        raw_diff = diff_last_n(last_n, repo_path=repo)
    config = ReviewConfig(mode=mode, model=model, output_format=output_format)
    _run_review(raw_diff, config, output)


def _print_banner() -> None:
    try:
        from rich.console import Console
        from rich.text import Text
        console = Console()
        text = Text(BANNER, style="bold cyan")
        console.print(text)
    except ImportError:
        print(BANNER)


def _run_review(raw_diff: str, config: ReviewConfig, output_file: str | None) -> None:
    if not raw_diff.strip():
        click.echo("Empty diff — nothing to review.")
        sys.exit(0)

    parsed = parse_diff(raw_diff)
    click.echo(
        f"Reviewing {len(parsed.files)} file(s) "
        f"(+{parsed.total_added} / -{parsed.total_removed} lines) "
        f"with {config.model}...",
        err=True,
    )

    result = review_diff(parsed, config)

    if config.output_format == "json":
        text = render_json(result)
        _write_or_print(text, output_file)
    elif config.output_format == "markdown":
        text = render_markdown(result)
        _write_or_print(text, output_file)
    else:
        if output_file:
            text = render_markdown(result)
            _write_or_print(text, output_file)
        else:
            render_terminal(result, config)


def _write_or_print(text: str, output_file: str | None) -> None:
    if output_file:
        Path(output_file).write_text(text)
        click.echo(f"Review written to {output_file}")
    else:
        click.echo(text)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
