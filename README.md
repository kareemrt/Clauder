# ⚡ GitPulse

> **Terminal Git Repository Analytics Dashboard** — beautiful, instant insights into any git repository.

```
╭──────────────────────────────────────────────────────────────────────────╮
│       ⚡ GitPulse  — Repository Analytics Dashboard                      │
│   📁 my-project  |  🗓 Jan 01, 2022 → Jul 29, 2026  |  ⏳ 1670 days     │
╰──────────────────────────────────────────────────────────────────────────╯
╭────────────────────╮ ╭────────────────────╮ ╭────────────────────╮ ╭───────────────────╮
│       2,847         │ │        1.7          │ │        12          │ │         8         │
│    Total Commits    │ │   Commits / Day     │ │     Branches       │ │  Tags / Releases  │
╰────────────────────╯ ╰────────────────────╯ ╰────────────────────╯ ╰───────────────────╯
```

---

## What is GitPulse?

GitPulse is a zero-config terminal analytics dashboard for git repositories. Point it at any repo and get a rich, color-coded breakdown of activity patterns, contributor stats, file hotspots, and growth trends — all rendered beautifully right in your terminal.

No external services. No API keys. No cloud. Just your local git history.

---

## Features

| Section | What it shows |
|---|---|
| 📅 **Commit Heatmap** | GitHub-style contribution graph for the last 52 weeks |
| 👥 **Contributors** | Top authors with commit counts and share bars |
| 🕐 **Hourly Activity** | When your team codes — morning/afternoon/night patterns |
| 📆 **Day-of-Week** | Weekday vs weekend activity breakdown |
| 🔥 **File Hotspots** | Most frequently changed files (churn indicators) |
| 💬 **Commit Keywords** | Most common words in commit messages |
| 📈 **Growth Timeline** | Monthly commit volume over the last 12 months |
| 🧬 **Language Breakdown** | File distribution by programming language |

---

## Installation

### Option 1: Clone and run directly

```bash
git clone https://github.com/kareemrt/Clauder.git
cd Clauder
pip install -r requirements.txt
python gitpulse.py /path/to/your/repo
```

### Option 2: Run on current directory

```bash
git clone https://github.com/kareemrt/Clauder.git
cd Clauder && pip install -r requirements.txt
cd /your/project
python /path/to/Clauder/gitpulse.py
```

### Requirements

- Python 3.11+
- `rich` library (`pip install rich`)
- Any git repository with at least one commit

---

## Usage

```
usage: gitpulse [-h] [--only SECTION [SECTION ...]] [repo]

⚡ GitPulse — Terminal Git Repository Analytics Dashboard

positional arguments:
  repo                  Path to git repository (default: current directory)

options:
  --only SECTION ...    Show only these sections

Sections: heatmap  contributors  hours  weekdays  hotspots  keywords  timeline  langs
```

### Examples

```bash
# Analyze the current directory
python gitpulse.py

# Analyze a specific repository
python gitpulse.py ~/projects/my-app

# Show only the heatmap and contributor sections
python gitpulse.py ~/projects/my-app --only heatmap contributors

# Check file hotspots and commit keywords
python gitpulse.py . --only hotspots keywords
```

---

## Sample Output

### 📅 Commit Activity Heatmap

The heatmap renders 52 weeks of commit history — exactly like GitHub's contribution graph, but in your terminal:

```
──────────────────── 📅  Commit Activity Heatmap  (last 52 weeks) ────────────────────

     Aug      Sep      Oct      Nov      Dec      Jan      Feb      Mar      Apr
  Mon  ░ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ █ ▓ ░ ░ ░ ▒ ░ ░ ▒ ▓ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▒ ░
       ░ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▓ ░ ░ ░ ▒ ░ ░ ▒ ▓ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▒ ░
  Wed  ░ ░ ▒ ░ ░ ▓ █ ▒ ░ ░ ░ █ █ ░ ░ ░ ▒ ░ ░ ▒ ▓ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▒ ░
       ░ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▓ ░ ░ ░ ▒ ░ ░ ▒ ▓ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▒ ░
  Fri  ░ ░ ░ ▒ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▓ ░ ░ ░ ▒ ░ ░ ▒ ▓ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▒ ░
       ░ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▓ ░ ░ ░ ▒ ░ ░ ▒ ▓ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ▒ ▒ ░
       ░ ░ ░ ░ ░ ░   ░   ░   ░   ░   ░   ░   ░   ░   ░   ░     ░   ░   ░ ▒ ░

  Legend: █ 7+   ▓ 4-6   ▒ 2-3   ░ 1   □ 0
```

### 👥 Top Contributors

