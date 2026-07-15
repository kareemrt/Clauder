"""Parse git history and compute repository statistics."""

import subprocess
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone


def _run(cmd, cwd="."):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, errors="replace"
    )
    return result.stdout.strip()


def get_repo_name(path="."):
    remote = _run(["git", "remote", "get-url", "origin"], cwd=path)
    if remote:
        name = remote.rstrip("/").split("/")[-1]
        return name.removesuffix(".git")
    return _run(["git", "rev-parse", "--show-toplevel"], cwd=path).split("/")[-1]


def _parse_commits(path=".", max_commits=2000):
    """Return list of commit dicts with author, date, subject."""
    sep = "\x1f"
    fmt = sep.join(["%H", "%ae", "%an", "%ai", "%s"])
    raw = _run(
        ["git", "log", f"--format={fmt}", f"--max-count={max_commits}"],
        cwd=path,
    )
    commits = []
    for line in raw.splitlines():
        parts = line.split(sep)
        if len(parts) < 5:
            continue
        sha, email, name, date_str, subject = parts[0], parts[1], parts[2], parts[3], parts[4]
        try:
            dt = datetime.fromisoformat(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        commits.append({"sha": sha, "email": email, "name": name, "date": dt, "subject": subject})
    return commits


def _parse_numstat(path=".", max_commits=500):
    """Return per-file line-change stats from recent commits."""
    raw = _run(
        ["git", "log", "--numstat", "--format=COMMIT:%H", f"--max-count={max_commits}"],
        cwd=path,
    )
    file_churn = defaultdict(lambda: {"added": 0, "removed": 0, "touches": 0})
    current_sha = None
    for line in raw.splitlines():
        if line.startswith("COMMIT:"):
            current_sha = line[7:]
            continue
        m = re.match(r"(\d+|-)\s+(\d+|-)\s+(.+)", line)
        if m:
            added = int(m.group(1)) if m.group(1) != "-" else 0
            removed = int(m.group(2)) if m.group(2) != "-" else 0
            fname = m.group(3).strip()
            file_churn[fname]["added"] += added
            file_churn[fname]["removed"] += removed
            file_churn[fname]["touches"] += 1
    return dict(file_churn)


def _language_breakdown(path="."):
    """Best-effort language breakdown by file extension."""
    raw = _run(
        ["git", "ls-files"],
        cwd=path,
    )
    ext_counts = defaultdict(int)
    for fname in raw.splitlines():
        if "." in fname:
            ext = fname.rsplit(".", 1)[-1].lower()
            ext_counts[ext] += 1
        else:
            ext_counts["(none)"] += 1
    return dict(sorted(ext_counts.items(), key=lambda x: -x[1]))


def analyze(path=".", max_commits=2000):
    """Run full analysis; return a stats dict."""
    commits = _parse_commits(path, max_commits=max_commits)
    if not commits:
        return {}

    now = datetime.now(tz=timezone.utc)
    total = len(commits)

    # Commits per day (last 30 days)
    daily: dict[str, int] = defaultdict(int)
    weekly: dict[str, int] = defaultdict(int)
    hour_hist = [0] * 24
    weekday_hist = [0] * 7

    for c in commits:
        day_key = c["date"].strftime("%Y-%m-%d")
        week_key = c["date"].strftime("%Y-W%W")
        daily[day_key] += 1
        weekly[week_key] += 1
        hour_hist[c["date"].hour] += 1
        weekday_hist[c["date"].weekday()] += 1

    # Recent 30-day window
    cutoff_30 = now - timedelta(days=30)
    recent_commits = [c for c in commits if c["date"] >= cutoff_30]
    daily_last30 = {
        (now - timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(29, -1, -1)
    }
    for c in recent_commits:
        k = c["date"].strftime("%Y-%m-%d")
        if k in daily_last30:
            daily_last30[k] += 1

    # Contributors
    contributor_map: dict[str, dict] = defaultdict(lambda: {"commits": 0, "name": ""})
    for c in commits:
        contributor_map[c["email"]]["commits"] += 1
        contributor_map[c["email"]]["name"] = c["name"]
    contributors = sorted(contributor_map.items(), key=lambda x: -x[1]["commits"])

    # File churn
    file_churn = _parse_numstat(path, max_commits=min(max_commits, 500))
    top_churn = sorted(file_churn.items(), key=lambda x: -(x[1]["touches"]))[:10]

    # Language breakdown
    langs = _language_breakdown(path)

    # Streak
    streak = 0
    d = now.date()
    while d.strftime("%Y-%m-%d") in daily:
        streak += 1
        d -= timedelta(days=1)

    # Total lines changed (from numstat)
    total_added = sum(v["added"] for v in file_churn.values())
    total_removed = sum(v["removed"] for v in file_churn.values())

    first_commit = commits[-1]["date"]
    last_commit = commits[0]["date"]
    age_days = max(1, (last_commit - first_commit).days)
    avg_per_day = round(total / age_days, 2)

    return {
        "repo_name": get_repo_name(path),
        "total_commits": total,
        "contributors": contributors,
        "daily_last30": daily_last30,
        "weekly": dict(sorted(weekly.items())[-16:]),
        "hour_hist": hour_hist,
        "weekday_hist": weekday_hist,
        "top_churn": top_churn,
        "languages": langs,
        "streak": streak,
        "total_added": total_added,
        "total_removed": total_removed,
        "avg_per_day": avg_per_day,
        "first_commit": first_commit,
        "last_commit": last_commit,
        "age_days": age_days,
        "recent_30_count": len(recent_commits),
    }
