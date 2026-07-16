"""Terminal rendering: heatmap, timeline, bar charts — all ANSI colored."""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# ANSI 256-color backgrounds for heatmap (green shades)
_HEAT = [
    "\033[48;5;235m",  # 0  — near-black
    "\033[48;5;22m",   # 1-2
    "\033[48;5;28m",   # 3-5
    "\033[48;5;34m",   # 6-10
    "\033[48;5;46m",   # 11+
]
_RESET = "\033[0m"

_AUTHOR_COLORS = [
    Fore.CYAN, Fore.YELLOW, Fore.MAGENTA, Fore.GREEN,
    "\033[38;5;208m",  # orange
    "\033[38;5;213m",  # pink
    Fore.BLUE,
]


def _tw() -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 100


def _heat_color(n: int) -> str:
    if n == 0:
        return _HEAT[0]
    if n <= 2:
        return _HEAT[1]
    if n <= 5:
        return _HEAT[2]
    if n <= 10:
        return _HEAT[3]
    return _HEAT[4]


def render_banner(repo_info: Dict, commits, author_stats: Dict) -> None:
    w = _tw()
    total = repo_info.get("total_commits", len(commits))
    n_authors = len(author_stats)
    ins = sum(s["insertions"] for s in author_stats.values())
    dels = sum(s["deletions"] for s in author_stats.values())
    if commits:
        span_days = max((commits[-1].date - commits[0].date).days, 1)
        first = commits[0].date.strftime("%Y-%m-%d")
        last = commits[-1].date.strftime("%Y-%m-%d")
    else:
        span_days = 0
        first = last = "—"

    border = "═" * (w - 2)
    print()
    print(f"  {Fore.CYAN}{Style.BRIGHT}{border}{_RESET}")
    print(f"  {Fore.CYAN}{Style.BRIGHT}⚡  CLAUDER — Git Time Machine{_RESET}")
    print(f"  {border}{_RESET}")
    cols = [
        ("Repository", repo_info.get("name", "?")),
        ("Branch",     repo_info.get("branch", "?")),
        ("Commits",    f"{total:,}"),
        ("Authors",    str(n_authors)),
        ("Active days",f"{span_days:,}"),
        ("Lines +",    f"+{ins:,}"),
        ("Lines −",    f"−{dels:,}"),
        ("Earliest",   first),
        ("Latest",     last),
    ]
    for label, val in cols:
        print(f"  {Fore.WHITE}{label:<14}{Fore.GREEN}{Style.BRIGHT}{val}{_RESET}")
    print(f"  {Fore.CYAN}{Style.BRIGHT}{border}{_RESET}")
    print()


def render_heatmap(date_map: Dict[str, int], weeks: int = 52) -> None:
    today = datetime.now()
    # align start to Monday, weeks ago
    start = today - timedelta(weeks=weeks, days=today.weekday())

    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    print(f"  {Fore.WHITE}{Style.BRIGHT}Contribution Heatmap  (last {weeks} weeks){_RESET}")
    print()

    # Month header
    header = "       "
    prev_month = ""
    for wk in range(weeks + 1):
        d = start + timedelta(weeks=wk)
        m = d.strftime("%b")
        if m != prev_month:
            header += m.ljust(4)
            prev_month = m
        else:
            header += "  "
    print(f"  {Fore.WHITE}{header[:_tw()]}{_RESET}")

    # Grid: 7 rows × weeks columns, each cell = 2 chars
    for dow in range(7):
        line = f"  {Fore.WHITE}{day_labels[dow]} {_RESET}"
        for wk in range(weeks + 1):
            d = start + timedelta(weeks=wk, days=dow)
            if d > today:
                line += "  "
                continue
            key = d.strftime("%Y-%m-%d")
            n = date_map.get(key, 0)
            line += f"{_heat_color(n)}  {_RESET}"
        print(line)

    # Legend
    print(f"\n  {Fore.WHITE}Less {_RESET}", end="")
    for c in _HEAT:
        print(f"{c}  {_RESET}", end="")
    print(f" {Fore.WHITE}More{_RESET}\n")


