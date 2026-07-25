"""Git log parsing and raw data extraction."""

import subprocess
import os
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path


def run_git(args: list[str], cwd: str) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        errors="replace",
    )
    return result.stdout.strip()


def get_repo_name(repo_path: str) -> str:
    name = run_git(["rev-parse", "--show-toplevel"], repo_path)
    return Path(name).name if name else Path(repo_path).name


def get_all_commits(repo_path: str) -> list[dict]:
    """Return list of commit dicts with timestamp, author, email, files changed."""
    sep = "\x1f"  # ASCII unit separator — safe in subprocess args, rare in real data
    fmt = f"%H{sep}%ae{sep}%an{sep}%ct{sep}%s"
    raw = run_git(["log", "--pretty=format:" + fmt, "--name-only", "--diff-filter=ACDMR"], repo_path)

    commits = []
    current = None
    for line in raw.splitlines():
        if sep in line:
            if current:
                commits.append(current)
            parts = line.split(sep)
            if len(parts) == 5:
                current = {
                    "hash": parts[0],
                    "email": parts[1],
                    "author": parts[2],
                    "timestamp": int(parts[3]),
                    "subject": parts[4],
                    "files": [],
                }
        elif line.strip() and current:
            current["files"].append(line.strip())
    if current:
        commits.append(current)
    return commits


def get_file_extensions(repo_path: str) -> dict[str, int]:
    """Count lines per file extension in the working tree."""
    raw = run_git(
        ["ls-files"],
        repo_path,
    )
    ext_counts: dict[str, int] = defaultdict(int)
    for filepath in raw.splitlines():
        p = Path(filepath)
        suffix = p.suffix.lower() or "(no ext)"
        try:
            full = os.path.join(repo_path, filepath)
            with open(full, "r", errors="replace") as f:
                lines = sum(1 for _ in f)
            ext_counts[suffix] += lines
        except Exception:
            pass
    return dict(ext_counts)


def get_first_last_commit_dates(commits: list[dict]) -> tuple[datetime, datetime]:
    timestamps = [c["timestamp"] for c in commits]
    if not timestamps:
        now = datetime.now(timezone.utc)
        return now, now
    first = datetime.fromtimestamp(min(timestamps), tz=timezone.utc)
    last = datetime.fromtimestamp(max(timestamps), tz=timezone.utc)
    return first, last
