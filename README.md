
```
  ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
 ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
 ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗  
 ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
 ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
  ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
                                            ⚡ git analytics engine
```

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/output-HTML%20%7C%20terminal-purple?style=flat-square" alt="Output">
  <img src="https://img.shields.io/badge/zero-external%20deps-orange?style=flat-square" alt="Zero deps">
</p>

---

**GitPulse** turns any git repository into a beautiful analytics dashboard — a GitHub-style contribution heatmap, contributor rankings, file hotspot analysis, and hourly activity patterns — all in a single self-contained HTML file plus a gorgeous terminal summary.

---

## Features

```
┌─────────────────────────────────────────────────────────────┐
│  📊  Contribution Heatmap    GitHub-style 52-week calendar  │
│  👤  Top Contributors        Ranked bar chart               │
│  🔥  File Hotspots           Most frequently changed paths  │
│  ⏰  Hourly Activity          UTC commit time distribution   │
│  📅  Day-of-week Patterns    Weekly rhythm visualization    │
│  📋  Recent Commits          Last 10 commits with details   │
│  💻  Terminal Summary        Rich-formatted CLI output      │
│  🌐  Self-contained HTML     No CDN, no server needed       │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# Install
pip install gitpulse    # or: pip install -e . (from source)

# Analyze current directory
gitpulse .

# Analyze a specific repo + custom output path
gitpulse ~/projects/myrepo --output myrepo-report.html

# Terminal summary only (no HTML)
gitpulse . --no-html
```

---

## Terminal Output

```
╭──────────────────────────────────────────────────────────────╮
│  ⚡ GitPulse  ·  my-awesome-project                          │
│  2023-01-15 → 2025-11-30  (1050 days)                        │
╰──────────────────────────────────────────────────────────────╯

   Total commits       4,231
   Contributors           12
   Active days           387
   Avg commits/day      4.03

Top contributors
  alice                  ████████████████████████████  1,832
  bob                    ████████████████████░░░░░░░░  1,241
  carol                  ████████████░░░░░░░░░░░░░░░░    742
  dan                    ██████░░░░░░░░░░░░░░░░░░░░░░    418

Activity by weekday
  ██▇▇▇▆▄▂▁
  Mon  Tue  Wed  Thu  Fri  Sat  Sun

Activity by hour (UTC)
  ▁▁▁▁▁▂▄▅▇█▇▆▅▄▃▃▂▂▁▁▁▁▁▁
  00              12              23

Hottest files
   1. src/core/engine.py                                  312x
   2. tests/test_engine.py                                287x
   3. src/api/routes.py                                   201x
   4. README.md                                            98x
```

---

## HTML Dashboard

The HTML report is a fully dark-themed, responsive single-page dashboard with:

```
┌──────────────────────────────────────────────────────────┐
│  ⚡ GitPulse — my-project                                 │
│  2023-01-15 → 2025-11-30  ·  1050 days  ·  Generated …  │
├──────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  Commits │ │ Authors  │ │  Active  │ │  Files   │   │
│  │  4,231   │ │    12    │ │   Days   │ │  Touched │   │
│  │          │ │          │ │   387    │ │  41,829  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
├──────────────────────────────────────────────────────────┤
│  Commit Activity — Last 52 Weeks                         │
│  ░░░░▒▒▒░░▒▒▒▓▓▓░░░░▒▒▒▓▓█▓▓▒▒▒░░░░░▒▒▒▓▓▓▒▒▒░░░░▒▒▒  │
│  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov   │
├──────────────────────────────────────────────────────────┤
│  Commits by Day of Week  │  Commits by Hour (UTC)        │
│  ┌─────────────────────┐ │ ┌──────────────────────────┐  │
│  │  ▌ ▌ ▌ ▌           │ │ │  peaks at 10:00–14:00    │  │
│  └─────────────────────┘ │ └──────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  Top Contributors        │  Hottest Files                │
│  #1  alice  ██████  1.8k │ #1  src/core.py  312x        │
│  #2  bob    █████   1.2k │ #2  tests/…      287x        │
├──────────────────────────────────────────────────────────┤
│  Recent Commits                                          │
│  a3f8d21  alice   feat: add streaming support   2025-11  │
│  9c41bb0  bob     fix: handle edge case in auth 2025-11  │
└──────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
gitpulse/
├── gitpulse/
│   ├── __init__.py      Package metadata
│   ├── analyzer.py      Git log parsing & statistical analysis
│   ├── reporter.py      Self-contained HTML + SVG chart generation
│   └── cli.py           CLI entry point (argparse + rich)
├── setup.py             Package configuration
└── README.md            This file
```

---

## How It Works

```
git log  ──►  analyzer.py  ──►  stats dict  ──►  reporter.py  ──►  report.html
                │                                     │
                └──────────────────────────────►  cli.py  ──►  terminal
```

1. **analyzer.py** shells out to `git log` and `git log --name-only` to collect
   commit metadata and file-change counts. All parsing is done with the Python
   standard library — no gitpython dependency.

2. **reporter.py** generates a single self-contained HTML file. Charts are pure
   inline SVG drawn with computed coordinates — no D3, no Chart.js, no CDN calls.
   The heatmap uses the same cell-based layout as GitHub's contribution graph.

3. **cli.py** uses `rich` for the terminal output (progress spinner, tables,
   sparkline bars) and orchestrates the pipeline.

---

## Requirements

| Dependency | Purpose |
|-----------|---------|
| Python ≥ 3.11 | f-strings, `datetime.fromisoformat` |
| `rich` ≥ 13.0 | Terminal formatting |
| `git` (any version) | Repo access via subprocess |

---

## License

MIT © GitPulse contributors
