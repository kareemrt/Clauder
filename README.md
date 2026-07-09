# 💓 CodePulse

> **Git Repository Health Visualizer** — beautiful terminal analytics for any git repo

```
💓 CodePulse — analyzing your-repo …

╭──────────────────────────────────────────────────────────────────────╮
│ REPOSITORY OVERVIEW                                                  │
╰──────────────────────────────────────────────────────────────────────╯
  📊  Total Commits        1,247
  👥  Contributors         23
  📁  Files Changed        389
  ➕  Lines Added          +84,391
  ➖  Lines Removed        -31,204
  📅  Active Days          312
  ⏳  Repo Age             2y 4m
  🔥  Most Active Day      Wednesday
```

---

## ✨ What Is CodePulse?

CodePulse is a **zero-dependency*** Python CLI that turns a bare `git log` into a rich, full-color terminal dashboard. Point it at any repository and get instant insights: who's driving the project, which files are fragile, when your team is most productive, and where the biggest risks hide.

> *Only dependency is `click` for the CLI interface — all visualizations are pure Python.*

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🗓️ **Contribution Heatmap** | GitHub-style calendar showing commit density over time |
| ⏰ **Hourly Activity Chart** | When does your team actually work? Reveal night-owl vs. 9-to-5 patterns |
| 📅 **Weekly Rhythm** | Which days see the most commits — and which are ghost towns |
| 🏷️ **Commit Type Breakdown** | Automatic categorization: features / fixes / docs / tests / refactors |
| 👥 **Contributor Leaderboard** | Ranked by commits, insertions, deletions, and unique files touched |
| 🔥 **Hotspot Files** | Files with the highest churn — prime candidates for refactoring or more tests |
| 🌐 **Language Breakdown** | Which file types are changing most, ranked by total churn |
| 📈 **Monthly Trend Sparkline** | At-a-glance trajectory of project activity over time |
| 📝 **Markdown Report** | Export a full `.md` report with tables and charts for your team |

---

## 📸 Screenshots

### Contribution Heatmap
```
╭──────────────────────────────────────────────────────────────────────╮
│ CONTRIBUTION HEATMAP                                                 │
╰──────────────────────────────────────────────────────────────────────╯
     Oct    NovNov      Dec      JanJan    FebFeb    MarMar      AprApr
  Mon · · ░ ░ · · ░ ░ · · · · · · · · · · · · · ░ · · · · · · · ░ ░ ░ █
      ░ · · · · ░ ░ · · ░ · · · · · · · · · · · ░ ░ · · · · ░ ░ · ░ ░ ▒
  Wed · ░ ░ · · ░ ░ · · · · · ░ · · · · · · · · ░ ░ · ░ ░ · · ░ ▒ · · ·
      · · ░ · · ▒ · · · · · · · · · ░ · · · · · ░ ░ · · · ░ · · ░ · · ░
  Fri · · · · · · ░ · · · · · · · · · · · · ░ · ░ · · · ░ ░ ░ · · ░ ░ ▓
      · · · · · · · · · · ░ · · · · · · ░ · ░ ░ · · · · · · · · · · ░ ▒
      · · · · · · · · · · · · · · · · ░ · · · · · ▒ · · ░ · · · · · ░ ·

  Legend: · none  ░ low  ▓ med  █ high   (200 total commits)
```

### Hourly Activity Pattern
```
╭──────────────────────────────────────────────────────────────────────╮
│ HOURLY ACTIVITY PATTERN                                              │
╰──────────────────────────────────────────────────────────────────────╯
  20 │· · · · ▄ █ ▄ ▄ ▄ ▄ · · ▄ ▄ ▄ · · · · · · · ▄ ▄
     │· · · · ▄ █ ▄ ▄ ▄ ▄ · · ▄ ▄ ▄ · ▄ · · · · · ▄ ▄
     │· · · · ▄ █ █ ▄ ▄ ▄ · · ▄ ▄ ▄ · ▄ · · · ▄ · ▄ ▄
     │· · · · ▄ █ █ ▄ ▄ ▄ · ▄ ▄ ▄ ▄ · ▄ · · · ▄ · ▄ █
     │· · · ▄ █ █ █ █ █ █ ▄ ▄ █ █ █ · ▄ ▄ ▄ ▄ ▄ · █ █
     │▄ · · ▄ █ █ █ █ █ █ ▄ ▄ █ █ █ ▄ █ ▄ ▄ ▄ █ · █ █
     │▄ · · █ █ █ █ █ █ █ █ █ █ █ █ ▄ █ █ █ █ █ · █ █
     │█ · ▄ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ · █ █
     └────────────────────────────────────────────────
      0       4       8       12       16       20
```

### Weekly Rhythm
```
╭──────────────────────────────────────────────────────────────────────╮
│ WEEKLY RHYTHM                                                        │
╰──────────────────────────────────────────────────────────────────────╯
  Mon │█████████████████████████████░│ 38
  Tue │██████████████████░░░░░░░░░░░░│ 24
  Wed │██████████████████████████████│ 39
  Thu │█████████████████████░░░░░░░░░│ 28
  Fri │████████████████████████████░░│ 37
  Sat │█████████████████░░░░░░░░░░░░░│ 23
  Sun │████████░░░░░░░░░░░░░░░░░░░░░░│ 11
```

### 🔥 Hotspot Files (Most Churn)
```
╭──────────────────────────────────────────────────────────────────────╮
│ 🔥 HOTSPOT FILES (top 15)                                            │
╰──────────────────────────────────────────────────────────────────────╯
  File                                          Commits    Churn  Authors
  ──────────────────────────────────────────────────────────────────────
  CHANGES.rst                                   80  🟡 6890       22
  src/click/core.py                             32  🔴 13544      11
  pyproject.toml                                19  🟢 457         6
  tests/test_termui.py                          18  🟡 2874        7
  src/click/termui.py                           14  🟡 2932        8
```