```
──────────────────────────────── 👥  Top Contributors ────────────────────────────────

╭─────┬──────────────────────┬────────────┬──────────────────────────────┬────────╮
│   # │ Author               │    Commits │ Share                        │      % │
├─────┼──────────────────────┼────────────┼──────────────────────────────┼────────┤
│   1 │ Alice Chen           │      1,243 │ ████████████████████░░░░░░░░ │  43.7% │
│   2 │ Bob Martinez         │        891 │ ██████████████░░░░░░░░░░░░░░ │  31.3% │
│   3 │ Carol Kim            │        432 │ ███████░░░░░░░░░░░░░░░░░░░░░ │  15.2% │
│   4 │ David Park           │        281 │ ████░░░░░░░░░░░░░░░░░░░░░░░░ │   9.8% │
╰─────┴──────────────────────┴────────────┴──────────────────────────────┴────────╯
```

### 🕐 Commit Activity by Hour

```
────────────────────────── 🕐  Commit Activity by Hour ──────────────────────────

  09:00 ███████████████████░░░░░░░░░░░░░░░░░░░░  187
  10:00 ████████████████████████████████████████  231 ← peak
  11:00 ████████████████████████████████░░░░░░░░  198
  14:00 ██████████████████████████░░░░░░░░░░░░░░  162
  15:00 █████████████████████████████░░░░░░░░░░░  174
  16:00 █████████████████████░░░░░░░░░░░░░░░░░░░  141
  22:00 ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   87

  Peak coding time: ☀️  Morning (around 10:00)
```

### 🔥 File Hotspots

```
──────────────────────── 🔥  File Hotspots (Most Changed) ────────────────────────

    #   File                                     Changes   Heat
 ─────────────────────────────────────────────────────────────────────────────
    1   src/api/auth.py                              247   ██████████████████
    2   src/models/user.py                           189   █████████████░░░░░
    3   tests/test_auth.py                           176   ████████████░░░░░░
    4   src/utils/helpers.py                         134   █████████░░░░░░░░░
    5   package.json                                  98   ██████░░░░░░░░░░░░
```

### 🧬 Language Breakdown

```
─────────────────── 🧬  Language Breakdown (by file count) ────────────────────

  Python            ████████████████████████████████████  142 files  48.3%
  TypeScript        █████████████████░░░░░░░░░░░░░░░░░░░   67 files  22.8%
  JavaScript        ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   31 files  10.5%
  Markdown          ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   18 files   6.1%
  YAML              ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   12 files   4.1%
  CSS               ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    9 files   3.1%
```

---

## Project Structure

```
Clauder/
├── gitpulse/
│   ├── __init__.py       # Package metadata
│   ├── analyzer.py       # Git data extraction engine (subprocess + git)
│   ├── visualizer.py     # Rich terminal rendering layer
│   └── main.py           # CLI entry point and orchestration
├── gitpulse.py           # Root runner (python gitpulse.py ...)
├── requirements.txt      # Dependencies (rich)
└── README.md             # This file
```

### Architecture

```
 ┌─────────────────────────────────────────────────────────┐
 │                    CLI (main.py)                        │
 │  argparse → validate args → orchestrate data + render   │
 └──────────────────┬──────────────────┬───────────────────┘
                    │                  │
         ┌──────────▼──────┐  ┌────────▼──────────┐
         │  analyzer.py    │  │  visualizer.py    │
         │                 │  │                   │
         │  subprocess     │  │  Rich Console     │
         │  ↓              │  │  Tables, Panels   │
         │  git log/ls     │  │  Text, Rules      │
         │  ↓              │  │  Heatmap blocks   │
         │  Pure Python    │  │  Bar charts       │
         │  Counter/dict   │  │  Color themes     │
         └─────────────────┘  └───────────────────┘
```

---

## How It Works

GitPulse uses **only standard `git` subprocesses** — no git library bindings required. It shells out to commands like:

```bash
git log --format="%ci|%ae|%an" --no-merges     # commit timestamps + authors
git log --format="%cd" --date=short              # date-only for heatmap
git log --name-only --format=""                  # files changed per commit
git ls-files                                     # current tracked files
git rev-list --count HEAD                        # total commit count
```

The **analyzer** module extracts raw data, the **visualizer** module renders it beautifully using the `rich` library, and **main.py** orchestrates everything with a clean CLI.

---

## Design Decisions

- **Zero external git libraries** — pure subprocess calls to `git` mean no version compatibility issues
- **Standard library + rich only** — minimal dependency surface, installs in seconds
- **Streaming status indicator** — uses `rich.status` so the user always sees progress
- **Modular sections** — each visualization is independent; use `--only` to focus
- **Terminal-first** — designed for 80+ column terminals; degrades gracefully on narrow displays

---

## Requirements

- Python 3.11+
- Git (any version that supports `--format=` in `git log`)
- `rich >= 13.0.0`

```
pip install rich
```

---

## License

MIT — do whatever you want with it.

---

*Built with [Rich](https://github.com/Textualize/rich) · Runs entirely locally · No data leaves your machine*
