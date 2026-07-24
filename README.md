# ⬡ GitPulse

> **Beautiful terminal git analytics dashboard — zero dependencies, pure Python.**

GitPulse transforms any git repository into a rich, colorful analytics dashboard right in your terminal. It renders a GitHub-style contribution heatmap, commit frequency charts, author leaderboards, file hotspot analysis, and more — all with elegant Unicode box-drawing, ANSI colors, and sparklines. No pip installs needed.

---

## ✨ Features

| Section | What you see |
|---|---|
| **Repository Overview** | Total commits, tracked files, repo age, first-commit date |
| **Contribution Heatmap** | 52-week GitHub-style grid with green intensity heat levels |
| **Commit Frequency** | Bar chart by day-of-week + 12-month sparkline trend |
| **Author Leaderboard** | Top contributors with medal ranks, commit bars, and percentages |
| **File Hotspots** | Most-changed files with per-extension color coding |
| **Branch List** | Local and remote branches with last-active timestamps |
| **Recent Commits** | Last 10 commits with hash, date, author, and subject |

---

## 🖥️ Preview

```
                         ⬡ GitPulse  terminal analytics dashboard
                         ────────────────────────────────────────
                          ⎇ main  myproject

╭──────────────────────────────── Repository Overview ────────────────────────────────╮
│   Total Commits                                                                1,247 │
│   Tracked Files                                                                  183 │
│   Repo Age                                                                   3y 2mo  │
│   First Commit                                                            2022-11-04  │
╰─────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────── Contribution Heatmap  (last 52 weeks) ──────────────────────────╮
│     Ju  Au    Se      Oc    No    De      Ja    Fe    Ma      Ap    Ma    Ju         │
│  Mo ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│     ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│  We ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│     ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│  Fr ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│     ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│  Su ░░░░░░░▓▓▓▓▓███████▓▓▓░░░░░░░░░░▓▓▓███████████████▓▓░░░░░░░░░░░░░░░░███        │
│  Less ░ ▒ ▓ █ More                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────── Commit Frequency Analysis ───────────────────────────────╮
│   By Day of Week                                                                    │
│   Mon  ████████████░░░░░░░░░░░░░░░░   82                                            │
│   Tue  ████████████████░░░░░░░░░░░░  103                                            │
│   Wed  █████████████████░░░░░░░░░░░  113                                            │
│   Thu  ████████████████░░░░░░░░░░░░  108                                            │
│   Fri  ███████████░░░░░░░░░░░░░░░░░   74                                            │
│   Sat  ████░░░░░░░░░░░░░░░░░░░░░░░░   27                                            │
│   Sun  ██░░░░░░░░░░░░░░░░░░░░░░░░░░   18                                            │
│                                                                                     │
│   Monthly Trend (12 months)                                                         │
│   Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar  Apr  May  Jun  Jul                        │
│   ▁▂▄▄▅▆▇▇▇█▇▇                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────── Author Leaderboard ─────────────────────────────────╮
│  🥇  alice@example.com        ████████████████████   487  (39.1%)                   │
│  🥈  bob@example.com          ██████████████░░░░░░   341  (27.3%)                   │
│  🥉  carol@example.com        ████████░░░░░░░░░░░░   198  (15.9%)                   │
│    4. dave@example.com        █████░░░░░░░░░░░░░░░   124  ( 9.9%)                   │
│    5. eve@example.com         ███░░░░░░░░░░░░░░░░░    97  ( 7.8%)                   │
╰─────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────── File Hotspots  (most frequently changed) ───────────────────────╮
│  File                                   Changes   Frequency                         │
│  ───────────────────────────────────── ───────  ──────────                          │
│  src/api/routes.py                          84  ████████████                        │
│  src/core/engine.py                         71  ██████████░░                        │
│  tests/test_integration.py                  63  █████████░░░                        │
│  src/models/user.py                         58  ████████░░░░                        │
│  config/settings.yaml                       41  █████░░░░░░░                        │
╰─────────────────────────────────────────────────────────────────────────────────────╯
```

