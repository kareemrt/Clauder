"""Claude API integration for code review."""

import json
import anthropic
from dataclasses import dataclass, field

from .config import ReviewConfig


@dataclass
class Issue:
    category: str
    severity: str
    title: str
    description: str
    file: str = ""
    line: str = ""
    suggestion: str = ""


@dataclass
class ReviewResult:
    summary: str
    score: int
    issues: list[Issue] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    raw_diff_lines: int = 0

    @property
    def critical_count(self):
        return sum(1 for i in self.issues if i.severity == "critical")

    @property
    def high_count(self):
        return sum(1 for i in self.issues if i.severity == "high")

    @property
    def medium_count(self):
        return sum(1 for i in self.issues if i.severity == "medium")

    @property
    def low_count(self):
        return sum(1 for i in self.issues if i.severity in ("low", "info"))

    def by_category(self) -> dict[str, list[Issue]]:
        cats: dict[str, list[Issue]] = {}
        for issue in self.issues:
            cats.setdefault(issue.category, []).append(issue)
        return cats


REVIEW_SYSTEM_PROMPT = """You are an expert code reviewer with deep knowledge of software engineering
best practices, security, performance optimization, and clean code principles.

Your task is to review code changes and produce a structured JSON analysis. Be thorough but pragmatic —
focus on real issues that matter, not nitpicks.

Return ONLY valid JSON matching this exact schema:
{
  "summary": "2-3 sentence overview of the changes and their quality",
  "score": <integer 0-100 representing overall code quality>,
  "highlights": ["list of 2-4 things done well"],
  "issues": [
    {
      "category": "<one of: bugs | security | performance | style | docs>",
      "severity": "<one of: critical | high | medium | low | info>",
      "title": "Short descriptive title",
      "description": "Clear explanation of the problem",
      "file": "filename if identifiable, else empty string",
      "line": "line number or range if identifiable, else empty string",
      "suggestion": "Concrete suggestion for how to fix this"
    }
  ]
}

Severity guide:
- critical: Will definitely cause bugs, crashes, or security vulnerabilities
- high: Likely to cause problems, significant code smell
- medium: Could cause issues, should be improved
- low: Minor improvement opportunity
- info: Just a note or alternative approach"""


def _build_review_prompt(diff: str, context: str = "") -> str:
    parts = []
    if context:
        parts.append(f"Context: {context}\n")
    parts.append("Please review the following code changes:\n")
    parts.append("```diff")
    parts.append(diff[:60_000])  # Cap at ~60k chars to stay within token limits
    parts.append("```")
    if len(diff) > 60_000:
        parts.append(f"\n[Note: diff truncated — showing first 60,000 of {len(diff):,} characters]")
    return "\n".join(parts)


def _build_file_prompt(files: dict[str, str], context: str = "") -> str:
    parts = []
    if context:
        parts.append(f"Context: {context}\n")
    parts.append("Please review the following file(s):\n")
    total = 0
    for name, content in files.items():
        chunk = content[:20_000]
        total += len(chunk)
        parts.append(f"**{name}**")
        parts.append(f"```\n{chunk}\n```")
        if total > 50_000:
            parts.append("\n[Note: remaining files truncated due to size]")
            break
    return "\n".join(parts)


def review_diff(diff: str, config: ReviewConfig, context: str = "") -> ReviewResult:
    config.validate()
    if not diff.strip():
        return ReviewResult(
            summary="No changes found to review.",
            score=100,
            highlights=["No changes detected."],
        )

    client = anthropic.Anthropic(api_key=config.api_key)
    prompt = _build_review_prompt(diff, context)

    message = client.messages.create(
        model=config.model,
        max_tokens=config.max_tokens,
        system=REVIEW_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    return _parse_response(raw, diff)


def review_files(file_paths: list[str], config: ReviewConfig, context: str = "") -> ReviewResult:
    config.validate()
    from .git_utils import get_file_content

    files = {}
    for path in file_paths:
        try:
            files[path] = get_file_content(path)
        except Exception as e:
            files[path] = f"[Error reading file: {e}]"

    client = anthropic.Anthropic(api_key=config.api_key)
    prompt = _build_file_prompt(files, context)

    message = client.messages.create(
        model=config.model,
        max_tokens=config.max_tokens,
        system=REVIEW_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    total_content = "\n".join(files.values())
    return _parse_response(raw, total_content)


def _parse_response(raw: str, source: str) -> ReviewResult:
    # Strip markdown code fences if Claude wrapped JSON in them
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return ReviewResult(
            summary=raw[:500],
            score=50,
            highlights=[],
            issues=[],
            raw_diff_lines=source.count("\n"),
        )

    issues = []
    for item in data.get("issues", []):
        issues.append(Issue(
            category=item.get("category", "style"),
            severity=item.get("severity", "low"),
            title=item.get("title", ""),
            description=item.get("description", ""),
            file=item.get("file", ""),
            line=item.get("line", ""),
            suggestion=item.get("suggestion", ""),
        ))

    return ReviewResult(
        summary=data.get("summary", ""),
        score=max(0, min(100, int(data.get("score", 70)))),
        highlights=data.get("highlights", []),
        issues=issues,
        raw_diff_lines=source.count("\n"),
    )