def render_timeline(commits, limit: int = 25) -> None:
    print(f"  {Fore.WHITE}{Style.BRIGHT}Recent Commits{_RESET}\n")

    recent = list(reversed(commits[-limit:]))
    authors = list(dict.fromkeys(c.author for c in recent))
    acolor = {a: _AUTHOR_COLORS[i % len(_AUTHOR_COLORS)] for i, a in enumerate(authors)}

    for i, c in enumerate(recent):
        col = acolor.get(c.author, Fore.WHITE)
        is_last = i == len(recent) - 1
        dot = "╰" if is_last else "◆"
        date_s = c.date.strftime("%Y-%m-%d %H:%M")
        msg = c.message[:55] + ("…" if len(c.message) > 55 else "")
        print(
            f"  {col}{dot}{_RESET} "
            f"{Fore.WHITE}{date_s}{_RESET}  "
            f"{Fore.CYAN}{c.hash[:7]}{_RESET}  "
            f"{col}{c.author:<16}{_RESET}  "
            f"{msg}"
        )
        if not is_last:
            print(f"  {Fore.WHITE}│{_RESET}")
    print()


def render_author_bars(author_stats: Dict, total: int) -> None:
    print(f"  {Fore.WHITE}{Style.BRIGHT}Contributors{_RESET}\n")

    sorted_a = sorted(author_stats.items(), key=lambda x: x[1]["commits"], reverse=True)[:10]
    if not sorted_a:
        return
    max_c = sorted_a[0][1]["commits"]
    bar_w = min(35, _tw() - 45)

    for i, (author, s) in enumerate(sorted_a):
        col = _AUTHOR_COLORS[i % len(_AUTHOR_COLORS)]
        c = s["commits"]
        pct = c / total * 100 if total else 0
        filled = int(c / max_c * bar_w) if max_c else 0
        bar = "█" * filled + "░" * (bar_w - filled)
        print(f"  {col}{author:<20}{_RESET}  {col}{bar}{_RESET}  {c:>4} commits  ({pct:.1f}%)")
    print()


def render_hotspots(hotspots: List[Tuple[str, int]]) -> None:
    print(f"  {Fore.WHITE}{Style.BRIGHT}File Hotspots (most-changed files){_RESET}\n")
    if not hotspots:
        print(f"  {Fore.WHITE}No data.{_RESET}")
        return

    max_c = hotspots[0][1]
    bar_w = min(28, _tw() - 50)

    for path, count in hotspots:
        display = path if len(path) <= 40 else "…" + path[-39:]
        filled = int(count / max_c * bar_w) if max_c else 0
        bar = "█" * filled + "░" * (bar_w - filled)
        print(f"  {Fore.YELLOW}{display:<41}{_RESET}  {Fore.RED}{bar}{_RESET}  {count}")
    print()


def render_hour_heatmap(hour_map: Dict[int, int]) -> None:
    print(f"  {Fore.WHITE}{Style.BRIGHT}Commit Activity by Hour (UTC){_RESET}\n")
    max_h = max(hour_map.values()) if hour_map else 1
    bar_w = min(40, _tw() - 15)

    for h in range(24):
        n = hour_map.get(h, 0)
        filled = int(n / max_h * bar_w) if max_h else 0
        bar = "█" * filled
        label = f"{h:02d}:00"
        print(f"  {Fore.WHITE}{label}  {Fore.CYAN}{bar:<{bar_w}}{_RESET}  {n}")
    print()


def render_weekly_velocity(weekly: List[int]) -> None:
    print(f"  {Fore.WHITE}{Style.BRIGHT}Weekly Velocity (commits per week, oldest → newest){_RESET}\n")
    max_v = max(weekly) if weekly else 1
    bar_h = 6  # rows tall
    cols = len(weekly)

    # Build a grid from top to bottom
    rows: List[str] = []
    for row in range(bar_h, 0, -1):
        threshold = row / bar_h * max_v
        line = "  "
        for v in weekly:
            if v >= threshold:
                line += f"{Fore.GREEN}█{_RESET}"
            else:
                line += " "
        rows.append(line)

    for r in rows:
        print(r)

    # x-axis tick: every 4 weeks
    axis = "  "
    for i in range(cols):
        if i % 4 == 0:
            axis += "|"
        else:
            axis += "─"
    print(f"{Fore.WHITE}{axis}{_RESET}")
    print()
