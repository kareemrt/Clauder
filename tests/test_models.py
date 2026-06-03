import pytest
from pydantic import ValidationError

from clauder.models import AgentReport, FileInfo, Finding, RepoData, SynthesisReport


def test_finding_valid():
    f = Finding(
        severity="high",
        category="security",
        title="Hardcoded secret",
        description="API key found in source",
        file="main.py",
        line=3,
        recommendation="Use environment variable instead",
    )
    assert f.severity == "high"
    assert f.file == "main.py"


def test_finding_invalid_severity():
    with pytest.raises(ValidationError):
        Finding(
            severity="urgent",
            category="security",
            title="Test",
            description="Test",
            recommendation="Fix it",
        )


def test_agent_report_score_clamped():
    with pytest.raises(ValidationError):
        AgentReport(agent="Scout", emoji="🔭", summary="Test", score=150)


def test_agent_report_defaults():
    r = AgentReport(agent="Scout", emoji="🔭", summary="All good", score=85)
    assert r.findings == []
    assert r.highlights == []


def test_synthesis_report():
    r = SynthesisReport(
        overall_score=78,
        grade="B",
        executive_summary="Solid codebase.",
        agent_reports=[],
    )
    assert r.grade == "B"
    assert r.critical_issues == []
    assert r.roadmap == []


def test_repo_data_defaults():
    r = RepoData(owner="foo", name="bar", url="https://github.com/foo/bar")
    assert r.files == []
    assert r.topics == []
    assert r.stars == 0
