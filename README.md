# ⚡ GitPulse

**Terminal Analytics Dashboard for Git Repositories**

GitPulse mines your git history and renders it as a beautiful, information-dense terminal dashboard — no external APIs, no configuration files, no internet required. Point it at any local repository and get instant insight into how the codebase evolves.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📅 **Contribution Heatmap** | GitHub-style 52-week activity grid rendered directly in your terminal |
| 📈 **Commit Velocity** | ASCII bar chart showing commit frequency over the repository's lifetime |
| 🔥 **File Churn Analysis** | Ranked list of files that change most often — your code's hotspots |
| 👥 **Author Contributions** | Per-author commit counts with colour-coded distribution bars |
| 🌐 **Language Distribution** | File extension breakdown as a stacked colour bar |
| 🕐 **Peak Commit Hours** | Hour-of-day activity histogram to spot team rhythms |
| 🔗 **Co-Change Pairs** | Files that frequently change together (coupling signals) |
| 📊 **HTML Export** | Standalone interactive report with Chart.js graphs |

---

## 📸 Dashboard Preview

```
╭──────────────────────────────  ⚡ GitPulse — my-project  ──────────────────────────────╮
│                                                                                         │
│  Commits        Authors          Files           Age                                    │
│  1,847          12               234             847 days                               │
│  Lines Added    Lines Removed    Commits/Day     Active                                 │
│  +128,341       -43,892          2.18            2022-01-03 → 2024-04-25                │
│                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────╯

Contribution Heatmap (last 52 weeks)
     Jul         Aug             Sep                 Oct             Nov
Dec                 Jan             Feb             Mar                 Apr
Su  ░   ░ ▒ ░   ░ ░ ▓ ▒ ░ ░   ▒ ░ ░ ▒ █ ▒ ░   ░ ▒ ▒ ░ ░   ░ ░ ▒ ░ ░ ░ ░
Mo  ▒ ░ ▓ ▓ ░ ░ ▒ ░ ▓ ▓ ▒ ░ ▒ █ ▒ ▒ ░ ▒ ▓ ░ ▓ ▒ ░ ▓ ▒ ░ ▒ ░ ▓ ▒ ░ ░ ░ ░
Tu  ░ ░ ▒ ▒ ▒ ░ ▒ ▒ ▒ ░ ▒ ▒ ░ ░ ▒ ▒ ▒ ░ ░ ▒ ░ ▒ ░ ░ ░ ▒ ░ ░ ░ ░ ▒ ░ ░ ░
We  ░ ░ ▒ █ ░ ░ ░ ▒ ▓ ▓ ░ ▒ ▒ ░ ░ ▒ ▒ ░ ▒ ▒ ░ ░ ▒ ▒ ░ ░ ▒ ░ ░ ▒ ▒ ▒ ░ ░
Th  ▓ ▒ ░ ░ ▒ ░ ▒ ░ ░ ░ ▒ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ▒ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░
Fr  ░ ░ ░ ░ ░ ░ ▒ ▒ ░ ░ ░ ░ ▒ ░ ░ ░ ░ ░ ▒ ░ ░ ░ ░ ▒ ░ ░ ▒ ░ ░ ░ ▒ ░ ░ ░
Sa                          ░           ░                   ░

    Less   ░ ▒ ▓ █ More

Commit Velocity Over Time
  14 │          █                               █   █
  12 │          █  █                         █  █   █
  10 │          █  █  █                   █  █  █   █  █
   8 │       █  █  █  █              █    █  █  █   █  █
   6 │    █  █  █  █  █  █      █   █    █  █  █   █  █  █
   4 │ █  █  █  █  █  █  █  █  █   █    █  █  █   █  █  █
   2 │ █  █  █  █  █  █  █  █  █   █    █  █  █   █  █  █
     └─────────────────────────────────────────────────────
      Jan'22  May'22  Sep'22  Jan'23  May'23  Sep'23  Jan'24

🔥 Most Changed Files
 src/api/handlers.py      ████████████████████████████████████████  47 changes
 tests/test_handlers.py   ██████████████████████████████████░░░░░░  39 changes
 src/models/user.py       █████████████████████████░░░░░░░░░░░░░░░  29 changes
 requirements.txt         ████████████████████░░░░░░░░░░░░░░░░░░░░  24 changes
 README.md                ████████████████░░░░░░░░░░░░░░░░░░░░░░░░  19 changes

Author Contributions
  #   Author              Commits   Share   Distribution
 ──────────────────────────────────────────────────────────────────
  1   Alice Chen              847   45.9%   ████████████████████████░░░░░░░░░░░░░
  2   Bob Martinez            421   22.8%   █████████████░░░░░░░░░░░░░░░░░░░░░░░░
  3   Carol Kim               298   16.1%   █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  4   David Park              181    9.8%   █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  5   Eve Wilson              100    5.4%   ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Git

### Install dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install rich click
```

