"""HTML report generator for GitPulse."""

from datetime import datetime
from collections import Counter


def generate_html_report(
    repo_name,
    stats,
    commits,
    churn,
    author_data,
    ext_counter,
    grid,
    weeks,
    grid_start,
    velocity_counts,
    velocity_labels,
    pairs,
):
    """Generate a standalone HTML report."""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Heatmap data
    max_heat = max(grid.values()) if grid else 1
    heatmap_rows = _build_heatmap_html(grid, weeks, grid_start, max_heat)

    # Language data for chart
    top_langs = ext_counter.most_common(8)
    lang_labels = [e for e, _ in top_langs]
    lang_values = [v for _, v in top_langs]

    # Author data
    top_authors = author_data[:10]
    author_labels = [a for a, _ in top_authors]
    author_values = [v for _, v in top_authors]

    # Top churn
    top_churn = churn.most_common(15)
    churn_labels = [f[-40:] for f, _ in top_churn]
    churn_values = [v for _, v in top_churn]

    # Velocity
    vel_labels = [d.strftime("%b %Y") for d in velocity_labels] if velocity_labels else []

    first = stats.get("first_commit", "").strftime("%Y-%m-%d") if stats.get("first_commit") else "N/A"
    last = stats.get("last_commit", "").strftime("%Y-%m-%d") if stats.get("last_commit") else "N/A"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitPulse — {repo_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #7d8590; --accent: #39d353;
    --cyan: #58a6ff; --yellow: #d29922; --red: #f85149;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 24px; }}
  h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 4px; }}
  h2 {{ font-size: 1.1rem; font-weight: 600; color: var(--muted); margin: 32px 0 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
  .subtitle {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 32px; }}
  .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 32px; }}
  .stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }}
  .stat-card .label {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }}
  .stat-card .value {{ font-size: 1.8rem; font-weight: 700; }}
  .stat-card .value.green {{ color: var(--accent); }}
  .stat-card .value.cyan {{ color: var(--cyan); }}
  .stat-card .value.yellow {{ color: var(--yellow); }}
  .stat-card .value.red {{ color: var(--red); }}
  .chart-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; margin-bottom: 24px; }}
  .chart-card canvas {{ max-height: 320px; }}
  .heatmap-container {{ overflow-x: auto; }}
  .heatmap {{ display: grid; grid-template-rows: repeat(7, 14px); grid-auto-flow: column; gap: 3px; margin-top: 12px; width: max-content; }}
  .heatmap-cell {{ width: 14px; height: 14px; border-radius: 2px; }}
  .heat-0 {{ background: #161b22; border: 1px solid #21262d; }}
  .heat-1 {{ background: #0e4429; }}
  .heat-2 {{ background: #006d32; }}
  .heat-3 {{ background: #26a641; }}
  .heat-4 {{ background: #39d353; }}
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media(max-width:768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
  .footer {{ margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.8rem; text-align: center; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; background: var(--surface); border: 1px solid var(--border); margin-right: 6px; }}
</style>
</head>
<body>
<h1>⚡ GitPulse</h1>
<p class="subtitle">
  <span class="badge">📁 {repo_name}</span>
  <span class="badge">🕐 Generated {now}</span>
  <span class="badge">📅 {first} → {last}</span>
</p>

<div class="stats-grid">
  <div class="stat-card"><div class="label">Total Commits</div><div class="value cyan">{stats.get("total_commits", 0):,}</div></div>
  <div class="stat-card"><div class="label">Contributors</div><div class="value green">{stats.get("total_authors", 0)}</div></div>
  <div class="stat-card"><div class="label">Files Tracked</div><div class="value yellow">{stats.get("total_files", 0):,}</div></div>
  <div class="stat-card"><div class="label">Repository Age</div><div class="value">{stats.get("age_days", 0)} days</div></div>
  <div class="stat-card"><div class="label">Lines Added</div><div class="value green">+{stats.get("lines_added", 0):,}</div></div>
  <div class="stat-card"><div class="label">Lines Removed</div><div class="value red">-{stats.get("lines_deleted", 0):,}</div></div>
  <div class="stat-card"><div class="label">Commits / Day</div><div class="value cyan">{stats.get("commits_per_day", 0)}</div></div>
</div>

<h2>📅 Contribution Heatmap</h2>
<div class="chart-card">
  <div class="heatmap-container">
    <div class="heatmap">{heatmap_rows}</div>
  </div>
</div>

<h2>📈 Commit Velocity</h2>
<div class="chart-card">
  <canvas id="velocityChart"></canvas>
</div>

<div class="two-col">
  <div>
    <h2>🌐 Languages</h2>
    <div class="chart-card"><canvas id="langChart"></canvas></div>
  </div>
  <div>
    <h2>👥 Authors</h2>
    <div class="chart-card"><canvas id="authorChart"></canvas></div>
  </div>
</div>

<h2>🔥 Most Changed Files</h2>
<div class="chart-card">
  <canvas id="churnChart"></canvas>
</div>

<div class="footer">Generated by <strong>GitPulse</strong> &mdash; Terminal Analytics Dashboard for Git Repositories</div>

<script>
const GRID_COLORS = ['#39d353','#26a641','#006d32','#58a6ff','#d29922','#f85149','#a371f7','#ff7b72'];
const opts = {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: '#e6edf3' }} }} }}, scales: {{ x: {{ ticks: {{ color: '#7d8590' }}, grid: {{ color: '#21262d' }} }}, y: {{ ticks: {{ color: '#7d8590' }}, grid: {{ color: '#21262d' }} }} }} }};

new Chart(document.getElementById('velocityChart'), {{
  type: 'line',
  data: {{
    labels: {vel_labels!r},
    datasets: [{{ label: 'Commits', data: {velocity_counts!r}, borderColor: '#58a6ff', backgroundColor: 'rgba(88,166,255,0.1)', fill: true, tension: 0.4, pointRadius: 2 }}]
  }},
  options: {{ ...opts, plugins: {{ ...opts.plugins, legend: {{ display: false }} }} }}
}});

new Chart(document.getElementById('langChart'), {{
  type: 'doughnut',
  data: {{
    labels: {lang_labels!r},
    datasets: [{{ data: {lang_values!r}, backgroundColor: GRID_COLORS, borderColor: '#0d1117', borderWidth: 2 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: '#e6edf3', font: {{ size: 11 }} }} }} }} }}
}});

new Chart(document.getElementById('authorChart'), {{
  type: 'bar',
  data: {{
    labels: {author_labels!r},
    datasets: [{{ label: 'Commits', data: {author_values!r}, backgroundColor: GRID_COLORS, borderRadius: 4 }}]
  }},
  options: {{ ...opts, indexAxis: 'y', plugins: {{ ...opts.plugins, legend: {{ display: false }} }} }}
}});

new Chart(document.getElementById('churnChart'), {{
  type: 'bar',
  data: {{
    labels: {churn_labels!r},
    datasets: [{{ label: 'Changes', data: {churn_values!r}, backgroundColor: 'rgba(242,139,53,0.7)', borderRadius: 4 }}]
  }},
  options: {{ ...opts, indexAxis: 'y', plugins: {{ ...opts.plugins, legend: {{ display: false }} }} }}
}});
</script>
</body>
</html>"""
    return html


def _build_heatmap_html(grid, weeks, grid_start, max_val):
    from datetime import timedelta

    def heat_class(val):
        if val == 0:
            return "heat-0"
        ratio = val / max_val
        if ratio < 0.25:
            return "heat-1"
        if ratio < 0.5:
            return "heat-2"
        if ratio < 0.75:
            return "heat-3"
        return "heat-4"

    cells = []
    for dow in range(7):
        for w in range(weeks):
            val = grid.get((w, dow), 0)
            dt = grid_start + timedelta(weeks=w, days=dow)
            title = f"{dt.strftime('%Y-%m-%d')}: {val} commit{'s' if val != 1 else ''}"
            cls = heat_class(val)
            cells.append(f'<div class="heatmap-cell {cls}" title="{title}"></div>')

    return "\n".join(cells)
