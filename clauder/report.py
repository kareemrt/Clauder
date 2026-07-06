"""HTML report generation for repository stories."""

import re
import json
from datetime import datetime
from pathlib import Path
from jinja2 import Environment

from .github_client import RepoData


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ repo_name }} — Clauder Story</title>
<style>
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface2: #1c2128;
    --border: #30363d;
    --text: #e6edf3;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --accent2: #f0883e;
    --green: #3fb950;
    --purple: #a371f7;
    --yellow: #d29922;
    --red: #f85149;
    --cyan: #56d364;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.6;
    min-height: 100vh;
  }

  /* Hero */
  .hero {
    background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 50%, #0d1117 100%);
    border-bottom: 1px solid var(--border);
    padding: 60px 24px 48px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(88,166,255,0.08) 0%, transparent 70%);
  }
  .badge {
    display: inline-block;
    background: rgba(88,166,255,0.1);
    border: 1px solid rgba(88,166,255,0.3);
    color: var(--accent);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
  }
  .hero h1 {
    font-size: clamp(28px, 5vw, 52px);
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 12px;
  }
  .hero h1 .repo-owner { color: var(--text-muted); }
  .hero h1 .repo-slash { color: var(--border); }
  .hero h1 .repo-name { color: var(--text); }
  .tagline {
    font-size: 18px;
    color: var(--text-muted);
    font-style: italic;
    margin-bottom: 32px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  .stat-row {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
  }
  .stat-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
  }
  .stat-pill .icon { font-size: 16px; }
  .stat-pill.stars .val { color: var(--yellow); }
  .stat-pill.forks .val { color: var(--accent); }
  .stat-pill.lang .val { color: var(--green); }
  .stat-pill.issues .val { color: var(--red); }

  /* Main content */
  .container { max-width: 900px; margin: 0 auto; padding: 0 24px 80px; }

  /* Language bar */
  .lang-section { margin: 40px 0 32px; }
  .section-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 12px;
  }
  .lang-bar {
    display: flex;
    height: 10px;
    border-radius: 6px;
    overflow: hidden;
    gap: 2px;
    margin-bottom: 10px;
  }
  .lang-seg { height: 100%; border-radius: 2px; transition: opacity 0.2s; }
  .lang-seg:hover { opacity: 0.8; }
  .lang-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 12px 24px;
    font-size: 12px;
    color: var(--text-muted);
  }
  .lang-legend-item { display: flex; align-items: center; gap: 6px; }
  .lang-dot { width: 8px; height: 8px; border-radius: 50%; }

  /* Contributors */
  .contributors { margin: 40px 0; }
  .contrib-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
    margin-top: 16px;
  }
  .contrib-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
    text-decoration: none;
    color: inherit;
  }
  .contrib-card:hover { border-color: var(--accent); transform: translateY(-2px); }
  .contrib-avatar {
    width: 48px; height: 48px; border-radius: 50%;
    border: 2px solid var(--border);
  }
  .contrib-login { font-weight: 600; font-size: 14px; }
  .contrib-count { font-size: 12px; color: var(--text-muted); }
  .contrib-bar {
    width: 100%; height: 3px; background: var(--border); border-radius: 2px;
  }
  .contrib-bar-fill { height: 100%; background: var(--accent); border-radius: 2px; }

  /* Story sections */
  .story { margin-top: 48px; }
  .story-section {
    margin-bottom: 32px;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
  }
  .story-section-header {
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 16px;
  }
  .story-section-icon { font-size: 18px; }
  .story-section-body {
    padding: 20px 24px;
    background: var(--surface);
    font-size: 15px;
    line-height: 1.75;
    color: #c9d1d9;
    white-space: pre-wrap;
  }
  .section-origin .story-section-header { background: rgba(86,211,100,0.1); color: var(--cyan); }
  .section-architects .story-section-header { background: rgba(210,153,34,0.1); color: var(--yellow); }
  .section-journey .story-section-header { background: rgba(88,166,255,0.1); color: var(--accent); }
  .section-technology .story-section-header { background: rgba(163,113,247,0.1); color: var(--purple); }
  .section-current .story-section-header { background: rgba(248,81,73,0.1); color: var(--red); }
  .section-future .story-section-header { background: rgba(240,136,62,0.1); color: var(--accent2); }
  .section-oneliner .story-section-header { background: rgba(255,255,255,0.05); color: var(--text); }
  .section-oneliner .story-section-body {
    font-size: 17px;
    font-style: italic;
    text-align: center;
    color: var(--accent);
    padding: 28px 40px;
  }

  /* Commit timeline */
  .timeline { margin: 40px 0; }
  .timeline-list { list-style: none; border-left: 2px solid var(--border); padding-left: 20px; margin-top: 16px; }
  .timeline-item { position: relative; margin-bottom: 16px; }
  .timeline-item::before {
    content: '';
    position: absolute;
    left: -26px; top: 6px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--surface2);
    border: 2px solid var(--border);
  }
  .timeline-item:first-child::before { background: var(--green); border-color: var(--green); }
  .commit-msg { font-size: 14px; color: var(--text); }
  .commit-meta { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
  .commit-sha {
    font-family: monospace;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 11px;
    color: var(--text-muted);
  }

  /* Footer */
  footer {
    text-align: center;
    padding: 32px 24px;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 13px;
  }
  footer a { color: var(--accent); text-decoration: none; }
  footer a:hover { text-decoration: underline; }

  @media (max-width: 600px) {
    .stat-row { gap: 10px; }
    .stat-pill { padding: 8px 14px; font-size: 13px; }
  }
</style>
</head>
<body>

<div class="hero">
  <div class="badge">◈ Clauder · Repository Story</div>
  <h1>
    <span class="repo-owner">{{ repo_owner }}</span>
    <span class="repo-slash">/</span>
    <span class="repo-name">{{ repo_name_only }}</span>
  </h1>
  <p class="tagline">"{{ tagline }}"</p>
  <div class="stat-row">
    <div class="stat-pill stars"><span class="icon">★</span><span class="val">{{ stats.stars | number_format }}</span><span style="color:var(--text-muted)">stars</span></div>
    <div class="stat-pill forks"><span class="icon">⑂</span><span class="val">{{ stats.forks | number_format }}</span><span style="color:var(--text-muted)">forks</span></div>
    {% if stats.language %}<div class="stat-pill lang"><span class="icon">◈</span><span class="val">{{ stats.language }}</span></div>{% endif %}
    <div class="stat-pill issues"><span class="icon">⊕</span><span class="val">{{ stats.open_issues }}</span><span style="color:var(--text-muted)">open issues</span></div>
  </div>
</div>

<div class="container">

  {% if languages %}
  <div class="lang-section">
    <div class="section-title">Language Breakdown</div>
    <div class="lang-bar">
      {% for lang in lang_segments %}
      <div class="lang-seg" style="width:{{ lang.pct }}%; background:{{ lang.color }};" title="{{ lang.name }}: {{ lang.pct }}%"></div>
      {% endfor %}
    </div>
    <div class="lang-legend">
      {% for lang in lang_segments %}
      <div class="lang-legend-item">
        <div class="lang-dot" style="background:{{ lang.color }};"></div>
        {{ lang.name }} {{ lang.pct }}%
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  {% if contributors %}
  <div class="contributors">
    <div class="section-title">Contributors</div>
    <div class="contrib-grid">
      {% for c in contributors %}
      <a class="contrib-card" href="{{ c.html_url }}" target="_blank" rel="noopener">
        <img class="contrib-avatar" src="{{ c.avatar_url }}" alt="{{ c.login }}" loading="lazy">
        <div class="contrib-login">{{ c.login }}</div>
        <div class="contrib-count">{{ c.contributions }} commits</div>
        <div class="contrib-bar"><div class="contrib-bar-fill" style="width:{{ c.pct }}%;"></div></div>
      </a>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  {% if commits %}
  <div class="timeline">
    <div class="section-title">Commit History</div>
    <ul class="timeline-list">
      {% for c in commits %}
      <li class="timeline-item">
        <div class="commit-msg">{{ c.message }}</div>
        <div class="commit-meta">
          <span class="commit-sha">{{ c.sha }}</span>
          {{ c.author }} · {{ c.date }}
        </div>
      </li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}

  <div class="story">
    <div class="section-title">The Story</div>
    {% for section in story_sections %}
    <div class="story-section section-{{ section.css_key }}">
      <div class="story-section-header">
        <span class="story-section-icon">{{ section.icon }}</span>
        {{ section.title }}
      </div>
      <div class="story-section-body">{{ section.content }}</div>
    </div>
    {% endfor %}
  </div>

