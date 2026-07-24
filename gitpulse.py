#!/usr/bin/env python3
"""
GitPulse — Beautiful terminal git analytics dashboard.
No external dependencies required beyond Python 3.7+ stdlib.
"""

import subprocess
import sys
import os
import re
from datetime import datetime, timedelta, date
from collections import defaultdict
from pathlib import Path


# ── ANSI color palette ────────────────────────────────────────────────────────

RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
ITALIC  = "\033[3m"

# Foreground
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
GRAY    = "\033[90m"

# Bright foreground
BGREEN  = "\033[92m"
BYELLOW = "\033[93m"
BBLUE   = "\033[94m"
BMAGENTA= "\033[95m"
BCYAN   = "\033[96m"
BWHITE  = "\033[97m"

# Background (for heatmap)
BG_DARK    = "\033[48;5;236m"
BG_LOW     = "\033[48;5;22m"
BG_MED     = "\033[48;5;28m"
BG_HIGH    = "\033[48;5;34m"
BG_MAX     = "\033[48;5;46m"

TERM_WIDTH = min(os.get_terminal_size().columns if sys.stdout.isatty() else 120, 120)


# ── Git helpers ───────────────────────────────────────────────────────────────

def git(args: list[str], cwd: str | None = None) -> str:
    """Run a git command and return stdout, empty string on error."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd or ".",
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_repo_root() -> str:
    root = git(["rev-parse", "--show-toplevel"])
    if not root:
        print(f"{RED}✗ Not inside a git repository.{RESET}")
        sys.exit(1)
    return root


def get_repo_name(root: str) -> str:
    name = git(["config", "--get", "remote.origin.url"], cwd=root)
    if name:
        name = re.sub(r".*[/:]", "", name).removesuffix(".git")
    return name or Path(root).name


# ── Data collection ───────────────────────────────────────────────────────────

def collect_commits(root: str, days: int = 365) -> list[dict]:
    """Return list of commit dicts for the last `days` days."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    log = git(
        ["log", "--all", f"--since={since}",
         "--format=%H|%ae|%an|%ad|%s", "--date=format:%Y-%m-%d"],
        cwd=root,
    )
    commits = []
    for line in log.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 4)
        if len(parts) == 5:
            commits.append({
                "hash":    parts[0],
                "email":   parts[1],
                "author":  parts[2],
                "date":    parts[3],
                "subject": parts[4],
            })
    return commits


