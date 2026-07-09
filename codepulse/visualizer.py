"""
Terminal visualizations — ASCII charts, heatmaps, and tables.
No external dependencies required.
"""
from collections import defaultdict
from datetime import datetime


COMMIT_TYPE_ICONS = {
    "feature": "✨",
    "fix":     "🐛",
    "docs":    "📝",
    "test":    "🧪",
    "refactor":"♻️ ",
    "chore":   "🔧",
    "style":   "🎨",
    "perf":    "⚡",
    "merge":   "🔀",
    "other":   "📦",
}

BLOCK_CHARS = ["░", "▒", "▓", "█"]
SPARK_CHARS  = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

DAY_NAMES  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HOUR_RANGE = list(range(24))


def _color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"


def bold(t):    return _color(t, "1")
def dim(t):     return _color(t, "2")
def green(t):   return _color(t, "32")
def cyan(t):    return _color(t, "36")
def yellow(t):  return _color(t, "33")
def red(t):     return _color(t, "31")
def magenta(t): return _color(t, "35")
def blue(t):    return _color(t, "34")


def header(title: str, width: int = 70) -> str:
    pad = max(0, width - len(title) - 4)
    left  = pad // 2
    right = pad - left
    bar = "─" * width
    return f"\n{bold(cyan('╭' + bar + '╮'))}\n{bold(cyan('│'))} {bold(title)}{' ' * (width - len(title) - 2)} {bold(cyan('│'))}\n{bold(cyan('╰' + bar + '╯'))}"


def sparkline(values: list[int], width: int = 40) -> str:
    if not values:
        return ""
    mn, mx = min(values), max(values)
    rng = mx - mn or 1
    chars = []
    for v in values[-width:]:
        idx = int((v - mn) / rng * (len(SPARK_CHARS) - 1))
        chars.append(SPARK_CHARS[idx])
    return "".join(chars)


def bar_chart(data: dict, title: str = "", max_bar: int = 40, top_n: int = 20, color_fn=cyan) -> str:
    if not data:
        return ""
    items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    mx = max(v for _, v in items) or 1
    max_label = max(len(str(k)) for k, _ in items)
    lines = []
    if title:
        lines.append(bold(title))
    for label, val in items:
        bar_len = int(val / mx * max_bar)
        bar = color_fn("█" * bar_len) + dim("░" * (max_bar - bar_len))
        pct = val / sum(v for _, v in items) * 100
        lines.append(f"  {str(label):<{max_label}} │{bar}│ {bold(str(val))} ({pct:.1f}%)")
    return "\n".join(lines)


def activity_heatmap(commits: list, width: int = 53) -> str:
    """GitHub-style contribution heatmap by week."""
    if not commits:
        return ""
    # Build day bucket: date -> count
    day_counts: dict = defaultdict(int)
    for c in commits:
        day_counts[c.date.date()] += 1

    if not day_counts:
        return ""

    dates = sorted(day_counts.keys())
    start = dates[0]
    end   = dates[-1]

    # Pad to Monday
    from datetime import timedelta, date
    cur = start - timedelta(days=start.weekday())
    weeks = []
    week  = []
    d = cur
    while d <= end + timedelta(days=6):
        if d.weekday() == 0 and week:
            weeks.append(week)
            week = []
        week.append((d, day_counts.get(d, 0)))
        d += timedelta(days=1)
    if week:
        weeks.append(week)

    weeks = weeks[-width:]  # keep last `width` weeks

    mx = max(day_counts.values()) if day_counts else 1

    def cell(count):
        if count == 0:
            return dim("·")
        idx = min(int(count / mx * 3), 3)
        return green(BLOCK_CHARS[idx])

    # Header: month labels
    month_labels = [""] * len(weeks)
    for i, week in enumerate(weeks):
        for day, _ in week:
            if day.day <= 7:
                month_labels[i] = day.strftime("%b")
                break

    header_line = "     " + "".join(f"{m:<2}" for m in month_labels)

    rows = []
    for wd in range(7):
        day_label = DAY_NAMES[wd] if wd in (0, 2, 4) else "   "
        cells = []
        for week in weeks:
            match = [v for d, v in week if d.weekday() == wd]
            cells.append(cell(match[0] if match else 0))
        rows.append(f"  {day_label} " + " ".join(cells))

    total = sum(day_counts.values())
    legend = (
        f"\n  Legend: {dim('·')} none  "
        f"{green(BLOCK_CHARS[0])} low  "
        f"{green(BLOCK_CHARS[2])} med  "
        f"{green(BLOCK_CHARS[3])} high"
        f"   ({bold(str(total))} total commits)"
    )
    return header_line + "\n" + "\n".join(rows) + legend


