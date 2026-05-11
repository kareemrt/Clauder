"""File system scanner and git utilities for Clauder."""

import subprocess
from pathlib import Path
from typing import Optional

_IGNORE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "env", "ENV",
    "node_modules", ".eggs", "build", "dist", ".tox",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
}


def scan_python_files(path: str, max_files: int = 50) -> list[str]:
    """Return Python files under *path*, skipping common noise dirs."""
    root = Path(path)
    if root.is_file():
        return [str(root)] if root.suffix == ".py" else []

    results: list[str] = []
    for py_file in sorted(root.rglob("*.py")):
        if any(part in _IGNORE_DIRS for part in py_file.parts):
            continue
        results.append(str(py_file))
        if len(results) >= max_files:
            break
    return results


def get_file_stats(path: str) -> dict:
    """Return basic line-count metrics for a Python file."""
    try:
        content = Path(path).read_text(encoding="utf-8")
    except Exception:
        return {}

    lines = content.split("\n")
    return {
        "total_lines": len(lines),
        "code_lines": sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#")),
        "comment_lines": sum(1 for ln in lines if ln.strip().startswith("#")),
        "blank_lines": sum(1 for ln in lines if not ln.strip()),
        "functions": sum(1 for ln in lines if ln.strip().startswith("def ")),
        "classes": sum(1 for ln in lines if ln.strip().startswith("class ")),
        "imports": sum(1 for ln in lines if ln.strip().startswith(("import ", "from "))),
        "avg_line_length": sum(len(ln) for ln in lines) // max(len(lines), 1),
        "max_line_length": max((len(ln) for ln in lines), default=0),
    }


def _git(args: list[str], cwd: str, timeout: int = 10) -> Optional[str]:
    """Run a git command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_git_commits(path: str, limit: int = 60) -> list[dict]:
    """Return recent non-merge commits as dicts."""
    output = _git(
        ["log", f"--max-count={limit}", "--format=%H|%ai|%an|%s", "--no-merges"],
        cwd=path,
    )
    if not output:
        return []

    commits = []
    for line in output.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0],
                "date": parts[1][:10],
                "author": parts[2],
                "message": parts[3],
            })
    return commits


def get_repo_info(path: str) -> dict:
    """Collect git repository metadata."""
    info: dict = {}

    remote = _git(["remote", "get-url", "origin"], cwd=path)
    if remote:
        info["remote"] = remote

    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    if branch:
        info["branch"] = branch

    count_str = _git(["rev-list", "--count", "HEAD"], cwd=path)
    if count_str and count_str.isdigit():
        info["total_commits"] = int(count_str)

    shortlog = _git(["shortlog", "-s", "HEAD"], cwd=path)
    if shortlog:
        contributors = []
        for line in shortlog.splitlines():
            parts = line.strip().split("\t", 1)
            if len(parts) == 2 and parts[0].isdigit():
                contributors.append({"commits": int(parts[0]), "name": parts[1]})
        info["contributors"] = contributors[:5]

    return info


def aggregate_stats(stats_list: list[dict]) -> dict:
    """Sum up per-file stats into project totals."""
    totals: dict = {}
    for stats in stats_list:
        for key, val in stats.items():
            if isinstance(val, int):
                totals[key] = totals.get(key, 0) + val
    return totals
