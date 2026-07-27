"""Configuration and constants for Clauder."""

from dataclasses import dataclass, field
from typing import Literal

ReviewMode = Literal["full", "security", "performance", "style", "bugs"]

REVIEW_PROMPTS: dict[str, str] = {
    "full": (
        "Perform a comprehensive code review covering correctness, security, "
        "performance, readability, and maintainability."
    ),
    "security": (
        "Focus exclusively on security vulnerabilities: injection attacks, "
        "authentication flaws, data exposure, insecure dependencies, "
        "cryptographic weaknesses, and OWASP Top 10 issues."
    ),
    "performance": (
        "Focus on performance: algorithmic complexity, unnecessary allocations, "
        "N+1 queries, blocking I/O, caching opportunities, and inefficient patterns."
    ),
    "style": (
        "Focus on code style and readability: naming conventions, function length, "
        "cyclomatic complexity, documentation, dead code, and consistency."
    ),
    "bugs": (
        "Hunt for bugs: off-by-one errors, null/undefined access, race conditions, "
        "exception handling gaps, incorrect logic, and edge cases."
    ),
}

SEVERITY_COLORS = {
    "critical": "bold red",
    "high":     "red",
    "medium":   "yellow",
    "low":      "cyan",
    "info":     "dim",
}

SEVERITY_EMOJI = {
    "critical": "🚨",
    "high":     "🔴",
    "medium":   "🟡",
    "low":      "🔵",
    "info":     "ℹ️",
}

MAX_DIFF_CHARS = 80_000  # ~20k tokens of diff content


@dataclass
class ReviewConfig:
    mode: ReviewMode = "full"
    model: str = "claude-opus-5"
    max_tokens: int = 4096
    github_token: str | None = None
    output_format: Literal["terminal", "markdown", "json"] = "terminal"
    include_summary: bool = True
    include_suggestions: bool = True
    min_severity: str = "info"