def hourly_chart(hourly: dict[int, int]) -> str:
    """24-hour activity bar chart."""
    values = [hourly.get(h, 0) for h in range(24)]
    mx = max(values) or 1
    HEIGHT = 8
    rows = []
    for row in range(HEIGHT, 0, -1):
        threshold = mx * row / HEIGHT
        cells = []
        for v in values:
            if v >= threshold:
                cells.append(blue("█"))
            elif v >= threshold * 0.5:
                cells.append(blue("▄"))
            else:
                cells.append(dim("·"))
        label = f"{mx * row // HEIGHT:>4} │" if row == HEIGHT else "     │"
        rows.append(label + " ".join(cells))
    rows.append("     └" + "─" * 48)
    rows.append("      " + " ".join(f"{h:>1}" if h % 4 == 0 else " " for h in range(24)))
    rows.append("      " + " ".join(" " if h % 4 != 0 else str(h).ljust(1) for h in range(24)))
    return "\n".join(rows)


def weekday_chart(weekday: dict[int, int]) -> str:
    values = [weekday.get(d, 0) for d in range(7)]
    mx = max(values) or 1
    lines = []
    for i, (v, name) in enumerate(zip(values, DAY_NAMES)):
        bar_len = int(v / mx * 30)
        bar = cyan("█" * bar_len) + dim("░" * (30 - bar_len))
        weekend = dim(name) if i >= 5 else name
        lines.append(f"  {weekend} │{bar}│ {bold(str(v))}")
    return "\n".join(lines)


def commit_type_breakdown(commits: list) -> str:
    counts: dict = defaultdict(int)
    for c in commits:
        counts[c.commit_type] += 1
    total = len(commits) or 1
    lines = []
    for ctype, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        icon = COMMIT_TYPE_ICONS.get(ctype, "  ")
        bar_len = int(count / total * 35)
        bar = magenta("█" * bar_len) + dim("░" * (35 - bar_len))
        pct = count / total * 100
        lines.append(f"  {icon} {ctype:<10} │{bar}│ {bold(str(count)):>5} ({pct:.0f}%)")
    return "\n".join(lines)


def top_files_table(file_stats: dict, top_n: int = 15) -> str:
    items = sorted(file_stats.values(), key=lambda f: f.commits, reverse=True)[:top_n]
    if not items:
        return ""
    lines = [
        f"  {'File':<45} {'Commits':>7}  {'Churn':>7}  {'Authors':>7}",
        "  " + "─" * 70,
    ]
    for fs in items:
        path = fs.path
        if len(path) > 43:
            path = "…" + path[-42:]
        churn_color = red if fs.churn > 1000 else yellow if fs.churn > 300 else green
        lines.append(
            f"  {path:<45} {bold(str(fs.commits)):>7}  "
            f"{churn_color(str(fs.churn)):>7}  {str(len(fs.authors)):>7}"
        )
    return "\n".join(lines)


def contributor_table(contributors: dict, top_n: int = 10) -> str:
    items = sorted(contributors.items(), key=lambda x: x[1]["commits"], reverse=True)[:top_n]
    if not items:
        return ""
    lines = [
        f"  {'Author':<25} {'Commits':>8}  {'Insertions':>11}  {'Deletions':>10}  {'Files':>6}",
        "  " + "─" * 65,
    ]
    for i, (author, stats) in enumerate(items):
        medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "  "
        lines.append(
            f"  {medal} {author:<23} {bold(str(stats['commits'])):>8}  "
            f"{green('+' + str(stats['insertions'])):>11}  "
            f"{red('-' + str(stats['deletions'])):>10}  "
            f"{str(len(stats['files'])):>6}"
        )
    return "\n".join(lines)


def summary_box(stats: dict) -> str:
    fields = [
        ("Total Commits",    bold(str(stats.get("total_commits", 0))),       "📊"),
        ("Contributors",     bold(str(stats.get("contributors", 0))),         "👥"),
        ("Files Changed",    bold(str(stats.get("files_changed", 0))),        "📁"),
        ("Lines Added",      green(f"+{stats.get('insertions', 0):,}"),       "➕"),
        ("Lines Removed",    red(f"-{stats.get('deletions', 0):,}"),          "➖"),
        ("Active Days",      bold(str(stats.get("active_days", 0))),          "📅"),
        ("Repo Age",         bold(stats.get("age", "?")),                     "⏳"),
        ("Most Active Day",  bold(stats.get("most_active_day", "?")),         "🔥"),
    ]
    lines = []
    for label, value, icon in fields:
        lines.append(f"  {icon}  {label:<20} {value}")
    return "\n".join(lines)
