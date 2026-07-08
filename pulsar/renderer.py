"""Terminal renderer — ASCII art visualizations of git stats."""

from datetime import datetime, timedelta, timezone
from collections import defaultdict

# ANSI colour helpers
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_DIM    = "\033[2m"
_RED    = "\033[91m"
_GREEN  = "\033[92m"
_YELLOW = "\033[93m"
_BLUE   = "\033[94m"
_MAGENTA= "\033[95m"
_CYAN   = "\033[96m"
_WHITE  = "\033[97m"

BARS   = " ▁▂▃▄▅▆▇█"
BLOCKS = " ░▒▓█"

PULSE_COLORS = [_CYAN, _BLUE, _MAGENTA, _RED, _YELLOW, _GREEN, _WHITE]


def _c(text, *codes):
    return "".join(codes) + text + _RESET


def _banner(repo_name: str, branch: str) -> str:
    logo = r"""
  ██████╗ ██╗   ██╗██╗     ███████╗ █████╗ ██████╗
  ██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗██╔══██╗
  ██████╔╝██║   ██║██║     ███████╗███████║██████╔╝
  ██╔═══╝ ██║   ██║██║     ╚════██║██╔══██║██╔══██╗
  ██║     ╚██████╔╝███████╗███████║██║  ██║██║  ██║
  ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
    """
    lines = [_c(logo, _CYAN, _BOLD)]
    lines.append(_c(f"  Git Repository Heartbeat Visualizer", _DIM))
    lines.append("")
    lines.append(_c(f"  ◈ Repository : ", _DIM) + _c(repo_name, _BOLD, _WHITE))
    lines.append(_c(f"  ◈ Branch     : ", _DIM) + _c(branch, _YELLOW))
    lines.append("")
    return "\n".join(lines)


def _section(title: str) -> str:
    bar = "─" * (74 - len(title) - 2)
    return _c(f"\n  ┌── {title} {bar}\n", _BLUE, _BOLD)


