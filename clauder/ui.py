"""Rich terminal UI components for Clauder."""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def banner():
    art = Text(justify="center")
    art.append("  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗  \n", style="bold cyan")
    art.append(" ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗ \n", style="bold cyan")
    art.append(" ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝ \n", style="bold blue")
    art.append(" ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗ \n", style="bold blue")
    art.append(" ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║ \n", style="bold magenta")
    art.append("  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ \n", style="bold magenta")
    sub = Text("  The Autonomous Code Healer  •  Powered by Claude\n", style="italic dim white", justify="center")
    console.print(art)
    console.print(sub)


def section(title: str, emoji: str = ""):
    console.print()
    console.rule(f"[bold cyan]{emoji}  {title}" if emoji else f"[bold cyan]{title}")


def success(msg: str):
    console.print(f"[bold green]✓[/]  {msg}")


def info(msg: str):
    console.print(f"[bold blue]ℹ[/]  {msg}")


def warn(msg: str):
    console.print(f"[bold yellow]⚠[/]  {msg}")


def error(msg: str):
    console.print(f"[bold red]✗[/]  {msg}")


def thinking(msg: str):
    console.print(f"[bold magenta]🤔[/]  [italic]{msg}[/italic]")


def show_diff(original: str, fixed: str, filename: str = "code.py"):
    import difflib
    diff = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        fixed.splitlines(keepends=True),
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm="",
    ))
    if diff:
        diff_text = "".join(diff)
        syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=False)
        console.print(Panel(syntax, title="[bold yellow]Proposed Fix[/]", border_style="yellow"))
    else:
        warn("No diff — Claude returned the same content.")


def show_code(code: str, filename: str = "code.py", title: str = ""):
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=title or f"[bold cyan]{filename}[/]", border_style="cyan"))


def show_findings_table(findings: list[dict]):
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Line", style="cyan", no_wrap=True, width=6)
    table.add_column("Severity", width=10)
    table.add_column("Issue", ratio=2)
    table.add_column("Suggestion", ratio=3)

    severity_colors = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "green", "INFO": "blue"}

    for f in findings:
        sev = f.get("severity", "INFO")
        color = severity_colors.get(sev, "white")
        table.add_row(
            str(f.get("line", "?")),
            f"[{color}]{sev}[/{color}]",
            f.get("issue", ""),
            f.get("suggestion", ""),
        )
    console.print(table)


def show_heal_summary(iterations: int, fixed: int, remaining: int):
    table = Table(box=box.SIMPLE_HEAVY, show_header=False, expand=False)
    table.add_column("Label", style="dim")
    table.add_column("Value", style="bold")
    table.add_row("Iterations", str(iterations))
    table.add_row("Tests Fixed", f"[green]{fixed}[/]")
    table.add_row("Remaining Failures", f"[{'red' if remaining else 'green'}]{remaining}[/]")
    console.print(Panel(table, title="[bold]Heal Summary[/]", border_style="cyan"))
