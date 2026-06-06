"""Git data extraction and analysis."""

from __future__ import annotations

import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


def _run(cmd: list[str], cwd: str) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip()


def find_git_root(path: str = ".") -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, cwd=path
    )
    return result.stdout.strip() if result.returncode == 0 else None


@dataclass
class CommitRecord:
    sha: str
    author: str
    email: str
    timestamp: datetime
    subject: str
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0


@dataclass
class RepoStats:
    root: str
    name: str
    total_commits: int
    first_commit: datetime | None
    last_commit: datetime | None
    authors: dict[str, int]          # author -> commit count
    daily_counts: dict[str, int]     # YYYY-MM-DD -> commit count
    file_churn: dict[str, int]       # filepath -> change count
    language_bytes: dict[str, int]   # extension -> total lines changed
    branch_count: int
    tag_count: int
    commits: list[CommitRecord] = field(default_factory=list)


def load_commits(root: str, limit: int = 5000) -> list[CommitRecord]:
    """Parse git log into CommitRecord list."""
    sep = "\x1f"
    fmt = sep.join(["%H", "%an", "%ae", "%at", "%s"])
    raw = _run(
        ["git", "log", f"--pretty=format:{fmt}", f"-{limit}"],
        cwd=root,
    )
    if not raw:
        return []

    commits: list[CommitRecord] = []
    for line in raw.splitlines():
        parts = line.split(sep, 4)
        if len(parts) < 5:
            continue
        sha, author, email, ts_str, subject = parts
        try:
            ts = datetime.fromtimestamp(int(ts_str), tz=timezone.utc)
        except ValueError:
            continue
        commits.append(CommitRecord(sha=sha, author=author, email=email,
                                    timestamp=ts, subject=subject))
    return commits


def _enrich_with_stats(commits: list[CommitRecord], root: str, sample: int = 200) -> None:
    """Fetch --shortstat for a sample of commits to get file/line counts."""
    for commit in commits[:sample]:
        out = _run(
            ["git", "show", "--shortstat", "--format=", commit.sha],
            cwd=root,
        )
        for line in out.splitlines():
            if "changed" in line:
                parts = line.split(",")
                for p in parts:
                    p = p.strip()
                    if "changed" in p:
                        try:
                            commit.files_changed = int(p.split()[0])
                        except ValueError:
                            pass
                    elif "insertion" in p:
                        try:
                            commit.insertions = int(p.split()[0])
                        except ValueError:
                            pass
                    elif "deletion" in p:
                        try:
                            commit.deletions = int(p.split()[0])
                        except ValueError:
                            pass


def load_file_churn(root: str, limit: int = 1000) -> dict[str, int]:
    """Count how many times each file has been touched."""
    raw = _run(
        ["git", "log", f"--pretty=format:", "--name-only", f"-{limit}"],
        cwd=root,
    )
    counter: Counter[str] = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if line:
            counter[line] += 1
    return dict(counter.most_common(50))


def load_language_stats(root: str, limit: int = 2000) -> dict[str, int]:
    """Aggregate lines changed by file extension."""
    raw = _run(
        ["git", "log", "--pretty=format:", "--numstat", f"-{limit}"],
        cwd=root,
    )
    ext_lines: defaultdict[str, int] = defaultdict(int)
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            added_str, deleted_str, filepath = parts
            try:
                added = int(added_str)
                deleted = int(deleted_str)
            except ValueError:
                continue
            ext = Path(filepath).suffix.lower() or "other"
            ext_lines[ext] += added + deleted
    # Keep top extensions
    top = sorted(ext_lines.items(), key=lambda x: x[1], reverse=True)[:15]
    return dict(top)


def analyze(path: str = ".") -> RepoStats | None:
    root = find_git_root(path)
    if not root:
        return None

    name = Path(root).name

    commits = load_commits(root)
    if not commits:
        return RepoStats(
            root=root, name=name, total_commits=0,
            first_commit=None, last_commit=None,
            authors={}, daily_counts={}, file_churn={},
            language_bytes={}, branch_count=0, tag_count=0,
        )

    # Author commit counts
    authors: Counter[str] = Counter()
    for c in commits:
        authors[c.author] += 1

    # Daily commit counts
    daily: Counter[str] = Counter()
    for c in commits:
        day = c.timestamp.strftime("%Y-%m-%d")
        daily[day] += 1

    # Branch count
    branch_raw = _run(["git", "branch", "-a"], cwd=root)
    branch_count = len([l for l in branch_raw.splitlines() if l.strip()])

    # Tag count
    tag_raw = _run(["git", "tag"], cwd=root)
    tag_count = len([l for l in tag_raw.splitlines() if l.strip()])

    file_churn = load_file_churn(root)
    language_bytes = load_language_stats(root)

    return RepoStats(
        root=root,
        name=name,
        total_commits=len(commits),
        first_commit=commits[-1].timestamp if commits else None,
        last_commit=commits[0].timestamp if commits else None,
        authors=dict(authors.most_common(20)),
        daily_counts=dict(daily),
        file_churn=file_churn,
        language_bytes=language_bytes,
        branch_count=branch_count,
        tag_count=tag_count,
        commits=commits[:500],
    )
