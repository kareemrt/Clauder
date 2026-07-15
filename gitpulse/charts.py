"""ASCII chart rendering utilities."""

import math

# ANSI colour helpers
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

# Foreground colours
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

# Background
BG_DARK = "\033[40m"

SPARK_CHARS = " ▁▂▃▄▅▆▇█"
BLOCK_FULL  = "█"
BLOCK_HALF  = "▌"
BAR_CHAR    = "━"
HEATMAP_LOW  = " ░▒▓"
HEATMAP_HIGH = "▓█"

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HOURS    = [f"{h:02d}" for h in range(24)]


def _colour_gradient(value, max_value):
    """Map 0..max_value → colour string."""
    if max_value == 0:
        return DIM + GRAY
    ratio = value / max_value
    if ratio == 0:
        return DIM + GRAY
    if ratio < 0.25:
        return BLUE
    if ratio < 0.5:
        return CYAN
    if ratio < 0.75:
        return YELLOW
    return GREEN + BOLD


def sparkline(values, width=None):
    """Render a mini sparkline using block chars."""
    if not values:
        return ""
    if width:
        # Downsample / upsample to width
        if len(values) > width:
            step = len(values) / width
            values = [values[int(i * step)] for i in range(width)]
        elif len(values) < width:
            values = values + [0] * (width - len(values))
    mx = max(values) if values else 1
    mn = min(values)
    span = mx - mn or 1
    chars = []
    for v in values:
        idx = int(((v - mn) / span) * (len(SPARK_CHARS) - 1))
        col = _colour_gradient(v, mx)
        chars.append(col + SPARK_CHARS[idx] + RESET)
    return "".join(chars)


def bar_chart(data: dict, width=40, colour=GREEN, label_width=20, max_bars=15):
    """Horizontal bar chart. data: {label: value}."""
    items = list(data.items())[:max_bars]
    mx = max((v for _, v in items), default=1)
    lines = []
    for label, value in items:
        bar_len = int((value / mx) * width) if mx else 0
        bar = colour + BLOCK_FULL * bar_len + RESET
        pad = width - bar_len
        label_str = label[:label_width].ljust(label_width)
        lines.append(f"  {DIM}{label_str}{RESET}  {bar}{' ' * pad}  {BOLD}{value}{RESET}")
    return "\n".join(lines)


def commit_heatmap(hour_hist, weekday_hist, title="Commit Timing"):
    """Two mini histograms: by hour and by weekday."""
    lines = [f"  {BOLD}{CYAN}{title}{RESET}"]

    # Hour histogram
    mx_h = max(hour_hist) or 1
    hour_line = "".join(
        _colour_gradient(h, mx_h) + (HEATMAP_LOW + HEATMAP_HIGH)[(h * 5) // (mx_h + 1)] + RESET
        for h in hour_hist
    )
    lines.append(f"  {DIM}Hour (00-23):{RESET} {hour_line}")
    lines.append(f"           {DIM}{''.join(str(i // 2) if i % 2 == 0 else ' ' for i in range(24))}{RESET}")

    # Weekday histogram
    mx_w = max(weekday_hist) or 1
    lines.append("")
    for i, (day, count) in enumerate(zip(WEEKDAYS, weekday_hist)):
        bar_len = int((count / mx_w) * 30)
        col = _colour_gradient(count, mx_w)
        bar = col + BLOCK_FULL * bar_len + RESET
        lines.append(f"  {DIM}{day}{RESET}  {bar}  {BOLD}{count}{RESET}")

    return "\n".join(lines)


def contributor_table(contributors, max_rows=10):
    """Ranked contributor table with bar."""
    if not contributors:
        return "  (no contributor data)"
    mx = contributors[0][1]["commits"] if contributors else 1
    lines = [
        f"  {BOLD}{CYAN}{'#':<4}{'Author':<28}{'Commits':>8}  {'Share':>6}{RESET}"
    ]
    lines.append(f"  {DIM}{'─'*4}{'─'*28}{'─'*8}  {'─'*6}{RESET}")
    total_c = sum(v["commits"] for _, v in contributors)
    for rank, (email, info) in enumerate(contributors[:max_rows], 1):
        name = info["name"] or email.split("@")[0]
        count = info["commits"]
        pct = count / total_c * 100 if total_c else 0
        bar_len = int((count / mx) * 12)
        col = [GREEN, CYAN, YELLOW, MAGENTA, BLUE][rank % 5]
        bar = col + BLOCK_FULL * bar_len + RESET
        lines.append(
            f"  {DIM}{rank:<4}{RESET}{name[:27]:<28}{BOLD}{count:>8}{RESET}  "
            f"{DIM}{pct:>5.1f}%{RESET}  {bar}"
        )
    return "\n".join(lines)


def language_bar(lang_data: dict, max_langs=8):
    """Coloured language breakdown bar + legend."""
    items = list(lang_data.items())[:max_langs]
    total = sum(v for _, v in items)
    colours = [GREEN, CYAN, YELLOW, MAGENTA, BLUE, RED, WHITE, GRAY]

    bar_width = 60
    bar_parts = []
    for i, (ext, count) in enumerate(items):
        part_len = max(1, int((count / total) * bar_width)) if total else 0
        col = colours[i % len(colours)]
        bar_parts.append(col + BLOCK_FULL * part_len + RESET)

    bar_str = "".join(bar_parts)
    legend = "  " + "  ".join(
        f"{colours[i % len(colours)]}{BLOCK_FULL}{RESET} .{ext}"
        for i, (ext, _) in enumerate(items)
    )
    return f"  {bar_str}\n{legend}"


def section_header(title):
    width = 64
    pad = (width - len(title) - 2) // 2
    return (
        f"\n  {CYAN}{DIM}{'─' * pad}{RESET} "
        f"{BOLD}{WHITE}{title}{RESET} "
        f"{CYAN}{DIM}{'─' * pad}{RESET}\n"
    )
