from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any

import anthropic

from clauder.models import AgentReport, Finding, RepoData


class AgentBase(ABC):
    name: str
    emoji: str
    description: str
    system_prompt: str

    def __init__(self, client: anthropic.AsyncAnthropic, model: str):
        self.client = client
        self.model = model

    async def analyze(self, repo_data: RepoData) -> AgentReport:
        context = _build_context(repo_data)
        user_message = self._build_user_message(repo_data, context)

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = response.content[0].text
        return self._parse_response(raw)

    def _build_user_message(self, repo_data: RepoData, context: str) -> str:
        return f"""Analyze this repository and return a JSON report.

Repository: {repo_data.owner}/{repo_data.name}
Description: {repo_data.description or 'N/A'}
Primary Language: {repo_data.language or 'Unknown'}
Stars: {repo_data.stars}
Topics: {', '.join(repo_data.topics) or 'none'}

File tree ({len(repo_data.file_tree)} total files, showing analyzed subset):
{chr(10).join(repo_data.file_tree[:100])}

--- FILE CONTENTS ---
{context}

Return ONLY valid JSON matching this schema:
{{
  "summary": "2-3 sentence summary of your findings",
  "score": <integer 0-100>,
  "findings": [
    {{
      "severity": "critical|high|medium|low|info",
      "category": "<category>",
      "title": "<short title>",
      "description": "<detailed description>",
      "file": "<path or null>",
      "line": <line number or null>,
      "recommendation": "<actionable fix>"
    }}
  ],
  "highlights": ["<positive aspect 1>", "<positive aspect 2>"]
}}"""

    def _parse_response(self, raw: str) -> AgentReport:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return AgentReport(
                agent=self.name,
                emoji=self.emoji,
                summary="Failed to parse agent response.",
                score=0,
                findings=[],
                highlights=[],
            )

        try:
            data = json.loads(match.group())
            findings = [Finding(**f) for f in data.get("findings", [])]
            return AgentReport(
                agent=self.name,
                emoji=self.emoji,
                summary=data.get("summary", ""),
                score=max(0, min(100, int(data.get("score", 50)))),
                findings=findings,
                highlights=data.get("highlights", []),
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return AgentReport(
                agent=self.name,
                emoji=self.emoji,
                summary=f"Parse error. Raw: {raw[:200]}",
                score=50,
                findings=[],
                highlights=[],
            )


def _build_context(repo_data: RepoData, max_chars: int = 60_000) -> str:
    parts = []
    total = 0
    for f in repo_data.files:
        block = f"=== {f.path} ===\n{f.content}\n"
        if total + len(block) > max_chars:
            parts.append(f"=== {f.path} === [truncated — context limit reached]\n")
            break
        parts.append(block)
        total += len(block)
    return "\n".join(parts)
