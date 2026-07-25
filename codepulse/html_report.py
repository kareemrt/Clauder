"""Self-contained HTML report generator for CodePulse."""

from datetime import datetime, timezone, timedelta
from .metrics import RepoMetrics
import json

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def build_heatmap_data(heatmap: dict[str, int]) -> list[dict]:
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(weeks=52)
    start = start - timedelta(days=start.weekday())
    data = []
    current = start
    for _ in range(53 * 7):
        date_str = current.strftime("%Y-%m-%d")
        data.append({"date": date_str, "count": heatmap.get(date_str, 0)})
        current += timedelta(days=1)
    return data


def generate_html(m: RepoMetrics, output_path: str) -> None:
    age = max((m.last_commit - m.first_commit).days, 1)
    velocity = round(m.total_commits / (age / 30), 1)

    heatmap_data = build_heatmap_data(m.heatmap)
    heatmap_json = json.dumps(heatmap_data)
    hour_data = json.dumps([m.commits_by_hour.get(h, 0) for h in range(24)])
    weekday_data = json.dumps([m.commits_by_weekday.get(d, 0) for d in range(7)])

    lang_data = sorted(m.language_lines.items(), key=lambda x: x[1], reverse=True)[:10]
    lang_labels = json.dumps([ext for ext, _ in lang_data])
    lang_values = json.dumps([lines for _, lines in lang_data])

    contrib_rows = ""
    medals = ["🥇", "🥈", "🥉"]
    for i, c in enumerate(m.contributors[:10]):
        medal = medals[i] if i < 3 else str(i + 1)
        contrib_rows += f"""
        <tr>
            <td>{medal}</td>
            <td>{c.name}</td>
            <td class="num">{c.commits}</td>
            <td class="num">{c.files_touched}</td>
            <td class="dim">{c.first_commit.strftime('%Y-%m-%d')}</td>
            <td class="dim">{c.last_commit.strftime('%Y-%m-%d')}</td>
        </tr>"""

    hot_rows = ""
    max_changes = m.hot_files[0][1] if m.hot_files else 1
    for path, count in m.hot_files[:15]:
        pct = int((count / max_changes) * 100)
        hot_rows += f"""
        <tr>
            <td class="filepath">{path}</td>
            <td class="num">{count}</td>
            <td><div class="heat-bar" style="width:{pct}%"></div></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CodePulse — {m.repo_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #c9d1d9; --muted: #8b949e; --green: #39d353;
    --green-dark: #006d32; --cyan: #58a6ff; --yellow: #e3b341;
    --red: #f85149; --purple: #bc8cff; --accent: #1f6feb;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: var(--bg); color: var(--text); min-height: 100vh; }}
  .header {{ background: var(--surface); border-bottom: 1px solid var(--border);
             padding: 24px 40px; display: flex; align-items: center; gap: 12px; }}
  .header .logo {{ font-size: 28px; font-weight: 800; color: var(--green); }}
  .header .repo {{ font-size: 18px; color: var(--muted); }}
  .header .badge {{ background: var(--green-dark); color: var(--green);
                    border-radius: 20px; padding: 2px 12px; font-size: 12px; font-weight: 600; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 32px 24px; }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px; margin-bottom: 40px; }}
  .card {{ background: var(--surface); border: 1px solid var(--border);
           border-radius: 10px; padding: 20px 24px; text-align: center; }}
  .card .value {{ font-size: 36px; font-weight: 800; }}
  .card .label {{ font-size: 13px; color: var(--muted); margin-top: 4px; }}
  .card.green .value {{ color: var(--green); }}
  .card.cyan .value {{ color: var(--cyan); }}
  .card.yellow .value {{ color: var(--yellow); }}
  .card.purple .value {{ color: var(--purple); }}
  .card.red .value {{ color: var(--red); }}
  .section {{ margin-bottom: 40px; }}
  .section-title {{ font-size: 18px; font-weight: 700; color: var(--text);
                    margin-bottom: 16px; padding-bottom: 8px;
                    border-bottom: 1px solid var(--border); }}
  .charts-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                  gap: 20px; }}
  .chart-box {{ background: var(--surface); border: 1px solid var(--border);
                border-radius: 10px; padding: 20px; }}
  .chart-box h3 {{ font-size: 14px; color: var(--muted); margin-bottom: 16px; font-weight: 600; }}
  canvas {{ max-height: 250px; }}
  .heatmap-wrap {{ background: var(--surface); border: 1px solid var(--border);
                   border-radius: 10px; padding: 24px; overflow-x: auto; }}
  #heatmap {{ display: flex; gap: 3px; }}
  .hm-col {{ display: flex; flex-direction: column; gap: 3px; }}
  .hm-cell {{ width: 11px; height: 11px; border-radius: 2px; background: #161b22;
              border: 1px solid rgba(255,255,255,0.05); cursor: pointer;
              transition: opacity 0.15s; }}
  .hm-cell:hover {{ opacity: 0.8; }}
  .hm-legend {{ display: flex; align-items: center; gap: 6px; margin-top: 12px;
                font-size: 12px; color: var(--muted); }}
  .hm-legend-cell {{ width: 11px; height: 11px; border-radius: 2px; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--surface);
           border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }}
  th {{ text-align: left; padding: 12px 16px; font-size: 13px; color: var(--muted);
        background: var(--bg); border-bottom: 1px solid var(--border); font-weight: 600; }}
  td {{ padding: 10px 16px; font-size: 14px; border-bottom: 1px solid var(--border); }}
  tr:last-child td {{ border-bottom: none; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; color: var(--green); font-weight: 600; }}
  .dim {{ color: var(--muted); }}
  .filepath {{ font-family: monospace; font-size: 13px; }}
  .heat-bar {{ height: 8px; background: linear-gradient(90deg, var(--yellow), var(--red));
               border-radius: 4px; min-width: 4px; }}
  .footer {{ text-align: center; color: var(--muted); font-size: 13px; padding: 32px;
             border-top: 1px solid var(--border); margin-top: 40px; }}
  .tooltip-box {{ position: fixed; background: var(--surface); border: 1px solid var(--border);
                  border-radius: 6px; padding: 6px 10px; font-size: 12px; pointer-events: none;
                  display: none; z-index: 100; }}
</style>
</head>
<body>
<div class="header">
  <span class="logo">⚡ CodePulse</span>
  <span class="repo">/ {m.repo_name}</span>
  <span class="badge">v1.0</span>
</div>
<div class="container">

  <div class="cards">
    <div class="card green"><div class="value">{m.total_commits:,}</div><div class="label">Total Commits</div></div>
    <div class="card cyan"><div class="value">{m.total_contributors}</div><div class="label">Contributors</div></div>
    <div class="card yellow"><div class="value">{m.active_days}</div><div class="label">Active Days</div></div>
    <div class="card purple"><div class="value">{m.total_files_changed:,}</div><div class="label">File Changes</div></div>
    <div class="card red"><div class="value">{velocity}</div><div class="label">Commits / Month</div></div>
  </div>

  <div class="section">
    <div class="section-title">Commit Activity — Last 52 Weeks</div>
    <div class="heatmap-wrap">
      <div id="heatmap"></div>
      <div class="hm-legend">
        Less
        <div class="hm-legend-cell" style="background:#161b22"></div>
        <div class="hm-legend-cell" style="background:#0e4429"></div>
        <div class="hm-legend-cell" style="background:#006d32"></div>
        <div class="hm-legend-cell" style="background:#26a641"></div>
        <div class="hm-legend-cell" style="background:#39d353"></div>
        More
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Top Contributors</div>
    <table>
      <thead><tr><th>#</th><th>Author</th><th style="text-align:right">Commits</th>
        <th style="text-align:right">Files Touched</th><th>First</th><th>Last</th></tr></thead>
      <tbody>{contrib_rows}</tbody>
    </table>
  </div>

  <div class="section">
    <div class="section-title">Commit Patterns & Languages</div>
    <div class="charts-grid">
      <div class="chart-box"><h3>By Hour of Day</h3><canvas id="hourChart"></canvas></div>
      <div class="chart-box"><h3>By Day of Week</h3><canvas id="weekdayChart"></canvas></div>
      <div class="chart-box"><h3>Language Distribution</h3><canvas id="langChart"></canvas></div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Hottest Files</div>
    <table>
      <thead><tr><th>File</th><th style="text-align:right">Changes</th><th>Heat</th></tr></thead>
      <tbody>{hot_rows}</tbody>
    </table>
  </div>

</div>
<div class="footer">
  Generated by <strong>CodePulse</strong> &middot;
  {m.first_commit.strftime('%b %Y')} – {m.last_commit.strftime('%b %Y')}
</div>

<div class="tooltip-box" id="tooltip"></div>

<script>
// --- Heatmap ---
const heatData = {heatmap_json};
const COLORS = ['#161b22','#0e4429','#006d32','#26a641','#39d353'];
const maxCount = Math.max(...heatData.map(d => d.count), 1);
function shade(c) {{
  if (!c) return 0;
  const r = c / maxCount;
  return Math.max(1, Math.min(4, Math.ceil(r * 4)));
}}
const hm = document.getElementById('heatmap');
const tooltip = document.getElementById('tooltip');
// Build 7-row columns
const weeks = [];
for (let i = 0; i < 53; i++) {{
  const col = document.createElement('div');
  col.className = 'hm-col';
  for (let d = 0; d < 7; d++) {{
    const idx = i * 7 + d;
    const cell = document.createElement('div');
    cell.className = 'hm-cell';
    if (idx < heatData.length) {{
      const entry = heatData[idx];
      cell.style.background = COLORS[shade(entry.count)];
      cell.addEventListener('mousemove', (e) => {{
        tooltip.style.display = 'block';
        tooltip.style.left = (e.clientX + 12) + 'px';
        tooltip.style.top = (e.clientY - 30) + 'px';
        tooltip.textContent = entry.date + ': ' + entry.count + ' commit' + (entry.count !== 1 ? 's' : '');
      }});
      cell.addEventListener('mouseleave', () => {{ tooltip.style.display = 'none'; }});
    }}
    col.appendChild(cell);
  }}
  hm.appendChild(col);
}}

// --- Charts ---
const chartDefaults = {{
  plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{}} }} }},
  scales: {{
    x: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#8b949e' }} }},
    y: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#8b949e' }} }},
  }},
  animation: false,
}};

const hourData = {hour_data};
new Chart(document.getElementById('hourChart'), {{
  type: 'bar',
  data: {{
    labels: Array.from({{length:24}}, (_, i) => i + 'h'),
    datasets: [{{ data: hourData, backgroundColor: hourData.map((_, i) =>
      i >= 6 && i < 12 ? '#e3b341' : i >= 12 && i < 18 ? '#58a6ff' : i >= 18 && i < 22 ? '#bc8cff' : '#6e7681'
    ), borderRadius: 3 }}],
  }},
  options: chartDefaults,
}});

const weekdayData = {weekday_data};
new Chart(document.getElementById('weekdayChart'), {{
  type: 'bar',
  data: {{
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [{{ data: weekdayData,
      backgroundColor: weekdayData.map((_, i) => i < 5 ? '#58a6ff' : '#e3b341'), borderRadius: 3 }}],
  }},
  options: chartDefaults,
}});

const langLabels = {lang_labels};
const langValues = {lang_values};
const langColors = ['#39d353','#58a6ff','#e3b341','#bc8cff','#f85149','#79c0ff','#ffa657','#7ee787','#d2a8ff','#ff7b72'];
new Chart(document.getElementById('langChart'), {{
  type: 'doughnut',
  data: {{
    labels: langLabels,
    datasets: [{{ data: langValues, backgroundColor: langColors, borderColor: '#161b22', borderWidth: 2 }}],
  }},
  options: {{
    animation: false,
    plugins: {{
      legend: {{ position: 'right', labels: {{ color: '#c9d1d9', font: {{ size: 12 }} }} }},
    }},
  }},
}});
</script>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html)
