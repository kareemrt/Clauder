# ⚡ Pulsar

> **Git Repository Heartbeat Visualizer** — See the living pulse of any codebase, right in your terminal.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)

```
  ██████╗ ██╗   ██╗██╗     ███████╗ █████╗ ██████╗
  ██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗██╔══██╗
  ██████╔╝██║   ██║██║     ███████╗███████║██████╔╝
  ██╔═══╝ ██║   ██║██║     ╚════██║██╔══██║██╔══██╗
  ██║     ╚██████╔╝███████╗███████║██║  ██║██║  ██║
  ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
```

---

## What Is Pulsar?

Every git repository has a **heartbeat** — the rhythm of commits over time, the hotspots of frantic activity, the long silences between releases. Pulsar makes that heartbeat visible.

Run `pulsar` in any git repository and get:

- **⚡ Animated sparkline** of commit activity across any time window
- **🔥 Hour × weekday heatmap** — find out when your team actually codes
- **👥 Contributor breakdown** — ranked bar charts with line-change stats
- **📁 Hotspot file finder** — which files change most (highest churn = most risk)
- **🌐 Language breakdown** — extension-based language distribution
- **📊 Standalone HTML report** — share a single-file dashboard with your team

All with **zero runtime dependencies** — pure Python + the `git` binary already on your system.

---

## Terminal Output

```
  ◈ Repository : my-awesome-app
  ◈ Branch     : main

  ┌── SUMMARY ─────────────────────────────────────────────────────────────────

  Total commits (all time)        1,842
  Commits (last 90 days)            347
  Lines added (period)           +48,291
  Lines removed (period)         -12,083
  Contributors (active)               9

  ┌── HEARTBEAT — last 90 days ────────────────────────────────────────────────

  Daily pulse (▁ low  ▄ mid  █ peak)

  ▁▁▂▃▅▇█▇▅▃▂▁▁▂▃▄▅▇█▇▅▄▃▂▁▁▂▄▆█▇▅▃▂▁▂▃▄▆█▇▅▄▃▂▁▁▂▃▅▇█▇▅▃▂▁▁▂▄▅▆▇█▇▅▃▂▁

  Weekly totals
  W 1  ████████████                                  12
  W 2  ████████████████████████████████████████████  44
  W 3  ████████████████████████████████████          37
  W 4  ██████████████████████████████████████████    42
  W 5  ████████████████████████                      24
  W 6  ████████████████████████████████████████████  44
  W 7  ██████████████████████████████████████        38
  W 8  ████████████████████████████████              32
  W 9  ██████████████████████████████                30
  W10  ████████████████████████                      24
  W11  ████████████████████████████████              32
  W12  ████████████████████████████████████          36
  W13  ████████████████████████                      24

  ┌── ACTIVITY HEATMAP — hour × weekday ───────────────────────────────────────

        Mon  Tue  Wed  Thu  Fri  Sat  Sun
  00:00  ░░   ░░   ░░   ░░   ░░   ░░   ░░
  03:00  ░░   ░░   ░░   ░░   ░░   ░░   ░░
  06:00  ▒▒   ▒▒   ░░   ▒▒   ░░   ░░   ░░
  09:00  ██   ██   ██   ██   █░   ▒▒   ░░
  12:00  ▓▓   ██   ▓▓   ██   ▓▓   ░░   ░░
  15:00  ██   ██   █░   ██   █░   ░░   ░░
  18:00  ▓▓   ▓▓   ▓░   ▓░   ▒▒   ▒▒   ░░
  21:00  ▒▒   ▒▒   ░░   ▒▒   ░░   ░░   ░░

  ┌── CONTRIBUTORS ────────────────────────────────────────────────────────────

  alice                   ████████████████████████████████████   142 commits  40.9%
  bob                     ██████████████████████████             105 commits  30.3%
  carol                   ████████████████                        63 commits  18.2%
  dave                    ████████                                31 commits   8.9%
  eve                     ██                                       6 commits   1.7%

  ┌── HOTSPOT FILES — most frequently changed ─────────────────────────────────

  src/api/routes.py                          ██████████████████████████████  87×
  src/models/user.py                         ████████████████████████        71×
  tests/test_api.py                          ██████████████████████          65×
  src/utils/auth.py                          ████████████████████            58×
  config/settings.py                         ██████████████████              52×

  ┌── LANGUAGE BREAKDOWN ──────────────────────────────────────────────────────

  Python              ████████████████████████████████████████   62.4%  311 files
  JavaScript          ███████████████████                        29.8%  149 files
  YAML                ████                                        5.2%   26 files
  Shell               █                                           1.6%    8 files
  Markdown            █                                           1.0%    5 files

  ◈ Analysis complete. Run with --report to generate an HTML report.
```

---

## HTML Report

Running `pulsar . --report report.html` generates a standalone, dark-themed HTML dashboard with interactive Chart.js charts:

