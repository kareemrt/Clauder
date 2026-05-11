"""Claude-powered deep code analysis engine."""

import os
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

import anthropic

ANALYSIS_TOOL = {
    "name": "submit_analysis",
    "description": "Submit structured code review results",
    "input_schema": {
        "type": "object",
        "properties": {
            "quality_score": {
                "type": "number",
                "description": "Overall quality score 0-10"
            },
            "grade": {
                "type": "string",
                "description": "Letter grade: A+, A, B+, B, C, D, or F"
            },
            "summary": {
                "type": "string",
                "description": "2-3 sentence executive summary of the code quality"
            },
            "bugs": {
                "type": "array",
                "description": "Potential bugs, errors, and logical issues",
                "items": {
                    "type": "object",
                    "properties": {
                        "line": {"type": "integer"},
                        "description": {"type": "string"},
                        "severity": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"]
                        },
                        "fix": {"type": "string"}
                    },
                    "required": ["description", "severity"]
                }
            },
            "security_concerns": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "severity": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"]
                        }
                    },
                    "required": ["description", "severity"]
                }
            },
            "complexity_hotspots": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "issue": {"type": "string"},
                        "suggestion": {"type": "string"}
                    },
                    "required": ["name", "issue"]
                }
            },
            "documentation_gaps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item": {"type": "string"},
                        "recommendation": {"type": "string"}
                    },
                    "required": ["item"]
                }
            },
            "strengths": {
                "type": "array",
                "items": {"type": "string"}
            },
            "improvements": {
                "type": "array",
                "items": {"type": "string"}
            },
            "patterns_used": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Design patterns and Python best practices identified"
            }
        },
        "required": [
            "quality_score", "grade", "summary",
            "bugs", "strengths", "improvements"
        ]
    }
}

SYSTEM_PROMPT = """You are ClauderBot, an elite Python code review specialist. You perform thorough, \
actionable code reviews covering correctness, security, maintainability, performance, and Pythonic style.

Be specific: reference function names, approximate line numbers, and provide concrete fix suggestions.
Prioritize real issues over minor style nitpicks. Security and correctness always come first."""


@dataclass
class FileAnalysis:
    path: str
    quality_score: float
    grade: str
    summary: str
    bugs: list = field(default_factory=list)
    security_concerns: list = field(default_factory=list)
    complexity_hotspots: list = field(default_factory=list)
    documentation_gaps: list = field(default_factory=list)
    strengths: list = field(default_factory=list)
    improvements: list = field(default_factory=list)
    patterns_used: list = field(default_factory=list)
    lines_of_code: int = 0
    functions_count: int = 0
    classes_count: int = 0
    error: Optional[str] = None


class ClaudeAnalyzer:
    MODEL = "claude-sonnet-4-6"
    MAX_FILE_CHARS = 14_000

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=key)

    def analyze_file(self, path: str) -> FileAnalysis:
        """Run deep AI review on a Python file using Claude tool use."""
        file_path = Path(path)
        if not file_path.exists():
            return FileAnalysis(
                path=path, quality_score=0, grade="N/A", summary="",
                error=f"File not found: {path}"
            )

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as exc:
            return FileAnalysis(
                path=path, quality_score=0, grade="N/A", summary="",
                error=str(exc)
            )

        lines = content.split("\n")
        loc = sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#"))
        functions = sum(1 for ln in lines if ln.strip().startswith("def "))
        classes = sum(1 for ln in lines if ln.strip().startswith("class "))

        truncated = content[: self.MAX_FILE_CHARS]
        was_truncated = len(content) > self.MAX_FILE_CHARS

        user_msg = (
            f"Review this Python file and call `submit_analysis` with your findings.\n\n"
            f"**File:** `{file_path.name}` | **Path:** `{path}`\n"
            f"**Metrics:** {len(lines)} lines, {loc} code lines, "
            f"{functions} functions, {classes} classes"
            + (" *(truncated)*" if was_truncated else "")
            + f"\n\n```python\n{truncated}\n```"
        )

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=[ANALYSIS_TOOL],
            tool_choice={"type": "tool", "name": "submit_analysis"},
            messages=[{"role": "user", "content": user_msg}],
        )

        data: dict = {}
        for block in response.content:
            if block.type == "tool_use" and block.name == "submit_analysis":
                data = block.input
                break

        return FileAnalysis(
            path=path,
            quality_score=float(data.get("quality_score", 0)),
            grade=data.get("grade", "?"),
            summary=data.get("summary", ""),
            bugs=data.get("bugs", []),
            security_concerns=data.get("security_concerns", []),
            complexity_hotspots=data.get("complexity_hotspots", []),
            documentation_gaps=data.get("documentation_gaps", []),
            strengths=data.get("strengths", []),
            improvements=data.get("improvements", []),
            patterns_used=data.get("patterns_used", []),
            lines_of_code=loc,
            functions_count=functions,
            classes_count=classes,
        )

    def chat_about_code(
        self,
        path: str,
        question: str,
        history: Optional[list] = None,
    ) -> str:
        """Chat with Claude about a specific file."""
        file_path = Path(path)
        code = file_path.read_text(encoding="utf-8") if file_path.exists() else ""

        messages: list = list(history or [])
        if not history:
            messages.append({
                "role": "user",
                "content": (
                    f"Here's the Python file `{file_path.name}` I want to discuss:\n\n"
                    f"```python\n{code[:8000]}\n```\n\n{question}"
                ),
            })
        else:
            messages.append({"role": "user", "content": question})

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text

    def generate_git_insights(self, commits: list) -> str:
        """Generate AI narrative from git commit history."""
        if not commits:
            return "No commit history available."

        commit_log = "\n".join(
            f"- {c['hash'][:7]} | {c['date']} | {c['author'][:20]} | {c['message']}"
            for c in commits[:60]
        )

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": (
                    "Analyze this git commit history and provide insightful observations about:\n"
                    "1. Development velocity and work patterns\n"
                    "2. Areas of frequent change (potential instability or active development)\n"
                    "3. The codebase evolution story\n"
                    "4. Notable trends or concerns\n\n"
                    f"Commits:\n{commit_log}\n\n"
                    "Write 3-4 concise, insightful paragraphs."
                ),
            }],
        )
        return response.content[0].text