</div>

<footer>
  Generated {{ generated_at }} by <strong>Clauder</strong> · Powered by <a href="https://anthropic.com" target="_blank">Claude AI</a>
</footer>

</body>
</html>
"""

LANG_COLORS = [
    "#58a6ff", "#f0883e", "#3fb950", "#a371f7",
    "#d29922", "#f85149", "#56d364", "#79c0ff",
]

SECTION_META = {
    "The Origin":       ("origin",      "★"),
    "The Architects":   ("architects",  "◆"),
    "The Journey":      ("journey",     "◈"),
    "The Technology":   ("technology",  "◉"),
    "The Current State":("current",     "◎"),
    "The Future":       ("future",      "◌"),
    "One-Line Story":   ("oneliner",    "✦"),
}


def _number_format(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)


def generate_html_report(data: RepoData, story: str, tagline: str, output_path: str) -> str:
    owner, _, repo_only = data.stats.full_name.partition("/")

    total_lang = sum(data.languages.values()) or 1
    lang_segments = [
        {
            "name": lang,
            "pct": round(bytes_count / total_lang * 100, 1),
            "color": LANG_COLORS[i % len(LANG_COLORS)],
        }
        for i, (lang, bytes_count) in enumerate(
            sorted(data.languages.items(), key=lambda x: -x[1])[:8]
        )
    ]

    max_contrib = data.contributors[0].contributions if data.contributors else 1
    contrib_list = [
        {
            "login": c.login,
            "contributions": c.contributions,
            "avatar_url": c.avatar_url,
            "html_url": c.html_url,
            "pct": round(c.contributions / max_contrib * 100),
        }
        for c in data.contributors[:12]
    ]

    commit_list = [
        {
            "sha": c.sha,
            "message": c.message[:100],
            "author": c.author,
            "date": c.date[:10] if c.date else "",
        }
        for c in data.commits[:20]
    ]

    # Parse story sections
    sections = []
    pattern = r"##\s+(.+?)\n(.*?)(?=##\s|\Z)"
    matches = re.findall(pattern, story, re.DOTALL)
    for title, content in matches:
        title = title.strip()
        css_key, icon = SECTION_META.get(title, ("misc", "◆"))
        sections.append({
            "title": title,
            "content": content.strip(),
            "css_key": css_key,
            "icon": icon,
        })

    env = Environment()
    env.filters["number_format"] = _number_format
    tmpl = env.from_string(HTML_TEMPLATE)

    html = tmpl.render(
        repo_name=data.stats.full_name,
        repo_owner=owner,
        repo_name_only=repo_only,
        tagline=tagline,
        stats=data.stats,
        languages=data.languages,
        lang_segments=lang_segments,
        contributors=contrib_list,
        commits=commit_list,
        story_sections=sections,
        generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    )

    Path(output_path).write_text(html, encoding="utf-8")
    return output_path
