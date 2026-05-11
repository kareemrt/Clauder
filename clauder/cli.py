"""Click CLI for Clauder."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm

from clauder import __version__
from clauder.analyzer import ClaudeAnalyzer
from clauder.scanner import scan_python_files, get_file_stats, get_git_commits, get_repo_info, aggregate_stats
from clauder.reporter import (
    console,
    render_banner,
    render_analysis,
    render_directory_summary,
    render_git_insights,
)

_err = Console(stderr=True, style="bold red")


def _require_api_key() -> str:
    import os
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        _err.print(
            "[red]Error:[/red] ANTHROPIC_API_KEY environment variable not set.\n"
            "Export it with:  export ANTHROPIC_API_KEY=sk-ant-..."
        )
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(__version__, prog_name="clauder")
def app():
    """Clauder — AI-Powered Code Review Dashboard.

    Powered by Claude (Anthropic). Requires ANTHROPIC_API_KEY to be set.
    """


# ---------------------------------------------------------------------------
# review command
# ---------------------------------------------------------------------------

@app.command("review")
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("--no-banner", is_flag=True, default=False, help="Suppress the ASCII banner")
@click.option("--max-files", default=10, show_default=True, help="Max files to review in directory mode")
def review(path: str, no_banner: bool, max_files: int):
    """Review a Python file or directory with Claude AI.

    PATH can be a single .py file or a directory (defaults to current dir).
    """
    _require_api_key()
    if not no_banner:
        render_banner()

    target = Path(path)
    analyzer = ClaudeAnalyzer()

    if target.is_file():
        _review_single_file(str(target), analyzer)
    else:
        _review_directory(str(target), analyzer, max_files)


def _review_single_file(path: str, analyzer: ClaudeAnalyzer):
    stats = get_file_stats(path)
    console.print(f"\n[bold cyan]Analyzing[/bold cyan] [white]{path}[/white] …\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Claude is reviewing your code…", total=None)
        analysis = analyzer.analyze_file(path)
        progress.update(task, completed=True)

    if analysis.error:
        _err.print(f"[red]Analysis failed:[/red] {analysis.error}")
        sys.exit(1)

    render_analysis(analysis, stats)


def _review_directory(path: str, analyzer: ClaudeAnalyzer, max_files: int):
    files = scan_python_files(path, max_files=max_files)
    if not files:
        console.print(f"[yellow]No Python files found in[/yellow] {path}")
        return

    console.print(
        f"\n[bold cyan]Found {len(files)} Python file(s)[/bold cyan] in [white]{path}[/white]\n"
    )

    analyses = []
    all_stats = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Reviewing files…", total=len(files))
        for f in files:
            progress.update(task, description=f"Reviewing [cyan]{Path(f).name}[/cyan]…")
            stats = get_file_stats(f)
            all_stats.append(stats)
            analysis = analyzer.analyze_file(f)
            analyses.append(analysis)
            progress.advance(task)

    total = aggregate_stats(all_stats)

    # Per-file details
    for analysis in analyses:
        if not analysis.error:
            render_analysis(analysis, get_file_stats(analysis.path))

    # Summary dashboard
    render_directory_summary(analyses, total)


# ---------------------------------------------------------------------------
# chat command
# ---------------------------------------------------------------------------

@app.command("chat")
@click.argument("path", type=click.Path(exists=True))
def chat(path: str):
    """Interactive AI chat about a Python file.

    PATH must be a .py file. Type 'exit' or 'quit' to leave.
    """
    _require_api_key()
    render_banner()

    file_path = Path(path)
    if file_path.suffix != ".py":
        _err.print("[red]Chat mode only supports .py files.[/red]")
        sys.exit(1)

    console.print(
        f"[bold cyan]Chat mode:[/bold cyan] [white]{path}[/white]\n"
        "[dim]Ask anything about this file. Type 'exit' to quit.[/dim]\n"
    )

    analyzer = ClaudeAnalyzer()
    history: list = []
    first = True

    while True:
        try:
            question = Prompt.ask("[bold cyan]You[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if question.strip().lower() in ("exit", "quit", "q"):
            console.print("[dim]Goodbye![/dim]")
            break
        if not question.strip():
            continue

        with Progress(
            SpinnerColumn(),
            TextColumn("[dim]Claude is thinking…[/dim]"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            response = analyzer.chat_about_code(path, question, history if not first else None)

        console.print(f"\n[bold green]Claude[/bold green]\n{response}\n")

        if first:
            history.append({
                "role": "user",
                "content": (
                    f"Here's the Python file `{file_path.name}` I want to discuss:\n\n"
                    f"```python\n{file_path.read_text()[:8000]}\n```\n\n{question}"
                ),
            })
            first = False
        else:
            history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})


# ---------------------------------------------------------------------------
# insights command
# ---------------------------------------------------------------------------

@app.command("insights")
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("--no-ai", is_flag=True, default=False, help="Show raw git log without AI narrative")
def insights(path: str, no_ai: bool):
    """Show AI-powered git commit insights for a repository.

    PATH defaults to the current directory.
    """
    if not no_ai:
        _require_api_key()

    render_banner()

    repo_info = get_repo_info(path)
    commits = get_git_commits(path)

    if not commits:
        console.print("[yellow]No git history found.[/yellow]")
        return

    narrative = ""
    if not no_ai:
        with Progress(
            SpinnerColumn(),
            TextColumn("[dim]Claude is analysing your commit history…[/dim]"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            analyzer = ClaudeAnalyzer()
            narrative = analyzer.generate_git_insights(commits)

    render_git_insights(narrative, commits, repo_info)


# ---------------------------------------------------------------------------
# scan command (no AI, fast)
# ---------------------------------------------------------------------------

@app.command("scan")
@click.argument("path", default=".", type=click.Path(exists=True))
def scan(path: str):
    """Quick metrics scan — no AI required.

    Shows file-by-file statistics for all Python files under PATH.
    """
    from rich.table import Table
    from rich import box as rich_box

    files = scan_python_files(path, max_files=200)
    if not files:
        console.print(f"[yellow]No Python files found in[/yellow] {path}")
        return

    t = Table(
        show_header=True, header_style="bold white",
        box=rich_box.ROUNDED, border_style="dim",
        title=f"[bold]Python Files in {path}[/bold]",
    )
    t.add_column("File", style="cyan")
    t.add_column("Lines", justify="right")
    t.add_column("Code", justify="right")
    t.add_column("Functions", justify="right")
    t.add_column("Classes", justify="right")
    t.add_column("Imports", justify="right")
    t.add_column("Max Line", justify="right")

    total_lines = total_code = total_fns = total_cls = 0

    for f in files:
        s = get_file_stats(f)
        total_lines += s.get("total_lines", 0)
        total_code  += s.get("code_lines", 0)
        total_fns   += s.get("functions", 0)
        total_cls   += s.get("classes", 0)
        t.add_row(
            Path(f).name,
            str(s.get("total_lines", 0)),
            str(s.get("code_lines", 0)),
            str(s.get("functions", 0)),
            str(s.get("classes", 0)),
            str(s.get("imports", 0)),
            str(s.get("max_line_length", 0)),
        )

    console.print(t)
    console.print(
        f"\n[bold]Totals:[/bold] {total_lines} lines · "
        f"{total_code} code · {total_fns} functions · {total_cls} classes"
    )
