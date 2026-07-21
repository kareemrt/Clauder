"""HTML report generator for GitPulse analysis."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from .analyzer import RepoStats


def generate_html_report(stats: RepoStats, output_path: str = "gitpulse-report.html") -> str:
    """Generate a self-contained HTML report and return the path."""
    html = _build_html(stats)
    path = Path(output_path)
    path.write_text(html, encoding="utf-8")
    return str(path.resolve())


def _build_html(stats: RepoStats) -> str:
    calendar_json = _build_calendar_json(stats)
    hourly_json = json.dumps([stats.commits_by_hour.get(h, 0) for h in range(24)])
    weekday_json = json.dumps([stats.commits_by_weekday.get(d, 0) for d in range(7)])
    monthly_labels = json.dumps(list(stats.commits_by_month.keys())[-24:])
    monthly_data = json.dumps(list(stats.commits_by_month.values())[-24:])

    contributors_rows = ""
    for i, c in enumerate(stats.contributors[:20], 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"#{i}")
        contributors_rows += f"""
        <tr>
          <td>{medal}</td>
          <td><strong>{_esc(c.name)}</strong><br><small class="muted">{_esc(c.email)}</small></td>
          <td class="num">{c.commits:,}</td>
          <td class="num green">+{c.additions:,}</td>
          <td class="num red">-{c.deletions:,}</td>
        </tr>"""

    hotspot_rows = ""
    max_churn = stats.file_hotspots[0].change_count if stats.file_hotspots else 1
    for hs in stats.file_hotspots[:15]:
        pct = hs.change_count / max_churn * 100
        hotspot_rows += f"""
        <tr>
          <td class="mono">{_esc(hs.path)}</td>
          <td class="num">{hs.change_count:,}</td>
          <td><div class="bar-wrap"><div class="bar-fill" style="width:{pct:.0f}%"></div></div></td>
        </tr>"""

    word_cloud_html = ""
    max_wc = stats.top_words[0][1] if stats.top_words else 1
    colors = ["#ef4444","#f97316","#eab308","#22c55e","#06b6d4",
               "#3b82f6","#8b5cf6","#ec4899","#14b8a6","#f59e0b"]
    for i, (word, count) in enumerate(stats.top_words):
        size = 0.8 + (count / max_wc) * 2.2
        color = colors[i % len(colors)]
        word_cloud_html += f'<span class="wc-word" style="font-size:{size:.1f}rem;color:{color}">{_esc(word)}</span> '

    first = stats.first_commit.strftime("%b %d, %Y") if stats.first_commit else "—"
    last = stats.last_commit.strftime("%b %d, %Y") if stats.last_commit else "—"
    freq = f"{stats.commit_frequency:.2f}" if stats.commit_frequency else "0"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitPulse — {_esc(stats.repo_name)}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #7d8590; --accent: #58a6ff;
    --green: #3fb950; --red: #f85149; --yellow: #d29922;
    --purple: #bc8cff; --orange: #ffa657;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.6; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; }}
  header {{ text-align: center; padding: 3rem 0 2rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }}
  header h1 {{ font-size: 3rem; background: linear-gradient(135deg, #58a6ff, #bc8cff, #3fb950); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
  header .subtitle {{ color: var(--muted); margin-top: .5rem; font-size: 1.1rem; }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; margin: 2rem 0; }}
  .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; text-align: center; }}
  .card .icon {{ font-size: 1.8rem; margin-bottom: .5rem; }}
  .card .val {{ font-size: 1.5rem; font-weight: 700; color: var(--accent); }}
  .card .lbl {{ font-size: .78rem; color: var(--muted); margin-top: .25rem; text-transform: uppercase; letter-spacing: .05em; }}
  section {{ margin: 2.5rem 0; }}
  section h2 {{ font-size: 1.3rem; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: .5rem; margin-bottom: 1.5rem; }}
  .chart-wrap {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }}
  .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
  @media(max-width:720px) {{ .charts-grid {{ grid-template-columns: 1fr; }} }}
  table {{ width: 100%; border-collapse: collapse; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
  th {{ background: #1c2128; color: var(--muted); text-transform: uppercase; font-size: .75rem; letter-spacing: .08em; padding: .75rem 1rem; text-align: left; }}
  td {{ padding: .7rem 1rem; border-top: 1px solid var(--border); font-size: .9rem; }}
  tr:hover td {{ background: #1c2128; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .green {{ color: var(--green); }}
  .red {{ color: var(--red); }}
  .muted {{ color: var(--muted); }}
  .mono {{ font-family: ui-monospace, monospace; font-size: .85rem; }}
  .bar-wrap {{ background: #21262d; border-radius: 4px; height: 10px; overflow: hidden; }}
  .bar-fill {{ background: linear-gradient(90deg, var(--accent), var(--purple)); height: 100%; border-radius: 4px; transition: width .3s; }}
  .word-cloud {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; text-align: center; line-height: 2.5; }}
  .wc-word {{ display: inline-block; margin: .2rem .4rem; font-weight: 700; transition: transform .2s; cursor: default; }}
  .wc-word:hover {{ transform: scale(1.15); }}
  .calendar-wrap {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; overflow-x: auto; }}
  .cal-grid {{ display: inline-grid; grid-template-rows: repeat(7, 1fr); grid-auto-flow: column; gap: 3px; }}
  .cal-cell {{ width: 14px; height: 14px; border-radius: 3px; }}
  footer {{ text-align: center; padding: 2rem 0; color: var(--muted); font-size: .85rem; border-top: 1px solid var(--border); margin-top: 3rem; }}
  footer a {{ color: var(--accent); text-decoration: none; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>⚡ GitPulse</h1>
    <div class="subtitle">Analytics Report for <strong style="color:var(--text)">{_esc(stats.repo_name)}</strong></div>
    <div class="subtitle" style="margin-top:.3rem;font-size:.9rem">{first} — {last} &nbsp;·&nbsp; {stats.total_commits:,} commits &nbsp;·&nbsp; {len(stats.contributors)} contributors</div>
  </header>

  <div class="cards">
    {_card("🔖", f"{stats.total_commits:,}", "Total Commits")}
    {_card("👥", f"{len(stats.contributors):,}", "Contributors")}
    {_card("📅", f"{stats.active_days:,}", "Active Days")}
    {_card("⚡", f"{freq}/day", "Commit Freq")}
    {_card("🌿", f"{stats.total_branches:,}", "Branches")}
    {_card("🏷️", f"{stats.total_tags:,}", "Tags")}
    {_card("⏳", f"{stats.age_days:,}d", "Repo Age")}
    {_card("🏆", f"{stats.longest_streak}d", "Longest Streak")}
  </div>

  <section>
    <h2>📅 Commit Activity Calendar</h2>
    <div class="calendar-wrap">
      <div class="cal-grid" id="cal-grid"></div>
      <div style="margin-top:.75rem;color:var(--muted);font-size:.78rem">
        Less &nbsp; <span style="display:inline-flex;gap:3px">
          <span style="width:14px;height:14px;background:#161b22;border:1px solid #30363d;border-radius:3px;display:inline-block"></span>
          <span style="width:14px;height:14px;background:#0e4429;border-radius:3px;display:inline-block"></span>
          <span style="width:14px;height:14px;background:#006d32;border-radius:3px;display:inline-block"></span>
          <span style="width:14px;height:14px;background:#26a641;border-radius:3px;display:inline-block"></span>
          <span style="width:14px;height:14px;background:#39d353;border-radius:3px;display:inline-block"></span>
        </span> &nbsp; More
      </div>
    </div>
  </section>

  <div class="charts-grid">
    <section>
      <h2>⏰ Activity by Hour</h2>
      <div class="chart-wrap"><canvas id="hourChart" height="200"></canvas></div>
    </section>
    <section>
      <h2>📆 Activity by Weekday</h2>
      <div class="chart-wrap"><canvas id="weekdayChart" height="200"></canvas></div>
    </section>
  </div>

  <section>
    <h2>📈 Monthly Commit History</h2>
    <div class="chart-wrap"><canvas id="monthChart" height="120"></canvas></div>
  </section>

  <section>
    <h2>👥 Top Contributors</h2>
    <table>
      <thead><tr><th>#</th><th>Author</th><th class="num">Commits</th><th class="num">Additions</th><th class="num">Deletions</th></tr></thead>
      <tbody>{contributors_rows}</tbody>
    </table>
  </section>

  <section>
    <h2>🔥 File Hotspots</h2>
    <table>
      <thead><tr><th>File</th><th class="num">Changes</th><th>Churn</th></tr></thead>
      <tbody>{hotspot_rows}</tbody>
    </table>
  </section>

  <section>
    <h2>💬 Commit Message Keywords</h2>
    <div class="word-cloud">{word_cloud_html}</div>
  </section>

  <footer>
    Generated by <a href="https://github.com/kareemrt/clauder">GitPulse</a> &nbsp;·&nbsp;
    Terminal Git Analytics Dashboard
  </footer>
</div>

<script>
const calData = {calendar_json};
const hourlyData = {hourly_json};
const weekdayData = {weekday_json};
const monthlyLabels = {monthly_labels};
const monthlyData = {monthly_data};

// Calendar
(function() {{
  const grid = document.getElementById('cal-grid');
  const today = new Date();
  const start = new Date(today);
  start.setDate(today.getDate() - 364);
  start.setDate(start.getDate() - start.getDay()); // align to Sunday
  const colors = ['#161b22','#0e4429','#006d32','#26a641','#39d353'];
  const maxVal = Math.max(...Object.values(calData), 1);
  for (let d = new Date(start); d <= today; d.setDate(d.getDate() + 1)) {{
    const key = d.toISOString().slice(0,10);
    const count = calData[key] || 0;
    const idx = count === 0 ? 0 : Math.min(4, Math.floor(count/maxVal*4)+1);
    const cell = document.createElement('div');
    cell.className = 'cal-cell';
    cell.style.background = colors[idx];
    cell.title = `${{key}}: ${{count}} commit${{count!==1?'s':''}}`;
    grid.appendChild(cell);
  }}
}})();

// Chart defaults
const chartDefaults = {{
  responsive: true,
  plugins: {{ legend: {{ display: false }} }},
  scales: {{
    x: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#7d8590' }} }},
    y: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#7d8590' }}, beginAtZero: true }}
  }}
}};

new Chart(document.getElementById('hourChart'), {{
  type: 'bar',
  data: {{
    labels: Array.from({{length:24}}, (_,i) => `${{String(i).padStart(2,'0')}}:00`),
    datasets: [{{ data: hourlyData, backgroundColor: hourlyData.map((_,i) => i>=9&&i<=17?'#58a6ff':'#3b82f6'), borderRadius: 4 }}]
  }},
  options: {{ ...chartDefaults }}
}});

new Chart(document.getElementById('weekdayChart'), {{
  type: 'bar',
  data: {{
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [{{ data: weekdayData, backgroundColor: weekdayData.map((_,i) => i>=5?'#bc8cff':'#58a6ff'), borderRadius: 4 }}]
  }},
  options: {{ ...chartDefaults }}
}});

new Chart(document.getElementById('monthChart'), {{
  type: 'line',
  data: {{
    labels: monthlyLabels,
    datasets: [{{ data: monthlyData, borderColor: '#58a6ff', backgroundColor: 'rgba(88,166,255,.15)', fill: true, tension: .4, pointRadius: 3, pointBackgroundColor: '#58a6ff' }}]
  }},
  options: {{ ...chartDefaults }}
}});
</script>
</body>
</html>"""


def _card(icon: str, val: str, lbl: str) -> str:
    return f'<div class="card"><div class="icon">{icon}</div><div class="val">{_esc(val)}</div><div class="lbl">{_esc(lbl)}</div></div>'


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _build_calendar_json(stats: RepoStats) -> str:
    return json.dumps(stats.calendar_data)
