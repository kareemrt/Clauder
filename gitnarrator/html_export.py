"""Generates a polished HTML story report from RepoStats and the AI narrative."""

from __future__ import annotations

import json
import os
from datetime import datetime

from .git_analyzer import RepoStats

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0d1117; color: #e6edf3; line-height: 1.7; }
.hero { background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        border-bottom: 1px solid #30363d; padding: 80px 40px; text-align: center; }
.hero h1 { font-size: 3rem; font-weight: 800; background: linear-gradient(90deg, #58a6ff, #bc8cff, #ff7b72);
           -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 16px; }
.hero .tagline { font-size: 1.2rem; color: #8b949e; margin-bottom: 32px; }
.badges { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.badge { background: #21262d; border: 1px solid #30363d; border-radius: 20px;
         padding: 6px 16px; font-size: 0.85rem; color: #58a6ff; }
.badge span { color: #e6edf3; font-weight: 600; }
.container { max-width: 1100px; margin: 0 auto; padding: 40px 24px; }
.section { margin-bottom: 60px; }
h2 { font-size: 1.6rem; font-weight: 700; color: #58a6ff; margin-bottom: 24px;
     padding-bottom: 10px; border-bottom: 1px solid #30363d; }
h3 { font-size: 1.1rem; color: #bc8cff; margin-bottom: 10px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }
.stat-card { background: #161b22; border: 1px solid #30363d; border-radius: 10px;
             padding: 24px; text-align: center; }
.stat-card .value { font-size: 2.2rem; font-weight: 800; color: #58a6ff; }
.stat-card .label { font-size: 0.85rem; color: #8b949e; margin-top: 4px; }
.narrative { background: #161b22; border: 1px solid #30363d; border-left: 4px solid #bc8cff;
             border-radius: 10px; padding: 32px; white-space: pre-wrap; font-size: 0.97rem;
             color: #c9d1d9; line-height: 1.9; }
.chapter-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
.chapter-card { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 24px; }
.chapter-card .num { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
.chapter-card .dates { font-size: 0.85rem; color: #8b949e; margin: 4px 0 12px; }
.chapter-card .commits { color: #58a6ff; font-weight: 600; }
.chapter-card .delta { font-size: 0.85rem; margin-top: 8px; }
.chapter-card .ins { color: #3fb950; }
.chapter-card .dels { color: #f85149; }
.bar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.bar-label { min-width: 160px; font-size: 0.9rem; color: #c9d1d9; overflow: hidden;
             text-overflow: ellipsis; white-space: nowrap; }
.bar-track { flex: 1; background: #21262d; border-radius: 4px; height: 14px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.3s; }
.bar-count { min-width: 48px; text-align: right; font-size: 0.85rem; color: #8b949e; }
.heatmap { display: flex; flex-wrap: wrap; gap: 3px; }
.heatmap-cell { width: 14px; height: 14px; border-radius: 2px; }
.heatmap-0 { background: #161b22; }
.heatmap-1 { background: #0e4429; }
.heatmap-2 { background: #006d32; }
.heatmap-3 { background: #26a641; }
.heatmap-4 { background: #39d353; }
.footer { text-align: center; padding: 40px; color: #484f58; font-size: 0.85rem;
          border-top: 1px solid #21262d; margin-top: 40px; }
"""

_BAR_COLORS = ["#58a6ff", "#bc8cff", "#ff7b72", "#3fb950", "#f0883e", "#79c0ff"]


def _bar_rows(items: list[tuple], max_val: int, label_key: bool = True) -> str:
    html = ""
    for i, (label, value) in enumerate(items):
        pct = (value / max_val * 100) if max_val else 0
        color = _BAR_COLORS[i % len(_BAR_COLORS)]
        short = label if len(str(label)) <= 30 else "…" + str(label)[-29:]
        html += (
            f'<div class="bar-row">'
            f'<div class="bar-label" title="{label}">{short}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%;background:{color}"></div></div>'
            f'<div class="bar-count">{value}</div>'
            f'</div>'
        )
    return html


def _heatmap_cells(weekly_activity: dict) -> str:
    if not weekly_activity:
        return ""
    max_val = max(weekly_activity.values())
    weeks = sorted(weekly_activity.keys())
    cells = ""
    for w in weeks:
        val = weekly_activity.get(w, 0)
        level = 0 if val == 0 else min(4, 1 + int(val / max_val * 3.99))
        title = f"{w}: {val} commits"
        cells += f'<div class="heatmap-cell heatmap-{level}" title="{title}"></div>'
    return f'<div class="heatmap">{cells}</div>'


def export_html(stats: RepoStats, narrative: str, output_path: str) -> str:
    duration = (stats.last_commit - stats.first_commit).days
    top_authors = sorted(stats.authors.items(), key=lambda x: x[1], reverse=True)[:8]
    top_files = sorted(stats.file_heatmap.items(), key=lambda x: x[1], reverse=True)[:10]
    top_langs = sorted(stats.primary_languages.items(), key=lambda x: x[1], reverse=True)[:8]

    author_max = top_authors[0][1] if top_authors else 1
    file_max = top_files[0][1] if top_files else 1
    lang_max = top_langs[0][1] if top_langs else 1

    # Chapter cards
    chapter_cards = ""
    for ch in stats.chapters:
        top_auth = max(ch["authors"].items(), key=lambda x: x[1])[0] if ch["authors"] else "?"
        start = ch["start_date"].strftime("%b %Y")
        end = ch["end_date"].strftime("%b %Y")
        chapter_cards += f"""
        <div class="chapter-card">
            <div class="num">Chapter {ch['number']}</div>
            <div class="dates">{start} → {end}</div>
            <div class="commits">{ch['commit_count']} commits</div>
            <div style="color:#bc8cff;font-size:0.9rem;margin-top:4px">{top_auth}</div>
            <div class="delta">
                <span class="ins">+{ch['insertions']}</span>
                &nbsp;
                <span class="dels">-{ch['deletions']}</span>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitNarrator — {stats.name}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="hero">
  <h1>The Story of {stats.name}</h1>
  <div class="tagline">Generated by GitNarrator &nbsp;·&nbsp; {datetime.utcnow().strftime('%B %d, %Y')}</div>
  <div class="badges">
    <div class="badge">Commits <span>{stats.total_commits}</span></div>
    <div class="badge">Contributors <span>{len(stats.authors)}</span></div>
    <div class="badge">Days Active <span>{duration}</span></div>
    <div class="badge">Files Touched <span>{len(stats.file_heatmap)}</span></div>
    <div class="badge">Chapters <span>{len(stats.chapters)}</span></div>
  </div>
</div>

<div class="container">

  <div class="section">
    <h2>Overview</h2>
    <div class="stats-grid">
      <div class="stat-card"><div class="value">{stats.total_commits}</div><div class="label">Total Commits</div></div>
      <div class="stat-card"><div class="value">{len(stats.authors)}</div><div class="label">Contributors</div></div>
      <div class="stat-card"><div class="value">{duration}</div><div class="label">Days Active</div></div>
      <div class="stat-card"><div class="value">{len(stats.file_heatmap)}</div><div class="label">Files Changed</div></div>
    </div>
  </div>

  <div class="section">
    <h2>The Narrative</h2>
    <div class="narrative">{narrative}</div>
  </div>

  <div class="section">
    <h2>Chapter Timeline</h2>
    <div class="chapter-grid">{chapter_cards}</div>
  </div>

  <div class="section">
    <h2>Commit Activity Heatmap</h2>
    {_heatmap_cells(stats.weekly_activity)}
    <p style="font-size:0.8rem;color:#484f58;margin-top:8px">Each cell = one week. Darker = more commits.</p>
  </div>

  <div class="section">
    <h2>Top Contributors</h2>
    {_bar_rows(top_authors, author_max)}
  </div>

  <div class="section">
    <h2>Hottest Files</h2>
    {_bar_rows(top_files, file_max)}
  </div>

  <div class="section">
    <h2>Languages</h2>
    {_bar_rows(top_langs, lang_max)}
  </div>

</div>
<div class="footer">
  Generated by <strong>GitNarrator</strong> · Powered by Claude AI · {datetime.utcnow().strftime('%Y')}
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
