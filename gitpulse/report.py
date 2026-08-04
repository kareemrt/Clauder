"""HTML report generator — produces a self-contained analytics page."""
from datetime import date, timedelta
import json
import html


def _safe(s: str) -> str:
    return html.escape(str(s))


def generate_html(data: dict, output_path: str = "gitpulse_report.html") -> str:
    info = data["repo_info"]
    commits = data["commits"]
    authors = data["author_stats"]
    file_stats = data["file_stats"]
    lang_stats = data["language_breakdown"]
    calendar = data["calendar"]
    monthly = data["monthly_commits"]

    # ── Preprocess data ───────────────────────────────────────────────────────

    ranked_authors = sorted(authors.items(), key=lambda x: -x[1]["commits"])[:8]
    author_names = [a[0] for a in ranked_authors]
    author_counts = [a[1]["commits"] for a in ranked_authors]

    top_files = list(file_stats.items())[:8]
    file_labels = [f[0].split("/")[-1] for f in top_files]
    file_counts = [f[1] for f in top_files]

    top_langs = list(lang_stats.items())[:7]
    lang_labels = [l[0] for l in top_langs]
    lang_counts = [l[1] for l in top_langs]

    month_labels = [m[0] for m in monthly]
    month_counts = [m[1] for m in monthly]

    # Calendar: last 365 days
    today = date.today()
    start = today - timedelta(days=364)
    cal_entries = []
    current = start
    while current <= today:
        cal_entries.append(
            {"d": current.isoformat(), "c": calendar.get(current.isoformat(), 0)}
        )
        current += timedelta(days=1)

    total_commits = info.get("total_commits", len(commits))
    num_authors = len(authors)
    num_files = len(file_stats)
    days_active = 0
    if commits:
        first = min(c["date"] for c in commits)
        last = max(c["date"] for c in commits)
        days_active = (last - first).days + 1

    recent_commits = commits[:20]

    # ── JSON blobs for JS ─────────────────────────────────────────────────────

    j_authors = json.dumps({"labels": author_names, "values": author_counts})
    j_files = json.dumps({"labels": file_labels, "values": file_counts})
    j_langs = json.dumps({"labels": lang_labels, "values": lang_counts})
    j_monthly = json.dumps({"labels": month_labels, "values": month_counts})
    j_calendar = json.dumps(cal_entries)

    # ── Recent commits HTML ───────────────────────────────────────────────────

    commit_rows = ""
    for commit in recent_commits:
        h = _safe(commit["hash"][:7])
        d = _safe(commit["date"].strftime("%Y-%m-%d"))
        author = _safe(commit["author"][:30])
        msg = _safe(commit["message"][:80])
        commit_rows += f"""
        <tr>
          <td><span class="hash">{h}</span></td>
          <td>{d}</td>
          <td>{author}</td>
          <td>{msg}</td>
        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitPulse — {_safe(info["name"])}</title>
  <style>
    :root {{
      --bg:       #0d1117;
      --surface:  #161b22;
      --border:   #30363d;
      --text:     #e6edf3;
      --muted:    #8b949e;
      --accent:   #58a6ff;
      --green:    #3fb950;
      --yellow:   #d29922;
      --purple:   #bc8cff;
      --orange:   #f0883e;
      --green1:   #0e4429;
      --green2:   #006d32;
      --green3:   #26a641;
      --green4:   #39d353;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.6;
    }}
    a {{ color: var(--accent); text-decoration: none; }}

    /* ── Layout ── */
    header {{
      background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
      border-bottom: 1px solid var(--border);
      padding: 32px 48px 28px;
    }}
    header h1 {{
      font-size: 28px;
      font-weight: 700;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    header h1 .logo {{ color: var(--accent); }}
    header h1 .sep {{ color: var(--muted); font-weight: 300; }}
    header p {{ color: var(--muted); margin-top: 6px; font-size: 13px; }}
    .badge {{
      display: inline-block;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 2px 10px;
      font-size: 12px;
      color: var(--muted);
    }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 32px 32px 64px; }}

    /* ── Stat cards ── */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 32px;
    }}
    @media (max-width: 700px) {{ .stats-grid {{ grid-template-columns: repeat(2,1fr); }} }}
    .stat-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px 24px;
    }}
    .stat-card .label {{ font-size: 12px; color: var(--muted); margin-bottom: 6px; }}
    .stat-card .value {{ font-size: 30px; font-weight: 700; color: var(--text); }}
    .stat-card .sub {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}

    /* ── Section ── */
    .section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 24px 28px;
      margin-bottom: 24px;
    }}
    .section h2 {{
      font-size: 16px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .section h2 .icon {{ font-size: 18px; }}

    /* ── Grid for side-by-side sections ── */
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    @media (max-width: 800px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

    /* ── Contribution calendar ── */
    #cal-container {{
      overflow-x: auto;
    }}
    #calendar {{
      display: grid;
      grid-auto-flow: column;
      grid-template-rows: repeat(7, 13px);
      gap: 3px;
      margin-top: 8px;
    }}
    .cal-day {{
      width: 13px;
      height: 13px;
      border-radius: 2px;
      background: #161b22;
      border: 1px solid rgba(255,255,255,0.06);
    }}
    .cal-day[data-count="0"] {{ background: #161b22; }}
    .cal-day[data-level="1"] {{ background: var(--green1); }}
    .cal-day[data-level="2"] {{ background: var(--green2); }}
    .cal-day[data-level="3"] {{ background: var(--green3); }}
    .cal-day[data-level="4"] {{ background: var(--green4); }}
    .cal-day:hover {{ outline: 1px solid #fff4; }}
    .cal-legend {{
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 10px;
      font-size: 11px;
      color: var(--muted);
    }}
    .leg-box {{ width: 13px; height: 13px; border-radius: 2px; }}

    /* ── Bar charts ── */
    .bar-list {{ list-style: none; }}
    .bar-item {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .bar-item .bar-label {{
      width: 140px;
      flex-shrink: 0;
      color: var(--text);
      font-size: 12px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .bar-track {{
      flex: 1;
      background: rgba(255,255,255,0.05);
      border-radius: 4px;
      height: 10px;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      border-radius: 4px;
      transition: width .3s ease;
    }}
    .bar-item .bar-count {{
      width: 36px;
      text-align: right;
      color: var(--muted);
      font-size: 12px;
      flex-shrink: 0;
    }}

    /* ── SVG line chart ── */
    #monthly-chart {{ width: 100%; height: 160px; overflow: visible; }}
    .chart-grid line {{ stroke: rgba(255,255,255,0.06); }}
    .chart-line {{ fill: none; stroke: var(--accent); stroke-width: 2; }}
    .chart-area {{ fill: url(#area-grad); opacity: 0.4; }}
    .tick-label {{ fill: var(--muted); font-size: 10px; font-family: inherit; }}

    /* ── Commits table ── */
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{
      text-align: left;
      color: var(--muted);
      font-weight: 500;
      padding: 0 12px 12px 0;
      border-bottom: 1px solid var(--border);
    }}
    td {{
      padding: 8px 12px 8px 0;
      border-bottom: 1px solid rgba(48,54,61,0.5);
      color: var(--text);
    }}
    .hash {{
      font-family: 'SFMono-Regular', Consolas, monospace;
      color: var(--accent);
      font-size: 12px;
    }}

    /* ── Donut chart ── */
    #donut-svg {{ display: block; margin: 0 auto; }}

    /* ── Tooltip ── */
    #tooltip {{
      position: fixed;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 12px;
      pointer-events: none;
      opacity: 0;
      transition: opacity .15s;
      z-index: 100;
    }}
  </style>
</head>
<body>
  <div id="tooltip"></div>

  <header>
    <h1>
      <span class="logo">GitPulse</span>
      <span class="sep">/</span>
      {_safe(info["name"])}
    </h1>
    <p>
      Branch: <strong>{_safe(info["branch"])}</strong>
      &nbsp;·&nbsp;
      Generated on {date.today().isoformat()}
    </p>
  </header>

  <main>
    <!-- ── Stat cards ── -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="label">Total Commits</div>
        <div class="value">{total_commits:,}</div>
      </div>
      <div class="stat-card">
        <div class="label">Contributors</div>
        <div class="value">{num_authors}</div>
      </div>
      <div class="stat-card">
        <div class="label">Files Changed</div>
        <div class="value">{num_files}</div>
      </div>
      <div class="stat-card">
        <div class="label">Days Active</div>
        <div class="value">{days_active}</div>
      </div>
    </div>

    <!-- ── Contribution Calendar ── -->
    <div class="section">
      <h2><span class="icon">📅</span> Contribution Calendar</h2>
      <div id="cal-container">
        <div id="calendar"></div>
      </div>
      <div class="cal-legend">
        Less &nbsp;
        <div class="leg-box" style="background:#161b22;border:1px solid #30363d;"></div>
        <div class="leg-box" style="background:var(--green1);"></div>
        <div class="leg-box" style="background:var(--green2);"></div>
        <div class="leg-box" style="background:var(--green3);"></div>
        <div class="leg-box" style="background:var(--green4);"></div>
        More
      </div>
    </div>

    <!-- ── Monthly trend + Authors ── -->
    <div class="two-col">
      <div class="section">
        <h2><span class="icon">📈</span> Monthly Commit Trend</h2>
        <svg id="monthly-chart" viewBox="0 0 500 160" preserveAspectRatio="xMidYMid meet">
          <defs>
            <linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.6"/>
              <stop offset="100%" stop-color="#58a6ff" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <g class="chart-grid" id="chart-grid"></g>
          <path class="chart-area" id="chart-area"></path>
          <path class="chart-line" id="chart-line"></path>
          <g id="chart-labels"></g>
        </svg>
      </div>

      <div class="section">
        <h2><span class="icon">🏆</span> Top Contributors</h2>
        <ul class="bar-list" id="author-bars"></ul>
      </div>
    </div>

    <!-- ── File Hotspots + Languages ── -->
    <div class="two-col">
      <div class="section">
        <h2><span class="icon">🔥</span> File Hotspots</h2>
        <ul class="bar-list" id="file-bars"></ul>
      </div>

      <div class="section">
        <h2><span class="icon">💻</span> Languages</h2>
        <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;">
          <svg id="donut-svg" width="140" height="140" viewBox="-70 -70 140 140"></svg>
          <ul class="bar-list" id="lang-legend" style="flex:1;min-width:120px;"></ul>
        </div>
      </div>
    </div>

    <!-- ── Recent Commits ── -->
    <div class="section">
      <h2><span class="icon">🕐</span> Recent Commits</h2>
      <div style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Hash</th>
              <th>Date</th>
              <th>Author</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>{commit_rows}</tbody>
        </table>
      </div>
    </div>

    <p style="text-align:center;color:var(--muted);font-size:12px;margin-top:24px;">
      Generated by <strong style="color:var(--accent)">GitPulse</strong> — beautiful git analytics
    </p>
  </main>

  <script>
    // ── Data ──────────────────────────────────────────────────────────────────
    const authorsData  = {j_authors};
    const filesData    = {j_files};
    const langsData    = {j_langs};
    const monthlyData  = {j_monthly};
    const calendarData = {j_calendar};

    const COLORS = [
      '#58a6ff','#bc8cff','#3fb950','#d29922',
      '#f0883e','#ea5151','#39d353','#79c0ff'
    ];

    // ── Tooltip ───────────────────────────────────────────────────────────────
    const tip = document.getElementById('tooltip');
    function showTip(e, text) {{
      tip.textContent = text;
      tip.style.opacity = 1;
      tip.style.left = (e.clientX + 14) + 'px';
      tip.style.top  = (e.clientY + 14) + 'px';
    }}
    function hideTip() {{ tip.style.opacity = 0; }}

    // ── Contribution Calendar ─────────────────────────────────────────────────
    const cal = document.getElementById('calendar');
    calendarData.forEach(entry => {{
      const d = document.createElement('div');
      d.className = 'cal-day';
      const c = entry.c;
      d.dataset.count = c;
      if (c === 0)      d.dataset.level = '0';
      else if (c === 1) d.dataset.level = '1';
      else if (c <= 3)  d.dataset.level = '2';
      else if (c <= 6)  d.dataset.level = '3';
      else              d.dataset.level = '4';
      d.addEventListener('mouseenter', e => showTip(e, `${{entry.d}}: ${{c}} commit${{c !== 1 ? 's' : ''}}`));
      d.addEventListener('mouseleave', hideTip);
      d.addEventListener('mousemove', e => {{ tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY+14)+'px'; }});
      cal.appendChild(d);
    }});

    // ── Generic horizontal bar chart ──────────────────────────────────────────
    function renderBars(containerId, labels, values, colors) {{
      const ul = document.getElementById(containerId);
      const max = Math.max(...values, 1);
      labels.forEach((lbl, i) => {{
        const pct = (values[i] / max * 100).toFixed(1);
        const color = Array.isArray(colors) ? colors[i % colors.length] : colors;
        ul.innerHTML += `
          <li class="bar-item">
            <span class="bar-label" title="${{lbl}}">${{lbl}}</span>
            <div class="bar-track">
              <div class="bar-fill" style="width:${{pct}}%;background:${{color}};"></div>
            </div>
            <span class="bar-count">${{values[i]}}</span>
          </li>`;
      }});
    }}

    renderBars('author-bars', authorsData.labels, authorsData.values, COLORS);
    renderBars('file-bars',   filesData.labels,   filesData.values,   '#d29922');

    // ── Monthly trend (SVG line chart) ────────────────────────────────────────
    (function() {{
      const W = 500, H = 160, PAD = {{top:16, right:16, bottom:36, left:36}};
      const cw = W - PAD.left - PAD.right;
      const ch = H - PAD.top  - PAD.bottom;
      const labels = monthlyData.labels;
      const values = monthlyData.values;
      if (!values.length) return;
      const maxV = Math.max(...values, 1);
      const x = i => PAD.left + (i / Math.max(labels.length - 1, 1)) * cw;
      const y = v => PAD.top  + (1 - v / maxV) * ch;

      // Grid
      const grid = document.getElementById('chart-grid');
      [0.25, 0.5, 0.75, 1].forEach(frac => {{
        const yPos = PAD.top + (1 - frac) * ch;
        grid.innerHTML += `<line x1="${{PAD.left}}" y1="${{yPos}}" x2="${{W - PAD.right}}" y2="${{yPos}}"/>`;
        const labelEl = document.createElementNS('http://www.w3.org/2000/svg','text');
        labelEl.setAttribute('x', PAD.left - 4);
        labelEl.setAttribute('y', yPos + 3);
        labelEl.setAttribute('text-anchor','end');
        labelEl.setAttribute('class','tick-label');
        labelEl.textContent = Math.round(frac * maxV);
        document.getElementById('chart-labels').appendChild(labelEl);
      }});

      // Points
      const pts = labels.map((_, i) => `${{x(i).toFixed(1)}},${{y(values[i]).toFixed(1)}}`).join(' ');
      const firstX = x(0).toFixed(1), lastX = x(labels.length-1).toFixed(1);
      const bottomY = (PAD.top + ch).toFixed(1);

      document.getElementById('chart-area').setAttribute('d',
        `M${{firstX}},${{bottomY}} L${{pts.split(' ').map(p=>p).join(' L')}} L${{lastX}},${{bottomY}} Z`
      );
      document.getElementById('chart-line').setAttribute('d',
        `M ${{pts.split(' ').join(' L ')}}`
      );

      // X-axis labels (every N months)
      const step = Math.max(1, Math.ceil(labels.length / 8));
      const labelsG = document.getElementById('chart-labels');
      labels.forEach((lbl, i) => {{
        if (i % step !== 0 && i !== labels.length - 1) return;
        const el = document.createElementNS('http://www.w3.org/2000/svg','text');
        el.setAttribute('x', x(i).toFixed(1));
        el.setAttribute('y', PAD.top + ch + 18);
        el.setAttribute('text-anchor','middle');
        el.setAttribute('class','tick-label');
        el.textContent = lbl.slice(2); // "24-01" form
        labelsG.appendChild(el);
      }});
    }})();

    // ── Languages donut ───────────────────────────────────────────────────────
    (function() {{
      const labels = langsData.labels;
      const values = langsData.values;
      if (!values.length) return;
      const total = values.reduce((a,b)=>a+b,0);
      let angle = -Math.PI / 2;
      const R = 55, r = 30;
      const svg = document.getElementById('donut-svg');
      const leg = document.getElementById('lang-legend');

      values.forEach((val, i) => {{
        const frac = val / total;
        const sweep = frac * 2 * Math.PI;
        const x1 = Math.cos(angle) * R, y1 = Math.sin(angle) * R;
        const x2 = Math.cos(angle + sweep) * R, y2 = Math.sin(angle + sweep) * R;
        const ix1 = Math.cos(angle) * r, iy1 = Math.sin(angle) * r;
        const ix2 = Math.cos(angle + sweep) * r, iy2 = Math.sin(angle + sweep) * r;
        const largeArc = sweep > Math.PI ? 1 : 0;
        const color = COLORS[i % COLORS.length];
        const path = document.createElementNS('http://www.w3.org/2000/svg','path');
        path.setAttribute('d', `M ${{x1}} ${{y1}} A ${{R}} ${{R}} 0 ${{largeArc}} 1 ${{x2}} ${{y2}} L ${{ix2}} ${{iy2}} A ${{r}} ${{r}} 0 ${{largeArc}} 0 ${{ix1}} ${{iy1}} Z`);
        path.setAttribute('fill', color);
        path.style.cursor = 'pointer';
        const pct = (frac * 100).toFixed(1);
        path.addEventListener('mouseenter', e => showTip(e, `${{labels[i]}}: ${{val}} (${{pct}}%)`));
        path.addEventListener('mouseleave', hideTip);
        path.addEventListener('mousemove', e => {{ tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY+14)+'px'; }});
        svg.appendChild(path);
        angle += sweep;

        leg.innerHTML += `
          <li class="bar-item" style="margin-bottom:6px;">
            <span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${{color}};flex-shrink:0;margin-right:6px;"></span>
            <span class="bar-label" style="width:80px;">${{labels[i]}}</span>
            <span class="bar-count">${{val}}</span>
          </li>`;
      }});
    }})();
  </script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
