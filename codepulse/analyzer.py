"""
Git repository analyzer — parses git log and extracts structured metrics.
"""
import subprocess
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Commit:
    hash: str
    author: str
    email: str
    date: datetime
    message: str
    files_changed: list = field(default_factory=list)
    insertions: int = 0
    deletions: int = 0

    @property
    def commit_type(self) -> str:
        msg = self.message.lower().strip()
        if re.match(r"^(feat|feature)[:(]", msg):
            return "feature"
        if re.match(r"^fix[:(]", msg):
            return "fix"
        if re.match(r"^(docs?|documentation)[:(]", msg):
            return "docs"
        if re.match(r"^(test|tests?)[:(]", msg):
            return "test"
        if re.match(r"^(refactor|refact)[:(]", msg):
            return "refactor"
        if re.match(r"^(chore|ci|build|release)[:(]", msg):
            return "chore"
        if re.match(r"^(style|format)[:(]", msg):
            return "style"
        if re.match(r"^(perf|performance)[:(]", msg):
            return "perf"
        if "merge" in msg[:20]:
            return "merge"
        return "other"

    @property
    def total_changes(self) -> int:
        return self.insertions + self.deletions


@dataclass
class FileStats:
    path: str
    commits: int = 0
    insertions: int = 0
    deletions: int = 0
    authors: set = field(default_factory=set)
    last_modified: Optional[datetime] = None

    @property
    def churn(self) -> int:
        return self.insertions + self.deletions

    @property
    def ext(self) -> str:
        return Path(self.path).suffix.lstrip(".") or "none"


class GitAnalyzer:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self._validate_repo()

    def _validate_repo(self):
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ValueError(f"{self.repo_path} is not a git repository")

    def _run_git(self, *args) -> str:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()

    def get_repo_name(self) -> str:
        remote = self._run_git("remote", "get-url", "origin")
        if remote:
            return remote.rstrip("/").split("/")[-1].replace(".git", "")
        return self.repo_path.name

    def get_commits(self, max_commits: int = 500) -> list[Commit]:
        # Format: hash|author|email|timestamp|message
        log = self._run_git(
            "log",
            f"-{max_commits}",
            "--format=%H|%an|%ae|%at|%s",
            "--no-merges",
        )
        if not log:
            return []

        commits = []
        for line in log.splitlines():
            parts = line.split("|", 4)
            if len(parts) < 5:
                continue
            hash_, author, email, ts, message = parts
            try:
                date = datetime.fromtimestamp(int(ts))
            except (ValueError, OSError):
                continue
            commits.append(Commit(
                hash=hash_,
                author=author,
                email=email,
                date=date,
                message=message,
            ))

        # Enrich with numstat
        self._enrich_with_numstat(commits)
        return commits

    def _enrich_with_numstat(self, commits: list[Commit]):
        if not commits:
            return
        # Get all numstats in one pass
        log = self._run_git(
            "log",
            f"-{len(commits)}",
            "--numstat",
            "--format=%H",
            "--no-merges",
        )
        if not log:
            return

        current_hash = None
        hash_to_commit = {c.hash: c for c in commits}

        for line in log.splitlines():
            line = line.strip()
            if not line:
                continue
            # A hash line (40 hex chars)
            if re.match(r"^[0-9a-f]{40}$", line):
                current_hash = line
                continue
            if current_hash and current_hash in hash_to_commit:
                parts = line.split("\t")
                if len(parts) == 3:
                    add_str, del_str, filepath = parts
                    try:
                        adds = int(add_str) if add_str != "-" else 0
                        dels = int(del_str) if del_str != "-" else 0
                    except ValueError:
                        continue
                    c = hash_to_commit[current_hash]
                    c.insertions += adds
                    c.deletions += dels
                    c.files_changed.append(filepath)

    def get_file_stats(self, commits: list[Commit]) -> dict[str, FileStats]:
        stats: dict[str, FileStats] = {}
        for commit in commits:
            for filepath in commit.files_changed:
                if filepath not in stats:
                    stats[filepath] = FileStats(path=filepath)
                fs = stats[filepath]
                fs.commits += 1
                fs.authors.add(commit.author)
                if fs.last_modified is None or commit.date > fs.last_modified:
                    fs.last_modified = commit.date

        # Re-run numstat per file for accurate per-file insertions/deletions
        for filepath, fs in stats.items():
            result = self._run_git(
                "log", "--numstat", "--follow", "--format=", "--", filepath
            )
            for line in result.splitlines():
                parts = line.split("\t")
                if len(parts) == 3:
                    try:
                        fs.insertions += int(parts[0]) if parts[0] != "-" else 0
                        fs.deletions += int(parts[1]) if parts[1] != "-" else 0
                    except ValueError:
                        pass

        return stats

    def get_contributor_stats(self, commits: list[Commit]) -> dict:
        contributors = defaultdict(lambda: {
            "commits": 0, "insertions": 0, "deletions": 0,
            "files": set(), "first_commit": None, "last_commit": None,
            "types": defaultdict(int),
        })
        for c in commits:
            a = contributors[c.author]
            a["commits"] += 1
            a["insertions"] += c.insertions
            a["deletions"] += c.deletions
            a["files"].update(c.files_changed)
            a["types"][c.commit_type] += 1
            if a["first_commit"] is None or c.date < a["first_commit"]:
                a["first_commit"] = c.date
            if a["last_commit"] is None or c.date > a["last_commit"]:
                a["last_commit"] = c.date
        return dict(contributors)

    def get_activity_by_month(self, commits: list[Commit]) -> dict:
        monthly = defaultdict(int)
        for c in commits:
            key = c.date.strftime("%Y-%m")
            monthly[key] += 1
        return dict(sorted(monthly.items()))

    def get_activity_by_hour(self, commits: list[Commit]) -> dict[int, int]:
        hourly = defaultdict(int)
        for c in commits:
            hourly[c.date.hour] += 1
        return dict(hourly)

    def get_activity_by_weekday(self, commits: list[Commit]) -> dict[int, int]:
        days = defaultdict(int)
        for c in commits:
            days[c.date.weekday()] += 1
        return dict(days)

    def get_language_breakdown(self, file_stats: dict[str, FileStats]) -> dict[str, int]:
        ext_map = defaultdict(int)
        for fs in file_stats.values():
            ext_map[fs.ext] += fs.churn
        return dict(sorted(ext_map.items(), key=lambda x: x[1], reverse=True))
