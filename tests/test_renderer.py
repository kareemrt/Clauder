"""Tests for output renderers."""

import json
import pytest
from clauder.renderer import render_json, render_markdown
from clauder.reviewer import ReviewResult, ReviewComment


@pytest.fixture
def sample_result() -> ReviewResult:
    return ReviewResult(
        summary="The changes improve security but introduce a performance regression.",
        overall_score=72,
        model="claude-opus-5",
        input_tokens=1200,
        output_tokens=300,
        comments=[
            ReviewComment(
                file="src/auth.py",
                line=15,
                severity="critical",
                category="security",
                message="SQL injection vulnerability via string interpolation.",
                suggestion="Use parameterized queries instead.",
            ),
            ReviewComment(
                file="src/utils.py",
                line=None,
                severity="info",
                category="style",
                message="Consider adding type hints.",
                suggestion=None,
            ),
        ],
    )


def test_render_json_valid(sample_result):
    output = render_json(sample_result)
    data = json.loads(output)
    assert data["overall_score"] == 72
    assert len(data["comments"]) == 2
    assert data["comments"][0]["severity"] == "critical"


def test_render_json_usage_fields(sample_result):
    data = json.loads(render_json(sample_result))
    assert data["usage"]["input_tokens"] == 1200


def test_render_markdown_contains_score(sample_result):
    md = render_markdown(sample_result)
    assert "72/100" in md


def test_render_markdown_contains_summary(sample_result):
    md = render_markdown(sample_result)
    assert "performance regression" in md


def test_render_markdown_critical_section(sample_result):
    md = render_markdown(sample_result)
    assert "CRITICAL" in md
    assert "SQL injection" in md


def test_render_markdown_no_comments():
    result = ReviewResult(summary="Looks good!", overall_score=95, model="claude-opus-5")
    md = render_markdown(result)
    assert "No issues found" in md
