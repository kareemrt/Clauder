"""Static code analysis powered by Claude."""

import json
import os
import re
from pathlib import Path

import anthropic


def analyze_file(file_path: Path, model: str = "claude-sonnet-5") -> list[dict]:
    """
    Ask Claude to analyze a Python file for bugs, code smells, and improvements.
    Returns a list of finding dicts with keys: line, severity, issue, suggestion.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)
    code = file_path.read_text()

    prompt = f"""You are an expert Python code reviewer. Analyze the following file for bugs, code smells, security issues, and improvement opportunities.

File: `{file_path.name}`
```python
{code}
```

Return a JSON array of findings. Each finding must have:
- "line": approximate line number (integer, or null)
- "severity": one of "HIGH", "MEDIUM", "LOW", "INFO"
- "issue": a short description of the problem (max 80 chars)
- "suggestion": a concrete fix suggestion (max 120 chars)

Return ONLY the JSON array, no other text. Example:
[{{"line": 12, "severity": "HIGH", "issue": "SQL injection via f-string", "suggestion": "Use parameterized queries instead"}}]

If there are no issues, return an empty array: []"""

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip any markdown code fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        findings = json.loads(raw)
        if isinstance(findings, list):
            return findings
    except json.JSONDecodeError:
        # Attempt to extract array from text
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass

    return [{"line": None, "severity": "INFO", "issue": "Could not parse Claude response", "suggestion": raw[:200]}]


def explain_traceback(traceback_text: str, model: str = "claude-sonnet-5") -> str:
    """Ask Claude to explain a Python traceback in plain English."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Explain the following Python traceback to a developer in plain, friendly English.

Traceback:
```
{traceback_text}
```

Structure your response as:
1. **What went wrong** — one sentence
2. **Why it happened** — root cause in 2-3 sentences
3. **How to fix it** — concrete actionable steps (bullet points)

Be concise and direct. No fluff."""

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
