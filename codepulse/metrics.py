"""Statistical processing of raw git data into insight objects."""

from collections import defaultdict, Counter
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field


@dataclass
class ContributorStats:
    name: str
    email: str
    commits: int
    files_touched: int
    first_commit: datetime
    last_commit: datetime


@dataclass
class RepoMetrics:
    repo_name: str
    total_commits: int
    total_contributors: int
    total_files_changed: int
    first_commit: datetime
    last_commit: datetime
    active_days: int

    contributors: list[ContributorStats] = field(default_factory=list)
    hot_files: list[tuple[str, int]] = field(default_factory=list)  # (path, change_count)
    commits_by_hour: dict[int, int] = field(default_factory=dict)
    commits_by_weekday: dict[int, int] = field(default_factory=dict)
    heatmap: dict[str, int] = field(default_factory=dict)  # "YYYY-MM-DD" -> count
    language_lines: dict[str, int] = field(default_factory=dict)


def build_metrics(repo_name: str, commits: list[dict], language_lines: dict[str, int]) -> RepoMetrics:
    if not commits:
        now = datetime.now(timezone.utc)
        return RepoMetrics(
            repo_name=repo_name,
            total_commits=0,
            total_contributors=0,
            total_files_changed=0,
            first_commit=now,
            last_commit=now,
            active_days=0,
        )

    # --- Contributors ---
    author_data: dict[str, dict] = {}
    for c in commits:
        key = c["email"]
        ts = datetime.fromtimestamp(c["timestamp"], tz=timezone.utc)
        if key not in author_data:
            author_data[key] = {
                "name": c["author"],
                "email": key,
                "commits": 0,
                "files": set(),
                "first": ts,
                "last": ts,
            }
        d = author_data[key]
        d["commits"] += 1
        d["files"].update(c["files"])
        if ts < d["first"]:
            d["first"] = ts
        if ts > d["last"]:
            d["last"] = ts

    contributors = sorted(
        [
            ContributorStats(
                name=d["name"],
                email=d["email"],
                commits=d["commits"],
                files_touched=len(d["files"]),
                first_commit=d["first"],
                last_commit=d["last"],
            )
            for d in author_data.values()
        ],
        key=lambda x: x.commits,
        reverse=True,
    )

    # --- Hot files ---
    file_counts: Counter = Counter()
    for c in commits:
        file_counts.update(c["files"])
    hot_files = file_counts.most_common(15)

    # --- Temporal patterns ---
    commits_by_hour: dict[int, int] = defaultdict(int)
    commits_by_weekday: dict[int, int] = defaultdict(int)
    heatmap: dict[str, int] = defaultdict(int)

    timestamps = [c["timestamp"] for c in commits]
    first_ts = min(timestamps)
    last_ts = max(timestamps)

    for c in commits:
        ts = datetime.fromtimestamp(c["timestamp"], tz=timezone.utc)
        commits_by_hour[ts.hour] += 1
        commits_by_weekday[ts.weekday()] += 1
        heatmap[ts.strftime("%Y-%m-%d")] += 1

    active_days = len(heatmap)

    return RepoMetrics(
        repo_name=repo_name,
        total_commits=len(commits),
        total_contributors=len(contributors),
        total_files_changed=sum(len(c["files"]) for c in commits),
        first_commit=datetime.fromtimestamp(first_ts, tz=timezone.utc),
        last_commit=datetime.fromtimestamp(last_ts, tz=timezone.utc),
        active_days=active_days,
        contributors=contributors,
        hot_files=hot_files,
        commits_by_hour=dict(commits_by_hour),
        commits_by_weekday=dict(commits_by_weekday),
        heatmap=dict(heatmap),
        language_lines=language_lines,
    )
