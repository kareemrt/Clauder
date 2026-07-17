"""Rich terminal and markdown output formatting."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box
from rich.rule import Rule
from rich.padding import Padding

from .reviewer import ReviewResult, Issue

CATEGORY_ICONS = {
    "bugs": "🐛",
    "security": "🔒",
    "performance": "⚡",
    "style": "🎨",
    "docs": "📝",
}

SEVERITY_COLORS = {
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "cyan",
    "info": "dim",
}

SEVERITY_BADGES = {
    "critical": "[bold red]● CRITICAL[/]",
    "high": "[red]● HIGH[/]",
    "medium": "[yellow]● MEDIUM[/]",
    "low": "[cyan]● LOW[/]",
    "info": "[dim]● INFO[/]",
}


def _score_color(score: int) -> str:
    if score >= 85:
        return "bold green"
    if score >= 65:
        return "bold yellow"
    if score >= 40:
        return "bold orange3"
    return "bold red"


def _score_bar(score: int, width: int = 20) -> str:
    filled = round(score / 100 * width)
    color = _score_color(score)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{color}]{bar}[/]"


def render_terminal(result: ReviewResult, console: Console | None = None) -> None:
    c = console or Console()

    # Header banner
    c.print()
    c.print(Panel(
        "[bold cyan]  ☁  CLAUDER  ☁[/]\n[dim]AI-powered code review[/]",
        style="bold",
        border_style="cyan",
        expand=False,
        padding=(0, 4),
    ))
    c.print()

    # Score panel
    score_color = _score_color(result.score)
    score_bar = _score_bar(result.score)
    issue_summary = (
        f"[bold red]{result.critical_count} critical[/]  "
        f"[red]{result.high_count} high[/]  "
        f"[yellow]{result.medium_count} medium[/]  "
        f"[cyan]{result.low_count} low[/]"
    )

    score_panel = Panel(
        f"[{score_color}]{result.score}/100[/]  {score_bar}\n\n"
        f"{issue_summary}\n\n"
        f"[italic]{result.summary}[/]",
        title="[bold]Review Score[/]",
        border_style=score_color.replace("bold ", ""),
        padding=(1, 2),
    )
    c.print(score_panel)
    c.print()

    # What's good
    if result.highlights:
        c.print(Rule("[bold green]✓ Highlights[/]", style="green"))
        for hl in result.highlights:
            c.print(f"  [green]✓[/] {hl}")
        c.print()

    # Issues by category
    by_cat = result.by_category()
    if not by_cat:
        c.print(Panel("[bold green]No issues found! Excellent work. 🎉[/]", border_style="green"))
        c.print()
        return

    c.print(Rule("[bold]Issues Found[/]"))
    c.print()

    for category, issues in sorted(by_cat.items()):
        icon = CATEGORY_ICONS.get(category, "•")
        c.print(f"[bold]{icon}  {category.upper()}[/]  [dim]({len(issues)} issue{'s' if len(issues) != 1 else ''})[/]")

        for i, issue in enumerate(sorted(issues, key=lambda x: ["critical","high","medium","low","info"].index(x.severity))):
            badge = SEVERITY_BADGES[issue.severity]
            location = ""
            if issue.file:
                location = f"[dim]{issue.file}"
                if issue.line:
                    location += f":{issue.line}"
                location += "[/]  "

            c.print(f"  {badge}  {location}[bold]{issue.title}[/]")
            c.print(f"    [dim]{issue.description}[/]")
            if issue.suggestion:
                c.print(f"    [italic cyan]→ {issue.suggestion}[/]")
            if i < len(issues) - 1:
                c.print()

        c.print()

    # Stats footer
    stats_table = Table.grid(padding=(0, 2))
    stats_table.add_column()
    stats_table.add_column()
    stats_table.add_row(
        f"[dim]Lines reviewed:[/] [bold]{result.raw_diff_lines:,}[/]",
        f"[dim]Total issues:[/] [bold]{len(result.issues)}[/]",
    )
    c.print(Padding(stats_table, (0, 1)))
    c.print()


def render_markdown(result: ReviewResult) -> str:
    lines = []
    lines.append("# 🔍 Clauder Code Review Report\n")
    lines.append(f"**Score:** {result.score}/100\n")
    lines.append(f"**Summary:** {result.summary}\n")

    if result.highlights:
        lines.append("## ✅ Highlights\n")
        for hl in result.highlights:
            lines.append(f"- {hl}")
        lines.append("")

    lines.append(f"## 📊 Issue Summary\n")
    lines.append(f"| Severity | Count |")
    lines.append(f"|----------|-------|")
    lines.append(f"| 🔴 Critical | {result.critical_count} |")
    lines.append(f"| 🟠 High | {result.high_count} |")
    lines.append(f"| 🟡 Medium | {result.medium_count} |")
    lines.append(f"| 🔵 Low/Info | {result.low_count} |")
    lines.append("")

    by_cat = result.by_category()
    if by_cat:
        lines.append("## 🐛 Issues\n")
        for category, issues in sorted(by_cat.items()):
            icon = CATEGORY_ICONS.get(category, "•")
            lines.append(f"### {icon} {category.title()}\n")
            for issue in sorted(issues, key=lambda x: ["critical","high","medium","low","info"].index(x.severity)):
                loc = f"`{issue.file}`" if issue.file else ""
                if issue.line and loc:
                    loc += f" line {issue.line}"
                header = f"**[{issue.severity.upper()}]** {issue.title}"
                if loc:
                    header += f" — {loc}"
                lines.append(f"#### {header}\n")
                lines.append(f"{issue.description}\n")
                if issue.suggestion:
                    lines.append(f"> **Fix:** {issue.suggestion}\n")

    lines.append(f"---\n*Generated by [Clauder](https://github.com/kareemrt/clauder) · {result.raw_diff_lines:,} lines reviewed*")
    return "\n".join(lines)


def render_json(result: ReviewResult) -> str:
    import json
    data = {
        "score": result.score,
        "summary": result.summary,
        "highlights": result.highlights,
        "issue_counts": {
            "critical": result.critical_count,
            "high": result.high_count,
            "medium": result.medium_count,
            "low": result.low_count,
        },
        "issues": [
            {
                "category": i.category,
                "severity": i.severity,
                "title": i.title,
                "description": i.description,
                "file": i.file,
                "line": i.line,
                "suggestion": i.suggestion,
            }
            for i in result.issues
        ],
    }
    return json.dumps(data, indent=2)
