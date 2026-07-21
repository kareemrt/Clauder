<div align="center">

```
  ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
  ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
  ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
```

**Terminal Git Analytics Dashboard**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Rich](https://img.shields.io/badge/powered%20by-Rich-ff69b4?style=flat-square)](https://github.com/Textualize/rich)
[![GitPython](https://img.shields.io/badge/powered%20by-GitPython-blue?style=flat-square)](https://gitpython.readthedocs.io)

*Analyze any git repository and surface beautiful insights — right in your terminal.*

</div>

---

## What is GitPulse?

GitPulse is a zero-configuration CLI tool that reads your repository's commit history and renders it as gorgeous terminal visualizations **and** a fully self-contained HTML report — no servers, no sign-ups, no API tokens.

```
$ gitpulse analyze ~/projects/myapp --report
```

In seconds you get:

| Terminal Output | HTML Report |
|----------------|-------------|
| ASCII commit calendar | Interactive Chart.js graphs |
| Rich contributor leaderboard | Clickable commit-calendar heatmap |
| Hour-of-day activity bars | Responsive, dark-themed layout |
| Weekday chart | Word-cloud of commit messages |
| File hotspot table | Shareable, offline-ready file |
| Commit message word cloud | |

---

## ✨ Features

### 📅 Commit Activity Calendar
A 52-week GitHub-style contribution heatmap rendered directly in your terminal.

```
  Jul  Aug    Sep      Oct      Nov      Dec
  Mon ·  ·  ·  ·  ·  ░  ▒  ▒  ▓  █  ▓  ░  ·  ·
     ·  ·  ·  ·  ·  ·  ▒  ▒  ▓  ▓  ▓  ░  ·  ·
  Wed ·  ·  ·  ·  ░  ░  ░  ▒  ▒  █  ▓  ░  ·  ·
     ·  ·  ·  ·  ·  ·  ·  ▒  ▒  ▓  ▓  ░  ·  ·
  Fri ·  ·  ·  ·  ·  ░  ░  ▒  ▒  ▒  ░  ·  ·  ·
     ·  ·  ·  ·  ·  ·  ·  ·  ▒  ▒  ▒  ·  ·  ·
  Sun ·  ·  ·  ·  ·  ·  ·  ·  ░  ▒  ░  ·  ·  ·

  Less  ░ ▒ ▓ █  More
```

### 👥 Contributor Leaderboard

```
┌────┬────────────────────┬─────────┬────────────┬────────────┬─────────────────────┐
│  # │ Name               │ Commits │ Additions  │ Deletions  │ Impact              │
├────┼────────────────────┼─────────┼────────────┼────────────┼─────────────────────┤
│ 🥇 │ Alice Chen         │   1,284 │  +128,450  │  -42,300   │ ████████████████░░░ │
│ 🥈 │ Bob Martínez       │     896 │   +89,201  │  -31,100   │ ████████████░░░░░░░ │
│ 🥉 │ Carol O'Brien      │     612 │   +54,009  │  -18,230   │ █████████░░░░░░░░░░ │
│  4 │ Dave Kim           │     445 │   +38,100  │  -12,900   │ ██████░░░░░░░░░░░░░ │
└────┴────────────────────┴─────────┴────────────┴────────────┴─────────────────────┘
```

### ⏰ Activity Heatmap by Hour

```
  ▁ ▁ ▁ ▁ ▁ ▂ ▃ ▅ ▆ █ █ ▇ ▆ ▇ █ ▇ ▅ ▄ ▃ ▂ ▂ ▁ ▁ ▁
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
  Peak hour: 10:00 (347 commits)
```

### 🔥 File Hotspots

```
  File                              Changes   Churn
  src/core/engine.py                    184   ████████████████████░░░░
  src/api/routes.py                     142   ███████████████░░░░░░░░░
  tests/test_integration.py            118   █████████████░░░░░░░░░░░
  src/utils/parser.py                    97   ██████████░░░░░░░░░░░░░░
  config/settings.py                     74   ████████░░░░░░░░░░░░░░░░
```

### 💬 Commit Message Word Cloud

```
  FIX  add  REFACTOR  update  feat  REMOVE  docs
  test  config  API  style  ci  build  MERGE
  improve  bump  cleanup  version  release
```

### 📊 HTML Report

The `--report` flag generates a **self-contained HTML file** with:

- **Interactive charts** powered by Chart.js
- **Clickable calendar** with per-day commit counts
- **Dark-themed design** with GitHub-inspired aesthetics
- **Fully offline** — no external dependencies at runtime
- **Mobile-responsive** layout

---

## 🚀 Installation

### From source

```bash
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .
```

### Requirements

- Python 3.10 or newer
- Git installed and accessible in `PATH`

---

## 📖 Usage

### Analyze the current directory

```bash
gitpulse analyze
```

### Analyze a specific repository

```bash
gitpulse analyze ~/projects/myapp
```

### Limit the number of commits (faster on large repos)

```bash
gitpulse analyze ~/projects/bigmonorepo -n 2000
```

### Generate a terminal report **and** an HTML report

```bash
gitpulse analyze . --report
# → Saves to gitpulse-report.html
```

### Generate only the HTML report (skip terminal output)

```bash
gitpulse report ~/projects/myapp -o ~/Desktop/report.html
```

### Full help

```
$ gitpulse --help

Usage: gitpulse [OPTIONS] COMMAND [ARGS]...

  GitPulse — Terminal Git Analytics Dashboard.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  analyze  Analyze REPO and display rich terminal statistics.
  report   Generate an HTML report for REPO without terminal output.
```

```
$ gitpulse analyze --help

Usage: gitpulse analyze [OPTIONS] [REPO]

  Analyze REPO and display rich terminal statistics.

Options:
  -n, --max-commits INTEGER  Maximum number of commits to analyze. [default: 5000]
  -r, --report               Also generate an HTML report.
  -o, --output TEXT          HTML report output path.  [default: gitpulse-report.html]
  --help                     Show this message and exit.
```

---

## 📁 Project Structure

```
clauder/
├── gitpulse/
│   ├── __init__.py       # Package metadata
│   ├── cli.py            # Click CLI entry point
│   ├── analyzer.py       # Git repository analysis engine
│   ├── visualizer.py     # Rich terminal rendering
│   └── reporter.py       # Self-contained HTML report generator
├── pyproject.toml        # Package configuration
├── requirements.txt      # Runtime dependencies
└── README.md
```

### Module responsibilities

| Module | Role |
|--------|------|
| `analyzer.py` | Walks commit history, extracts contributor stats, file churn, time patterns, calendar data, and word frequencies |
| `visualizer.py` | Renders every metric as Rich tables, progress bars, bar charts, and the ASCII calendar |
| `reporter.py` | Generates a fully self-contained HTML file with Chart.js visualizations and an interactive calendar heatmap |
| `cli.py` | Click-based CLI — exposes `analyze` and `report` commands with options |

---

## ⚙️ How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  git repo    │────▶│  analyzer    │────▶│   RepoStats      │
│  (any path)  │     │  (gitpython) │     │   dataclass      │
└──────────────┘     └──────────────┘     └────────┬─────────┘
                                                    │
                          ┌─────────────────────────┤
                          ▼                         ▼
                 ┌──────────────────┐    ┌─────────────────────┐
                 │  visualizer.py   │    │    reporter.py       │
                 │  (Rich tables,   │    │  (self-contained     │
                 │   charts, ASCII) │    │   HTML + Chart.js)   │
                 └──────────────────┘    └─────────────────────┘
                          │                         │
                          ▼                         ▼
                   Terminal output           *.html file
```

**Analysis pipeline:**

1. `gitpython` opens the repository and iterates commits up to `--max-commits`
2. Each commit contributes to: calendar data, contributor stats, hour/weekday histograms, and a word-frequency counter (stop-words filtered)
3. A separate `git log --numstat` pass populates per-author line addition/deletion counts efficiently
4. File hotspots are built by counting how many commits touched each file path
5. Streak detection runs a single pass over the sorted set of active dates
6. All data lands in a single `RepoStats` dataclass, passed to either `render_all()` or `generate_html_report()`

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [Rich](https://github.com/Textualize/rich) | ≥ 13.0 | Beautiful terminal output — tables, panels, progress bars |
| [GitPython](https://gitpython.readthedocs.io) | ≥ 3.1 | Git repository access without shelling out |
| [Click](https://click.palletsprojects.com) | ≥ 8.1 | CLI argument parsing and command routing |

No network access is required at analysis time. The HTML report fetches Chart.js from a CDN when opened in a browser.

---

## 🤝 Contributing

Contributions are welcome! Ideas for future features:

- [ ] `--since` / `--until` date filtering
- [ ] JSON output mode for pipeline integration
- [ ] Side-by-side repo comparison (`gitpulse compare repo-a repo-b`)
- [ ] Detect and highlight refactor vs. feature vs. fix commit patterns
- [ ] Export calendar as SVG

To contribute:

```bash
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .
```

---

## 📜 License

MIT © [Kareem](https://github.com/kareemrt)
