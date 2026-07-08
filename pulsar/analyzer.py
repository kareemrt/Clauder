"""Git history analysis — extracts commit stats from any repository."""

import subprocess
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def _run(cmd, cwd):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _safe_run(cmd, cwd):
    try:
        return _run(cmd, cwd)
    except subprocess.CalledProcessError:
        return ""


def analyze(repo_path: str, days: int = 90) -> dict:
    """Return a stats dict for the git repo at *repo_path* covering the last *days* days."""
    path = str(Path(repo_path).resolve())

    # Basic repo info
    repo_name = _safe_run(["git", "rev-parse", "--show-toplevel"], path)
    repo_name = Path(repo_name).name if repo_name else Path(path).name

    current_branch = _safe_run(["git", "rev-parse", "--abbrev-ref", "HEAD"], path)
    total_commits = _safe_run(["git", "rev-list", "--count", "HEAD"], path)
    total_commits = int(total_commits) if total_commits.isdigit() else 0

    # All commits: timestamp|author|subject|files_changed|insertions|deletions
    log_fmt = "%at|%aN|%s"
    since = f"--since={days} days ago"
    raw_log = _safe_run(
        ["git", "log", since, f"--pretty=format:{log_fmt}", "--shortstat"], path
    )

    commits = []
    author_commits: dict[str, int] = defaultdict(int)
    author_lines: dict[str, int] = defaultdict(int)
    daily_counts: dict[str, int] = defaultdict(int)
    hourly_matrix = defaultdict(int)  # key: (weekday, hour)
    file_churn: dict[str, int] = defaultdict(int)
    words: dict[str, int] = defaultdict(int)

    pending_meta = None
    for line in raw_log.splitlines():
        line = line.strip()
        if not line:
            continue

        if "|" in line and not line.startswith(" "):
            parts = line.split("|", 2)
            if len(parts) == 3 and parts[0].isdigit():
                pending_meta = parts
                continue

        # Shortstat line: " 3 files changed, 42 insertions(+), 7 deletions(-)"
        if pending_meta and "changed" in line:
            ts, author, subject = pending_meta
            dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
            day_key = dt.strftime("%Y-%m-%d")
            hourly_matrix[(dt.weekday(), dt.hour)] += 1

            ins = re.search(r"(\d+) insertion", line)
            dels = re.search(r"(\d+) deletion", line)
            insertions = int(ins.group(1)) if ins else 0
            deletions = int(dels.group(1)) if dels else 0

            commits.append({
                "ts": int(ts),
                "author": author,
                "subject": subject,
                "insertions": insertions,
                "deletions": deletions,
                "day": day_key,
            })
            author_commits[author] += 1
            author_lines[author] += insertions + deletions
            daily_counts[day_key] += 1

            # Word frequency from commit messages (skip boring words)
            skip = {"fix", "the", "and", "for", "add", "use", "update",
                    "remove", "change", "merge", "branch", "into", "with",
                    "from", "this", "that", "feat", "refactor", "chore", "docs"}
            for word in re.findall(r"[a-z]{3,}", subject.lower()):
                if word not in skip:
                    words[word] += 1

            pending_meta = None
        elif pending_meta and not line.startswith(" "):
            # commit with no stat (e.g. merge commit)
            ts, author, subject = pending_meta
            dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
            day_key = dt.strftime("%Y-%m-%d")
            hourly_matrix[(dt.weekday(), dt.hour)] += 1
            commits.append({"ts": int(ts), "author": author, "subject": subject,
                             "insertions": 0, "deletions": 0, "day": day_key})
            author_commits[author] += 1
            daily_counts[day_key] += 1
            pending_meta = parts if "|" in line else None

    # Top changed files
    raw_files = _safe_run(
        ["git", "log", since, "--name-only", "--pretty=format:"],
        path,
    )
    for fname in raw_files.splitlines():
        fname = fname.strip()
        if fname:
            file_churn[fname] += 1

    # Language breakdown via file extensions
    raw_tree = _safe_run(["git", "ls-files"], path)
    lang_counts: dict[str, int] = defaultdict(int)
    ext_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".jsx": "React/JSX", ".tsx": "React/TSX", ".go": "Go",
        ".rs": "Rust", ".java": "Java", ".cpp": "C++", ".c": "C",
        ".cs": "C#", ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
        ".kt": "Kotlin", ".html": "HTML", ".css": "CSS", ".scss": "SCSS",
        ".sh": "Shell", ".yaml": "YAML", ".yml": "YAML", ".json": "JSON",
        ".md": "Markdown", ".sql": "SQL", ".r": "R", ".scala": "Scala",
    }
    for fpath in raw_tree.splitlines():
        ext = Path(fpath.strip()).suffix.lower()
        lang = ext_map.get(ext, "Other")
        lang_counts[lang] += 1

    # Contributors sorted by commit count
    contributors = sorted(
        [{"name": a, "commits": c, "lines": author_lines[a]}
         for a, c in author_commits.items()],
        key=lambda x: x["commits"], reverse=True
    )

    top_files = sorted(
        [{"path": f, "changes": c} for f, c in file_churn.items()],
        key=lambda x: x["changes"], reverse=True
    )[:15]

    top_words = sorted(
        [{"word": w, "count": c} for w, c in words.items()],
        key=lambda x: x["count"], reverse=True
    )[:20]

    total_insertions = sum(c["insertions"] for c in commits)
    total_deletions = sum(c["deletions"] for c in commits)

    return {
        "repo_name": repo_name,
        "branch": current_branch,
        "total_commits": total_commits,
        "period_commits": len(commits),
        "days": days,
        "commits": commits,
        "daily_counts": dict(daily_counts),
        "hourly_matrix": {f"{k[0]},{k[1]}": v for k, v in hourly_matrix.items()},
        "contributors": contributors,
        "top_files": top_files,
        "top_words": top_words,
        "lang_counts": dict(lang_counts),
        "total_insertions": total_insertions,
        "total_deletions": total_deletions,
    }
