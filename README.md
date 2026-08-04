# GitPulse

> **Beautiful git repository analytics — terminal-first, zero dependencies.**

```
   ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
  ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
  ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
```

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is GitPulse?

GitPulse transforms any git repository's raw history into a **visual story**.
In seconds you get:

- A **GitHub-style contribution calendar** spanning the last 52 weeks
- An **author leaderboard** showing who drove the most changes
- A **file hotspots** chart revealing which files are touched most often
- A **language breakdown** of everything tracked in the repo
- A **monthly trend** graph of commit velocity over time
- A **self-contained HTML report** — open it in any browser, share it anywhere

Everything is built on Python's standard library — no `pip install` required.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Analyze the current repo
python main.py .

# Analyze any git repository on your machine
python main.py /path/to/your/project

# Generate an HTML report alongside terminal output
python main.py /path/to/your/project --report

# Save the report to a custom path
python main.py . --report --output ~/Desktop/myproject_analytics.html

# Disable colors (for piping / CI logs)
python main.py . --no-color > report.txt
```

---

## Terminal Output

```
  ──────────────────────────────────────────────────────────────────────────────
  Git Repository Analytics  ·  my-awesome-project
  ──────────────────────────────────────────────────────────────────────────────

  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄ 📊 Summary ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄

  Repository:            my-awesome-project
  Branch:                main
  Total commits:         847
  Contributors:          12
  Active since:          2022-03-14
  Last commit:           2026-08-04
  Days active:           1604
  Avg commits/day:       0.53

  ┄┄┄┄┄ 📅 Contribution Calendar (last 52 weeks) ┄┄┄┄┄

       22/08  22/09  22/10  22/11  22/12  23/01  23/02
  Mon  ·  ░  ▒  ·  ▓  ░  ·  ░  ·  ▒  ▓  ░  ·  ·
  Tue  ·  ·  ░  ▒  ·  ·  ▒  ▓  █  ░  ·  ▒  ░  ·
  Wed  ░  ▒  ·  ░  ▒  ▓  ·  ·  ▒  ░  ▓  █  ·  ▒
  Thu  ·  ░  ▒  ·  ·  ░  ▓  ▒  ·  ░  ·  ▓  ▒  ░
  Fri  ▒  ·  ░  ▓  ▒  ·  ░  ·  ▓  ▒  ░  ·  ·  ▓
  Sat  ·  ·  ·  ░  ·  ·  ·  ░  ·  ▒  ·  ·  ░  ·
  Sun  ·  ·  ▒  ·  ·  ░  ·  ·  ▒  ·  ░  ·  ▒  ·

  · none  ░ 1  ▒ 2–3  ▓ 4–6  █ 7+

  ┄┄┄┄┄┄┄┄┄┄┄ 🏆 Contributor Leaderboard ┄┄┄┄┄┄┄┄┄┄┄

  🥇  Alice Chen              ████████████████████████  312
  🥈  Bob Okafor              ██████████████████░░░░░░  203
  🥉  Priya Nair              ████████████░░░░░░░░░░░░  141
    #4  David Kim              ██████░░░░░░░░░░░░░░░░░░   89
    #5  Sam Rivera             ███░░░░░░░░░░░░░░░░░░░░░   57

  ┄┄┄┄┄┄ 🔥 File Hotspots (most frequently changed) ┄┄┄┄

  src/api/auth.py         ████████████████████████░░   48
  src/db/models.py        ███████████████████░░░░░░░   38
  tests/test_api.py       ██████████████░░░░░░░░░░░░   29
  README.md               ████████░░░░░░░░░░░░░░░░░░   17
