"""Rich terminal UI for Clauder: The Oracle."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.text import Text
from rich.columns import Columns
from rich import box
from rich.rule import Rule
from rich.align import Align

from .analyzer import CodeMetrics

console = Console()

VERDICT_STYLES = {
    "TRANSCENDENT": ("bright_cyan", "✦ TRANSCENDENT ✦", "⚡"),
    "BLESSED":      ("bright_green", "✧ BLESSED ✧", "☽"),
    "ENCHANTED":    ("bright_yellow", "⊕ ENCHANTED ⊕", "◈"),
    "MUNDANE":      ("dim white", "○ MUNDANE ○", "◯"),
    "CURSED":       ("bright_red", "☠ CURSED ☠", "⚠"),
}

SEVERITY_STYLES = {
    "CRITICAL": ("bright_red", "⚠ CRITICAL"),
    "WARNING":  ("yellow", "⚡ WARNING"),
    "INFO":     ("cyan", "◉ INFO"),
    "WISDOM":   ("bright_magenta", "✦ WISDOM"),
}

ORACLE_BANNER = r"""
  ╔═══════════════════════════════════════════════════════════════╗
  ║    ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗   ║
  ║   ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗  ║
  ║   ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝  ║
  ║   ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗  ║
  ║   ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║  ║
  ║    ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝  ║
  ║                   ✦  T H E   O R A C L E  ✦                  ║
  ╚═══════════════════════════════════════════════════════════════╝
