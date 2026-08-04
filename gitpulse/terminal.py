"""Terminal visualizer — rich ANSI output for GitPulse."""
from datetime import date, timedelta

# ── ANSI helpers ──────────────────────────────────────────────────────────────

C = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
}


def c(color: str, text: str) -> str:
    return f"{C.get(color, '')}{text}{C['reset']}"


def bold(text: str) -> str:
    return f"{C['bold']}{text}{C['reset']}"


# ── Layout ────────────────────────────────────────────────────────────────────

BANNER = r"""
   ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
  ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
  ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
"""

WIDTH = 76


def divider(ch="─", color="dim"):
    return c(color, ch * WIDTH)


def section_header(title: str, icon: str = ""):
    label = f" {icon} {title} " if icon else f" {title} "
    side = (WIDTH - len(label) - 2) // 2
    line = "┄" * side + label + "┄" * (WIDTH - side - len(label) - 2)
    print()
    print(c("cyan", line))
    print()


def bar(value: int, max_value: int, width: int = 28, fill="█", empty="░") -> str:
    filled = int(width * value / max(max_value, 1))
    return c("green", fill * filled) + c("dim", empty * (width - filled))


# ── Sections ──────────────────────────────────────────────────────────────────

def print_banner(repo_name: str):
    print(c("cyan", BANNER))
    print(f"  {bold(c('yellow', 'Git Repository Analytics'))}  ·  {c('magenta', repo_name)}")
    print(f"  {divider()}")


def print_summary(data: dict):
    section_header("Summary", "📊")
    info = data["repo_info"]
    commits = data["commits"]
    authors = data["author_stats"]

    def row(label, value, color="white"):
        print(f"  {c('dim', label + ':'): <26}{c(color, str(value))}")

    row("Repository", info["name"], "cyan")
    row("Branch", info["branch"], "yellow")
    row("Total commits", info["total_commits"], "bold")
    row("Contributors", len(authors), "bold")

    if commits:
        first = min(c["date"] for c in commits)
        last = max(c["date"] for c in commits)
        row("Active since", first.strftime("%Y-%m-%d"))
        row("Last commit", last.strftime("%Y-%m-%d"), "green")
        days = (last - first).days + 1
        row("Days active", days)
        avg = info["total_commits"] / max(days, 1)
        row("Avg commits/day", f"{avg:.2f}")

    if info["remote"]:
        remote = info["remote"]
        if len(remote) > 55:
            remote = remote[:52] + "..."
        row("Remote", remote, "dim")


def print_commit_calendar(calendar_data: dict):
    section_header("Contribution Calendar (last 52 weeks)", "📅")

    today = date.today()
    # Start on the most recent Monday 52 weeks ago
    start = today - timedelta(weeks=52)
    start -= timedelta(days=start.weekday())  # back to Monday

    weeks = []
    current = start
    while current <= today:
        week = []
        for _ in range(7):
            week.append((current.isoformat(), calendar_data.get(current.isoformat(), 0)))
            current += timedelta(days=1)
        weeks.append(week)

    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Print month headers
    month_row = "       "
    prev_month = None
    for week in weeks:
        monday = week[0][0]
        m = monday[5:7]
        if m != prev_month:
            month_row += monday[2:7].replace("-", "/")[:4]
            prev_month = m
        else:
            month_row += "  "
    print(c("dim", "  " + month_row[:WIDTH]))

    for day_idx, day_name in enumerate(day_labels):
        row = f"  {c('dim', day_name)} "
        for week in weeks:
            _, count = week[day_idx]
            if count == 0:
                cell = c("dim", "·")
            elif count == 1:
                cell = c("green", "░")
            elif count <= 3:
                cell = c("green", "▒")
            elif count <= 6:
                cell = c("green", "▓")
            else:
                cell = c("green", "█")
            row += cell + " "
        print(row)

    legend = (
        f"  {c('dim', '· none')}  "
        f"{c('green', '░ 1')}  "
        f"{c('green', '▒ 2–3')}  "
        f"{c('green', '▓ 4–6')}  "
        f"{c('green', '█ 7+')}"
    )
    print(f"\n{legend}")


def print_monthly_trend(monthly_commits: list):
    section_header("Monthly Commit Trend", "📈")
    if not monthly_commits:
        print("  No data.")
        return
    max_val = max(v for _, v in monthly_commits)
    for month, count in monthly_commits[-24:]:  # last 24 months
        blen = int(50 * count / max(max_val, 1))
        trend_bar = c("magenta", "▬" * blen)
        print(f"  {c('dim', month)}  {trend_bar}  {bold(str(count))}")


def print_leaderboard(author_stats: dict):
    section_header("Contributor Leaderboard", "🏆")
    ranked = sorted(author_stats.items(), key=lambda x: -x[1]["commits"])
    if not ranked:
        print("  No contributors found.")
        return
    max_commits = ranked[0][1]["commits"]
    medals = ["🥇", "🥈", "🥉"]
    for i, (author, stats) in enumerate(ranked[:10]):
        rank = medals[i] if i < 3 else f"  #{i+1}"
        name = author[:24] + ("…" if len(author) > 24 else "")
        b = bar(stats["commits"], max_commits, width=24)
        count_str = bold(str(stats["commits"]))
        print(f"  {rank}  {c('white', f'{name:<25}')} {b}  {count_str}")


def print_hotspots(file_stats: dict):
    section_header("File Hotspots (most frequently changed)", "🔥")
    items = list(file_stats.items())[:10]
    if not items:
        print("  No file data.")
        return
    max_val = items[0][1]
    for filepath, count in items:
        parts = filepath.split("/")
        short = filepath if len(filepath) <= 30 else "…/" + "/".join(parts[-2:])
        b = bar(count, max_val, width=24, fill="█", empty="░")
        # color bar yellow for hotspots
        b = c("yellow", "█" * int(24 * count / max(max_val, 1))) + c(
            "dim", "░" * (24 - int(24 * count / max(max_val, 1)))
        )
        print(f"  {c('white', f'{short:<31}')} {b}  {bold(str(count))}")


def print_languages(lang_breakdown: dict):
    section_header("Language Breakdown", "💻")
    items = list(lang_breakdown.items())[:8]
    if not items:
        print("  No files found.")
        return
    total = sum(v for _, v in items)
    palette = ["cyan", "blue", "magenta", "green", "yellow", "red", "white", "dim"]
    for i, (ext, count) in enumerate(items):
        pct = 100 * count / max(total, 1)
        color = palette[i % len(palette)]
        filled = int(28 * count / max(items[0][1], 1))
        b = c(color, "█" * filled) + c("dim", "░" * (28 - filled))
        print(f"  {c('white', f'{ext:<12}')} {b}  {bold(str(count)):<6} {c('dim', f'{pct:.1f}%')}")


def print_recent_commits(commits: list, n: int = 12):
    section_header(f"Recent Commits", "🕐")
    for commit in commits[:n]:
        h = c("dim", commit["hash"][:7])
        d = c("yellow", commit["date"].strftime("%Y-%m-%d"))
        author = c("cyan", f"{commit['author'][:15]:<16}")
        msg = commit["message"]
        if len(msg) > 52:
            msg = msg[:49] + "…"
        print(f"  {h}  {d}  {author}  {msg}")


def print_footer():
    print()
    print(f"  {divider()}")
    print(f"  {c('dim', 'Generated by')} {c('cyan', 'GitPulse')} {c('dim', '· github.com/kareemrt/clauder')}")
    print()