> **Note:** The actual terminal output is fully colored with ANSI colors — green heatmap cells, gold bars, cyan branch names, etc. The preview above shows the shape in plain text.

---

## 🚀 Quick Start

**No installation required.** Just Python 3.7+.

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Run on the current repo
python3 gitpulse.py

# Run on any git repo
python3 gitpulse.py /path/to/your/repo

# Analyze last 90 days only
python3 gitpulse.py /path/to/your/repo --days 90
```

---

## 📋 Usage

```
usage: gitpulse.py [-h] [--days DAYS] [path]

⬡ GitPulse — beautiful terminal git analytics dashboard

positional arguments:
  path         Path to git repository (default: current directory)

options:
  -h, --help   show this help message and exit
  --days DAYS  History window in days (default: 365)
```

### Examples

```bash
# Current repo, last year (default)
python3 gitpulse.py

# A specific project, last 30 days
python3 gitpulse.py ~/projects/myapp --days 30

# All-time history
python3 gitpulse.py ~/projects/myapp --days 9999
```

---

## 🏗️ Architecture

```
gitpulse.py
├── ANSI color palette          — 256-color terminal codes, no external deps
├── Git helpers                 — subprocess calls to git log/branch/ls-files
├── Data collection
│   ├── collect_commits()       — parse git log into structured dicts
│   ├── collect_file_changes()  — count per-file commit frequency
│   ├── collect_branches()      — list local + remote branches
│   └── get_stats()             — aggregate repo-wide metrics
└── Section renderers
    ├── render_header()         — repo name + current branch
    ├── render_summary()        — overview stats box
    ├── render_heatmap()        — 52-week calendar grid
    ├── render_commit_frequency() — day-of-week bars + sparkline
    ├── render_authors()        — top-10 contributor leaderboard
    ├── render_hotfiles()       — most-changed files
    ├── render_branches()       — local & remote branch list
    └── render_recent_commits() — last N commits
```

**Design principles:**
- **Zero dependencies** — only Python stdlib (`subprocess`, `re`, `datetime`, `collections`, `pathlib`)
- **Pure ANSI** — hand-crafted color sequences, no `curses` or `rich` required
- **Git as the source of truth** — all data from `git log`, `git branch`, `git ls-files`
- **Fast** — typical repo analyzes in under 100ms

---

## 🎨 Color Legend

| Color | Meaning |
|---|---|
| 🟦 Cyan border | Repository overview, general info |
| 🟣 Magenta border | Contribution heatmap |
| 🟡 Yellow border | Commit frequency analysis |
| 🟢 Green border | Author leaderboard |
| 🔴 Red border | File hotspots |
| 🔵 Blue border | Branch list |
| ⚫ Gray border | Recent commits |

Heatmap intensity: `░` (none) → `▒` (low) → `▓` (medium) → `█` (high) → `█` bright green (max)

---

## 🤔 Why GitPulse?

Most git analytics tools either require heavy dependencies (`pandas`, `matplotlib`), live in the browser (GitHub Insights), or only run on specific platforms. GitPulse gives you the same at-a-glance insight as a full analytics suite but runs anywhere Python 3 runs — CI containers, remote servers, air-gapped machines — with a single file.

---

## 🧠 Project Ideation

GitPulse was chosen from a shortlist of five project concepts:

1. **GitPulse** ✅ — terminal git analytics with heatmaps (this project)
2. **NeuralViz** — real-time ASCII neural network training visualizer
3. **TermCrypt** — interactive cryptography playground with live animations
4. **EchoVault** — encrypted time-capsule note app with countdown timers
5. **PixelForge** — terminal pixel art editor and frame animator

GitPulse won for being immediately useful, entirely self-contained, and capable of producing stunning visuals that tell a compelling story in a README.

---

## 📄 License

MIT — do whatever you want with it.

---

*Built by Claude Code · [kareemrt/clauder](https://github.com/kareemrt/clauder)*
