# Clauder

```
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|

  Git Repository Intelligence Dashboard
```

> Beautiful terminal analytics for any git repository — contribution heatmaps,
> author leaderboards, file churn rankings, language breakdowns, and live
> activity feeds, all in one gorgeous CLI dashboard.

![Python](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)

---

## Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| Panel | What it shows |
|---|---|
| **Overview** | Repo name, commits, contributors, active days, age, branches & tags |
| **Heatmap** | 26-week GitHub-style contribution calendar with colour intensity |
| **Timeline** | Sparkline bar chart of daily commit activity for the past 30 days |
| **Authors** | Ranked leaderboard with per-author bars and percentage shares |
| **Languages** | Lines-changed breakdown by file extension with coloured activity bars |
| **Churn** | Hottest files ranked by change frequency with heat-colour bars |
| **Pulse** | Scrollable activity feed of the 20 most recent commits |

All output is rendered with [Rich](https://github.com/Textualize/rich) — full
24-bit colour, Unicode block characters, and clean table borders.  Zero
external APIs.  Works entirely from your local `.git` directory.

---

## Screenshots

### Full dashboard — `clauder report`

```
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|

                  Git Repository Intelligence Dashboard

──────────────────────────── Repository Overview ─────────────────────────────

          ╭─────┬──────────────────┬──────────────────────────────╮
          │ 📦  │ Repository       │ my-saas-app                  │
          │ 🔖  │ Total Commits    │ 1,847                        │
          │ 👥  │ Contributors     │ 12                           │
          │ 📅  │ Active Days      │ 312 (68.4%)                  │
          │ ⏱   │ Age              │ 456 days                     │
          │ 🌿  │ Branches         │ 8                            │
          │ 🏷   │ Tags             │ 14                           │
          │ 🏆  │ Top Author       │ Alice Chen (423)             │
          ╰─────┴──────────────────┴──────────────────────────────╯
```

### Contribution Heatmap — `clauder heatmap`

```
───────────────────────── Contribution Heatmap ──────────────────────────

          J   F   M    A   M   J
  Mo   ░░░░▒▒▓▓████████████████████░░░▓▓████████████████████████
  Tu   ░░░▒▒▒▓▓██████████████████████████████████████████████
  We   ░░░░░▒▒▓▓██████████████████████████████████████████░░
  Th   ░░░░░░▒▒▓▓████████████████████████████████████████░░
  Fr   ░░░░░░░▒▒▓█████████████████████████████████████░░░░
  Sa   ░░░░░░░░░▒▒▒▓▓████████████████████░░░░░░░░░░░░░░░
  Su   ░░░░░░░░░░░▒▒▒▓▓██████████████████░░░░░░░░░░░░░░

  Less  ░▒▓██  More

  (empty = no commits  ░ = 1-2  ▒ = 3-4  ▓ = 5-6  █ = 7+ commits/day)
  In a colour terminal each level renders as a distinct shade of green.
```

### Author Leaderboard — `clauder authors`

```
─────────────────────────── Author Leaderboard ───────────────────────────

    #   Author               Commits    Share   Contribution
 ─────────────────────────────────────────────────────────────────────────
    1   Alice Chen               423    22.9%   █████████▊░░░░░░░░░░░░░░
    2   Bob Martinez             381    20.6%   ████████▉░░░░░░░░░░░░░░░
    3   Carol Williams           302    16.3%   ███████░░░░░░░░░░░░░░░░░
    4   Dan Kim                  274    14.8%   ██████▎░░░░░░░░░░░░░░░░░
    5   Eve Thompson             251    13.6%   █████▊░░░░░░░░░░░░░░░░░░
```

### File Churn — `clauder churn`

```
──────────────────────── File Churn — Hottest Files ──────────────────────

   #   File                            Changes   Heat
 ─────────────────────────────────────────────────────────────────────────
   1   src/api/routes.py                   147   ████████████████████████
   2   src/auth/views.py                   132   █████████████████████▌░░
   3   frontend/app.js                     119   ███████████████████▌░░░░
   4   tests/test_api.py                    98   ████████████████░░░░░░░░
   5   src/utils/helpers.py                 87   ██████████████░░░░░░░░░░
```

### Timeline Sparkline — `clauder timeline`

```
────────────────────── Commit Activity — Last 30 Days ───────────────────

     ▄▁▆ █  ▆▃▃▁▁▃▃▆▄  ▃▃▄▃▁▂▃▅▄▃▃▂▁

  08 May13 May18 May23 May28 May02 Jun
```

### Language Activity — `clauder langs`

```
───────────────────────────── Language Activity ─────────────────────────

  Ext           Lines Δ     Share   Activity
 ──────────────────────────────────────────────────────────────────────
  .py            12,880     48.2%   ████████████████████████████████
  .js             5,440     20.3%   ████████████████░░░░░░░░░░░░░░░░
  .ts             3,920     14.7%   ████████████░░░░░░░░░░░░░░░░░░░░
  .css            2,100      7.9%   ██████▍░░░░░░░░░░░░░░░░░░░░░░░░░
  .md             1,380      5.2%   ████▎░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

### Recent Activity Feed — `clauder pulse`

```
──────────────────────── Recent Commits — Activity Pulse ────────────────

  When      Author           Message
 ────────────────────────────────────────────────────────────────────────
  2h ago    Alice Chen       feat: add OAuth2 integration
  5h ago    Bob Martinez     fix: resolve race condition in async handler
  1d ago    Carol Williams   refactor: extract validation logic
  1d ago    Dan Kim          test: add unit tests for payment service
  2d ago    Eve Thompson     docs: update API reference for v2 endpoints
```

---

## Installation

**From PyPI (once published):**

```bash
pip install clauder
```

**From source:**

```bash
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .
```

**Requirements:**

- Python 3.9 or newer
- `git` available on your `PATH`
- A terminal with 256-colour or truecolor support (iTerm2, Windows Terminal,
  Ghostty, Alacritty, etc.) for the best visual experience

---

## Usage

Point Clauder at any git repository — the current directory by default:

```bash
# Full dashboard (all panels)
clauder report

# Full dashboard for a different repo
clauder report /path/to/some-repo

# Individual panels
clauder overview
clauder heatmap
clauder authors
clauder churn
clauder langs
clauder timeline
clauder pulse
```

Any command that accepts a `PATH` argument will default to `.` when omitted.

---

## Commands

```
clauder [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  report    Full dashboard — all panels in one view.
  overview  Repository overview card.
  heatmap   52-week GitHub-style contribution heatmap.
  timeline  Sparkline commit activity for the last 30 days.
  authors   Author leaderboard and contribution breakdown.
  langs     Language activity breakdown by lines changed.
  churn     File churn — the hottest (most-changed) files.
  pulse     Recent commit activity feed.
```

---

## Architecture

```
clauder/
│
├── src/clauder/
│   ├── __init__.py          # package metadata & version
│   ├── cli.py               # Click command definitions
│   ├── git_analysis.py      # git log parsing & data aggregation
│   └── visualize.py         # Rich terminal rendering
│
├── pyproject.toml           # PEP 517/518 build config + entry-point
├── requirements.txt         # pinned runtime deps
└── README.md
```

### Data flow

```
  git log (subprocess)
       │
       ▼
  git_analysis.py
  ┌────────────────────────────────────┐
  │  load_commits()                    │  → raw CommitRecord list
  │  load_file_churn()                 │  → filepath → change count
  │  load_language_stats()             │  → ext → lines changed
  │  analyze() → RepoStats             │  → fully aggregated snapshot
  └────────────────────────────────────┘
       │
       ▼
  visualize.py
  ┌────────────────────────────────────┐
  │  render_overview()                 │  Rich Table (overview card)
  │  render_heatmap()                  │  Unicode block calendar
  │  render_timeline()                 │  sparkline bar chart
  │  render_authors()                  │  ranked table + progress bars
  │  render_languages()                │  extension breakdown
  │  render_file_churn()               │  heat-ranked file list
  │  render_pulse()                    │  commit activity feed
  │  render_full_report()              │  all of the above
  └────────────────────────────────────┘
       │
       ▼
  Rich Console → terminal
```

### Key design decisions

- **Zero network calls.** All data is read directly from local `.git` history
  via `subprocess` + `git log`.  No GitHub API tokens or internet access required.
- **Single-pass parsing.** Commit records are extracted in one `git log` pass
  using a custom field separator (`\x1f`) — no temp files or multiple subprocesses.
- **Graceful degradation.** Every panel checks for empty data and renders a
  friendly placeholder rather than crashing.  Works on repos with a single commit.
- **Rich for rendering.** `Table`, `Text`, and styled strings handle layout,
  wrapping, and colour declaratively — no manual ANSI escape codes.
- **Read-only.** Clauder never writes to your repository.

---

## Contributing

Contributions are welcome.  To get started:

```bash
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .
```

**Ideas for new panels / features:**

- `clauder diff <branch>` — compare two branches side-by-side
- `clauder streaks` — longest commit streak per author
- `clauder velocity` — rolling 30-day commit rate trend
- Export panels to SVG / PNG for embedding in docs
- Config file (`~/.clauderrc`) for custom colour schemes

Please open an issue before starting significant work so we can discuss the approach first.

---

## License

MIT © [kareemrt](https://github.com/kareemrt/clauder)