```

---

## HTML Report

Run with `--report` to get a single-file HTML dashboard you can open in any browser.

The report includes:

| Section | Description |
|---------|-------------|
| **Stat Cards** | Total commits, contributors, files, days active |
| **Contribution Calendar** | 365-day heatmap with hover tooltips |
| **Monthly Trend** | SVG line chart of commit velocity |
| **Top Contributors** | Animated horizontal bar chart |
| **File Hotspots** | Files ranked by change frequency |
| **Language Donut** | Interactive donut chart by file extension |
| **Recent Commits** | Last 20 commits in a searchable table |

The HTML file is **fully self-contained** — no internet connection required to view it, and it looks identical everywhere.

---

## Project Structure

```
clauder/
├── main.py                   # Entry point & CLI argument parser
├── gitpulse/
│   ├── __init__.py           # Package metadata
│   ├── core.py               # Git analysis engine (subprocess-based)
│   ├── terminal.py           # ANSI terminal visualizer
│   └── report.py             # Self-contained HTML report generator
├── requirements.txt          # (empty — zero runtime deps)
└── README.md
```

### Architecture

```
                  ┌──────────────────────────────────────┐
                  │              main.py                  │
                  │  CLI arg parsing → orchestration      │
                  └─────────────┬────────────────┬────────┘
                                │                │
                  ┌─────────────▼──────┐  ┌──────▼───────────────┐
                  │   gitpulse/core.py  │  │ gitpulse/terminal.py │
                  │                    │  │                        │
                  │  GitAnalyzer       │  │  ANSI color output     │
                  │  ├ get_commits()   │  │  Contribution calendar │
                  │  ├ get_file_stats()│  │  Bar charts            │
                  │  ├ get_lang_...()  │  │  Leaderboard           │
                  │  └ analyze() ──────┼──►  Monthly trend         │
                  └────────────────────┘  └────────────────────────┘
                                │
                  ┌─────────────▼──────────────┐
                  │    gitpulse/report.py        │
                  │                              │
                  │  generate_html(data, path)   │
                  │  ├ Stat cards                │
                  │  ├ Calendar heatmap (CSS)    │
                  │  ├ SVG line chart            │
                  │  ├ Bar charts (CSS)          │
                  │  ├ Donut chart (inline SVG)  │
                  │  └ Commits table             │
                  └──────────────────────────────┘
```

---

## How It Works

GitPulse calls `git` directly via `subprocess` — no library wrappers, no
parsing of `.git` internals. All analysis is done by reading the output of:

| git command | Purpose |
|-------------|---------|
| `git log --format=%H\x1f%an\x1f%ae\x1f%ai\x1f%s` | Commit metadata |
| `git log --name-only` | Files changed per commit |
| `git ls-files` | All currently tracked files |
| `git rev-list --count HEAD` | Total commit count |
| `git rev-parse --show-toplevel` | Repo name |

The HTML report uses **zero external CDNs** — all charts are drawn with inline CSS
and SVG, so the file works offline and can be committed directly to a repo.

---

## Options

```
Usage:
    python main.py [REPO_PATH] [--report] [--output FILE] [--no-color]

Arguments:
    REPO_PATH     Path to a git repository  (default: current directory)

Options:
    --report      Generate a self-contained HTML analytics report
    --output      Where to save the HTML report  (default: gitpulse_report.html)
    --no-color    Disable ANSI color codes (good for piping or CI logs)
    --help        Print this help message
```

---

## Requirements

- **Python 3.8+** (uses `dict` ordering, walrus operator not required)
- **git** available in `$PATH`
- Any OS: Linux, macOS, Windows (WSL or Git Bash)
- Zero pip dependencies

---

## Ideas & Roadmap

- [ ] `--since` / `--until` date range filtering
- [ ] `--author` focus mode — deep-dive a single contributor
- [ ] Diff size analysis (lines added/removed per commit)
- [ ] `--watch` mode: re-render on new commits
- [ ] Export to Markdown for embedding in PR descriptions
- [ ] JSON output (`--json`) for piping into other tools

---

## License

MIT — do whatever you want with it.

---

*Built by Claude for [Clauder](https://github.com/kareemrt/clauder)*