```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ PULSAR                                                   │
│  Git Repository Heartbeat Visualizer                        │
│  my-awesome-app · main · last 90 days                       │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│  TOTAL   │  RECENT  │  LINES   │  LINES   │  CONTRIBUTORS  │
│ COMMITS  │ COMMITS  │  ADDED   │ REMOVED  │    ACTIVE      │
│  1,842   │   347    │ +48,291  │ -12,083  │       9        │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│  ⚡ Heartbeat — Daily Commit Activity                        │
│  ╭─────────────────────────────────────────────────────╮   │
│  │ ▃▅▇█▇▅▃▂▁▂▄▆█▇▅▃▂▁▂▄▆█▇▅▄▃▂▁▂▄▅▆▇█ (bar chart)   │   │
│  ╰─────────────────────────────────────────────────────╯   │
├──────────────────────────┬──────────────────────────────────┤
│  👥 Contributors          │  🌐 Language Breakdown          │
│  ╭──────────────────╮    │  ╭──────────────────╮           │
│  │  (doughnut chart)│    │  │  (doughnut chart)│           │
│  ╰──────────────────╯    │  ╰──────────────────╯           │
├──────────────────────────┴──────────────────────────────────┤
│  🔥 Activity Heatmap — Hour × Weekday (stacked bar chart)   │
│  ╭──────────────────────────────────────────────────────╮  │
│  │ Mon Tue Wed Thu Fri Sat Sun   (stacked by hour)      │  │
│  ╰──────────────────────────────────────────────────────╯  │
├──────────────────────────┬──────────────────────────────────┤
│  📁 Hotspot Files         │  💬 Commit Message Words        │
│   src/api/routes.py  87× │   [auth] [api] [fix] [refactor] │
│   src/models/user.py 71× │   [test] [user] [config] [dep]  │
│   tests/test_api.py  65× │   [migration] [schema] [cache]  │
└──────────────────────────┴──────────────────────────────────┘
```

---

## Installation

### Option 1 — pip install (from this repo)

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -e .
```

Then use it anywhere:

```bash
pulsar /path/to/any/git/repo
```

### Option 2 — Run directly

```bash
python -m pulsar /path/to/any/git/repo
```

No install needed — just clone and run.

---

## Usage

```
usage: pulsar [REPO] [options]

positional arguments:
  REPO            path to the git repository (default: current directory)

options:
  --days N        number of days to analyse (default: 90)
  --report FILE   write a standalone HTML report to FILE
  --no-color      disable ANSI colour output
  --version       show version and exit
  -h, --help      show this help message and exit
```

### Examples

```bash
# Analyse current directory, last 90 days
pulsar .

# Analyse a specific repo for the last 6 months
pulsar ~/projects/my-app --days 180

# Generate an HTML report to share with your team
pulsar . --report team-report.html

# Plain text (great for piping or logging)
pulsar . --no-color > report.txt

# Run without installing
python -m pulsar .
```

---

## Project Structure

```
clauder/
├── pulsar/
│   ├── __init__.py       # version info
│   ├── __main__.py       # python -m pulsar entry point
│   ├── analyzer.py       # git history extraction (subprocess + regex)
│   ├── renderer.py       # ANSI terminal rendering
│   ├── report.py         # standalone HTML generation
│   └── cli.py            # argparse CLI
├── setup.py              # pip install support
├── requirements.txt      # (none — zero runtime deps)
└── README.md
```

### Architecture

```
  git repository
       │
       ▼
  ┌─────────────────┐
  │   analyzer.py   │  git log --shortstat + git ls-files
  │                 │  → daily counts, author stats,
  │                 │    file churn, hourly matrix
  └────────┬────────┘
           │  stats dict
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌──────────┐  ┌──────────┐
│renderer  │  │ report   │
│  .py     │  │   .py    │
│          │  │          │
│ ANSI art │  │ HTML +   │
│ sparkline│  │ Chart.js │
│ heatmap  │  │ dashboard│
└──────────┘  └──────────┘
    │
    ▼
  cli.py  (argparse, wires it all together)
```

---

## How It Works

Pulsar uses only Python's standard library and the system `git` binary — no heavy frameworks, no network calls.

1. **`analyzer.py`** shells out to `git log --shortstat` with a custom format string, parsing each commit's timestamp, author, subject line, and line-change counts in a single pass. File churn comes from `git log --name-only`, and language breakdown from `git ls-files`.

2. **`renderer.py`** maps daily commit counts to Unicode block characters (`▁▂▃▄▅▆▇█`) for the sparkline, and uses a `(weekday, hour)` matrix for the activity heatmap. ANSI escape codes provide colour without any external library.

3. **`report.py`** embeds all stats as a JSON blob in a self-contained HTML file, then drives Chart.js (loaded from CDN) to render interactive bar, doughnut, and stacked-bar charts.

4. **`cli.py`** ties it together with `argparse` — no framework overhead.

---

## Why Pulsar?

| Tool | Terminal output | HTML report | Zero deps | Any repo |
|------|:-:|:-:|:-:|:-:|
| `git log --stat` | plain text | ✗ | ✓ | ✓ |
| GitHub Insights | ✗ | ✓ | hosted | GitHub only |
| `gitstats` | ✗ | ✓ | ✗ | ✓ |
| **Pulsar** | **rich ANSI** | **✓** | **✓** | **✓** |

---

## Requirements

- Python 3.9+
- `git` binary (any modern version)
- That's it.

---

## License

MIT — use it, fork it, embed it, ship it.

---

*Built by Claude (claude-code) as an experiment in autonomous software creation.*
