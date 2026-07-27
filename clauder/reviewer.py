"""Core review logic: send diff to Claude and parse the response."""

import json
import re
from dataclasses import dataclass, field

import anthropic

from .config import MAX_DIFF_CHARS, REVIEW_PROMPTS, ReviewConfig
from .diff_parser import ParsedDiff


@dataclass
class ReviewComment:
    file: str
    line: int | None
    severity: str  # critical / high / medium / low / info
    category: str  # security / bug / performance / style / suggestion
    message: str
    suggestion: str | None = None


@dataclass
class ReviewResult:
    summary: str
    comments: list[ReviewComment] = field(default_factory=list)
    overall_score: int = 0  # 0-100
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def by_severity(self) -> dict[str, list[ReviewComment]]:
        result: dict[str, list[ReviewComment]] = {}
        for c in self.comments:
            result.setdefault(c.severity, []).append(c)
        return result

    @property
    def critical_count(self) -> int:
        return len(self.by_severity.get("critical", []))

    @property
    def high_count(self) -> int:
        return len(self.by_severity.get("high", []))


_SYSTEM_PROMPT = """\
You are Clauder, an expert code review assistant. Analyze the provided git diff and produce a structured JSON response.

Your JSON response must have this exact shape:
{
  "summary": "<2-3 sentence overview of the changes and their quality>",
  "overall_score": <integer 0-100, where 100 is perfect>,
  "comments": [
    {
      "file": "<filename>",
      "line": <line number or null>,
      "severity": "<critical|high|medium|low|info>",
      "category": "<security|bug|performance|style|suggestion>",
      "message": "<clear, actionable description of the issue>",
      "suggestion": "<concrete code fix or improvement, or null>"
    }
  ]
}

Severity guide:
- critical: Must fix before merging (security vuln, data loss, crash)
- high: Should fix before merging (serious bug, major performance issue)
- medium: Should address soon (code smell, minor bug risk)
- low: Nice to have (style, naming)
- info: Observation or praise

Be specific. Reference exact line content when possible. Respond ONLY with valid JSON."""


def _build_user_message(diff: ParsedDiff, config: ReviewConfig) -> str:
    mode_instruction = REVIEW_PROMPTS[config.mode]
    diff_text = "\n\n".join(f.to_review_text() for f in diff.files if not f.is_binary)
    if len(diff_text) > MAX_DIFF_CHARS:
        diff_text = diff_text[:MAX_DIFF_CHARS] + "\n\n[diff truncated — too large]"

    stats = (
        f"Files changed: {len(diff.files)} | "
        f"+{diff.total_added} lines / -{diff.total_removed} lines"
    )
    return f"{mode_instruction}\n\nDiff stats: {stats}\n\n{diff_text}"


def _parse_response(raw: str) -> dict:
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())
    return json.loads(raw)


def review_diff(diff: ParsedDiff, config: ReviewConfig) -> ReviewResult:
    """Send the diff to Claude and return a structured ReviewResult."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model=config.model,
        max_tokens=config.max_tokens,
        system=_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": _build_user_message(diff, config)}
        ],
    )

    raw_text = message.content[0].text
    data = _parse_response(raw_text)

    comments = [
        ReviewComment(
            file=c.get("file", ""),
            line=c.get("line"),
            severity=c.get("severity", "info"),
            category=c.get("category", "suggestion"),
            message=c.get("message", ""),
            suggestion=c.get("suggestion"),
        )
        for c in data.get("comments", [])
    ]

    return ReviewResult(
        summary=data.get("summary", ""),
        overall_score=int(data.get("overall_score", 0)),
        comments=comments,
        model=config.model,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
    )
