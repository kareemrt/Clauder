import re

import pytest
from rich.console import Console

from clauder.models import AgentReport, Finding, SynthesisReport
from clauder.reporter import Reporter, _ascii_score_bar, _score_bar


def _make_report(score=72) -> SynthesisReport:
    agent = AgentReport(
        agent="Security",
        emoji="🔒",
        summary="One critical issue found.",
        score=45,
        findings=[
            Finding(
                severity="critical",
                category="secrets",
                title="Hardcoded API key",
                description="API key found in main.py",
                file="main.py",
                line=3,
                recommendation="Move to environment variable",
            )
        ],
        highlights=["Good use of HTTPS"],
    )
    return SynthesisReport(
        overall_score=score,
        grade="C",
        executive_summary="The project has some security concerns but reasonable structure.",
        critical_issues=["Hardcoded secret in main.py"],
        strengths=["Clear README"],
        roadmap=["Rotate leaked API key", "Add secret scanning CI check"],
        agent_reports=[agent],
    )


def test_ascii_score_bar():
    bar = _ascii_score_bar(75)
    assert "75/100" in bar
    assert "█" in bar
    assert "░" in bar


def test_score_bar_zero():
    bar = _ascii_score_bar(0)
    assert "0/100" in bar
    assert "█" not in bar


def test_score_bar_hundred():
    bar = _ascii_score_bar(100)
    assert "100/100" in bar
    assert "░" not in bar


def test_reporter_get_markdown():
    report = _make_report()
    reporter = Reporter()
    md = reporter.get_markdown(report)

    assert "# Clauder Analysis Report" in md
    assert "72/100" in md
    assert "Hardcoded API key" in md
    assert "Move to environment variable" in md
    assert "Hardcoded secret in main.py" in md
    assert "Clear README" in md
    assert "Action Roadmap" in md


def test_reporter_markdown_grade():
    report = _make_report(score=92)
    report.grade = "A"
    md = Reporter().get_markdown(report)
    assert "Grade" in md
    assert "A" in md


def test_reporter_display_no_crash(capsys):
    report = _make_report()
    console = Console(file=open("/dev/null", "w"), highlight=False)
    Reporter(console=console).display(report)


def test_reporter_save_markdown(tmp_path):
    report = _make_report()
    out = tmp_path / "report.md"
    Reporter().save_markdown(report, out)
    content = out.read_text()
    assert "Clauder Analysis Report" in content
    assert "72/100" in content
