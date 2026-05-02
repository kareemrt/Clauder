"""Parses a git repository and extracts structured history data."""

from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import git


@dataclass
class CommitInfo:
    sha: str
    message: str
    author: str
    date: datetime
    files_changed: list[str]
    insertions: int
    deletions: int


@dataclass
class RepoStats:
    name: str
    total_commits: int
    authors: dict[str, int]           # author -> commit count
    file_heatmap: dict[str, int]       # filepath -> change frequency
    timeline: list[CommitInfo]
    first_commit: datetime
    last_commit: datetime
    primary_languages: dict[str, int]  # extension -> file count
    weekly_activity: dict[str, int]    # ISO week -> commit count
    chapters: list[dict]               # grouped commit clusters


def _ext(path: str) -> str:
    _, e = os.path.splitext(path)
    return e.lower() if e else "(no ext)"


def analyze_repo(repo_path: str, max_commits: int = 500) -> RepoStats:
    """Load and analyze a git repository, returning structured stats."""
    repo = git.Repo(repo_path, search_parent_directories=True)
    name = os.path.basename(repo.working_dir)

    commits: list[CommitInfo] = []
    authors: dict[str, int] = defaultdict(int)
    file_heatmap: dict[str, int] = defaultdict(int)
    weekly_activity: dict[str, int] = defaultdict(int)
    lang_counts: dict[str, int] = defaultdict(int)

    for commit in list(repo.iter_commits())[:max_commits]:
        try:
            stats = commit.stats
            files = list(stats.files.keys())
            ins = stats.total.get("insertions", 0)
            dels = stats.total.get("deletions", 0)
        except Exception:
            files, ins, dels = [], 0, 0

        dt = datetime.fromtimestamp(commit.committed_date, tz=timezone.utc)
        week = dt.strftime("%Y-W%W")

        ci = CommitInfo(
            sha=commit.hexsha[:7],
            message=commit.message.strip().splitlines()[0],
            author=commit.author.name,
            date=dt,
            files_changed=files,
            insertions=ins,
            deletions=dels,
        )
        commits.append(ci)
        authors[commit.author.name] += 1
        weekly_activity[week] += 1

        for f in files:
            file_heatmap[f] += 1
            lang_counts[_ext(f)] += 1

    if not commits:
        raise ValueError("No commits found in repository.")

    commits.sort(key=lambda c: c.date)
    chapters = _build_chapters(commits)

    return RepoStats(
        name=name,
        total_commits=len(commits),
        authors=dict(authors),
        file_heatmap=dict(file_heatmap),
        timeline=commits,
        first_commit=commits[0].date,
        last_commit=commits[-1].date,
        primary_languages=dict(lang_counts),
        weekly_activity=dict(weekly_activity),
        chapters=chapters,
    )


def _build_chapters(commits: list[CommitInfo], min_chapter_size: int = 5) -> list[dict]:
    """Split commit history into narrative chapters by time gaps and activity bursts."""
    if not commits:
        return []

    chapters = []
    current: list[CommitInfo] = [commits[0]]

    for prev, curr in zip(commits, commits[1:]):
        gap_days = (curr.date - prev.date).days
        # New chapter on large time gaps (>14 days) or every ~30 commits
        if gap_days > 14 or len(current) >= 30:
            chapters.append(_summarize_chapter(current, len(chapters) + 1))
            current = []
        current.append(curr)

    if current:
        chapters.append(_summarize_chapter(current, len(chapters) + 1))

    return chapters


def _summarize_chapter(commits: list[CommitInfo], number: int) -> dict:
    top_files: dict[str, int] = defaultdict(int)
    authors: dict[str, int] = defaultdict(int)
    total_ins = total_dels = 0

    for c in commits:
        authors[c.author] += 1
        total_ins += c.insertions
        total_dels += c.deletions
        for f in c.files_changed:
            top_files[f] += 1

    hottest = sorted(top_files.items(), key=lambda x: x[1], reverse=True)[:5]
    messages = [c.message for c in commits[:10]]

    return {
        "number": number,
        "commit_count": len(commits),
        "start_date": commits[0].date,
        "end_date": commits[-1].date,
        "authors": dict(authors),
        "insertions": total_ins,
        "deletions": total_dels,
        "hottest_files": hottest,
        "sample_messages": messages,
        "duration_days": max(1, (commits[-1].date - commits[0].date).days),
    }
