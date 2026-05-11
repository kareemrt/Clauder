"""Rich terminal UI for Clauder analysis output."""

from pathlib import Path

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = Console(highlight=False)

BANNER = r"""
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|
"""

GRADE_STYLES = {
    "A+": ("bold bright_green", "bright_green"),
    "A":  ("bold green",        "green"),
    "B+": ("bold cyan",         "cyan"),
    "B":  ("bold blue",         "blue"),
    "C":  ("bold yellow",       "yellow"),
    "D":  ("bold orange1",      "orange1"),
    "F":  ("bold red",          "red"),
}

SEVERITY_COLOR = {
    "critical": "bold red",
    "high":     "red",
    "medium":   "yellow",
    "low":      "dim white",
}

SEVERITY_ICON = {
    "critical": "🚨",
    "high":     "🔴",
    "medium":   "🟡",
    "low":      "⚪",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _score_bar(score: float, width: int = 20) -> Text:
    filled = max(0, min(width, int((score / 10) * width)))
    color = "green" if score >= 8 else "yellow" if score >= 6 else "orange1" if score >= 4 else "red"
    bar = Text()
    bar.append("█" * filled, style=f"bold {color}")
    bar.append("░" * (width - filled), style="dim")
    bar.append(f"  {score:.1f}/10", style=f"bold {color}")
    return bar


def _grade_panel(grade: str) -> Panel:
    text_style, border = GRADE_STYLES.get(grade, ("bold white", "white"))
    return Panel(
        Align(Text(f"\n{grade}", style=text_style, justify="center"), align="center"),
        title="[dim]Grade[/dim]",
        border_style=border,
        width=13,
        height=5,
    )


# ---------------------------------------------------------------------------
# Public renderers
# ---------------------------------------------------------------------------

def render_banner() -> None:
    console.print(Text(BANNER, style="bold cyan"), justify="center")
    console.print(
        "[dim]AI-Powered Code Review Dashboard[/dim]  ·  "
        "[dim cyan]Powered by Claude[/dim cyan]",
        justify="center",
    )
    console.print()


def render_file_header(path: str, stats: dict) -> None:
    name = Path(path).name
    row = Table.grid(padding=(0, 2))
    for _ in range(5):
        row.add_column()
    row.add_row(
        f"[dim]Lines[/dim] [bold white]{stats.get('total_lines', 0)}[/bold white]",
        f"[dim]Code[/dim] [bold cyan]{stats.get('code_lines', 0)}[/bold cyan]",
        f"[dim]Functions[/dim] [bold blue]{stats.get('functions', 0)}[/bold blue]",
        f"[dim]Classes[/dim] [bold magenta]{stats.get('classes', 0)}[/bold magenta]",
        f"[dim]Imports[/dim] [bold yellow]{stats.get('imports', 0)}[/bold yellow]",
    )
    console.print(Panel(
        row,
        title=f"[bold cyan]📄 {name}[/bold cyan]",
        subtitle=f"[dim]{path}[/dim]",
        border_style="cyan",
    ))


def render_analysis(analysis, stats: dict = None) -> None:
    """Render a full single-file analysis report."""
    _, border = GRADE_STYLES.get(analysis.grade, ("bold white", "white"))

    console.print(Rule(f"[bold cyan]Analysis: {Path(analysis.path).name}[/bold cyan]"))
    console.print()

    # --- Top row: grade + score + summary ---
    score_grid = Table.grid(padding=(0, 1))
    score_grid.add_row("Quality:", _score_bar(analysis.quality_score))
    score_grid.add_row()
    score_grid.add_row(Text(analysis.summary, style="italic"))

    top = Table.grid(padding=(0, 2), expand=True)
    top.add_column(width=15)
    top.add_column(ratio=1)
    top.add_row(_grade_panel(analysis.grade), score_grid)
    console.print(top)
    console.print()

    # --- File stats row ---
    if stats:
        items = [
            f"[dim]Lines[/dim] [bold]{stats.get('total_lines', 0)}[/bold]",
            f"[dim]Code[/dim] [bold cyan]{stats.get('code_lines', 0)}[/bold cyan]",
            f"[dim]Functions[/dim] [bold blue]{stats.get('functions', 0)}[/bold blue]",
            f"[dim]Classes[/dim] [bold magenta]{stats.get('classes', 0)}[/bold magenta]",
            f"[dim]Comments[/dim] [bold green]{stats.get('comment_lines', 0)}[/bold green]",
        ]
        console.print(Columns(
            [Panel(item, border_style="dim", padding=(0, 1)) for item in items],
            equal=True,
        ))
        console.print()

    # --- Bugs ---
    if analysis.bugs:
        t = Table(
            show_header=True, header_style="bold white",
            border_style="red", box=box.ROUNDED,
            title=f"[bold red]Bugs & Issues ({len(analysis.bugs)})[/bold red]",
            expand=True,
        )
        t.add_column("Severity", width=14)
        t.add_column("Line", width=6, justify="right")
        t.add_column("Description", ratio=3)
        t.add_column("Suggested Fix", ratio=2, style="dim green")
        for bug in analysis.bugs:
            sev = bug.get("severity", "low")
            icon = SEVERITY_ICON.get(sev, "⚪")
            t.add_row(
                Text(f"{icon} {sev.upper()}", style=SEVERITY_COLOR.get(sev, "white")),
                str(bug.get("line", "?")),
                bug.get("description", ""),
                bug.get("fix", ""),
            )
        console.print(t)
        console.print()

    # --- Security ---
    if analysis.security_concerns:
        t = Table(
            show_header=True, header_style="bold white",
            border_style="red", box=box.ROUNDED,
            title=f"[bold red]Security Concerns ({len(analysis.security_concerns)})[/bold red]",
            expand=True,
        )
        t.add_column("Severity", width=14)
        t.add_column("Description", ratio=1)
        for concern in analysis.security_concerns:
            sev = concern.get("severity", "medium")
            icon = SEVERITY_ICON.get(sev, "⚪")
            t.add_row(
                Text(f"{icon} {sev.upper()}", style=SEVERITY_COLOR.get(sev, "white")),
                concern.get("description", ""),
            )
        console.print(t)
        console.print()

    # --- Strengths & Improvements side by side ---
    strengths_text = "\n".join(f"[bold green]✓[/bold green] {s}" for s in analysis.strengths) \
        or "[dim]None identified[/dim]"
    improvements_text = "\n".join(f"[bold yellow]→[/bold yellow] {i}" for i in analysis.improvements) \
        or "[dim]None identified[/dim]"
    console.print(Columns([
        Panel(strengths_text,    title="[bold green]Strengths[/bold green]",    border_style="green"),
        Panel(improvements_text, title="[bold yellow]Improvements[/bold yellow]", border_style="yellow"),
    ], equal=True))
    console.print()

    # --- Complexity hotspots ---
    if analysis.complexity_hotspots:
        t = Table(
            show_header=True, header_style="bold white",
            border_style="yellow", box=box.ROUNDED,
            title="[bold yellow]Complexity Hotspots[/bold yellow]",
            expand=True,
        )
        t.add_column("Function / Class", style="bold cyan", ratio=1)
        t.add_column("Issue", ratio=2)
        t.add_column("Suggestion", ratio=2, style="dim")
        for hs in analysis.complexity_hotspots:
            t.add_row(hs.get("name", "?"), hs.get("issue", ""), hs.get("suggestion", ""))
        console.print(t)
        console.print()

    # --- Documentation gaps ---
    if analysis.documentation_gaps:
        lines = "\n".join(
            f"[dim]📝[/dim] [bold]{g.get('item', '')}[/bold]: {g.get('recommendation', '')}"
            for g in analysis.documentation_gaps
        )
        console.print(Panel(lines, title="[bold blue]Documentation Gaps[/bold blue]", border_style="blue"))
        console.print()

    # --- Patterns used ---
    if analysis.patterns_used:
        patterns = "  ".join(f"[bold cyan]{p}[/bold cyan]" for p in analysis.patterns_used)
        console.print(Panel(patterns, title="[bold dim]Patterns & Practices[/bold dim]", border_style="dim"))
        console.print()


def render_directory_summary(analyses: list, total_stats: dict) -> None:
    """Render aggregated project dashboard."""
    valid = [a for a in analyses if not a.error]
    if not valid:
        console.print("[red]No files could be analyzed.[/red]")
        return

    avg_score = sum(a.quality_score for a in valid) / len(valid)
    total_bugs = sum(len(a.bugs) for a in valid)
    critical = sum(
        sum(1 for b in a.bugs if b.get("severity") in ("critical", "high"))
        for a in valid
    )

    console.print(Rule("[bold cyan]📊 Project Summary Dashboard[/bold cyan]"))
    console.print()

    metrics = [
        Panel(
            Align(
                f"[bold white]{len(valid)}[/bold white]\n[dim]files reviewed[/dim]",
                align="center",
            ),
            border_style="cyan", width=20,
        ),
        Panel(
            Align(
                f"{_score_bar(avg_score, 14)}\n[dim]average quality[/dim]",
                align="center",
            ),
            border_style="cyan", width=30,
        ),
        Panel(
            Align(
                f"[bold {'red' if critical else 'green'}]{total_bugs}[/bold {'red' if critical else 'green'}] "
                f"[dim]bugs found[/dim]\n[dim]({critical} high/critical)[/dim]",
                align="center",
            ),
            border_style="red" if critical else "green", width=22,
        ),
        Panel(
            Align(
                f"[bold blue]{total_stats.get('total_lines', 0)}[/bold blue]\n[dim]total lines[/dim]",
                align="center",
            ),
            border_style="blue", width=18,
        ),
    ]
    console.print(Columns(metrics, equal=False))
    console.print()

    t = Table(
        show_header=True, header_style="bold white",
        box=box.ROUNDED, border_style="dim",
        title="[bold]Per-File Scores[/bold]", expand=True,
    )
    t.add_column("File", style="cyan")
    t.add_column("Grade", justify="center", width=8)
    t.add_column("Score", width=30)
    t.add_column("Bugs", justify="center", width=6)
    t.add_column("Security", justify="center", width=9)
    t.add_column("LOC", justify="right", width=7)

    for a in sorted(valid, key=lambda x: x.quality_score, reverse=True):
        text_style, _ = GRADE_STYLES.get(a.grade, ("bold white", "white"))
        bugs = len(a.bugs)
        secs = len(a.security_concerns)
        t.add_row(
            Path(a.path).name,
            Text(a.grade, style=text_style),
            _score_bar(a.quality_score, 15),
            Text(str(bugs), style="bold red" if bugs > 5 else "yellow" if bugs else "green"),
            Text(str(secs), style="bold red" if secs else "green"),
            str(a.lines_of_code),
        )
    console.print(t)
    console.print()


def render_git_insights(insights: str, commits: list, repo_info: dict) -> None:
    """Render git history intelligence panel."""
    console.print(Rule("[bold cyan]🔀 Git Intelligence[/bold cyan]"))
    console.print()

    if repo_info:
        grid = Table.grid(padding=(0, 3))
        for _ in range(3):
            grid.add_column()
        grid.add_row(
            f"[dim]Branch:[/dim] [bold cyan]{repo_info.get('branch', '?')}[/bold cyan]",
            f"[dim]Total commits:[/dim] [bold white]{repo_info.get('total_commits', '?')}[/bold white]",
            f"[dim]Remote:[/dim] [dim]{repo_info.get('remote', 'N/A')}[/dim]",
        )
        console.print(Panel(grid, border_style="dim", title="[dim]Repository Info[/dim]"))
        console.print()

    if insights:
        console.print(Panel(
            insights,
            title="[bold green]AI-Generated Commit Insights[/bold green]",
            border_style="green",
            padding=(1, 2),
        ))
        console.print()

    if commits:
        t = Table(
            show_header=True, header_style="bold white",
            box=box.ROUNDED, border_style="dim",
            title="[bold]Recent Commits[/bold]",
        )
        t.add_column("Hash", style="dim cyan", width=9)
        t.add_column("Date", width=12)
        t.add_column("Author", style="blue", width=20)
        t.add_column("Message")
        for c in commits[:15]:
            msg = c["message"]
            t.add_row(
                c["hash"][:7],
                c["date"],
                c["author"][:18],
                (msg[:70] + "…") if len(msg) > 70 else msg,
            )
        console.print(t)
        console.print()
