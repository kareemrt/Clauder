# ⚡ CodePulse

> **Instant, beautiful git repository analytics — right in your terminal.**

```
                    ⚡ CodePulse — Git Repository Analytics
                    my-awesome-project
────────────────────────────────────────────────────────────────────────

 ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
 │    1,247    │  │     12      │  │    183      │  │   4,891     │
 │   commits   │  │contributors │  │ active days │  │file changes │
 └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
 ┌─────────────┐
 │    42.3     │
 │commits/month│
 └─────────────┘
```

CodePulse is a **zero-config git analytics tool** that transforms any local repository into a rich, interactive dashboard. Get contributor leaderboards, a GitHub-style heatmap, commit timing patterns, language breakdowns, and hottest files — in seconds.

---

## Features

- **Contribution Heatmap** — GitHub-style 52-week activity grid rendered in the terminal
- **Contributor Leaderboard** — ranked table of authors by commit count + files touched
- **Timing Patterns** — discover when your team actually codes (hour-of-day & day-of-week charts)
- **Language Breakdown** — line counts by file extension with proportional bars
- **Hot Files** — files changed most often (where bugs live)
- **Summary Cards** — total commits, contributors, active days, file changes, velocity
- **HTML Export** — self-contained interactive report with Chart.js visualizations
- **Zero external dependencies** beyond `rich` and `click`

---

## Demo

### Terminal Dashboard

```
────────────────────── Commit Activity (Last 52 Weeks) ──────────────────────
     Jan      Feb      Mar      Apr      May      Jun      Jul
Mon ···░░░░░░░░▒▒▒▒▒▒▓▓▓▓▓▓███████████████▓▓▓▓▓▒▒▒░░░░···············
    ·········░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░···············
Wed ···░░░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░░░···················
    ···░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░·····················
Fri ·············░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░···························

  Less ░░▒▒▓▓██ More
```

### Contributor Leaderboard

```
──────────────────────────── Top Contributors ───────────────────────────────
  #     Author              Commits   Files Touched   First        Last
 ──────────────────────────────────────────────────────────────────────────
  🥇    Alice Chen              487             312   2023-01-04   2024-07-19
  🥈    Bob Müller              321             198   2023-02-11   2024-07-18
  🥉    Carol Osei              189             145   2023-03-01   2024-07-15
   4.   Dan Patel               134              89   2023-05-22   2024-07-12
   5.   Eve Rossi                56              41   2024-01-10   2024-06-30
```

### Timing Patterns

```
╭─── By Hour of Day ───╮  ╭─── By Weekday ────╮  ╭──── Languages ────────────╮
│ 09h ██████████     43│  │ Mon ████████    87 │  │ .py         ███ 42,111 ln│
│ 10h █████████████  61│  │ Tue ████████████211│  │ .js         ██  28,442 ln│
│ 11h ████████████   57│  │ Wed █████████   189│  │ .ts         █   14,210 ln│
│ 14h █████████████  64│  │ Thu █████████   176│  │ .md         ░    5,021 ln│
│ 15h ████████████   58│  │ Fri ██████      122│  │ .yaml       ░    1,233 ln│
│ 16h ████████████   55│  │ Sat ██           34│  │ .sh             312 ln   │
│ 21h ███████        31│  │ Sun █            12│  │                           │
╰──────────────────────╯  ╰───────────────────╯  ╰──────────────────────────╯
```

### HTML Report

The `--html` flag generates a self-contained, **interactive HTML report** with:

- Zoomable Chart.js bar/doughnut charts
- Hoverable contribution heatmap (shows exact date + count on hover)
- Dark-mode GitHub-inspired design
- No server required — open with any browser

---

## Installation

```bash
# 1. Clone this repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run it!
python main.py /path/to/your/repo
```

**Requirements:** Python 3.11+, Git

---

## Usage

```
Usage: main.py [OPTIONS] [REPO_PATH]

  ⚡ CodePulse — Instant git repository analytics.

  Analyze REPO_PATH (defaults to current directory) and display
  a rich terminal dashboard.

Options:
  --html FILE       Export an interactive HTML report to FILE.
  --no-terminal     Skip the terminal dashboard (use with --html).
  --help            Show this message and exit.
```

### Examples

```bash
# Analyze the current directory
python main.py

# Analyze a specific repo
python main.py ~/projects/my-app

# Generate only an HTML report (no terminal output)
python main.py ~/projects/my-app --html report.html --no-terminal

# Terminal dashboard + HTML report
python main.py ~/projects/my-app --html report.html
```

---

## Project Structure

```
codepulse/
├── __init__.py        Package metadata
├── git_data.py        Git subprocess wrappers — raw log parsing, file listing
├── metrics.py         Statistical processing → RepoMetrics dataclass
├── terminal.py        Rich terminal dashboard — heatmap, charts, tables
├── cli.py             Click CLI entry point
└── html_report.py     Self-contained HTML + Chart.js report generator

main.py                Top-level entry point
requirements.txt       Dependencies (rich, click)
README.md              This file
```

### Architecture Overview

```
  git log (subprocess)
       │
       ▼
  git_data.py ──► raw commit list + file extensions
       │
       ▼
  metrics.py ──► RepoMetrics (contributors, heatmap, patterns, hot files)
       │
       ├──► terminal.py ──► Rich console dashboard
       │
       └──► html_report.py ──► self-contained .html file
```

---

## How It Works

1. **Data Collection** (`git_data.py`): Runs `git log` with a custom format to extract commit metadata (hash, author, email, timestamp, changed files) without any external dependencies.

2. **Metric Building** (`metrics.py`): Processes the raw commit list into structured `ContributorStats` and `RepoMetrics` objects — aggregating by author, computing temporal distributions, building the heatmap dict, and ranking hot files.

3. **Terminal Rendering** (`terminal.py`): Uses `rich` to render an emoji-accented dashboard with Unicode block characters for the heatmap (`░▒▓█`), bar charts built from repeated `█` characters, and styled `Table`/`Panel` layouts.

4. **HTML Export** (`html_report.py`): Serializes metrics to JSON and embeds them into a single-file HTML document with inline Chart.js for interactive doughnut and bar charts, plus a JavaScript-rendered heatmap grid with hover tooltips.

---

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **Commits/Month** | Total commits ÷ age in months — a code velocity proxy |
| **Active Days** | Distinct calendar days with at least one commit |
| **Files Touched** | Per-author count of distinct files ever modified |
| **Hot Files** | Files with the highest total change frequency (churn) |
| **Heatmap** | Commit density per day over the trailing 52 weeks |

---

## Ideas for the Future

- [ ] Branch comparison mode (`--compare main feature/xyz`)
- [ ] Team timezone auto-detection from commit timestamps
- [ ] PR cycle time analysis (merge lag histogram)
- [ ] Blame-based ownership map — who owns what percentage of each directory
- [ ] ASCII commit graph rendering
- [ ] `--since` / `--until` date range filtering

---

## License

MIT — use freely, attribution appreciated.

---

*Built by Claude for the Clauder project.*