### Top Contributors
```
╭──────────────────────────────────────────────────────────────────────╮
│ TOP CONTRIBUTORS                                                     │
╰──────────────────────────────────────────────────────────────────────╯
  Author                     Commits   Insertions   Deletions   Files
  ─────────────────────────────────────────────────────────────────
  🥇 Kevin Deldycke          75      +5935        -687         55
  🥈 Edward G                21      +4144        -3924        39
  🥉 Edward Girling          12      +822         -579         10
     David Lord              11      +896         -701         27
     jorenham                10      +449         -191          7
```

---

## 🚀 Installation

### Via pip (recommended)
```bash
pip install codepulse
```

### From source
```bash
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .
```

### Requirements
- Python 3.11+
- `click` (auto-installed)
- A POSIX terminal with UTF-8 support (Windows Terminal works too)

---

## 📖 Usage

### Basic analysis (current directory)
```bash
codepulse
```

### Analyze a specific repository
```bash
codepulse /path/to/your/repo
```

### Deeper analysis (more commits)
```bash
codepulse . --max-commits 1000
```

### Export a Markdown report
```bash
codepulse . --report
# Creates CODEPULSE_REPORT.md in the current directory

codepulse . --report --report-path docs/health-report.md
```

### Pipe-friendly output
```bash
codepulse . --no-color | less
```

### Full options
```
Usage: codepulse [OPTIONS] [REPO_PATH]

  💓 CodePulse — Git Repository Health Visualizer

Options:
  -n, --max-commits INTEGER  Maximum number of commits to analyze.  [default: 500]
  --top-files INTEGER        Number of top-churned files to show.   [default: 15]
  --report                   Also write a Markdown report.
  --report-path TEXT         Path for the Markdown report output.   [default: CODEPULSE_REPORT.md]
  --no-color                 Disable ANSI colors (useful for piping).
  --version                  Show the version and exit.
  --help                     Show this message and exit.
```

---

## 🧠 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                         CodePulse Flow                          │
└─────────────────────────────────────────────────────────────────┘

  1. git log --format=%H|%an|%ae|%at|%s   ←── Raw commit metadata
         │
         ▼
  2. git log --numstat                     ←── Per-file insertions/deletions
         │
         ▼
  3. GitAnalyzer                           ←── Parses & structures data
     ├── Commit objects (type-classified)
     ├── FileStats (per-file churn)
     ├── Contributor aggregates
     └── Temporal indexes (hourly/daily/monthly)
         │
         ▼
  4. Visualizer                            ←── Pure-Python ASCII renderer
     ├── Heatmap (week × day grid)
     ├── Bar charts & sparklines
     └── Tables with ANSI colors
         │
         ▼
  5. Reporter (optional)                   ←── Markdown export
     └── CODEPULSE_REPORT.md
```

### Commit Type Classification

CodePulse auto-detects [Conventional Commits](https://www.conventionalcommits.org/) from commit message prefixes:

| Prefix | Type | Icon |
|--------|------|------|
| `feat:` / `feature:` | Feature | ✨ |
| `fix:` | Bug Fix | 🐛 |
| `docs:` | Documentation | 📝 |
| `test:` | Tests | 🧪 |
| `refactor:` | Refactor | ♻️ |
| `chore:` / `ci:` / `build:` | Chore | 🔧 |
| `style:` | Style | 🎨 |
| `perf:` | Performance | ⚡ |
| `merge` (in message) | Merge | 🔀 |
| *(other)* | Other | 📦 |

### Hotspot Risk Levels

Files are colored by total churn (insertions + deletions):

| Symbol | Threshold | Meaning |
|--------|-----------|---------|
| 🟢 | < 300 lines | Stable, low risk |
| 🟡 | 300–1000 lines | Watch this file |
| 🔴 | > 1000 lines | High churn hotspot — needs tests! |

---

## 📋 Example Markdown Report

When `--report` is used, CodePulse writes a `CODEPULSE_REPORT.md` with:

- Summary statistics table
- Commit type breakdown with inline bar charts
- Monthly activity timeline
- Top contributors with add/remove counts
- Hotspot files with risk indicators
- Language breakdown by churn
- Last 20 commits log

---

## 🗂️ Project Structure

```
clauder/
├── codepulse/
│   ├── __init__.py       # Package metadata & version
│   ├── analyzer.py       # Git log parsing & data extraction
│   ├── visualizer.py     # ASCII charts, heatmaps, tables
│   ├── reporter.py       # Markdown report generation
│   └── cli.py            # Click CLI entry point
├── pyproject.toml        # Build & dependency config
├── requirements.txt      # Pinned dependencies
└── README.md             # You are here
```

---

## 🔮 Roadmap

- [ ] `--watch` mode: re-render on new commits (inotify/FSEvents)
- [ ] JSON output mode (`--format=json`) for scripting
- [ ] Team comparison: side-by-side contributor productivity
- [ ] Blame integration: map hotspot files to their primary author
- [ ] GitHub Actions integration: post CodePulse summaries on PRs

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Commit with Conventional Commits: `git commit -m "feat: add JSON output"`
4. Open a pull request

All contributions welcome — especially new visualization ideas!

---

## 📄 License

MIT © [Kareem T](https://github.com/kareemrt)

---

<div align="center">

Built with 💓 by Claude Code

*"Know your codebase like you know your heartbeat."*

</div>
