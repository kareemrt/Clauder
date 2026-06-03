from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from clauder.models import AgentReport, Finding, SynthesisReport

SEVERITY_COLORS = {
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "cyan",
    "info": "dim",
}

GRADE_COLORS = {
    "A": "bold green",
    "B": "green",
    "C": "yellow",
    "D": "orange1",
    "F": "bold red",
}

SCORE_BAR_CHARS = 20


def _score_bar(score: int, width: int = SCORE_BAR_CHARS) -> str:
    filled = round(score / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    if score >= 75:
        color = "green"
    elif score >= 50:
        color = "yellow"
    else:
        color = "red"
    return f"[{color}]{bar}[/{color}] [bold]{score}/100[/bold]"


class Reporter:
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def display(self, report: SynthesisReport) -> None:
        self._print_header(report)
        self._print_agent_summaries(report.agent_reports)
        self._print_findings(report.agent_reports)
        self._print_synthesis(report)

    def _print_header(self, report: SynthesisReport) -> None:
        grade_color = GRADE_COLORS.get(report.grade, "white")
        self.console.print()
        self.console.print(Rule("[bold cyan]ANALYSIS COMPLETE[/bold cyan]", style="cyan"))
        self.console.print()

        header_table = Table.grid(expand=True, padding=(0, 2))
        header_table.add_column(justify="left")
        header_table.add_column(justify="right")
        header_table.add_row(
            f"[bold]Overall Score[/bold]\n{_score_bar(report.overall_score)}",
            f"[{grade_color}]Grade\n{'  ' + report.grade + '  ':^8}[/{grade_color}]",
        )
        self.console.print(Panel(header_table, border_style="cyan"))

    def _print_agent_summaries(self, agent_reports: list[AgentReport]) -> None:
        self.console.print()
        self.console.print("[bold]Agent Scores[/bold]")

        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("Agent", min_width=14)
        table.add_column("Score", justify="right", min_width=8)
        table.add_column("Bar", min_width=25)
        table.add_column("Summary")

        for r in agent_reports:
            table.add_row(
                f"{r.emoji} {r.agent}",
                f"[bold]{r.score}/100[/bold]",
                _score_bar(r.score),
                r.summary[:80] + ("…" if len(r.summary) > 80 else ""),
            )

        self.console.print(table)

    def _print_findings(self, agent_reports: list[AgentReport]) -> None:
        all_findings: list[tuple[str, Finding]] = []
        for r in agent_reports:
            for f in r.findings:
                all_findings.append((f"{r.emoji} {r.agent}", f))

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        all_findings.sort(key=lambda x: severity_order.get(x[1].severity, 5))

        if not all_findings:
            return

        self.console.print()
        self.console.print("[bold]Findings[/bold]")

        table = Table(show_header=True, header_style="bold cyan", border_style="dim", show_lines=True)
        table.add_column("Sev.", min_width=8)
        table.add_column("Agent", min_width=14)
        table.add_column("Title", min_width=24)
        table.add_column("File")
        table.add_column("Recommendation")

        for agent_label, f in all_findings:
            color = SEVERITY_COLORS.get(f.severity, "white")
            file_str = f.path or "" if hasattr(f, "path") else (f.file or "")
            table.add_row(
                f"[{color}]{f.severity.upper()}[/{color}]",
                agent_label,
                f.title,
                file_str[:35] + ("…" if len(file_str) > 35 else ""),
                f.recommendation[:60] + ("…" if len(f.recommendation) > 60 else ""),
            )

        self.console.print(table)

    def _print_synthesis(self, report: SynthesisReport) -> None:
        self.console.print()
        self.console.print("[bold]Executive Summary[/bold]")
        self.console.print(Panel(report.executive_summary, border_style="cyan"))

        if report.critical_issues:
            self.console.print()
            self.console.print("[bold red]Critical Issues[/bold red]")
            for i, issue in enumerate(report.critical_issues, 1):
                self.console.print(f"  [red]{i}.[/red] {issue}")

        if report.strengths:
            self.console.print()
            self.console.print("[bold green]Strengths[/bold green]")
            for strength in report.strengths:
                self.console.print(f"  [green]✓[/green] {strength}")

        if report.roadmap:
            self.console.print()
            self.console.print("[bold yellow]Action Roadmap[/bold yellow]")
            for i, action in enumerate(report.roadmap, 1):
                self.console.print(f"  [yellow]{i}.[/yellow] {action}")

        self.console.print()

    def save_markdown(self, report: SynthesisReport, path: Path) -> None:
        path = Path(path)
        path.write_text(_render_markdown(report))

    def get_markdown(self, report: SynthesisReport) -> str:
        return _render_markdown(report)


def _render_markdown(report: SynthesisReport) -> str:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}
    grade_emoji = {"A": "🌟", "B": "✅", "C": "⚠️", "D": "🔶", "F": "❌"}

    lines = [
        f"# Clauder Analysis Report",
        f"",
        f"> Generated by [Clauder](https://github.com/kareemrt/clauder) on {timestamp}",
        f"",
        f"## Overall Health",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| **Score** | {report.overall_score}/100 |",
        f"| **Grade** | {grade_emoji.get(report.grade, '')} {report.grade} |",
        f"| **Agents Run** | {len(report.agent_reports)} |",
        f"",
        f"```",
        _ascii_score_bar(report.overall_score),
        f"```",
        f"",
        f"## Executive Summary",
        f"",
        report.executive_summary,
        f"",
    ]

    if report.critical_issues:
        lines += [
            f"## 🚨 Critical Issues",
            f"",
            *[f"- {issue}" for issue in report.critical_issues],
            f"",
        ]

    if report.strengths:
        lines += [
            f"## 💪 Strengths",
            f"",
            *[f"- {s}" for s in report.strengths],
            f"",
        ]

    if report.roadmap:
        lines += [
            f"## 🗺️ Action Roadmap",
            f"",
            *[f"{i}. {action}" for i, action in enumerate(report.roadmap, 1)],
            f"",
        ]

    lines += [
        f"## Agent Reports",
        f"",
    ]

    for r in report.agent_reports:
        lines += [
            f"### {r.emoji} {r.agent} Agent — {r.score}/100",
            f"",
            f"{r.summary}",
            f"",
        ]

        if r.highlights:
            lines += [
                f"**Highlights:**",
                *[f"- ✅ {h}" for h in r.highlights],
                f"",
            ]

        if r.findings:
            sorted_findings = sorted(r.findings, key=lambda f: severity_order.get(f.severity, 5))
            lines += [
                f"**Findings:**",
                f"",
                f"| Severity | Title | File | Recommendation |",
                f"|----------|-------|------|----------------|",
            ]
            for f in sorted_findings:
                sev_icon = severity_emoji.get(f.severity, "")
                file_str = f.file or "—"
                lines.append(
                    f"| {sev_icon} {f.severity.upper()} | {f.title} | `{file_str}` | {f.recommendation} |"
                )
            lines.append(f"")

    lines += [
        f"---",
        f"",
        f"*Powered by [Clauder](https://github.com/kareemrt/clauder) — Multi-Agent AI Repository Intelligence*",
    ]

    return "\n".join(lines)


def _ascii_score_bar(score: int, width: int = 40) -> str:
    filled = round(score / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"Score: [{bar}] {score}/100"
