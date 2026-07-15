# GitPulse ⚡

> **Repository Vital Signs Dashboard** — beautiful terminal analytics for any git repo, zero dependencies.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![Works Offline](https://img.shields.io/badge/offline-yes-success.svg)](#)

---

## What is GitPulse?

GitPulse turns any git repository into a live terminal dashboard — like a health monitor for your codebase. Run it in seconds, get instant insight into how a project has evolved, who drives it, when code is written, and which files are the busiest.

```
   ██████╗ ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔════╝ ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
  ██║   ██║██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
  ╚██████╔╝██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
  Repository Vital Signs Dashboard
```

---

## Features

| Feature | Description |
|---|---|
| **Activity Sparkline** | 30-day commit velocity rendered as a Unicode sparkline (`▁▂▃▄▅▆▇█`) |
| **Weekly Bars** | Last 16 weeks of commit volume as ASCII bar charts |
| **Commit Timing Heatmap** | When does your team code? Hour-of-day + day-of-week histograms |
| **Contributor Leaderboard** | Ranked contributor table with proportional bars and share percentages |
| **Hot Files** | Most-touched files — find the churn hotspots at a glance |
| **Language Breakdown** | Coloured language bar from tracked file extensions |
| **Streak Counter** | Consecutive days with commits 🔥 |
| **Zero Dependencies** | Pure Python standard library — no pip installs required |

---

## Demo Output

```
  ─────────────────────── OVERVIEW ──────────────────────
  Repository   my-project
  Age          2y 3mo   (2021-08-14 → 2023-11-22)
  Commits      1,847    avg 2.45/day · 72 in last 30d
  Contributors 12
  Lines +/-    +142,038 / -89,221
  Streak       🔥 5 days

  ─────────────────── ACTIVITY · Last 30 Days ───────────
  ▁▁▁▂▁▃▂▄▃▂▁▂▄▅▆▇▆▅▄▃▄▅▆▅▄▃▂▃▄▃
  30d ago                               today

  Weekly commit volume (last 16w)
  W32  ██████████████████              18
  W33  ████████████████████████        24
  W34  ████████████████                16
  W35  ██████████████████████████████  30
  W36  ████████████████████████        23

  ───────────────────── COMMIT TIMING ───────────────────
  Hour (00-23): ░░░░░░▒▒▒▓▓███████▓▓▓▒▒░░
          0 1 2 3 4 5 6 7 8 9 10 11 12...

  Mon  ████████████████████████████    41
  Tue  ██████████████████████████████  45
  Wed  █████████████████████████████   43
  Thu  ████████████████████████████    40
  Fri  ████████████████████████        36
  Sat  ████████████                    18
  Sun  ██████                           9

  ──────────────────── CONTRIBUTORS ─────────────────────
  #   Author              Commits   Share
  ────────────────────────────────────────  ──────
  1   Alice Chen              523   28.3%  ████████████
  2   Bob Nguyen              412   22.3%  █████████
  3   Carol Smith             389   21.1%  █████████
  4   David Park              201   10.9%  █████

  ────────────────── HOT FILES · Most Touched ───────────
  api/routes.py               ███████████████████████████  89
  src/core/engine.py          ████████████████████████     78
  tests/test_integration.py   ████████████████████         64
  config/settings.py          ████████████████             52

  ─────────────────────── LANGUAGES ─────────────────────
  ████████████████████████████████████████████████████████
  █ .py  █ .ts  █ .md  █ .yml  █ .json  █ .sh
```

---

## Installation

### Option 1 — Run directly (no install needed)

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
python main.py /path/to/any/git/repo
```

### Option 2 — Install as a CLI tool

```bash
pip install -e .
gitpulse /path/to/any/git/repo
```

### Option 3 — Analyse the current directory

```bash
# From inside any git repo:
python /path/to/clauder/main.py .
```

---

## Usage

```
usage: gitpulse [-h] [--max-commits N] [--no-color] [--version] [path]

Repository Vital Signs Dashboard

positional arguments:
  path              Path to git repository (default: current directory)

options:
  -h, --help        show this help message and exit
  --max-commits N   Maximum commits to analyse (default: 2000)
  --no-color        Disable ANSI colour output
  --version         show program's version number and exit
```

### Examples

```bash
# Analyse the current repo
gitpulse

# Analyse another repo
gitpulse ~/projects/my-app

# Deep analysis (up to 5000 commits)
gitpulse ~/projects/large-repo --max-commits 5000

# Pipe-friendly plain output
gitpulse --no-color | tee report.txt
```

---

## Project Structure

```
clauder/
├── gitpulse/
│   ├── __init__.py      # Package metadata
│   ├── analyzer.py      # Git log parsing + statistics engine
│   ├── charts.py        # ASCII/Unicode chart rendering primitives
│   ├── dashboard.py     # Dashboard layout + final render
│   └── cli.py           # argparse CLI entry point
├── main.py              # Quick-run entry point: python main.py
├── pyproject.toml       # PEP 517 packaging
├── requirements.txt     # (empty — no runtime deps)
└── README.md
```

### Architecture

```
                    ┌─────────────────────┐
    git log ──────► │   analyzer.py        │  Parses git log --numstat
    git ls-files    │   - commit history   │  Builds statistics dicts
                    │   - contributor map  │
                    │   - file churn       │
                    └──────────┬──────────┘
                               │  stats dict
                    ┌──────────▼──────────┐
                    │   charts.py          │  Pure render functions
                    │   - sparkline()      │  No state, no side effects
                    │   - bar_chart()      │  ANSI colour helpers
                    │   - commit_heatmap() │
                    │   - contributor_table│
                    └──────────┬──────────┘
                               │  strings
                    ┌──────────▼──────────┐
                    │   dashboard.py       │  Assembles sections
                    │   render(stats)      │  Returns single string
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   cli.py             │  argparse + print()
                    └─────────────────────┘
```

---

## How It Works

### 1. Git Log Parsing (`analyzer.py`)
GitPulse runs `git log` with a custom format string to extract commit metadata without any external parsing libraries:

```python
sep = "\x1f"   # ASCII unit-separator — never appears in commit messages
fmt = sep.join(["%H", "%ae", "%an", "%ai", "%s"])
# → git log --format=<fmt> --max-count=2000
```

### 2. Numstat for File Churn
To find hot files, GitPulse runs `git log --numstat` and aggregates lines added/removed per file across recent commits. Files with the most "touches" surface at the top.

### 3. Unicode Sparklines
The sparkline maps daily commit counts to 9 Unicode block characters:

```python
SPARK_CHARS = " ▁▂▃▄▅▆▇█"
# value 0 → ' ', max → '█', interpolated between
```

### 4. ANSI Colour Gradient
Bars and heatmap cells use a gradient that maps value ratios to terminal colours — grey for zero, blue → cyan → yellow → bold green for increasing values.

---

## Requirements

- **Python 3.10+**
- **git** in `PATH`
- A terminal with ANSI escape code support (every modern terminal)
- **Zero Python packages** — no `pip install` needed at runtime

---

## Why GitPulse?

Most git analytics tools require GitHub API access, a browser, or a heavyweight install. GitPulse works:

- **Offline** — reads local git history only
- **Instantly** — no index to build, no database to seed
- **Anywhere** — any git repo on your filesystem
- **Privately** — your commit history never leaves your machine

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built by Claude as an autonomous coding session — from idea to shipped in one run.*
