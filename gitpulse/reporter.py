"""Generate a self-contained HTML analytics report."""

from datetime import datetime, timedelta, timezone
import html
import json


_DOW_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_MONTH_NAMES = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def _bar_chart_svg(data: dict, label_fn=str, width=520, height=160) -> str:
    if not data:
        return ""
    items = list(data.items())
    max_val = max(v for _, v in items) or 1
    bar_w = (width - 60) / len(items)
    pad_left = 45
    bars = []
    for i, (k, v) in enumerate(items):
        bh = int((v / max_val) * (height - 40))
        x = pad_left + i * bar_w + bar_w * 0.1
        y = height - 20 - bh
        bw = bar_w * 0.8
        label = label_fn(k)
        bars.append(
            f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="3" '
            f'fill="var(--accent)" opacity="0.85">'
            f'<title>{label}: {v}</title></rect>'
        )
        if len(items) <= 12 or i % max(1, len(items) // 8) == 0:
            bars.append(
                f'<text x="{x + bw/2:.1f}" y="{height - 4}" '
                f'text-anchor="middle" font-size="9" fill="var(--muted)">{label}</text>'
            )
    # y-axis ticks
    for tick in [0, max_val // 2, max_val]:
        ty = height - 20 - int((tick / max_val) * (height - 40))
        bars.append(
            f'<line x1="{pad_left-4}" y1="{ty}" x2="{pad_left}" y2="{ty}" '
            f'stroke="var(--muted)" stroke-width="1"/>'
            f'<text x="{pad_left-6}" y="{ty+3}" text-anchor="end" '
            f'font-size="8" fill="var(--muted)">{tick}</text>'
        )
    bars.append(
        f'<line x1="{pad_left}" y1="0" x2="{pad_left}" y2="{height-20}" '
        f'stroke="var(--border)" stroke-width="1"/>'
    )
    bars.append(
        f'<line x1="{pad_left}" y1="{height-20}" x2="{width}" y2="{height-20}" '
        f'stroke="var(--border)" stroke-width="1"/>'
    )
    return (
        f'<svg viewBox="0 0 {width} {height}" width="100%" '
        f'style="display:block;overflow:visible">{"".join(bars)}</svg>'
    )


def _heatmap_svg(by_date: dict, weeks: int = 52) -> str:
    """GitHub-style contribution calendar."""
    today = datetime.now(timezone.utc).date()
    # Find the Sunday before `weeks` weeks ago
    start = today - timedelta(weeks=weeks)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # back to Sunday

    cell = 11
    gap = 2
    pad_top = 20
    pad_left = 28
    total_w = weeks * (cell + gap) + pad_left + 4
    total_h = 7 * (cell + gap) + pad_top + 20

    max_count = max(by_date.values()) if by_date else 1

    cells = []
    month_labels = {}

    d = start
    for week in range(weeks + 1):
        for dow in range(7):
            if d > today:
                d += timedelta(days=1)
                continue
            ds = d.strftime("%Y-%m-%d")
            count = by_date.get(ds, 0)
            intensity = count / max_count if max_count else 0
            # Color levels 0-4
            level = 0 if count == 0 else min(4, 1 + int(intensity * 3.99))
            x = pad_left + week * (cell + gap)
            y = pad_top + dow * (cell + gap)
            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
                f'class="hm-{level}"><title>{ds}: {count} commit{"s" if count != 1 else ""}</title></rect>'
            )
            # Track month label position
            if d.day == 1 or (week == 0 and dow == 0):
                month_labels[week] = _MONTH_NAMES[d.month - 1]
            d += timedelta(days=1)

    # Month labels
    for week, label in month_labels.items():
        x = pad_left + week * (cell + gap)
        cells.append(
            f'<text x="{x}" y="{pad_top - 6}" font-size="9" fill="var(--muted)">{label}</text>'
        )

    # Weekday labels
    for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        if i % 2 == 1:
            y = pad_top + i * (cell + gap) + cell - 1
            cells.append(
                f'<text x="{pad_left - 4}" y="{y}" font-size="8" '
                f'fill="var(--muted)" text-anchor="end">{day}</text>'
            )

    # Legend
    lx = total_w - 80
    ly = total_h - 12
    cells.append(f'<text x="{lx - 4}" y="{ly + 8}" font-size="8" fill="var(--muted)">Less</text>')
    for i in range(5):
        cells.append(
            f'<rect x="{lx + i * (cell + gap) + 28}" y="{ly}" width="{cell}" height="{cell}" '
            f'rx="2" class="hm-{i}"/>'
        )
    cells.append(f'<text x="{lx + 5 * (cell+gap) + 32}" y="{ly + 8}" font-size="8" fill="var(--muted)">More</text>')

    return (
        f'<svg viewBox="0 0 {total_w} {total_h}" width="100%" '
        f'style="display:block">{"".join(cells)}</svg>'
    )


def _horizontal_bar(label: str, value: int, max_val: int, rank: int) -> str:
    pct = int((value / max_val) * 100) if max_val else 0
    return f"""
    <div class="hbar-row">
      <span class="hbar-rank">#{rank}</span>
      <span class="hbar-label" title="{html.escape(label)}">{html.escape(label[:28])}</span>
      <div class="hbar-track">
        <div class="hbar-fill" style="width:{pct}%"></div>
      </div>
      <span class="hbar-val">{value:,}</span>
    </div>"""


def generate_html(repo_name: str, stats: dict) -> str:
    if not stats:
        return "<p>No commits found in this repository.</p>"

    start_dt, end_dt = stats["date_range"]
    span_days = (end_dt - start_dt).days + 1

    # ── Charts ──────────────────────────────────────────────────────────────
    heatmap = _heatmap_svg(stats["by_date"])

    dow_svg = _bar_chart_svg(
        stats["by_dow"],
        label_fn=lambda k: _DOW_LABELS[k],
        height=130,
    )
    hour_svg = _bar_chart_svg(
        stats["by_hour"],
        label_fn=lambda k: f"{k:02d}",
        width=600,
        height=130,
    )

    # ── Authors ──────────────────────────────────────────────────────────────
    top_authors = stats["by_author"][:10]
    max_commits = top_authors[0][1] if top_authors else 1
    author_rows = "".join(
        _horizontal_bar(a, v, max_commits, i + 1)
        for i, (a, v) in enumerate(top_authors)
    )

    # ── Files ────────────────────────────────────────────────────────────────
    top_files = stats["top_files"][:12]
    max_file = top_files[0][1] if top_files else 1
    file_rows = "".join(
        _horizontal_bar(f, v, max_file, i + 1)
        for i, (f, v) in enumerate(top_files)
    )

    # ── Recent commits ───────────────────────────────────────────────────────
    recent_rows = ""
    for c in stats["recent_commits"]:
        ds = c["date"].strftime("%Y-%m-%d %H:%M")
        recent_rows += f"""
        <tr>
          <td class="sha">{c['sha']}</td>
          <td>{html.escape(c['author'])}</td>
          <td class="subject">{html.escape(c['subject'][:72])}</td>
          <td class="date-cell">{ds}</td>
        </tr>"""

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GitPulse — {html.escape(repo_name)}</title>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --surface2: #21262d;
    --border: #30363d; --text: #e6edf3; --muted: #8b949e;
    --accent: #238636; --accent2: #1f6feb; --accent3: #a371f7;
    --hm0: #161b22; --hm1: #0e4429; --hm2: #006d32;
    --hm3: #26a641; --hm4: #39d353;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    font-size: 14px; line-height: 1.6;
  }}
  a {{ color: var(--accent2); text-decoration: none; }}

  /* ── Layout ── */
  .header {{
    background: var(--surface); border-bottom: 1px solid var(--border);
    padding: 20px 32px; display: flex; align-items: center; gap: 16px;
  }}
  .header h1 {{ font-size: 22px; font-weight: 600; }}
  .header .subtitle {{ color: var(--muted); font-size: 13px; }}
  .logo {{ font-size: 28px; }}
  .main {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px; }}
  .grid-4 {{
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-bottom: 24px;
  }}
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
  @media (max-width: 700px) {{
    .grid-4 {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-2 {{ grid-template-columns: 1fr; }}
  }}

  /* ── Cards ── */
  .card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px;
  }}
  .card-title {{
    font-size: 12px; text-transform: uppercase; letter-spacing: .08em;
    color: var(--muted); margin-bottom: 12px; font-weight: 600;
  }}
  .stat-val {{ font-size: 32px; font-weight: 700; line-height: 1; }}
  .stat-sub {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
  .stat-val.green {{ color: var(--accent3); }}
  .stat-val.blue {{ color: var(--accent2); }}

  /* ── Heatmap colors ── */
  .hm-0 {{ fill: var(--hm0); }} .hm-1 {{ fill: var(--hm1); }}
  .hm-2 {{ fill: var(--hm2); }} .hm-3 {{ fill: var(--hm3); }}
  .hm-4 {{ fill: var(--hm4); }}

  /* ── Horizontal bars ── */
  .hbar-row {{
    display: flex; align-items: center; gap: 8px;
    padding: 5px 0; border-bottom: 1px solid var(--border);
  }}
  .hbar-row:last-child {{ border-bottom: none; }}
  .hbar-rank {{ font-size: 11px; color: var(--muted); width: 22px; flex-shrink: 0; }}
  .hbar-label {{
    width: 160px; flex-shrink: 0; font-size: 12px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }}
  .hbar-track {{
    flex: 1; background: var(--surface2); border-radius: 3px; height: 8px;
  }}
  .hbar-fill {{ height: 100%; border-radius: 3px; background: var(--accent2); }}
  .hbar-val {{ font-size: 12px; color: var(--muted); width: 36px; text-align: right; flex-shrink: 0; }}

  /* ── Commits table ── */
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{
    text-align: left; color: var(--muted); font-weight: 500;
    padding: 8px 12px; border-bottom: 1px solid var(--border);
    font-size: 11px; text-transform: uppercase; letter-spacing: .06em;
  }}
  td {{ padding: 8px 12px; border-bottom: 1px solid var(--surface2); }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: var(--surface2); }}
  .sha {{ font-family: monospace; font-size: 12px; color: var(--accent3); }}
  .subject {{ max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .date-cell {{ color: var(--muted); font-size: 12px; white-space: nowrap; }}

  /* ── Footer ── */
  .footer {{
    text-align: center; color: var(--muted); font-size: 12px;
    padding: 24px; border-top: 1px solid var(--border); margin-top: 32px;
  }}
  .badge {{
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 20px; padding: 3px 10px; font-size: 11px; color: var(--muted);
  }}
</style>
</head>
<body>

<header class="header">
  <span class="logo">⚡</span>
  <div>
    <h1>GitPulse — {html.escape(repo_name)}</h1>
    <div class="subtitle">
      {start_dt.strftime("%b %d, %Y")} → {end_dt.strftime("%b %d, %Y")}
      &nbsp;·&nbsp; {span_days:,} days &nbsp;·&nbsp;
      Generated {generated}
    </div>
  </div>
</header>

<main class="main">

  <!-- ── Stat tiles ── -->
  <div class="grid-4">
    <div class="card">
      <div class="card-title">Total Commits</div>
      <div class="stat-val">{stats['total_commits']:,}</div>
      <div class="stat-sub">{stats['total_commits'] / max(span_days, 1):.2f} / day avg</div>
    </div>
    <div class="card">
      <div class="card-title">Contributors</div>
      <div class="stat-val blue">{stats['total_authors']:,}</div>
      <div class="stat-sub">unique authors</div>
    </div>
    <div class="card">
      <div class="card-title">Active Days</div>
      <div class="stat-val green">{len(stats['by_date']):,}</div>
      <div class="stat-sub">{len(stats['by_date']) / max(span_days, 1) * 100:.1f}% of tracked days</div>
    </div>
    <div class="card">
      <div class="card-title">Files Touched</div>
      <div class="stat-val">{sum(v for _, v in stats['top_files']):,}</div>
      <div class="stat-sub">total file edits</div>
    </div>
  </div>

  <!-- ── Heatmap ── -->
  <div class="card" style="margin-bottom:24px;overflow-x:auto">
    <div class="card-title">Commit Activity — Last 52 Weeks</div>
    {heatmap}
  </div>

  <!-- ── DOW + Hour ── -->
  <div class="grid-2">
    <div class="card">
      <div class="card-title">Commits by Day of Week</div>
      {dow_svg}
    </div>
    <div class="card">
      <div class="card-title">Commits by Hour (UTC)</div>
      {hour_svg}
    </div>
  </div>

  <!-- ── Authors + Files ── -->
  <div class="grid-2">
    <div class="card">
      <div class="card-title">Top Contributors</div>
      {author_rows or '<p style="color:var(--muted);font-size:13px">No data</p>'}
    </div>
    <div class="card">
      <div class="card-title">Hottest Files</div>
      {file_rows or '<p style="color:var(--muted);font-size:13px">No data</p>'}
    </div>
  </div>

  <!-- ── Recent Commits ── -->
  <div class="card">
    <div class="card-title">Recent Commits</div>
    <div style="overflow-x:auto">
      <table>
        <thead>
          <tr><th>SHA</th><th>Author</th><th>Message</th><th>Date (UTC)</th></tr>
        </thead>
        <tbody>{recent_rows}</tbody>
      </table>
    </div>
  </div>

</main>

<footer class="footer">
  <span class="badge">⚡ GitPulse</span>
  &nbsp; Open-source git analytics · Generated {generated}
</footer>

</body>
</html>"""
