"""
Git data extraction and analysis engine.
"""

import subprocess
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class Commit:
    hash: str
    author: str
    email: str
    date: datetime
    message: str
    insertions: int = 0
    deletions: int = 0
    files: List[str] = field(default_factory=list)


@dataclass
class RepoStats:
    repo_path: str
    repo_name: str
    total_commits: int
    total_authors: int
    first_commit: Optional[datetime]
    last_commit: Optional[datetime]
    commits: List[Commit]
    author_commits: Dict[str, int]
    author_lines: Dict[str, int]
    hot_files: List[Tuple[str, int]]
    monthly_commits: Dict[str, int]
    language_breakdown: Dict[str, int]
    total_insertions: int
    total_deletions: int
    avg_commits_per_month: float
    longest_streak_days: int
    peak_month: str
    busiest_author: str


def _run_git(cmd: List[str], cwd: str) -> str:
    result = subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout.strip()


def _parse_commits(repo_path: str) -> List[Commit]:
    """Parse full commit log with stat information."""
    sep = "|||"
    fmt = f"%H{sep}%aN{sep}%aE{sep}%aI{sep}%s"
    raw = _run_git(["log", f"--format={fmt}", "--numstat"], repo_path)

    commits: List[Commit] = []
    current: Optional[Commit] = None

    for line in raw.splitlines():
        # Check if this is a commit header line
        if sep in line:
            parts = line.split(sep)
            if len(parts) == 5:
                if current:
                    commits.append(current)
                try:
                    dt = datetime.fromisoformat(parts[3].replace("Z", "+00:00"))
                except ValueError:
                    dt = datetime.now()
                current = Commit(
                    hash=parts[0],
                    author=parts[1],
                    email=parts[2],
                    date=dt,
                    message=parts[4],
                )
        elif current and line.strip():
            # numstat line: insertions\tdeletions\tfilename
            m = re.match(r"^(\d+|-)\s+(\d+|-)\s+(.+)$", line)
            if m:
                ins = int(m.group(1)) if m.group(1) != "-" else 0
                dels = int(m.group(2)) if m.group(2) != "-" else 0
                fname = m.group(3)
                current.insertions += ins
                current.deletions += dels
                current.files.append(fname)

    if current:
        commits.append(current)

    return commits


def _get_language_breakdown(repo_path: str) -> Dict[str, int]:
    """Count files by extension."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=10,
    )
    ext_counts: Dict[str, int] = defaultdict(int)
    for f in result.stdout.strip().splitlines():
        ext = Path(f).suffix.lower() or "(none)"
        ext_counts[ext] += 1
    return dict(sorted(ext_counts.items(), key=lambda x: -x[1])[:10])


def _count_hot_files(commits: List[Commit]) -> List[Tuple[str, int]]:
    file_counts: Dict[str, int] = defaultdict(int)
    for c in commits:
        for f in c.files:
            # Handle rename notation "old => new"
            if " => " in f:
                f = f.split(" => ")[-1].strip("{}")
            file_counts[f] += 1
    return sorted(file_counts.items(), key=lambda x: -x[1])[:15]


def _compute_streak(commits: List[Commit]) -> int:
    """Find the longest consecutive daily commit streak."""
    if not commits:
        return 0
    days = sorted({c.date.date() for c in commits})
    if not days:
        return 0
    best = streak = 1
    for i in range(1, len(days)):
        delta = (days[i] - days[i - 1]).days
        streak = streak + 1 if delta == 1 else 1
        best = max(best, streak)
    return best


def analyze(repo_path: str) -> RepoStats:
    """Full analysis of a git repository. Returns RepoStats."""
    path = Path(repo_path).resolve()
    repo_name = path.name

    commits = _parse_commits(str(path))

    if not commits:
        # Return empty stats for repos with no commits
        return RepoStats(
            repo_path=str(path),
            repo_name=repo_name,
            total_commits=0,
            total_authors=0,
            first_commit=None,
            last_commit=None,
            commits=[],
            author_commits={},
            author_lines={},
            hot_files=[],
            monthly_commits={},
            language_breakdown={},
            total_insertions=0,
            total_deletions=0,
            avg_commits_per_month=0.0,
            longest_streak_days=0,
            peak_month="N/A",
            busiest_author="N/A",
        )

    author_commits: Dict[str, int] = defaultdict(int)
    author_lines: Dict[str, int] = defaultdict(int)
    monthly_commits: Dict[str, int] = defaultdict(int)
    total_ins = total_dels = 0

    for c in commits:
        author_commits[c.author] += 1
        author_lines[c.author] += c.insertions + c.deletions
        key = c.date.strftime("%Y-%m")
        monthly_commits[key] += 1
        total_ins += c.insertions
        total_dels += c.deletions

    # Sort monthly chronologically
    monthly_sorted = dict(sorted(monthly_commits.items()))

    num_months = max(len(monthly_sorted), 1)
    avg_per_month = len(commits) / num_months

    peak_month = max(monthly_sorted, key=lambda k: monthly_sorted[k]) if monthly_sorted else "N/A"
    busiest_author = max(author_commits, key=lambda k: author_commits[k]) if author_commits else "N/A"

    return RepoStats(
        repo_path=str(path),
        repo_name=repo_name,
        total_commits=len(commits),
        total_authors=len(author_commits),
        first_commit=commits[-1].date if commits else None,
        last_commit=commits[0].date if commits else None,
        commits=commits,
        author_commits=dict(sorted(author_commits.items(), key=lambda x: -x[1])),
        author_lines=dict(sorted(author_lines.items(), key=lambda x: -x[1])),
        hot_files=_count_hot_files(commits),
        monthly_commits=monthly_sorted,
        language_breakdown=_get_language_breakdown(str(path)),
        total_insertions=total_ins,
        total_deletions=total_dels,
        avg_commits_per_month=round(avg_per_month, 1),
        longest_streak_days=_compute_streak(commits),
        peak_month=peak_month,
        busiest_author=busiest_author,
    )