def _heartbeat(daily_counts: dict, days: int) -> str:
    today = datetime.now(tz=timezone.utc).date()
    counts = []
    for i in range(days - 1, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        counts.append(daily_counts.get(d, 0))

    if not any(counts):
        return _c("  (no commits in this period)\n", _DIM)

    max_c = max(counts) or 1
    buckets = days // 7  # weeks
    weekly = []
    for w in range(buckets):
        week_slice = counts[w * 7: (w + 1) * 7]
        weekly.append(sum(week_slice))

    max_w = max(weekly) if weekly else 1

    def bar_char(v, mx):
        idx = round(v / mx * (len(BARS) - 1))
        return BARS[idx]

    lines = []
    lines.append(_c("  Daily pulse (▁ low  ▄ mid  █ peak)\n", _DIM))

    # sparkline across all days
    spark = ""
    for i, v in enumerate(counts):
        ch = bar_char(v, max_c)
        col = PULSE_COLORS[i % len(PULSE_COLORS)] if v > 0 else _DIM
        spark += _c(ch, col)
    lines.append("  " + spark)
    lines.append("")

    # weekly summary bar chart
    lines.append(_c("  Weekly totals\n", _DIM))
    peak = max(weekly) if weekly else 1
    for w, total in enumerate(weekly):
        label = f"  W{w+1:>2} "
        filled = round(total / peak * 40)
        bar = "█" * filled
        col = _GREEN if total > peak * 0.7 else _CYAN if total > peak * 0.3 else _DIM
        lines.append(label + _c(bar, col) + _c(f"  {total}", _DIM))
    lines.append("")
    return "\n".join(lines)


def _heatmap(hourly_matrix_raw: dict) -> str:
    """24h × 7-day activity heatmap."""
    # Parse "weekday,hour" -> count
    matrix: dict[tuple, int] = defaultdict(int)
    for key, v in hourly_matrix_raw.items():
        wd, hr = map(int, key.split(","))
        matrix[(wd, hr)] += v

    if not matrix:
        return _c("  (no data)\n", _DIM)

    max_v = max(matrix.values()) if matrix else 1
    days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    lines = []
    header = "        " + "  ".join(_c(d, _BOLD) for d in days_labels)
    lines.append(header)

    for hr in range(0, 24, 3):
        row = f"  {hr:02d}:00  "
        for wd in range(7):
            v = matrix.get((wd, hr), 0)
            # aggregate 3-hour block
            block = sum(matrix.get((wd, h), 0) for h in range(hr, min(hr + 3, 24)))
            ratio = block / (max_v * 3) if max_v else 0
            idx = min(int(ratio * (len(BLOCKS) - 1)), len(BLOCKS) - 1)
            ch = BLOCKS[idx] * 2
            if idx == 0:
                col = _DIM
            elif idx == 1:
                col = _BLUE
            elif idx == 2:
                col = _CYAN
            elif idx == 3:
                col = _YELLOW
            else:
                col = _c("", _RED, _BOLD)
                col = _RED + _BOLD
            row += _c(ch, col) + "  "
        lines.append(row)
    lines.append("")
    return "\n".join(lines)


def _contributors(contributors: list, period_commits: int) -> str:
    if not contributors:
        return _c("  (no contributor data)\n", _DIM)

    lines = []
    max_commits = contributors[0]["commits"] if contributors else 1
    colors = [_YELLOW, _CYAN, _GREEN, _MAGENTA, _RED, _BLUE, _WHITE]

    for i, c in enumerate(contributors[:10]):
        col = colors[i % len(colors)]
        pct = c["commits"] / period_commits * 100 if period_commits else 0
        bar_len = round(c["commits"] / max_commits * 35)
        bar = "█" * bar_len
        name = c["name"][:22].ljust(22)
        lines.append(
            f"  {_c(name, col, _BOLD)}  {_c(bar, col)}  "
            f"{_c(str(c['commits']).rjust(4) + ' commits', _DIM)}"
            f"  {_c(f'{pct:.1f}%', _DIM)}"
        )
    lines.append("")
    return "\n".join(lines)


def _top_files(top_files: list) -> str:
    if not top_files:
        return _c("  (no file data)\n", _DIM)

    lines = []
    max_changes = top_files[0]["changes"] if top_files else 1

    for f in top_files[:10]:
        bar_len = round(f["changes"] / max_changes * 30)
        bar = "░" * bar_len
        path = f["path"]
        if len(path) > 40:
            path = "…" + path[-39:]
        path = path.ljust(41)
        lines.append(
            f"  {_c(path, _CYAN)}  {_c(bar, _MAGENTA)}  "
            f"{_c(str(f['changes']) + 'x', _DIM)}"
        )
    lines.append("")
    return "\n".join(lines)


def _languages(lang_counts: dict) -> str:
    if not lang_counts:
        return _c("  (no file data)\n", _DIM)

    total = sum(lang_counts.values())
    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    colors = [_YELLOW, _CYAN, _GREEN, _MAGENTA, _RED, _BLUE, _WHITE, _DIM]

    lines = []
    for i, (lang, count) in enumerate(sorted_langs):
        col = colors[i % len(colors)]
        pct = count / total * 100
        bar_len = round(pct / 100 * 40)
        bar = "█" * bar_len
        lines.append(
            f"  {_c(lang[:18].ljust(18), col, _BOLD)}  {_c(bar, col)}  "
            f"{_c(f'{pct:5.1f}%  {count} files', _DIM)}"
        )
    lines.append("")
    return "\n".join(lines)


def _summary_stats(stats: dict) -> str:
    lines = [
        f"  {'Total commits (all time)':<30}  {_c(str(stats['total_commits']), _BOLD, _WHITE)}",
        f"  {'Commits (last ' + str(stats['days']) + ' days)':<30}  {_c(str(stats['period_commits']), _BOLD, _CYAN)}",
        f"  {'Lines added (period)':<30}  {_c('+' + str(stats['total_insertions']), _GREEN, _BOLD)}",
        f"  {'Lines removed (period)':<30}  {_c('-' + str(stats['total_deletions']), _RED, _BOLD)}",
        f"  {'Contributors (active)':<30}  {_c(str(len(stats['contributors'])), _BOLD, _YELLOW)}",
        "",
    ]
    return "\n".join(lines)


def render(stats: dict) -> str:
    """Render the full terminal report as a string."""
    out = []
    out.append(_banner(stats["repo_name"], stats["branch"]))
    out.append(_section("SUMMARY"))
    out.append(_summary_stats(stats))
    out.append(_section(f"HEARTBEAT — last {stats['days']} days"))
    out.append(_heartbeat(stats["daily_counts"], stats["days"]))
    out.append(_section("ACTIVITY HEATMAP — hour × weekday"))
    out.append(_heatmap(stats["hourly_matrix"]))
    out.append(_section("CONTRIBUTORS"))
    out.append(_contributors(stats["contributors"], stats["period_commits"]))
    out.append(_section("HOTSPOT FILES — most frequently changed"))
    out.append(_top_files(stats["top_files"]))
    out.append(_section("LANGUAGE BREAKDOWN"))
    out.append(_languages(stats["lang_counts"]))
    out.append(_c("  ◈ Analysis complete. Run with --report to generate an HTML report.\n", _DIM))
    return "\n".join(out)
