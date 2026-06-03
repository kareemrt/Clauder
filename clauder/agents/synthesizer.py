from __future__ import annotations

import json
import re

import anthropic

from clauder.models import AgentReport, RepoData, SynthesisReport


SYNTHESIZER_SYSTEM = """You are the Synthesis Agent — the final reviewer who integrates all specialist reports into an executive summary.

You receive findings from five agents: Scout, Security, Quality, Architecture, and Docs.
Your job is to:
1. Compute a single overall health score (weighted average, security issues weigh more)
2. Assign a letter grade: A (90-100), B (75-89), C (60-74), D (45-59), F (<45)
3. Write a crisp 3-4 sentence executive summary hitting the most important points
4. Surface the top 3-5 critical/high severity issues across all agents
5. List 3-5 genuine strengths discovered
6. Create a prioritized action roadmap (top 5 things to fix/improve)

Return only valid JSON matching this schema exactly:
{
  "overall_score": <integer 0-100>,
  "grade": "A|B|C|D|F",
  "executive_summary": "<3-4 sentences>",
  "critical_issues": ["<issue 1>", "<issue 2>", ...],
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "roadmap": ["<action 1>", "<action 2>", ...]
}"""


class SynthesizerAgent:
    def __init__(self, client: anthropic.AsyncAnthropic, model: str):
        self.client = client
        self.model = model

    async def synthesize(self, repo_data: RepoData, agent_reports: list[AgentReport]) -> SynthesisReport:
        reports_text = "\n\n".join(
            f"## {r.emoji} {r.agent} Agent (score: {r.score}/100)\n"
            f"Summary: {r.summary}\n"
            f"Findings:\n" + "\n".join(
                f"  [{f.severity.upper()}] {f.title}: {f.description} → {f.recommendation}"
                for f in r.findings
            ) + "\n"
            f"Highlights: {', '.join(r.highlights)}"
            for r in agent_reports
        )

        user_message = f"""Synthesize these agent reports for {repo_data.owner}/{repo_data.name}:

{reports_text}

Individual scores: {', '.join(f'{r.agent}={r.score}' for r in agent_reports)}

Return only the JSON synthesis."""

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYNTHESIZER_SYSTEM,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = response.content[0].text
        return self._parse(raw, agent_reports)

    def _parse(self, raw: str, agent_reports: list[AgentReport]) -> SynthesisReport:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            avg = sum(r.score for r in agent_reports) // max(len(agent_reports), 1)
            return SynthesisReport(
                overall_score=avg,
                grade=_score_to_grade(avg),
                executive_summary="Synthesis failed — see individual agent reports.",
                agent_reports=agent_reports,
            )

        try:
            data = json.loads(match.group())
            score = max(0, min(100, int(data.get("overall_score", 50))))
            return SynthesisReport(
                overall_score=score,
                grade=data.get("grade", _score_to_grade(score)),
                executive_summary=data.get("executive_summary", ""),
                critical_issues=data.get("critical_issues", []),
                strengths=data.get("strengths", []),
                roadmap=data.get("roadmap", []),
                agent_reports=agent_reports,
            )
        except Exception:
            avg = sum(r.score for r in agent_reports) // max(len(agent_reports), 1)
            return SynthesisReport(
                overall_score=avg,
                grade=_score_to_grade(avg),
                executive_summary="Synthesis parse error — see individual reports.",
                agent_reports=agent_reports,
            )


def _score_to_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 45:
        return "D"
    return "F"
