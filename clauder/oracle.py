"""The Oracle — Claude AI integration for mystical code review."""

import json
import os
import re
from typing import Optional
import anthropic

from .prompts import ORACLE_SYSTEM_PROMPT, QUICK_PROPHECY_PROMPT
from .analyzer import CodeMetrics


DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_CODE_CHARS = 50_000


def _truncate_code(code: str, max_chars: int = MAX_CODE_CHARS) -> tuple[str, bool]:
    if len(code) <= max_chars:
        return code, False
    truncated = code[:max_chars]
    last_newline = truncated.rfind("\n")
    if last_newline > max_chars * 0.8:
        truncated = truncated[:last_newline]
    return truncated + "\n\n[... truncated for Oracle review ...]", True


def consult_oracle(
    code: str,
    file_path: str,
    metrics: Optional[CodeMetrics],
    language: str = "Unknown",
    api_key: Optional[str] = None,
) -> dict:
    """Send code to The Oracle and receive its mystical review."""
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    code_excerpt, was_truncated = _truncate_code(code)

    context_lines = [f"File: {file_path}", f"Language: {language}"]
    if metrics:
        context_lines += [
            f"Lines of code: {metrics.code_lines} (total: {metrics.total_lines})",
            f"Functions: {metrics.function_count}, Classes: {metrics.class_count}",
            f"Complexity score: {metrics.complexity_score}",
            f"Has tests: {metrics.has_tests}",
            f"Has docstrings: {metrics.has_docstrings}",
        ]
        if metrics.warnings:
            context_lines.append(f"Pre-analysis warnings: {'; '.join(metrics.warnings)}")
    if was_truncated:
        context_lines.append("Note: Code was truncated due to length")

    context = "\n".join(context_lines)
    user_message = f"""Context:\n{context}\n\n```{language.lower()}\n{code_excerpt}\n```"""

    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=4096,
        system=ORACLE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Oracle returned unparseable response:\n{raw}")


def quick_prophecy(code_snippet: str, api_key: Optional[str] = None) -> str:
    """Get a single-paragraph Oracle prophecy for a code snippet."""
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=512,
        system=QUICK_PROPHECY_PROMPT,
        messages=[{"role": "user", "content": f"```\n{code_snippet}\n```"}],
    )
    return response.content[0].text.strip()
