"""Git repository analysis: parse commits, authors, file hotspots."""

import os
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple


@dataclass
class Commit:
    hash: str
    author: str
    email: str
    date: datetime
    message: str
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0


def _run(repo_path: str, args: List[str], timeout: int = 60) -> str:
    try:
        r = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return r.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def get_repo_info(repo_path: str) -> Dict:
    name = os.path.basename(os.path.abspath(repo_path))
    remote = _run(repo_path, ["remote", "get-url", "origin"]).strip()
    branch = _run(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    total_raw = _run(repo_path, ["rev-list", "--count", "HEAD"]).strip()
    total = int(total_raw) if total_raw.isdigit() else 0
    return {"name": name, "remote": remote, "branch": branch, "total_commits": total}


def get_commits(repo_path: str) -> List[Commit]:
    """Parse full commit history into Commit objects with stat info."""
    FSEP = "<|FS|>"
    CSEP = "<|CS|>"
    fmt = f"%H{FSEP}%an{FSEP}%ae{FSEP}%ai{FSEP}%s{CSEP}"

    raw = _run(repo_path, ["log", "--pretty=format:" + fmt, "--no-merges"])
    commits: List[Commit] = []

    for entry in raw.split(CSEP):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(FSEP)
        if len(parts) < 5:
            continue
        try:
            # git iso: "2024-01-15 10:30:00 +0000" — fromisoformat needs T separator
            date_str = parts[3].strip()
            # strip timezone offset for naive datetime
            date_str = re.sub(r"\s[+-]\d{4}$", "", date_str)
            date = datetime.fromisoformat(date_str)
        except (ValueError, IndexError):
            continue

        commits.append(Commit(
            hash=parts[0].strip(),
            author=parts[1].strip(),
            email=parts[2].strip(),
            date=date,
            message=parts[4].strip(),
        ))

    # Enrich with numstat (lines added/deleted) — one pass, much faster than per-commit show
    numstat_raw = _run(
        repo_path,
        ["log", "--no-merges", "--numstat", "--pretty=format:COMMIT:%H"],
        timeout=120,
    )

    stats_by_hash: Dict[str, Tuple[int, int, int]] = {}
    current_hash = None
    ins = dels = files = 0

    for line in numstat_raw.splitlines():
        if line.startswith("COMMIT:"):
            if current_hash:
                stats_by_hash[current_hash] = (files, ins, dels)
            current_hash = line[7:].strip()
            ins = dels = files = 0
        elif current_hash and line.strip():
            parts_n = line.split("\t")
            if len(parts_n) >= 2:
                try:
                    ins += int(parts_n[0])
                    dels += int(parts_n[1])
                    files += 1
                except ValueError:
                    pass  # binary files show "-"

    if current_hash:
        stats_by_hash[current_hash] = (files, ins, dels)

    for c in commits:
        if c.hash in stats_by_hash:
            c.files_changed, c.insertions, c.deletions = stats_by_hash[c.hash]

    return sorted(commits, key=lambda c: c.date)


def get_author_stats(commits: List[Commit]) -> Dict[str, Dict]:
    stats: Dict[str, Dict] = defaultdict(lambda: {
        "commits": 0, "insertions": 0, "deletions": 0,
        "first_commit": None, "last_commit": None,
    })
    for c in commits:
        s = stats[c.author]
        s["commits"] += 1
        s["insertions"] += c.insertions
        s["deletions"] += c.deletions
        if s["first_commit"] is None or c.date < s["first_commit"]:
            s["first_commit"] = c.date
        if s["last_commit"] is None or c.date > s["last_commit"]:
            s["last_commit"] = c.date
    return dict(stats)


def get_commit_date_map(commits: List[Commit]) -> Dict[str, int]:
    """Map 'YYYY-MM-DD' -> commit count."""
    counts: Counter = Counter()
    for c in commits:
        counts[c.date.strftime("%Y-%m-%d")] += 1
    return dict(counts)


def get_file_hotspots(repo_path: str, limit: int = 15) -> List[Tuple[str, int]]:
    """Files ranked by how many commits touched them."""
    raw = _run(repo_path, ["log", "--no-merges", "--name-only", "--format="])
    counts: Counter = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if line:
            counts[line] += 1
    return counts.most_common(limit)


def get_commit_heatmap_by_hour(commits: List[Commit]) -> Dict[int, int]:
    counts: Counter = Counter()
    for c in commits:
        counts[c.date.hour] += 1
    return dict(counts)


def get_weekly_velocity(commits: List[Commit], weeks: int = 52) -> List[int]:
    """Returns commit counts per week for the last N weeks."""
    from datetime import timedelta
    today = datetime.now()
    weekly: List[int] = [0] * weeks
    for c in commits:
        delta = (today - c.date).days
        week_idx = delta // 7
        if 0 <= week_idx < weeks:
            weekly[weeks - 1 - week_idx] += 1
    return weekly
