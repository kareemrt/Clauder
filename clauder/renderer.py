"""Render ReviewResult to terminal (Rich), Markdown, or JSON."""

import json
import sys

from .config import SEVERITY_COLORS, SEVERITY_EMOJI, ReviewConfig
from .reviewer import ReviewResult


def _score_bar(score: int, width: int = 20) -> str:
    filled = round(score / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {score}/100"


# ──────────────────────────────────────────────────────────
# Terminal renderer (uses Rich if available, plain fallback)
# ──────────────────────────────────────────────────────────
def render_terminal(result: ReviewResult, config: ReviewConfig) -> None:
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        from rich import box
        _render_rich(result, config, Console())
    except ImportError:
        _render_plain(result, config)


def _render_rich(result: ReviewResult, config: ReviewConfig, console) -> None:
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    from rich.text import Text

    # Header
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🤖 Clauder AI Code Review[/bold cyan]",
        border_style="cyan",
    ))

    # Score
    score = result.overall_score
    score_color = "green" if score >= 80 else ("yellow" if score >= 60 else "red")
    console.print(f"\n[bold]Overall Score:[/bold] [{score_color}]{_score_bar(score)}[/{score_color}]")

    # Summary
    if result.summary:
        console.print(Panel(result.summary, title="[bold]Summary[/bold]", border_style="dim"))

    # Stats
    by_sev = result.by_severity
    stats_parts = []
    for sev in ("critical", "high", "medium", "low", "info"):
        count = len(by_sev.get(sev, []))
        if count:
            color = SEVERITY_COLORS[sev]
            emoji = SEVERITY_EMOJI[sev]
            stats_parts.append(f"[{color}]{emoji} {sev}: {count}[/{color}]")
    if stats_parts:
        console.print("  " + "  |  ".join(stats_parts))
    console.print()

    # Comments table
    if result.comments:
        table = Table(box=box.ROUNDED, expand=True, show_lines=True)
        table.add_column("Sev", style="bold", width=8)
        table.add_column("File", style="dim", max_width=30)
        table.add_column("Line", width=6)
        table.add_column("Message")
        table.add_column("Category", width=12)

        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        sorted_comments = sorted(result.comments, key=lambda c: sev_order.get(c.severity, 99))

        for c in sorted_comments:
            color = SEVERITY_COLORS.get(c.severity, "white")
            emoji = SEVERITY_EMOJI.get(c.severity, "")
            sev_cell = f"[{color}]{emoji} {c.severity}[/{color}]"
            line_str = str(c.line) if c.line else "—"
            msg = c.message
            if c.suggestion:
                msg += f"\n[dim italic]💡 {c.suggestion}[/dim italic]"
            table.add_row(sev_cell, c.file, line_str, msg, f"[dim]{c.category}[/dim]")

        console.print(table)
    else:
        console.print("[green]✅ No issues found![/green]")

    # Token usage
    console.print(
        f"\n[dim]Model: {result.model} | "
        f"Tokens: {result.input_tokens:,} in / {result.output_tokens:,} out[/dim]\n"
    )


def _render_plain(result: ReviewResult, config: ReviewConfig) -> None:
    print("\n=== Clauder AI Code Review ===")
    print(f"Score: {_score_bar(result.overall_score)}")
    print(f"\nSummary:\n{result.summary}\n")
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    for c in sorted(result.comments, key=lambda c: sev_order.get(c.severity, 99)):
        line = f":{c.line}" if c.line else ""
        print(f"[{c.severity.upper()}] {c.file}{line} — {c.message}")
        if c.suggestion:
            print(f"  -> {c.suggestion}")
    print(f"\nModel: {result.model} | {result.input_tokens} in / {result.output_tokens} out tokens\n")


# ──────────────────────────────────────────────────────────
# Markdown renderer
# ──────────────────────────────────────────────────────────
def render_markdown(result: ReviewResult) -> str:
    lines = ["# 🤖 Clauder AI Code Review", ""]
    score = result.overall_score
    lines += [f"**Overall Score:** `{score}/100`", ""]

    if result.summary:
        lines += ["## Summary", "", result.summary, ""]

    by_sev = result.by_severity
    badge_parts = []
    for sev in ("critical", "high", "medium", "low", "info"):
        count = len(by_sev.get(sev, []))
        if count:
            badge_parts.append(f"{SEVERITY_EMOJI[sev]} **{sev}**: {count}")
    if badge_parts:
        lines += ["## Issue Breakdown", "", " | ".join(badge_parts), ""]

    if result.comments:
        lines += ["## Comments", ""]
        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        for c in sorted(result.comments, key=lambda c: sev_order.get(c.severity, 99)):
            emoji = SEVERITY_EMOJI.get(c.severity, "")
            loc = f"`{c.file}`" + (f" line {c.line}" if c.line else "")
            lines.append(f"### {emoji} {c.severity.upper()} — {loc}")
            lines.append(f"**Category:** {c.category}")
            lines.append(f"\n{c.message}\n")
            if c.suggestion:
                lines.append(f"> 💡 **Suggestion:** {c.suggestion}\n")
    else:
        lines += ["## Comments", "", "✅ No issues found!", ""]

    lines += [
        "---",
        f"*Generated by [Clauder](https://github.com/kareemrt/clauder) | "
        f"Model: `{result.model}` | "
        f"Tokens: {result.input_tokens:,} in / {result.output_tokens:,} out*",
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────
# JSON renderer
# ──────────────────────────────────────────────────────────
def render_json(result: ReviewResult) -> str:
    return json.dumps(
        {
            "summary": result.summary,
            "overall_score": result.overall_score,
            "model": result.model,
            "usage": {
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
            },
            "comments": [
                {
                    "file": c.file,
                    "line": c.line,
                    "severity": c.severity,
                    "category": c.category,
                    "message": c.message,
                    "suggestion": c.suggestion,
                }
                for c in result.comments
            ],
        },
        indent=2,
    )
