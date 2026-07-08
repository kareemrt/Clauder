"""HTML report generator — produces a standalone, self-contained HTML file."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pulsar — {repo_name}</title>
<style>
  :root {{
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --red: #f85149;
    --yellow: #d29922;
    --purple: #bc8cff;
    --orange: #db6d28;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'SF Mono', 'Fira Code', monospace;
    padding: 2rem;
    line-height: 1.6;
  }}
  .header {{
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
  }}
  .logo {{
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: 0.3rem;
    background: linear-gradient(135deg, #58a6ff, #bc8cff, #f78166);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .subtitle {{ color: var(--muted); margin-top: 0.5rem; font-size: 0.9rem; }}
  .meta {{ color: var(--accent); margin-top: 1rem; font-size: 1.1rem; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }}
  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
  }}
  .card h3 {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-bottom: 0.75rem;
  }}
  .stat-value {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--accent);
  }}
  .stat-sub {{ color: var(--muted); font-size: 0.8rem; margin-top: 0.25rem; }}
  .chart-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }}
  .chart-card h2 {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
  }}
  canvas {{ max-width: 100%; }}
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }}
  @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
  .file-list {{ list-style: none; }}
  .file-list li {{
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.82rem;
  }}
  .file-list li:last-child {{ border-bottom: none; }}
  .file-path {{ color: var(--text); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .file-count {{ color: var(--accent); margin-left: 1rem; flex-shrink: 0; }}
  .word-cloud {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }}
  .word-tag {{
    background: rgba(88,166,255,0.1);
    border: 1px solid rgba(88,166,255,0.3);
    border-radius: 4px;
    padding: 0.2rem 0.6rem;
    color: var(--accent);
    font-size: 0.78rem;
  }}
  .footer {{
    text-align: center;
    color: var(--muted);
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
  }}
  .footer a {{ color: var(--accent); text-decoration: none; }}
</style>
</head>
<body>
<div class="header">
  <div class="logo">⚡ PULSAR</div>
  <div class="subtitle">Git Repository Heartbeat Visualizer</div>
  <div class="meta">{repo_name} · {branch} · last {days} days</div>
</div>

<div class="grid">
  <div class="card">
    <h3>Total Commits</h3>
    <div class="stat-value">{total_commits}</div>
    <div class="stat-sub">all time</div>
  </div>
  <div class="card">
    <h3>Recent Commits</h3>
    <div class="stat-value">{period_commits}</div>
    <div class="stat-sub">last {days} days</div>
  </div>
  <div class="card">
    <h3>Lines Added</h3>
    <div class="stat-value" style="color:var(--green)">+{total_insertions}</div>
    <div class="stat-sub">in period</div>
  </div>
  <div class="card">
    <h3>Lines Removed</h3>
    <div class="stat-value" style="color:var(--red)">-{total_deletions}</div>
    <div class="stat-sub">in period</div>
  </div>
  <div class="card">
    <h3>Contributors</h3>
    <div class="stat-value" style="color:var(--yellow)">{contributor_count}</div>
    <div class="stat-sub">active in period</div>
  </div>
</div>

<div class="chart-card">
  <h2>⚡ Heartbeat — Daily Commit Activity</h2>
  <canvas id="heartbeatChart" height="100"></canvas>
</div>

<div class="two-col">
  <div class="chart-card">
    <h2>👥 Contributors</h2>
    <canvas id="contributorsChart"></canvas>
  </div>
  <div class="chart-card">
    <h2>🌐 Language Breakdown</h2>
    <canvas id="langChart"></canvas>
  </div>
</div>

<div class="chart-card">
  <h2>🔥 Activity Heatmap — Hour × Weekday</h2>
  <canvas id="heatmapChart" height="140"></canvas>
</div>

<div class="two-col">
  <div class="chart-card">
    <h2>📁 Hotspot Files</h2>
    <ul class="file-list">
      {file_list_html}
    </ul>
  </div>
  <div class="chart-card">
    <h2>💬 Commit Message Words</h2>
    <div class="word-cloud">
      {word_cloud_html}
    </div>
  </div>
</div>

<div class="footer">
  Generated by <a href="https://github.com/kareemrt/clauder">Pulsar</a> on {generated_at}
</div>

<script>
const STATS = {stats_json};

// colour palette
const PALETTE = [
  '#58a6ff','#bc8cff','#3fb950','#f78166','#d29922',
  '#79c0ff','#a5d6ff','#56d364','#ffa198','#e3b341'
];

// ── Heartbeat chart ──────────────────────────────────────────────────────────
(function() {{
  const today = new Date();
  const labels = [], data = [];
  for (let i = STATS.days - 1; i >= 0; i--) {{
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const key = d.toISOString().slice(0, 10);
    labels.push(i % 7 === 0 ? key : '');
    data.push(STATS.daily_counts[key] || 0);
  }}
  const ctx = document.getElementById('heartbeatChart').getContext('2d');
  new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels,
      datasets: [{{
        data,
        backgroundColor: data.map(v => v > 0 ? 'rgba(88,166,255,0.7)' : 'rgba(88,166,255,0.1)'),
        borderColor: data.map(v => v > 0 ? '#58a6ff' : 'transparent'),
        borderWidth: 1,
        borderRadius: 2,
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{
        title: (items) => labels[items[0].dataIndex] || '',
        label: (item) => item.raw + ' commit' + (item.raw !== 1 ? 's' : ''),
      }} }} }},
      scales: {{
        x: {{ ticks: {{ color: '#8b949e', font: {{ size: 9 }} }}, grid: {{ color: '#30363d' }} }},
        y: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#21262d' }}, beginAtZero: true }},
      }}
    }}
  }});
}})();

// ── Contributors doughnut ─────────────────────────────────────────────────────
(function() {{
  const top = STATS.contributors.slice(0, 8);
  const ctx = document.getElementById('contributorsChart').getContext('2d');
  new Chart(ctx, {{
    type: 'doughnut',
    data: {{
      labels: top.map(c => c.name),
      datasets: [{{ data: top.map(c => c.commits), backgroundColor: PALETTE, borderWidth: 2, borderColor: '#161b22' }}]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ position: 'right', labels: {{ color: '#c9d1d9', font: {{ size: 11 }} }} }},
        tooltip: {{ callbacks: {{ label: (i) => ` ${{i.raw}} commits` }} }}
      }}
    }}
  }});
}})();

// ── Language doughnut ─────────────────────────────────────────────────────────
(function() {{
  const entries = Object.entries(STATS.lang_counts).sort((a,b) => b[1]-a[1]).slice(0, 8);
  const ctx = document.getElementById('langChart').getContext('2d');
  new Chart(ctx, {{
    type: 'doughnut',
    data: {{
      labels: entries.map(e => e[0]),
      datasets: [{{ data: entries.map(e => e[1]), backgroundColor: PALETTE, borderWidth: 2, borderColor: '#161b22' }}]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ position: 'right', labels: {{ color: '#c9d1d9', font: {{ size: 11 }} }} }},
        tooltip: {{ callbacks: {{ label: (i) => ` ${{i.raw}} files` }} }}
      }}
    }}
  }});
}})();

// ── Heatmap bar chart ─────────────────────────────────────────────────────────
(function() {{
  const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const hours = Array.from({{length: 24}}, (_, i) => `${{String(i).padStart(2,'0')}}:00`);
  // build per-hour datasets (one dataset per weekday)
  const datasets = days.map((day, wd) => ({{
    label: day,
    data: hours.map((_, hr) => STATS.hourly_matrix[`${{wd}},${{hr}}`] || 0),
    backgroundColor: PALETTE[wd],
    stack: 'stack',
  }}));
  const ctx = document.getElementById('heatmapChart').getContext('2d');
  new Chart(ctx, {{
    type: 'bar',
    data: {{ labels: hours, datasets }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ labels: {{ color: '#c9d1d9', font: {{ size: 10 }} }} }} }},
      scales: {{
        x: {{ stacked: true, ticks: {{ color: '#8b949e', font: {{ size: 9 }}, maxRotation: 45 }}, grid: {{ color: '#21262d' }} }},
        y: {{ stacked: true, ticks: {{ color: '#8b949e' }}, grid: {{ color: '#21262d' }}, beginAtZero: true }},
      }}
    }}
  }});
}})();
</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</body>
</html>
"""

