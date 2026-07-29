"""Git repository analysis engine — extracts raw data via subprocess git commands."""

import subprocess
import os
import re
from collections import defaultdict, Counter
from datetime import datetime, timezone
from typing import Optional


def _run_git(args: list[str], repo_path: str) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_repo(path: str) -> str:
    """Return the repo root or raise if path is not a git repo."""
    try:
        root = _run_git(["rev-parse", "--show-toplevel"], path)
        return root
    except RuntimeError:
        raise ValueError(f"'{path}' is not inside a git repository.")


def get_repo_name(repo_path: str) -> str:
    try:
        remote = _run_git(["remote", "get-url", "origin"], repo_path)
        return remote.rstrip("/").split("/")[-1].removesuffix(".git")
    except RuntimeError:
        return os.path.basename(repo_path)


def get_basic_stats(repo_path: str) -> dict:
    total_commits = int(_run_git(["rev-list", "--count", "HEAD"], repo_path))
    branches_out = _run_git(["branch", "-a"], repo_path)
    branch_count = len([b for b in branches_out.splitlines() if b.strip()])

    try:
        tags_out = _run_git(["tag"], repo_path)
        tag_count = len([t for t in tags_out.splitlines() if t.strip()])
    except RuntimeError:
        tag_count = 0

    first_commit_ts = _run_git(["log", "--reverse", "--format=%ct", "--max-count=1"], repo_path)
    last_commit_ts = _run_git(["log", "--format=%ct", "--max-count=1"], repo_path)

    first_date = datetime.fromtimestamp(int(first_commit_ts), tz=timezone.utc)
    last_date = datetime.fromtimestamp(int(last_commit_ts), tz=timezone.utc)
    age_days = (last_date - first_date).days or 1

    return {
        "total_commits": total_commits,
        "branch_count": branch_count,
        "tag_count": tag_count,
        "first_date": first_date,
        "last_date": last_date,
        "age_days": age_days,
        "commits_per_day": round(total_commits / age_days, 2),
    }


def get_contributor_stats(repo_path: str) -> list[dict]:
    raw = _run_git(
        ["log", "--format=%ae|%an", "--no-merges"],
        repo_path,
    )
    if not raw:
        return []
    counter: Counter = Counter()
    names: dict = {}
    for line in raw.splitlines():
        if "|" not in line:
            continue
        email, name = line.split("|", 1)
        counter[email] += 1
        names[email] = name

    total = sum(counter.values())
    result = []
    for email, count in counter.most_common(10):
        result.append({
            "name": names[email],
            "email": email,
            "commits": count,
            "pct": round(count / total * 100, 1),
        })
    return result


def get_hourly_distribution(repo_path: str) -> dict[int, int]:
    raw = _run_git(["log", "--format=%ci", "--no-merges"], repo_path)
    dist: dict[int, int] = defaultdict(int)
    for line in raw.splitlines():
        try:
            dt = datetime.fromisoformat(line.strip())
            dist[dt.hour] += 1
        except (ValueError, AttributeError):
            pass
    return dict(dist)


def get_weekday_distribution(repo_path: str) -> dict[int, int]:
    raw = _run_git(["log", "--format=%ci", "--no-merges"], repo_path)
    dist: dict[int, int] = defaultdict(int)
    for line in raw.splitlines():
        try:
            dt = datetime.fromisoformat(line.strip())
            dist[dt.weekday()] += 1  # 0=Mon … 6=Sun
        except (ValueError, AttributeError):
            pass
    return dict(dist)


def get_commit_heatmap(repo_path: str, weeks: int = 52) -> dict[str, int]:
    """Return {YYYY-MM-DD: count} for the last `weeks` weeks."""
    raw = _run_git(["log", "--format=%cd", "--date=short", "--no-merges"], repo_path)
    counts: Counter = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if line:
            counts[line] += 1
    return dict(counts)


def get_file_hotspots(repo_path: str, top_n: int = 10) -> list[dict]:
    raw = _run_git(
        ["log", "--no-merges", "--name-only", "--format="],
        repo_path,
    )
    counter: Counter = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if line and not line.startswith("commit "):
            counter[line] += 1
    result = []
    for path, count in counter.most_common(top_n):
        result.append({"file": path, "changes": count})
    return result


def get_commit_keywords(repo_path: str, top_n: int = 20) -> list[tuple[str, int]]:
    raw = _run_git(["log", "--format=%s", "--no-merges"], repo_path)
    stop_words = {
        "a", "an", "the", "and", "or", "but", "for", "in", "on", "at", "to",
        "of", "with", "from", "by", "is", "are", "was", "were", "be", "been",
        "this", "that", "it", "its", "as", "not", "add", "fix", "update",
        "use", "set", "get", "remove", "change", "new", "old", "some", "all",
        "also", "more", "no", "do", "if", "up", "out", "into", "when",
    }
    counter: Counter = Counter()
    for line in raw.splitlines():
        words = re.findall(r"[a-zA-Z]{3,}", line.lower())
        for w in words:
            if w not in stop_words:
                counter[w] += 1
    return counter.most_common(top_n)


def get_growth_timeline(repo_path: str, buckets: int = 12) -> list[dict]:
    """Return monthly commit counts for the last `buckets` months."""
    raw = _run_git(["log", "--format=%cd", "--date=format:%Y-%m", "--no-merges"], repo_path)
    counter: Counter = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if line:
            counter[line] += 1
    sorted_months = sorted(counter.keys())[-buckets:]
    return [{"month": m, "commits": counter[m]} for m in sorted_months]


def get_language_breakdown(repo_path: str) -> list[dict]:
    """Approximate language breakdown by file extension."""
    try:
        raw = _run_git(
            ["ls-files"],
            repo_path,
        )
    except RuntimeError:
        return []

    ext_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".jsx": "React JSX", ".tsx": "React TSX", ".java": "Java",
        ".go": "Go", ".rs": "Rust", ".cpp": "C++", ".c": "C",
        ".cs": "C#", ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
        ".kt": "Kotlin", ".sh": "Shell", ".html": "HTML", ".css": "CSS",
        ".scss": "SCSS", ".md": "Markdown", ".json": "JSON", ".yaml": "YAML",
        ".yml": "YAML", ".toml": "TOML", ".sql": "SQL",
    }
    counter: Counter = Counter()
    for f in raw.splitlines():
        ext = os.path.splitext(f.strip())[1].lower()
        lang = ext_map.get(ext)
        if lang:
            counter[lang] += 1

    total = sum(counter.values()) or 1
    return [
        {"lang": lang, "files": count, "pct": round(count / total * 100, 1)}
        for lang, count in counter.most_common(8)
    ]
