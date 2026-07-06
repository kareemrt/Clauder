"""Tests for Clauder."""

import pytest
from unittest.mock import patch, MagicMock
from clauder.github_client import RepoStats, RepoData, Contributor, CommitInfo
from clauder.report import generate_html_report
from clauder.renderer import StoryRenderer
from rich.console import Console
import io


def make_sample_data() -> RepoData:
    stats = RepoStats(
        full_name="test/repo",
        description="A test repository",
        stars=42,
        forks=7,
        watchers=42,
        open_issues=3,
        language="Python",
        topics=["test", "demo"],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-06-01T00:00:00Z",
        homepage=None,
        license="MIT",
        size_kb=1234,
    )
    contributors = [
        Contributor("alice", 100, "https://avatars.githubusercontent.com/u/1", "https://github.com/alice"),
        Contributor("bob", 50, "https://avatars.githubusercontent.com/u/2", "https://github.com/bob"),
    ]
    commits = [
        CommitInfo("abc1234", "feat: add initial project structure", "Alice", "2024-01-15T10:00:00Z", "https://github.com/test/repo/commit/abc1234"),
        CommitInfo("def5678", "fix: resolve import error", "Bob", "2024-02-01T12:00:00Z", "https://github.com/test/repo/commit/def5678"),
    ]
    return RepoData(
        stats=stats,
        contributors=contributors,
        commits=commits,
        languages={"Python": 85000, "Shell": 5000, "Makefile": 2000},
        recent_issues=[{"title": "Bug in parser", "state": "open", "url": "https://github.com/test/repo/issues/1", "labels": ["bug"]}],
        recent_prs=[{"title": "Add feature X", "state": "merged", "url": "https://github.com/test/repo/pull/1", "merged": True}],
    )


def test_repo_stats_fields():
    data = make_sample_data()
    assert data.stats.full_name == "test/repo"
    assert data.stats.stars == 42
    assert data.stats.language == "Python"


def test_contributor_count():
    data = make_sample_data()
    assert len(data.contributors) == 2
    assert data.contributors[0].login == "alice"
    assert data.contributors[0].contributions == 100


def test_commit_parsing():
    data = make_sample_data()
    assert len(data.commits) == 2
    assert data.commits[0].sha == "abc1234"
    assert "initial project" in data.commits[0].message


def test_html_report_generation(tmp_path):
    data = make_sample_data()
    story = """## The Origin
This is a test repository created for demonstration purposes.

## The Architects
Alice and Bob built this together.

## The Journey
They started in January and iterated rapidly.

## The Technology
Python was their language of choice.

## The Current State
The project is actively maintained.

## The Future
Expect great things ahead.

## One-Line Story
A small repo with big dreams."""
    tagline = "Small but mighty test repo."
    output = str(tmp_path / "report.html")
    result = generate_html_report(data, story, tagline, output)
    assert result == output

    html = open(output).read()
    assert "test/repo" in html
    assert "Small but mighty test repo." in html
    assert "The Origin" in html
    assert "Alice" in html
    assert "Python" in html


def test_renderer_does_not_crash():
    data = make_sample_data()
    buf = io.StringIO()
    console = Console(file=buf, width=120)
    renderer = StoryRenderer(console=console)
    story = """## The Origin
Test content here.

## One-Line Story
A one-liner."""
    renderer.render_full(data, story, "Test tagline.")
    output = buf.getvalue()
    assert "test/repo" in output or "Test tagline" in output


def test_language_bar_empty():
    data = make_sample_data()
    data.languages.clear()
    buf = io.StringIO()
    console = Console(file=buf, width=120)
    renderer = StoryRenderer(console=console)
    renderer.render_language_bar({})
    # Should not raise


def test_parse_sections_in_renderer():
    buf = io.StringIO()
    console = Console(file=buf, width=120)
    renderer = StoryRenderer(console=console)
    story = "## The Origin\nSome content.\n## The Future\nMore content."
    sections = renderer._parse_sections(story)
    assert len(sections) == 2
    assert sections[0][0] == "The Origin"
    assert "Some content" in sections[0][1]
