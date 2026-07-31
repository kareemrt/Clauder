"""Parse git log and compute repository statistics."""

import subprocess
import re
from datetime import datetime, timezone
from collections import defaultdict, Counter
from pathlib import Path


def _run(cmd, cwd):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def get_repo_name(repo_path: str) -> str:
    try:
        remote = _run(["git", "remote", "get-url", "origin"], repo_path)
        return Path(remote.rstrip("/").rstrip(".git")).name
    except Exception:
        return Path(repo_path).resolve().name


def parse_commits(repo_path: str) -> list[dict]:
    """Return list of commit dicts with author, date, files_changed."""
    sep = "|||"
    fmt = f"%H{sep}%aN{sep}%aE{sep}%ai{sep}%s"
    try:
        raw = _run(["git", "log", f"--format={fmt}", "--no-merges"], repo_path)
    except subprocess.CalledProcessError:
        return []

    commits = []
    for line in raw.splitlines():
        parts = line.split(sep, 4)
        if len(parts) != 5:
            continue
        sha, author, email, date_str, subject = parts
        try:
            dt = datetime.fromisoformat(date_str).astimezone(timezone.utc)
        except ValueError:
            continue
        commits.append(
            {
                "sha": sha[:8],
                "author": author,
                "email": email,
                "date": dt,
                "subject": subject,
            }
        )
    return commits


def parse_file_changes(repo_path: str) -> Counter:
    """Count how many times each file path was touched across all commits."""
    try:
        raw = _run(
            ["git", "log", "--no-merges", "--name-only", "--format="],
            repo_path,
        )
    except subprocess.CalledProcessError:
        return Counter()

    counter: Counter = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if line:
            counter[line] += 1
    return counter


def compute_stats(commits: list[dict], file_changes: Counter) -> dict:
    if not commits:
        return {}

    earliest = min(c["date"] for c in commits)
    latest = max(c["date"] for c in commits)

    by_author: Counter = Counter()
    by_dow: Counter = Counter()      # 0=Mon … 6=Sun
    by_hour: Counter = Counter()
    by_date: Counter = Counter()     # YYYY-MM-DD → count

    for c in commits:
        by_author[c["author"]] += 1
        by_dow[c["date"].weekday()] += 1
        by_hour[c["date"].hour] += 1
        by_date[c["date"].strftime("%Y-%m-%d")] += 1

    return {
        "total_commits": len(commits),
        "total_authors": len(by_author),
        "date_range": (earliest, latest),
        "by_author": by_author.most_common(),
        "by_dow": {k: by_dow[k] for k in range(7)},
        "by_hour": {k: by_hour[k] for k in range(24)},
        "by_date": dict(by_date),
        "top_files": file_changes.most_common(15),
        "recent_commits": commits[:10],
    }
