"""Git analysis engine — extracts all stats from a repository."""
import subprocess
from datetime import datetime
from collections import defaultdict
from pathlib import Path


class GitAnalyzer:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path).resolve()

    def _git(self, *args, allow_empty=False):
        result = subprocess.run(
            ["git", "-C", str(self.repo_path)] + list(args),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 and not allow_empty:
            return ""
        return result.stdout.strip()

    # ── Commit data ───────────────────────────────────────────────────────────

    def get_commits(self):
        """Return list of commit dicts in reverse-chronological order."""
        raw = self._git(
            "log",
            "--format=%H\x1f%an\x1f%ae\x1f%ai\x1f%s",
            "--no-merges",
        )
        commits = []
        for line in raw.splitlines():
            parts = line.split("\x1f", 4)
            if len(parts) < 5:
                continue
            raw_date = parts[3].strip()
            # git outputs "2024-01-15 10:30:00 +0000" — strip TZ for fromisoformat
            try:
                dt = datetime.fromisoformat(raw_date.rsplit(" ", 1)[0])
            except ValueError:
                continue
            commits.append(
                {
                    "hash": parts[0],
                    "author": parts[1],
                    "email": parts[2],
                    "date": dt,
                    "message": parts[4],
                }
            )
        return commits

    def get_total_commit_count(self):
        out = self._git("rev-list", "--count", "HEAD", allow_empty=True)
        return int(out) if out.isdigit() else 0

    # ── File stats ────────────────────────────────────────────────────────────

    def get_file_change_stats(self):
        """Count how many commits touched each file."""
        raw = self._git("log", "--name-only", "--format=", "--no-merges")
        counts: dict[str, int] = defaultdict(int)
        for line in raw.splitlines():
            line = line.strip()
            if line:
                counts[line] += 1
        return dict(sorted(counts.items(), key=lambda x: -x[1]))

    def get_language_breakdown(self):
        """Count tracked files by extension."""
        raw = self._git("ls-files")
        ext_counts: dict[str, int] = defaultdict(int)
        for f in raw.splitlines():
            ext = Path(f).suffix.lower() or "(none)"
            ext_counts[ext] += 1
        return dict(sorted(ext_counts.items(), key=lambda x: -x[1]))

    # ── Aggregates ────────────────────────────────────────────────────────────

    def get_author_stats(self, commits):
        stats: dict[str, dict] = defaultdict(lambda: {"commits": 0, "dates": []})
        for c in commits:
            stats[c["author"]]["commits"] += 1
            stats[c["author"]]["dates"].append(c["date"])
        return dict(stats)

    def get_calendar_data(self, commits):
        """Return {date_iso: commit_count} for all-time history."""
        counts: dict[str, int] = defaultdict(int)
        for c in commits:
            counts[c["date"].date().isoformat()] += 1
        return dict(counts)

    def get_monthly_commits(self, commits):
        """Return sorted list of (YYYY-MM, count) tuples."""
        monthly: dict[str, int] = defaultdict(int)
        for c in commits:
            monthly[c["date"].strftime("%Y-%m")] += 1
        return sorted(monthly.items())

    # ── Repo info ─────────────────────────────────────────────────────────────

    def get_repo_info(self):
        name = self._git("rev-parse", "--show-toplevel").split("/")[-1]
        branch = self._git("rev-parse", "--abbrev-ref", "HEAD")
        remote = self._git("remote", "get-url", "origin", allow_empty=True)
        return {
            "name": name or self.repo_path.name,
            "branch": branch or "HEAD",
            "remote": remote,
            "total_commits": self.get_total_commit_count(),
        }

    # ── Full analysis ─────────────────────────────────────────────────────────

    def analyze(self):
        commits = self.get_commits()
        return {
            "repo_info": self.get_repo_info(),
            "commits": commits,
            "author_stats": self.get_author_stats(commits),
            "file_stats": self.get_file_change_stats(),
            "language_breakdown": self.get_language_breakdown(),
            "calendar": self.get_calendar_data(commits),
            "monthly_commits": self.get_monthly_commits(commits),
        }
