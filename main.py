#!/usr/bin/env python3
"""Clauder: The Oracle — AI-powered code review CLI."""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


def _get_api_key(api_key: Optional[str]) -> Optional[str]:
    return api_key or os.environ.get("ANTHROPIC_API_KEY")


@click.group()
@click.version_option("1.0.0", prog_name="clauder")
def cli():
    """
    \b
    ✦  Clauder: The Oracle  ✦
    AI-powered code review with mystical insight.

    Consult the Oracle to reveal your code's destiny.
    """


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--save", "-s", type=click.Path(), default=None, help="Save review to JSON file")
@click.option("--api-key", envvar="ANTHROPIC_API_KEY", help="Anthropic API key")
@click.option("--no-banner", is_flag=True, default=False, help="Skip the Oracle banner")
def review(file_path: str, save: Optional[str], api_key: Optional[str], no_banner: bool):
    """Consult The Oracle to review a source code file."""
    from clauder.display import (
        print_banner, print_scanning, print_full_review, save_review
    )
    from clauder.analyzer import analyze_file, read_file_content, detect_language
    from clauder.oracle import consult_oracle

    key = _get_api_key(api_key)
    if not key:
        console.print(
            "[bold red]Error:[/bold red] No API key found. "
            "Set ANTHROPIC_API_KEY or use --api-key."
        )
        sys.exit(1)

    if not no_banner:
        print_banner()

    print_scanning(file_path)

    # Analyze file metrics
    metrics = analyze_file(file_path)
    code = read_file_content(file_path)
    language = detect_language(file_path) if metrics is None else metrics.language

    if not code:
        console.print(f"[red]Cannot read file: {file_path}[/red]")
        sys.exit(1)

    # Consult The Oracle
    with Progress(
        SpinnerColumn(spinner_name="moon"),
        TextColumn("[bright_magenta]The Oracle contemplates your code...[/bright_magenta]"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("oracle", total=None)
        try:
            review_result = consult_oracle(
                code=code,
                file_path=file_path,
                metrics=metrics,
                language=language,
                api_key=key,
            )
        except Exception as e:
            console.print(f"[red]Oracle error:[/red] {e}")
            sys.exit(1)

    print_full_review(review_result, metrics, file_path)

    if save:
        save_review(review_result, metrics, file_path, save)


@cli.command()
@click.option("--api-key", envvar="ANTHROPIC_API_KEY", help="Anthropic API key")
@click.option("--no-banner", is_flag=True, default=False, help="Skip the Oracle banner")
def scan(api_key: Optional[str], no_banner: bool):
    """Scan all Python files in the current directory and summarize findings."""
    from clauder.display import print_banner, print_scanning, print_full_review
    from clauder.analyzer import analyze_file, read_file_content, detect_language
    from clauder.oracle import consult_oracle
    from rich.table import Table
    from rich import box

    key = _get_api_key(api_key)
    if not key:
        console.print("[bold red]Error:[/bold red] No API key. Set ANTHROPIC_API_KEY.")
        sys.exit(1)

    if not no_banner:
        print_banner()

    py_files = list(Path(".").rglob("*.py"))
    if not py_files:
        console.print("[yellow]No Python files found in current directory.[/yellow]")
        return

    console.print(f"\n[dim]Found [bold]{len(py_files)}[/bold] Python files to scan.[/dim]\n")

    scores = []
    for fp in py_files:
        if any(part.startswith(".") for part in fp.parts):
            continue
        console.print(f"  [dim]⟳[/dim] Scanning [cyan]{fp}[/cyan]...")
        metrics = analyze_file(str(fp))
        code = read_file_content(str(fp))
        if not code or len(code.strip()) < 10:
            continue
        try:
            result = consult_oracle(str(fp), str(fp), metrics, "Python", key)
            scores.append((str(fp), result.get("score", 0), result.get("verdict", "MUNDANE")))
        except Exception as e:
            console.print(f"    [red]Error:[/red] {e}")

    if not scores:
        console.print("[yellow]No files could be reviewed.[/yellow]")
        return

    console.print()
    table = Table(title="✦ Oracle Scan Results ✦", box=box.ROUNDED, border_style="bright_magenta")
    table.add_column("File", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Verdict", style="bold")

    verdict_colors = {
        "TRANSCENDENT": "bright_cyan",
        "BLESSED": "bright_green",
        "ENCHANTED": "bright_yellow",
        "MUNDANE": "dim white",
        "CURSED": "bright_red",
    }

    for fp, score, verdict in sorted(scores, key=lambda x: x[1], reverse=True):
        color = verdict_colors.get(verdict, "white")
        table.add_row(fp, str(score), f"[{color}]{verdict}[/{color}]")

    avg = sum(s for _, s, _ in scores) / len(scores)
    console.print(table)
    console.print(f"\n[dim]Average score: [bold]{avg:.1f}/100[/bold] across {len(scores)} files[/dim]\n")


@cli.command()
@click.argument("code_snippet")
@click.option("--api-key", envvar="ANTHROPIC_API_KEY", help="Anthropic API key")
def prophecy(code_snippet: str, api_key: Optional[str]):
    """Get a quick Oracle prophecy for a code snippet (pass code as argument or '-' for stdin)."""
    from clauder.oracle import quick_prophecy
    from rich.panel import Panel

    key = _get_api_key(api_key)
    if not key:
        console.print("[bold red]Error:[/bold red] No API key. Set ANTHROPIC_API_KEY.")
        sys.exit(1)

    if code_snippet == "-":
        code_snippet = sys.stdin.read()

    with Progress(
        SpinnerColumn(spinner_name="moon"),
        TextColumn("[bright_magenta]The Oracle speaks...[/bright_magenta]"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("oracle", total=None)
        result = quick_prophecy(code_snippet, key)

    console.print()
    console.print(
        Panel(
            f"[italic bright_yellow]{result}[/italic bright_yellow]",
            title="[bold bright_magenta]✦  Oracle's Prophecy  ✦[/bold bright_magenta]",
            border_style="bright_magenta",
            padding=(1, 3),
        )
    )
    console.print()


if __name__ == "__main__":
    cli()
