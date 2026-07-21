"""Core git repository analysis engine."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import git


@dataclass
class ContributorStats:
    name: str
    email: str
    commits: int = 0
    additions: int = 0
    deletions: int = 0

    @property
    def lines_changed(self) -> int:
        return self.additions + self.deletions

    @property
    def impact_score(self) -> float:
        return self.commits * 10 + self.additions * 0.1 + self.deletions * 0.05


@dataclass
class FileHotspot:
    path: str
    change_count: int
    additions: int = 0
    deletions: int = 0


@dataclass
class RepoStats:
    repo_name: str
    repo_path: str
    total_commits: int = 0
    total_branches: int = 0
    total_tags: int = 0
    active_days: int = 0
    first_commit: datetime | None = None
    last_commit: datetime | None = None
    contributors: list[ContributorStats] = field(default_factory=list)
    file_hotspots: list[FileHotspot] = field(default_factory=list)
    commits_by_hour: dict[int, int] = field(default_factory=dict)
    commits_by_weekday: dict[int, int] = field(default_factory=dict)
    commits_by_month: dict[str, int] = field(default_factory=dict)
    calendar_data: dict[str, int] = field(default_factory=dict)
    top_words: list[tuple[str, int]] = field(default_factory=list)
    longest_streak: int = 0
    current_streak: int = 0
    branch_names: list[str] = field(default_factory=list)

    @property
    def age_days(self) -> int:
        if not self.first_commit or not self.last_commit:
            return 0
        return (self.last_commit - self.first_commit).days + 1

    @property
    def commit_frequency(self) -> float:
        if self.age_days == 0:
            return 0.0
        return self.total_commits / self.age_days


_STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "it", "its", "this", "that", "these", "those", "i", "we", "you", "he",
    "she", "they", "them", "their", "our", "your", "my", "up", "out", "not",
    "also", "into", "if", "so", "no", "new", "use", "used", "when", "more",
    "after", "before", "some", "make", "made", "than", "then",
}


def analyze(repo_path: str = ".", max_commits: int = 5000) -> RepoStats:
    """Analyze a git repository and return structured stats."""
    path = Path(repo_path).resolve()
    repo = git.Repo(str(path), search_parent_directories=True)

    stats = RepoStats(
        repo_name=path.name,
        repo_path=str(path),
    )

    # Branch & tag info
    stats.branch_names = [b.name for b in repo.branches]
    stats.total_branches = len(stats.branch_names)
    try:
        stats.total_tags = len(list(repo.tags))
    except Exception:
        stats.total_tags = 0

    # Walk commits
    contributors: dict[str, ContributorStats] = {}
    file_change_counter: Counter[str] = Counter()
    file_additions: dict[str, int] = defaultdict(int)
    file_deletions: dict[str, int] = defaultdict(int)
    hour_counter: Counter[int] = Counter()
    weekday_counter: Counter[int] = Counter()
    month_counter: Counter[str] = Counter()
    calendar: Counter[str] = Counter()
    all_words: Counter[str] = Counter()
    active_dates: set[str] = set()

    commits = list(repo.iter_commits(max_count=max_commits))
    stats.total_commits = len(commits)

    for commit in commits:
        # Time data
        dt = datetime.fromtimestamp(commit.committed_date, tz=timezone.utc)
        day_str = dt.strftime("%Y-%m-%d")
        active_dates.add(day_str)
        calendar[day_str] += 1
        hour_counter[dt.hour] += 1
        weekday_counter[dt.weekday()] += 1
        month_counter[dt.strftime("%Y-%m")] += 1

        # Timestamps
        if stats.first_commit is None or dt < stats.first_commit:
            stats.first_commit = dt
        if stats.last_commit is None or dt > stats.last_commit:
            stats.last_commit = dt

        # Contributors
        key = commit.author.email.lower()
        if key not in contributors:
            contributors[key] = ContributorStats(
                name=commit.author.name,
                email=commit.author.email.lower(),
            )
        contributors[key].commits += 1

        # Diff stats per file
        try:
            for diff_item in commit.diff(commit.parents[0] if commit.parents else git.NULL_TREE):
                fpath = diff_item.b_path or diff_item.a_path
                if fpath:
                    file_change_counter[fpath] += 1
        except Exception:
            pass

        # Commit message words
        words = re.findall(r"[a-zA-Z]{3,}", commit.message.lower())
        for w in words:
            if w not in _STOP_WORDS:
                all_words[w] += 1

    # Attempt to get line stats from git log (faster than per-commit diff)
    try:
        log_output = repo.git.log(
            "--numstat", "--pretty=format:%ae",
            f"-{min(max_commits, 2000)}"
        )
        _parse_numstat(log_output, contributors)
    except Exception:
        pass

    stats.contributors = sorted(contributors.values(), key=lambda c: c.commits, reverse=True)
    stats.file_hotspots = [
        FileHotspot(path=p, change_count=c)
        for p, c in file_change_counter.most_common(20)
    ]
    stats.commits_by_hour = dict(sorted(hour_counter.items()))
    stats.commits_by_weekday = dict(sorted(weekday_counter.items()))
    stats.commits_by_month = dict(sorted(month_counter.items()))
    stats.calendar_data = dict(calendar)
    stats.active_days = len(active_dates)
    stats.top_words = all_words.most_common(30)
    stats.longest_streak, stats.current_streak = _compute_streaks(active_dates)

    return stats


def _parse_numstat(log_output: str, contributors: dict[str, ContributorStats]) -> None:
    """Parse git log --numstat output to populate line change stats."""
    current_email: str | None = None
    for line in log_output.splitlines():
        line = line.strip()
        if not line:
            continue
        if "@" in line and "\t" not in line:
            current_email = line.lower()
        elif "\t" in line and current_email and current_email in contributors:
            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    adds = int(parts[0]) if parts[0] != "-" else 0
                    dels = int(parts[1]) if parts[1] != "-" else 0
                    contributors[current_email].additions += adds
                    contributors[current_email].deletions += dels
                except ValueError:
                    pass


def _compute_streaks(active_dates: set[str]) -> tuple[int, int]:
    """Compute longest and current commit streak in days."""
    if not active_dates:
        return 0, 0

    from datetime import date, timedelta

    sorted_days = sorted(date.fromisoformat(d) for d in active_dates)
    today = date.today()

    longest = 1
    current_len = 1
    for i in range(1, len(sorted_days)):
        if (sorted_days[i] - sorted_days[i - 1]).days == 1:
            current_len += 1
            longest = max(longest, current_len)
        else:
            current_len = 1

    # Current streak (from today backwards)
    current_streak = 0
    check = today
    while check.isoformat() in active_dates or (check - today).days == 0:
        if check.isoformat() in active_dates:
            current_streak += 1
            check -= timedelta(days=1)
        else:
            break

    return longest, current_streak