# ── Note: the Chart.js script tag above loads from CDN.
# In offline environments users should download chart.js manually.


def generate(stats: dict, output_path: str) -> None:
    """Write a standalone HTML report to *output_path*."""
    file_list_html = "\n      ".join(
        f'<li><span class="file-path">{f["path"]}</span>'
        f'<span class="file-count">{f["changes"]}×</span></li>'
        for f in stats["top_files"][:12]
    )

    word_cloud_html = "\n      ".join(
        f'<span class="word-tag" style="font-size:{min(1.1, 0.75 + w["count"] * 0.04):.2f}rem">'
        f'{w["word"]}</span>'
        for w in stats["top_words"][:20]
    )

    stats_json = json.dumps({
        "days": stats["days"],
        "daily_counts": stats["daily_counts"],
        "contributors": stats["contributors"],
        "lang_counts": stats["lang_counts"],
        "hourly_matrix": stats["hourly_matrix"],
    })

    html = _HTML_TEMPLATE.format(
        repo_name=stats["repo_name"],
        branch=stats["branch"],
        days=stats["days"],
        total_commits=stats["total_commits"],
        period_commits=stats["period_commits"],
        total_insertions=stats["total_insertions"],
        total_deletions=stats["total_deletions"],
        contributor_count=len(stats["contributors"]),
        file_list_html=file_list_html,
        word_cloud_html=word_cloud_html,
        stats_json=stats_json,
        generated_at=datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    Path(output_path).write_text(html, encoding="utf-8")
