"""Code analysis utilities — metrics, language detection, complexity."""

import re
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


LANGUAGE_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".jsx": "JavaScript (React)", ".tsx": "TypeScript (React)",
    ".go": "Go", ".rs": "Rust", ".java": "Java", ".c": "C",
    ".cpp": "C++", ".cs": "C#", ".rb": "Ruby", ".php": "PHP",
    ".swift": "Swift", ".kt": "Kotlin", ".sh": "Shell",
    ".html": "HTML", ".css": "CSS", ".sql": "SQL",
    ".yaml": ".yaml", ".yml": "YAML", ".json": "JSON",
    ".md": "Markdown", ".tf": "Terraform",
}

COMPLEXITY_KEYWORDS = {
    "Python": ["if", "elif", "else", "for", "while", "try", "except", "with", "lambda", "and", "or"],
    "JavaScript": ["if", "else", "for", "while", "try", "catch", "&&", "||", "?"],
    "TypeScript": ["if", "else", "for", "while", "try", "catch", "&&", "||", "?"],
    "default": ["if", "else", "for", "while", "try", "catch"],
}


@dataclass
class CodeMetrics:
    language: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    avg_line_length: float
    max_line_length: int
    function_count: int
    class_count: int
    complexity_score: int
    has_tests: bool
    has_docstrings: bool
    file_path: str
    file_size_kb: float
    warnings: list[str] = field(default_factory=list)


def detect_language(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    return LANGUAGE_MAP.get(ext, "Unknown")


def count_functions(content: str, language: str) -> int:
    patterns = {
        "Python": r"^\s*def\s+\w+",
        "JavaScript": r"(function\s+\w+|const\s+\w+\s*=\s*(async\s+)?\(|=>\s*\{)",
        "TypeScript": r"(function\s+\w+|const\s+\w+\s*=\s*(async\s+)?\(|=>\s*\{)",
        "Go": r"^\s*func\s+",
        "Rust": r"^\s*fn\s+",
        "Java": r"(public|private|protected|static)\s+\w+\s+\w+\s*\(",
        "default": r"^\s*(def|func|function|fn)\s+\w+",
    }
    pattern = patterns.get(language, patterns["default"])
    return len(re.findall(pattern, content, re.MULTILINE))


def count_classes(content: str, language: str) -> int:
    patterns = {
        "Python": r"^\s*class\s+\w+",
        "JavaScript": r"^\s*class\s+\w+",
        "TypeScript": r"^\s*(class|interface|type)\s+\w+",
        "Java": r"^\s*(public|private)?\s*(class|interface|enum)\s+\w+",
        "default": r"^\s*class\s+\w+",
    }
    pattern = patterns.get(language, patterns["default"])
    return len(re.findall(pattern, content, re.MULTILINE))


def calculate_complexity(content: str, language: str) -> int:
    """Rough cyclomatic complexity approximation."""
    keywords = COMPLEXITY_KEYWORDS.get(language, COMPLEXITY_KEYWORDS["default"])
    score = 1
    for kw in keywords:
        score += len(re.findall(r"\b" + re.escape(kw) + r"\b", content))
    return min(score, 999)


def analyze_file(file_path: str) -> Optional[CodeMetrics]:
    try:
        path = Path(file_path)
        if not path.exists():
            return None

        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        language = detect_language(file_path)

        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        line_lengths = []
        warnings = []

        comment_patterns = {
            "Python": r"^\s*#",
            "JavaScript": r"^\s*(//|/\*|\*)",
            "TypeScript": r"^\s*(//|/\*|\*)",
            "default": r"^\s*(#|//|/\*|\*)",
        }
        comment_re = re.compile(comment_patterns.get(language, comment_patterns["default"]))

        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif comment_re.match(line):
                comment_lines += 1
            else:
                code_lines += 1
            line_lengths.append(len(line))

        max_len = max(line_lengths) if line_lengths else 0
        avg_len = sum(line_lengths) / len(line_lengths) if line_lengths else 0

        if max_len > 120:
            warnings.append(f"Lines exceeding 120 characters detected (max: {max_len})")
        if code_lines > 0 and comment_lines / code_lines < 0.05:
            warnings.append("Very few comments — consider documenting complex logic")

        has_tests = bool(re.search(r"(def test_|it\(|describe\(|#\[test\]|@Test)", content))
        has_docstrings = bool(re.search(r'("""|\'\'\')[^"\']+(\"\"\"|\'\'\')', content, re.DOTALL))

        return CodeMetrics(
            language=language,
            total_lines=len(lines),
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            avg_line_length=round(avg_len, 1),
            max_line_length=max_len,
            function_count=count_functions(content, language),
            class_count=count_classes(content, language),
            complexity_score=calculate_complexity(content, language),
            has_tests=has_tests,
            has_docstrings=has_docstrings,
            file_path=file_path,
            file_size_kb=round(path.stat().st_size / 1024, 2),
            warnings=warnings,
        )
    except Exception as e:
        return None


def read_file_content(file_path: str) -> Optional[str]:
    try:
        return Path(file_path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