def collect_file_changes(root: str, days: int = 365) -> dict[str, int]:
    """Return {filepath: change_count} for the last `days` days."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    log = git(
        ["log", "--all", f"--since={since}",
         "--name-only", "--format=", "--diff-filter=ACMR"],
        cwd=root,
    )
    counts: dict[str, int] = defaultdict(int)
    for line in log.splitlines():
        line = line.strip()
        if line:
            counts[line] += 1
    return dict(counts)


def collect_branches(root: str) -> list[dict]:
    """Return branch info list."""
    out = git(["branch", "-a", "--format=%(refname:short)|%(objectname:short)|%(committerdate:relative)"], cwd=root)
    branches = []
    seen = set()
    for line in out.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            name = parts[0].strip()
            if name not in seen:
                seen.add(name)
                branches.append({"name": name, "hash": parts[1], "when": parts[2]})
    return branches


def get_stats(root: str) -> dict:
    """Collect misc repo stats."""
    total_commits = git(["rev-list", "--all", "--count"], cwd=root)
    total_files = git(["ls-files", "--cached"], cwd=root)
    first_commit_date = git(["log", "--all", "--format=%ad", "--date=format:%Y-%m-%d", "--reverse"], cwd=root)
    current_branch = git(["branch", "--show-current"], cwd=root)
    return {
        "total_commits": int(total_commits) if total_commits.isdigit() else 0,
        "total_files": len(total_files.splitlines()) if total_files else 0,
        "first_commit": first_commit_date.splitlines()[0] if first_commit_date else "N/A",
        "current_branch": current_branch or "HEAD",
    }


# ── Rendering helpers ─────────────────────────────────────────────────────────

def center(text: str, width: int = TERM_WIDTH, fill: str = " ") -> str:
    plain = re.sub(r"\033\[[0-9;]*m", "", text)
    pad = max(0, width - len(plain))
    return fill * (pad // 2) + text + fill * (pad - pad // 2)


def box_top(title: str, width: int = TERM_WIDTH, color: str = CYAN) -> str:
    inner = width - 4
    t = f" {title} "
    dash = "─" * ((inner - len(t)) // 2)
    extra = "─" if (inner - len(t)) % 2 else ""
    return f"{color}╭─{dash}{t}{dash}{extra}─╮{RESET}"


def box_bot(width: int = TERM_WIDTH, color: str = CYAN) -> str:
    return f"{color}╰{'─' * (width - 2)}╯{RESET}"


def box_row(content: str, width: int = TERM_WIDTH, color: str = CYAN) -> str:
    plain = re.sub(r"\033\[[0-9;]*m", "", content)
    pad = max(0, width - 4 - len(plain))
    return f"{color}│{RESET} {content}{' ' * pad} {color}│{RESET}"


def hbar(value: float, max_val: float, width: int = 20, color: str = BGREEN) -> str:
    if max_val == 0:
        filled = 0
    else:
        filled = round(value / max_val * width)
    return f"{color}{'█' * filled}{GRAY}{'░' * (width - filled)}{RESET}"


def sparkline(values: list[int]) -> str:
    chars = " ▁▂▃▄▅▆▇█"
    if not values or max(values) == 0:
        return GRAY + "─" * len(values) + RESET
    m = max(values)
    return BGREEN + "".join(chars[min(8, round(v / m * 8))] for v in values) + RESET


# ── Section renderers ─────────────────────────────────────────────────────────

def render_header(repo_name: str, stats: dict) -> None:
    print()
    logo = f"{BOLD}{BMAGENTA}⬡ GitPulse{RESET}  {DIM}{GRAY}terminal analytics dashboard{RESET}"
    print(center(logo))
    print(center(f"{GRAY}{'─' * 40}{RESET}"))
    repo_line = f"{YELLOW}⎇ {stats['current_branch']}{RESET}  {BCYAN}{repo_name}{RESET}"
    print(center(repo_line))
    print()


def render_summary(stats: dict) -> None:
    w = TERM_WIDTH
    print(box_top("Repository Overview", w, CYAN))

    age_days = 0
    if stats["first_commit"] != "N/A":
        try:
            first = datetime.strptime(stats["first_commit"], "%Y-%m-%d")
            age_days = (datetime.now() - first).days
        except Exception:
            pass
    age_str = f"{age_days // 365}y {age_days % 365 // 30}mo" if age_days > 30 else f"{age_days}d"

    cols = [
        (f"  {BOLD}Total Commits{RESET}", f"{BWHITE}{stats['total_commits']:,}{RESET}"),
        (f"  {BOLD}Tracked Files{RESET}", f"{BWHITE}{stats['total_files']:,}{RESET}"),
        (f"  {BOLD}Repo Age{RESET}",      f"{BWHITE}{age_str}{RESET}"),
        (f"  {BOLD}First Commit{RESET}",  f"{BWHITE}{stats['first_commit']}{RESET}"),
    ]
    for label, value in cols:
        label_plain = re.sub(r"\033\[[0-9;]*m", "", label)
        value_plain = re.sub(r"\033\[[0-9;]*m", "", value)
        gap = w - 4 - len(label_plain) - len(value_plain)
        line = label + " " * max(1, gap) + value
        print(box_row(line, w, CYAN))

    print(box_bot(w, CYAN))
    print()


def render_heatmap(commits: list[dict]) -> None:
    """Render a GitHub-style 52-week contribution heatmap."""
    w = TERM_WIDTH
    print(box_top("Contribution Heatmap  (last 52 weeks)", w, MAGENTA))

    # Build date → count map
    counts: dict[str, int] = defaultdict(int)
    for c in commits:
        counts[c["date"]] += 1

    today = date.today()
    # Start from the Monday 52 weeks ago
    start = today - timedelta(weeks=52)
    start -= timedelta(days=start.weekday())  # rewind to Monday

    weeks: list[list[tuple[date, int]]] = []
    cur = start
    while cur <= today:
        week = []
        for _ in range(7):
            week.append((cur, counts.get(cur.strftime("%Y-%m-%d"), 0)))
            cur += timedelta(days=1)
        weeks.append(week)

    max_count = max((c for w in weeks for _, c in w), default=1) or 1

    def heat_color(n: int) -> str:
        if n == 0:     return BG_DARK
        elif n < max_count * 0.25: return BG_LOW
        elif n < max_count * 0.50: return BG_MED
        elif n < max_count * 0.75: return BG_HIGH
        else:                       return BG_MAX

    # Day labels (left column)
    day_labels = ["Mo", "  ", "We", "  ", "Fr", "  ", "Su"]

    # Month labels line
    month_str = "    "
    prev_month = None
    for week in weeks:
        first_day = week[0][0]
        m = first_day.strftime("%b")
        if m != prev_month:
            month_str += m[:2]
            prev_month = m
        else:
            month_str += "  "

    print(box_row(f"  {GRAY}{month_str}{RESET}", w, MAGENTA))

    for day_idx in range(7):
        row = f"  {GRAY}{day_labels[day_idx]}{RESET} "
        for week in weeks:
            d, n = week[day_idx]
            cell = f"{heat_color(n)}  {RESET}"
            row += cell
        print(box_row(row, w, MAGENTA))

    # Legend
    legend = (
        f"  {GRAY}Less {RESET}"
        f"{BG_DARK}  {RESET}"
        f"{BG_LOW}  {RESET}"
        f"{BG_MED}  {RESET}"
        f"{BG_HIGH}  {RESET}"
        f"{BG_MAX}  {RESET}"
        f" {GRAY}More{RESET}"
    )
    print(box_row(legend, w, MAGENTA))
    print(box_bot(w, MAGENTA))
    print()


def render_commit_frequency(commits: list[dict]) -> None:
    """Render commit frequency by hour-of-day and day-of-week."""
    w = TERM_WIDTH
    print(box_top("Commit Frequency Analysis", w, YELLOW))

    # By day of week — we only have dates (not times), so use a simpler day-of-week count
    day_counts: dict[int, int] = defaultdict(int)
    month_counts: dict[str, int] = defaultdict(int)
    for c in commits:
        try:
            d = datetime.strptime(c["date"], "%Y-%m-%d")
            day_counts[d.weekday()] += 1
            month_counts[d.strftime("%b %Y")] += 1
        except Exception:
            pass

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    max_day = max(day_counts.values(), default=1) or 1

    print(box_row(f"  {BOLD}By Day of Week{RESET}", w, YELLOW))
    for i, name in enumerate(day_names):
        cnt = day_counts[i]
        bar = hbar(cnt, max_day, 30, BYELLOW)
        line = f"  {GRAY}{name}{RESET}  {bar}  {BYELLOW}{cnt:3d}{RESET}"
        print(box_row(line, w, YELLOW))

    print(box_row("", w, YELLOW))

    # Last 12 months sparkline
    today = date.today()
    monthly: list[int] = []
    month_labels: list[str] = []
    for i in range(11, -1, -1):
        mo = today.replace(day=1) - timedelta(days=i * 28)
        key = mo.strftime("%b %Y")
        monthly.append(month_counts.get(key, 0))
        month_labels.append(mo.strftime("%b"))

    spark = sparkline(monthly)
    print(box_row(f"  {BOLD}Monthly Trend (12 months){RESET}", w, YELLOW))
    label_str = "  ".join(f"{GRAY}{l}{RESET}" for l in month_labels)
    print(box_row(f"  {label_str}", w, YELLOW))
    print(box_row(f"  {spark}", w, YELLOW))

    print(box_bot(w, YELLOW))
    print()


def render_authors(commits: list[dict]) -> None:
    """Render author leaderboard."""
    w = TERM_WIDTH
    print(box_top("Author Leaderboard", w, BGREEN))

    author_counts: dict[str, int] = defaultdict(int)
    author_names: dict[str, str] = {}
    for c in commits:
        author_counts[c["email"]] += 1
        author_names[c["email"]] = c["author"]

    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    total = sum(author_counts.values()) or 1
    max_cnt = sorted_authors[0][1] if sorted_authors else 1

    medals = ["🥇", "🥈", "🥉"]
    colors = [BGREEN, BYELLOW, BCYAN]

    for rank, (email, cnt) in enumerate(sorted_authors[:10], 1):
        name = author_names[email][:24]
        pct = cnt / total * 100
        medal = medals[rank - 1] if rank <= 3 else f"  {rank}."
        color = colors[rank - 1] if rank <= 3 else GRAY
        bar = hbar(cnt, max_cnt, 20, color)
        line = f"  {medal}  {color}{name:<24}{RESET}  {bar}  {color}{cnt:4d}{GRAY} ({pct:4.1f}%){RESET}"
        print(box_row(line, w, BGREEN))

    if not sorted_authors:
        print(box_row(f"  {GRAY}No commits found in range.{RESET}", w, BGREEN))

    print(box_bot(w, BGREEN))
    print()


def render_hotfiles(file_changes: dict[str, int]) -> None:
    """Render file hotspot analysis."""
    w = TERM_WIDTH
    print(box_top("File Hotspots  (most frequently changed)", w, RED))

    if not file_changes:
        print(box_row(f"  {GRAY}No file change data available.{RESET}", w, RED))
        print(box_bot(w, RED))
        print()
        return

    sorted_files = sorted(file_changes.items(), key=lambda x: x[1], reverse=True)[:12]
    max_changes = sorted_files[0][1] if sorted_files else 1

    # Extension → color mapping
    def ext_color(path: str) -> str:
        ext = Path(path).suffix.lower()
        mapping = {
            ".py": BBLUE, ".js": BYELLOW, ".ts": BCYAN,
            ".go": BGREEN, ".rs": RED, ".java": BYELLOW,
            ".md": BWHITE, ".json": GRAY, ".yaml": MAGENTA,
            ".yml": MAGENTA, ".sh": BGREEN, ".html": RED,
            ".css": BLUE, ".c": GRAY, ".cpp": GRAY, ".h": GRAY,
        }
        return mapping.get(ext, BWHITE)

    print(box_row(f"  {'File':<40}  {'Changes':>7}  {'Frequency':>12}", w, RED))
    print(box_row(f"  {'─' * 40}  {'─' * 7}  {'─' * 12}", w, RED))
    for path, cnt in sorted_files:
        display = path if len(path) <= 40 else "…" + path[-39:]
        color = ext_color(path)
        bar = hbar(cnt, max_changes, 12, color)
        line = f"  {color}{display:<40}{RESET}  {BWHITE}{cnt:>7}{RESET}  {bar}"
        print(box_row(line, w, RED))

    print(box_bot(w, RED))
    print()


def render_branches(branches: list[dict]) -> None:
    """Render branch list."""
    w = TERM_WIDTH
    print(box_top("Branches", w, BBLUE))

    local   = [b for b in branches if not b["name"].startswith("origin/")]
    remotes = [b for b in branches if b["name"].startswith("origin/")]

    def render_group(label: str, items: list[dict], color: str) -> None:
        print(box_row(f"  {BOLD}{label}{RESET}", w, BBLUE))
        for b in items[:8]:
            name = b["name"][:50]
            when = b["when"][:20] if b["when"] else ""
            gap = w - 4 - 4 - 50 - 20
            line = f"  {color}⎇ {name:<50}{RESET}{GRAY}{' ' * max(0, gap)}{when:>20}{RESET}"
            print(box_row(line, w, BBLUE))
        if not items:
            print(box_row(f"    {GRAY}none{RESET}", w, BBLUE))

    render_group("Local", local, BBLUE)
    print(box_row("", w, BBLUE))
    render_group("Remote", remotes, BCYAN)

    print(box_bot(w, BBLUE))
    print()


def render_recent_commits(commits: list[dict], n: int = 10) -> None:
    """Render recent commit log."""
    w = TERM_WIDTH
    print(box_top(f"Recent Commits  (last {n})", w, GRAY))

    for c in commits[:n]:
        h = c["hash"][:7]
        author = c["author"][:16]
        subject = c["subject"]
        date_str = c["date"]
        max_subj = w - 4 - 7 - 1 - 16 - 1 - 10 - 3
        if len(subject) > max_subj:
            subject = subject[:max_subj - 1] + "…"
        line = (
            f"{YELLOW}{h}{RESET} "
            f"{GRAY}{date_str}{RESET} "
            f"{BCYAN}{author:<16}{RESET} "
            f"{WHITE}{subject}{RESET}"
        )
        print(box_row(line, w, GRAY))

    if not commits:
        print(box_row(f"  {GRAY}No commits found.{RESET}", w, GRAY))

    print(box_bot(w, GRAY))
    print()


def render_footer(elapsed: float) -> None:
    print(center(
        f"{DIM}{GRAY}Generated by {BMAGENTA}GitPulse{GRAY} in {elapsed:.2f}s  •  "
        f"python gitpulse.py [path] [--days N]{RESET}"
    ))
    print()


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    import time
    import argparse

    parser = argparse.ArgumentParser(
        description="GitPulse — beautiful terminal git analytics dashboard"
    )
    parser.add_argument("path", nargs="?", default=".", help="Path to git repository")
    parser.add_argument("--days", type=int, default=365, help="History window in days (default: 365)")
    args = parser.parse_args()

    t0 = time.time()

    os.chdir(args.path)
    root = get_repo_root()
    repo_name = get_repo_name(root)

    # Collect all data
    commits      = collect_commits(root, days=args.days)
    file_changes = collect_file_changes(root, days=args.days)
    branches     = collect_branches(root)
    stats        = get_stats(root)

    # Render dashboard
    render_header(repo_name, stats)
    render_summary(stats)
    render_heatmap(commits)
    render_commit_frequency(commits)
    render_authors(commits)
    render_hotfiles(file_changes)
    render_branches(branches)
    render_recent_commits(commits, n=10)
    render_footer(time.time() - t0)


if __name__ == "__main__":
    main()