"""


def print_banner():
    console.print(ORACLE_BANNER, style="bright_cyan", justify="center")
    console.print(
        "  [dim italic]Ancient wisdom meets modern code. The Oracle sees all.[/dim italic]\n",
        justify="center",
    )


def print_scanning(file_path: str):
    console.print(
        f"\n[dim]Consulting the Oracle for:[/dim] [bold cyan]{file_path}[/bold cyan]"
    )


def make_score_bar(score: int, width: int = 20) -> Text:
    filled = int(score / 100 * width)
    bar = Text()
    if score >= 80:
        color = "bright_green"
    elif score >= 60:
        color = "yellow"
    elif score >= 40:
        color = "bright_red"
    else:
        color = "red"
    bar.append("█" * filled, style=color)
    bar.append("░" * (width - filled), style="dim")
    bar.append(f" {score}/100", style=color)
    return bar


def print_oracle_vision(review: dict):
    vision = review.get("vision", "The Oracle remains silent...")
    console.print()
    console.print(
        Panel(
            f"[italic bright_yellow]{vision}[/italic bright_yellow]",
            title="[bold bright_magenta]✦  Oracle's Vision  ✦[/bold bright_magenta]",
            border_style="bright_magenta",
            padding=(1, 3),
        )
    )


def print_verdict(review: dict, file_path: str):
    verdict = review.get("verdict", "MUNDANE")
    score = review.get("score", 50)
    style, label, icon = VERDICT_STYLES.get(verdict, VERDICT_STYLES["MUNDANE"])

    verdict_text = Text(justify="center")
    verdict_text.append(f"\n{icon}  ", style=style)
    verdict_text.append(label, style=f"bold {style}")
    verdict_text.append(f"  {icon}\n", style=style)
    verdict_text.append(f"\nOVERALL SCORE: ", style="dim")
    verdict_text.append(f"{score}/100", style=f"bold {style}")
    verdict_text.append("\n")

    console.print()
    console.print(
        Panel(
            Align.center(verdict_text),
            title=f"[bold]The Oracle's Verdict for[/bold] [cyan]{Path(file_path).name}[/cyan]",
            border_style=style,
            box=box.DOUBLE_EDGE,
            padding=(0, 4),
        )
    )


def print_rune_scores(review: dict):
    runes = review.get("runes", {})
    if not runes:
        return

    console.print()
    console.print(Rule("[bold bright_magenta]✦  The Four Runes  ✦[/bold bright_magenta]"))
    console.print()

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Rune", style="bold", width=16)
    table.add_column("Score", width=30)
    table.add_column("Value", width=8)

    rune_icons = {
        "quality": "◈  Quality",
        "security": "🔒 Security",
        "readability": "◉  Readability",
        "performance": "⚡ Performance",
    }

    for key, icon in rune_icons.items():
        score = runes.get(key, 0)
        table.add_row(icon, make_score_bar(score, 25), f"[bold]{score}[/bold]")

    console.print(table)


def print_metrics(metrics: Optional[CodeMetrics]):
    if not metrics:
        return

    console.print()
    console.print(Rule("[bold bright_blue]◈  Code Metrics  ◈[/bold bright_blue]"))
    console.print()

    cols = []

    info_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    info_table.add_column("Key", style="dim", width=18)
    info_table.add_column("Value", style="bold cyan")

    info_table.add_row("Language", metrics.language)
    info_table.add_row("File Size", f"{metrics.file_size_kb} KB")
    info_table.add_row("Total Lines", str(metrics.total_lines))
    info_table.add_row("Code Lines", str(metrics.code_lines))
    info_table.add_row("Comments", str(metrics.comment_lines))
    info_table.add_row("Blank Lines", str(metrics.blank_lines))
    cols.append(info_table)

    struct_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    struct_table.add_column("Key", style="dim", width=18)
    struct_table.add_column("Value", style="bold cyan")

    struct_table.add_row("Functions", str(metrics.function_count))
    struct_table.add_row("Classes", str(metrics.class_count))
    struct_table.add_row("Avg Line Len", str(metrics.avg_line_length))
    struct_table.add_row("Max Line Len", str(metrics.max_line_length))
    struct_table.add_row("Complexity", str(metrics.complexity_score))
    struct_table.add_row("Has Tests", "✓ Yes" if metrics.has_tests else "✗ No")
    struct_table.add_row("Has Docstrings", "✓ Yes" if metrics.has_docstrings else "✗ No")
    cols.append(struct_table)

    console.print(Columns(cols, equal=True, expand=False))


def print_prophecies(review: dict):
    prophecies = review.get("prophecies", [])
    if not prophecies:
        return

    console.print()
    console.print(Rule("[bold bright_red]⚡  Prophecies  ⚡[/bold bright_red]"))

    for i, p in enumerate(prophecies, 1):
        severity = p.get("severity", "INFO")
        color, label = SEVERITY_STYLES.get(severity, SEVERITY_STYLES["INFO"])
        title = p.get("title", "Unnamed Prophecy")
        message = p.get("message", "")
        remedy = p.get("remedy", "")
        line = p.get("line")

        location = f" [dim](line {line})[/dim]" if line else ""
        body = f"[italic]{message}[/italic]"
        if remedy:
            body += f"\n\n[bold green]Remedy:[/bold green] {remedy}"

        console.print()
        console.print(
            Panel(
                body,
                title=f"[{color}]{label}[/{color}] [bold]{i}. {title}[/bold]{location}",
                border_style=color,
                padding=(0, 2),
            )
        )


def print_incantation(review: dict):
    incantation = review.get("incantation", "")
    haiku = review.get("haiku", "")
    if not incantation and not haiku:
        return

    console.print()
    console.print(Rule("[bold bright_cyan]✦  Final Words  ✦[/bold bright_cyan]"))

    if incantation:
        console.print()
        console.print(f"[bright_cyan italic]  {incantation}[/bright_cyan italic]")

    if haiku:
        console.print()
        haiku_lines = haiku.split("\n") if "\n" in haiku else [haiku]
        haiku_text = "\n".join(f"  [dim]{line}[/dim]" for line in haiku_lines)
        console.print(
            Panel(
                haiku_text,
                title="[dim]Oracle's Haiku[/dim]",
                border_style="dim",
                box=box.MINIMAL,
                padding=(0, 4),
            )
        )


def print_full_review(review: dict, metrics: Optional[CodeMetrics], file_path: str):
    print_oracle_vision(review)
    print_verdict(review, file_path)
    print_rune_scores(review)
    print_metrics(metrics)
    print_prophecies(review)
    print_incantation(review)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print()
    console.print(f"[dim]Oracle consulted at {timestamp}[/dim]")
    console.print()


def save_review(review: dict, metrics: Optional[CodeMetrics], file_path: str, output_path: str):
    data = {
        "file": file_path,
        "timestamp": datetime.now().isoformat(),
        "review": review,
        "metrics": (
            {
                "language": metrics.language,
                "total_lines": metrics.total_lines,
                "code_lines": metrics.code_lines,
                "comment_lines": metrics.comment_lines,
                "function_count": metrics.function_count,
                "class_count": metrics.class_count,
                "complexity_score": metrics.complexity_score,
                "has_tests": metrics.has_tests,
            }
            if metrics
            else None
        ),
    }
    Path(output_path).write_text(json.dumps(data, indent=2))
    console.print(f"[dim]Review saved to [cyan]{output_path}[/cyan][/dim]")