### Run

```bash
# Analyse the current directory
python gitpulse.py

# Analyse any repo
python gitpulse.py /path/to/your/repo

# Also export an interactive HTML report
python gitpulse.py /path/to/your/repo --export

# Customise how many commits and weeks to show
python gitpulse.py . --limit 5000 --weeks 26
```

---

## 📂 Project Structure

```
gitpulse/
│
├── gitpulse.py            ← Entry point (run this)
├── requirements.txt
│
└── gitpulse/
    ├── __init__.py
    ├── analyzer.py        ← Git data extraction & statistical analysis
    ├── charts.py          ← Rich-powered ASCII chart renderers
    ├── cli.py             ← Click CLI, orchestration, spinner UX
    └── report.py          ← Standalone HTML report generator (Chart.js)
```

---

## 🧮 How It Works

```
Git History
    │
    ▼
analyzer.py ──────────────────────────────────────────────┐
  • git log (commit metadata, timestamps, authors)         │
  • git log --name-only (per-commit file lists → churn)    │
  • git ls-files (tracked files → language stats)          │
  • git log --numstat (line additions / deletions)         │
    │                                                      │
    ▼                                                      │
  Statistical transforms:                                  │
    • Build 52×7 heatmap grid                              │
    • Bucket commits into velocity time series             │
    • Co-change pair counting (O(k²) per commit)           │
    • Peak-hour histogram, author aggregation              │
    │                                                      ▼
    └──────────────► charts.py + report.py
                       • Rich Text/Table/Panel rendering
                       • ASCII art bar/sparkline/heatmap
                       • Self-contained Chart.js HTML
```

---

## ⚙️ CLI Reference

```
Usage: gitpulse.py [OPTIONS] [REPO_PATH]

  Analyse a git repository and render a beautiful terminal dashboard.

  REPO_PATH defaults to the current directory.

Options:
  -l, --limit INTEGER   Max commits to analyse.  [default: 2000]
  -w, --weeks INTEGER   Heatmap weeks to display.  [default: 52]
  -e, --export          Export HTML report.
  -o, --output TEXT     HTML output path.  [default: gitpulse_report.html]
  --no-banner           Skip the ASCII banner.
  --help                Show this message and exit.
```

---

## 📊 HTML Report

Running with `--export` produces a fully self-contained HTML file (no server needed) featuring:

- **Interactive Chart.js visualisations** — hover tooltips, responsive resize
- **Contribution heatmap** — each cell shows exact date and commit count on hover
- **Velocity line chart** — smooth curve with fill area
- **Language doughnut** — proportional colour breakdown
- **Author bar chart** — horizontal bars for easy comparison
- **File churn bar chart** — sorted by change frequency

Open `gitpulse_report.html` in any browser — no internet connection required after generation.

---

## 🔬 Analytics Explained

### File Churn
Files that change frequently are either central to your product or accumulating technical debt. GitPulse counts how many commits touched each file.

### Co-Change Pairs
When files A and B change together in N commits, they likely share hidden coupling. High co-change scores between unrelated files often signal missing abstractions.

### Commit Velocity
Buckets all commits into equal time windows and plots them. Spikes reveal crunch periods; valleys reveal team holidays, company pivots, or rewrites-in-progress.

### Peak Hours
Aggregates commit timestamps by UTC hour. Useful for understanding your team's working rhythm and for setting merge windows.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-idea`
3. Commit your changes: `git commit -m "Add my idea"`
4. Push to the branch: `git push origin feature/my-idea`
5. Open a Pull Request

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ by an AI that loves data &amp; beautiful terminals.<br>
<strong>⚡ GitPulse</strong> — because your git history deserves more than <code>git log</code>.
</div>
