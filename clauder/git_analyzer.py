"""Parse and analyze a git repository's commit history."""

from __future__ import annotations

import os
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import git


@dataclass
class CommitInfo:
    sha: str
    message: str
    author: str
    date: datetime
    files_changed: int
    insertions: int
    deletions: int


@dataclass
class RepoStats:
    path: str
    name: str
    total_commits: int
    contributors: list[tuple[str, int]]  # (name, count)
    first_commit: Optional[CommitInfo]
    last_commit: Optional[CommitInfo]
    most_active_day: Optional[str]
    total_files_changed: int
    total_insertions: int
    total_deletions: int
    commits_by_month: dict[str, int]
    top_files: list[tuple[str, int]]  # (filepath, change_count)
    commits: list[CommitInfo] = field(default_factory=list)


def analyze_repo(repo_path: str, max_commits: int = 200) -> RepoStats:
    """Analyze a git repository and return structured stats."""
    repo = git.Repo(repo_path)
    name = Path(repo_path).name

    commits: list[CommitInfo] = []
    author_counts: Counter = Counter()
    day_counts: Counter = Counter()
    month_counts: Counter = Counter()
    file_counts: Counter = Counter()
    total_insertions = 0
    total_deletions = 0

    for commit in list(repo.iter_commits())[:max_commits]:
        try:
            stats = commit.stats
            files_changed = len(stats.files)
            insertions = stats.total.get("insertions", 0)
            deletions = stats.total.get("deletions", 0)

            for filepath in stats.files:
                file_counts[filepath] += 1
        except Exception:
            files_changed = 0
            insertions = 0
            deletions = 0

        dt = datetime.fromtimestamp(commit.committed_date)
        info = CommitInfo(
            sha=commit.hexsha[:7],
            message=commit.message.strip().splitlines()[0][:80],
            author=commit.author.name,
            date=dt,
            files_changed=files_changed,
            insertions=insertions,
            deletions=deletions,
        )
        commits.append(info)
        author_counts[commit.author.name] += 1
        day_counts[dt.strftime("%A")] += 1
        month_counts[dt.strftime("%Y-%m")] += 1
        total_insertions += insertions
        total_deletions += deletions

    most_active_day = day_counts.most_common(1)[0][0] if day_counts else None

    return RepoStats(
        path=repo_path,
        name=name,
        total_commits=len(commits),
        contributors=author_counts.most_common(),
        first_commit=commits[-1] if commits else None,
        last_commit=commits[0] if commits else None,
        most_active_day=most_active_day,
        total_files_changed=sum(c.files_changed for c in commits),
        total_insertions=total_insertions,
        total_deletions=total_deletions,
        commits_by_month=dict(sorted(month_counts.items())),
        top_files=file_counts.most_common(10),
        commits=commits,
    )


def build_story_context(stats: RepoStats) -> str:
    """Build a rich text description of the repo for Claude to narrate."""
    lines = [
        f"Repository: {stats.name}",
        f"Total commits: {stats.total_commits}",
        f"Contributors: {', '.join(f'{n} ({c} commits)' for n, c in stats.contributors[:8])}",
        f"Most active day of the week: {stats.most_active_day}",
        f"Total lines added: {stats.total_insertions:,}",
        f"Total lines removed: {stats.total_deletions:,}",
    ]

    if stats.first_commit:
        lines.append(
            f"Project born: {stats.first_commit.date.strftime('%B %d, %Y')} "
            f"with commit '{stats.first_commit.message}' by {stats.first_commit.author}"
        )
    if stats.last_commit:
        lines.append(
            f"Latest activity: {stats.last_commit.date.strftime('%B %d, %Y')} "
            f"— '{stats.last_commit.message}' by {stats.last_commit.author}"
        )

    if stats.top_files:
        lines.append(
            "Most-touched files: "
            + ", ".join(f"{f} ({c}x)" for f, c in stats.top_files[:5])
        )

    lines.append("\nChronological commit highlights (oldest to newest, sample):")
    sample = stats.commits[-20:][::-1] if len(stats.commits) > 20 else stats.commits[::-1]
    for c in sample:
        lines.append(
            f"  [{c.date.strftime('%Y-%m-%d')}] {c.sha} by {c.author}: {c.message}"
        )

    return "\n".join(lines)
