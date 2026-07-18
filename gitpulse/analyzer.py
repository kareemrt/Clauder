"""Git repository data extraction and analysis engine."""

import subprocess
import os
import re
from collections import defaultdict, Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path


def run_git(args, cwd):
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def get_repo_name(repo_path):
    remote = run_git(["remote", "get-url", "origin"], repo_path)
    if remote:
        name = re.sub(r"\.git$", "", remote.split("/")[-1])
        return name
    return Path(repo_path).resolve().name


def get_commits(repo_path, limit=5000):
    """Return list of commit dicts with timestamp, author, files changed."""
    fmt = "%H|%ae|%an|%at|%s"
    log = run_git(
        ["log", f"--pretty=format:{fmt}", f"-{limit}", "--no-merges"],
        repo_path,
    )
    commits = []
    for line in log.splitlines():
        parts = line.split("|", 4)
        if len(parts) < 5:
            continue
        sha, email, author, ts_str, subject = parts
        try:
            ts = int(ts_str)
        except ValueError:
            continue
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        commits.append(
            {
                "sha": sha,
                "email": email,
                "author": author,
                "ts": ts,
                "dt": dt,
                "subject": subject,
            }
        )
    return commits


def get_file_churn(repo_path, limit=5000):
    """Return Counter of files by number of times they appeared in commits."""
    log = run_git(
        [
            "log",
            "--name-only",
            f"--pretty=format:%H",
            f"-{limit}",
            "--no-merges",
        ],
        repo_path,
    )
    churn = Counter()
    for line in log.splitlines():
        line = line.strip()
        if not line or len(line) == 40 and all(c in "0123456789abcdef" for c in line):
            continue
        churn[line] += 1
    return churn


def get_file_stats(repo_path):
    """Count files by extension in the working tree."""
    try:
        tracked = run_git(["ls-files"], repo_path)
        ext_counter = Counter()
        for f in tracked.splitlines():
            ext = Path(f).suffix.lower() or "(no ext)"
            ext_counter[ext] += 1
        return ext_counter
    except Exception:
        return Counter()


def get_co_change_pairs(repo_path, limit=2000):
    """Find files that frequently change together (co-change analysis)."""
    log = run_git(
        [
            "log",
            "--name-only",
            f"--pretty=format:---COMMIT---",
            f"-{limit}",
            "--no-merges",
        ],
        repo_path,
    )
    pairs = Counter()
    current_files = []
    for line in log.splitlines():
        line = line.strip()
        if line == "---COMMIT---":
            files = sorted(set(current_files))
            for i in range(len(files)):
                for j in range(i + 1, len(files)):
                    pairs[(files[i], files[j])] += 1
            current_files = []
        elif line:
            current_files.append(line)
    return pairs


def build_heatmap(commits, weeks=52):
    """Build a weeks×7 heatmap grid of commit counts."""
    now = datetime.now(tz=timezone.utc)
    # Align to Sunday start of the week
    days_since_sunday = (now.weekday() + 1) % 7
    grid_end = now - timedelta(days=days_since_sunday)
    grid_start = grid_end - timedelta(weeks=weeks - 1, days=6)

    grid = defaultdict(int)
    for c in commits:
        dt = c["dt"]
        if grid_start <= dt <= now:
            day_offset = (dt - grid_start).days
            week = day_offset // 7
            dow = day_offset % 7
            grid[(week, dow)] += 1

    return grid, weeks, grid_start


def build_velocity(commits, buckets=24):
    """Weekly commit counts over time for velocity chart."""
    if not commits:
        return [], []

    sorted_commits = sorted(commits, key=lambda c: c["ts"])
    oldest = sorted_commits[0]["dt"]
    newest = sorted_commits[-1]["dt"]
    span = (newest - oldest).total_seconds()

    if span == 0:
        return [1], [oldest]

    bucket_seconds = span / buckets
    counts = [0] * buckets
    labels = []

    for i in range(buckets):
        labels.append(oldest + timedelta(seconds=i * bucket_seconds))

    for c in sorted_commits:
        idx = int((c["dt"] - oldest).total_seconds() / bucket_seconds)
        idx = min(idx, buckets - 1)
        counts[idx] += 1

    return counts, labels


def author_stats(commits):
    """Return dict of author -> commit count, sorted by count."""
    counts = Counter()
    for c in commits:
        counts[c["author"]] += 1
    return counts.most_common()


def peak_hours(commits):
    """Return commit counts by hour of day (UTC)."""
    hours = Counter()
    for c in commits:
        hours[c["dt"].hour] += 1
    return [hours.get(h, 0) for h in range(24)]


def summary_stats(commits, churn, repo_path):
    """Compute high-level summary numbers."""
    if not commits:
        return {}

    sorted_commits = sorted(commits, key=lambda c: c["ts"])
    first_commit = sorted_commits[0]["dt"]
    last_commit = sorted_commits[-1]["dt"]
    age_days = max((last_commit - first_commit).days, 1)

    tracked = run_git(["ls-files"], repo_path)
    total_files = len([f for f in tracked.splitlines() if f.strip()])

    additions = run_git(
        ["log", "--pretty=tformat:", "--numstat", "--no-merges", "-500"], repo_path
    )
    total_add = total_del = 0
    for line in additions.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            try:
                total_add += int(parts[0])
                total_del += int(parts[1])
            except ValueError:
                pass

    return {
        "total_commits": len(commits),
        "total_authors": len(set(c["author"] for c in commits)),
        "total_files": total_files,
        "first_commit": first_commit,
        "last_commit": last_commit,
        "age_days": age_days,
        "commits_per_day": round(len(commits) / age_days, 2),
        "lines_added": total_add,
        "lines_deleted": total_del,
        "most_churned_file": churn.most_common(1)[0] if churn else ("N/A", 0),
    }
