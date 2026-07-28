# Chronicle — Git Repository Historian

```
  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗ ██████╗██╗     ███████╗
 ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗  ██║██║██╔════╝██║     ██╔════╝
 ██║     ███████║██████╔╝██║   ██║██╔██╗ ██║██║██║     ██║     █████╗
 ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╗██║██║██║     ██║     ██╔══╝
 ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚████║██║╚██████╗███████╗███████╗
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝╚══════╝
```

> **Turn your git history into a beautiful, visual story.**

Chronicle is a Python CLI tool that dives deep into any git repository's commit history and renders it as a rich, colour-coded terminal dashboard — plus an optional standalone HTML report with interactive charts. No servers, no accounts, no API keys. Just `git` and Python.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Commit Timeline** | ASCII bar chart of monthly commit velocity |
| **Contributor Leaderboard** | Ranked table with commit counts, lines changed & activity bars |
| **Hot Files Map** | Identifies the most-churned files with heat indicators |
| **Language Breakdown** | Donut chart of file-type distribution |
| **Project Insights** | Auto-generated narrative observations about the codebase |
| **HTML Report** | Self-contained report with SVG charts, zero dependencies |
| **Beautiful TUI** | Powered by [Rich](https://github.com/Textualize/rich) — colours, panels, tables |

---

## Project Ideas (Why Chronicle?)

During development, five ideas were evaluated:

1. **Chronicle** ← *chosen* — Git repo historian with rich TUI + HTML reports
2. **Mnemosyne** — AI-powered spaced repetition flashcard system
3. **TerminalPoet** — ASCII art poetry generated from code structure
4. **Sentinel** — Smart file watcher with beautiful change visualization
5. **Lexicon** — Codebase vocabulary analyzer mapping domain language evolution

Chronicle was chosen because it is immediately useful on any project, produces genuinely beautiful output, and requires zero external dependencies beyond Python's standard library and `rich`.

---

## Architecture

```
Clauder/
├── chronicle/               ← Main package
│   ├── __init__.py
│   ├── analyzer.py          ← Git data extraction engine
│   │                            - _run_git()       subprocess wrapper
│   │                            - _parse_commits() log + numstat parser
│   │                            - _count_hot_files() file churn counter
│   │                            - _compute_streak() consecutive-day finder
│   │                            - analyze()        returns RepoStats dataclass
│   ├── renderer.py          ← Output rendering
│   │                            - render_terminal() Rich dashboard
│   │                            - render_html()     standalone HTML + SVG report
│   │                            - _svg_bar_chart()  commit timeline SVG
│   │                            - _svg_donut()      language breakdown SVG
│   └── cli.py               ← Click CLI entry point
│
├── run_chronicle.py         ← Quick runner script
├── setup.py                 ← Package install config
└── README.md
```

### Data flow

```
git log --format=... --numstat
         │
         ▼
   _parse_commits()          ← parses raw text into List[Commit]
         │
         ▼
     analyze()               ← aggregates into RepoStats dataclass
         │
    ┌────┴────┐
    ▼         ▼
render_       render_
terminal()    html()
  (Rich)      (SVG + HTML)
```

---

## Installation

**Requirements:** Python ≥ 3.10, Git

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install rich click

# Or install as a package
pip install -e .
```

---

## Usage

```bash
# Analyse the current directory
python run_chronicle.py

# Analyse a specific repo
python run_chronicle.py /path/to/some/project

# Generate a self-contained HTML report
python run_chronicle.py --html

# Save the HTML report to a custom path
python run_chronicle.py --html --out my_report.html

# Disable colour (for piping / logging)
python run_chronicle.py --no-color

# If installed as a package
chronicle /path/to/repo --html
```

---

## Terminal Dashboard Preview

```
  Analyzing /path/to/repo...

  ██████╗██╗  ██╗██████╗  ██████╗ ...
 ██╔════╝██║  ██║██╔══██╗██╔═══██╗...
  (Chronicle ASCII banner in cyan/magenta/blue)

 ╭─────────────╮ ╭──────────────╮ ╭────────────────╮ ╭────────────────╮
 │    1,247    │ │      8       │ │    +84,321     │ │    -31,085     │
 │   Commits   │ │  Authors     │ │  Lines Added   │ │ Lines Removed  │
 ╰─────────────╯ ╰──────────────╯ ╰────────────────╯ ╰────────────────╯

─────────────────────── Commit Timeline ───────────────────────
  2024-01  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   23
  2024-02  ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░   47
  2024-03  ████████████████████████████████████████   98  ← peak
  2024-04  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   41
  ...

─────────────────────── Top Contributors ──────────────────────
  Rank  Author            Commits   Lines    Activity
  🥇   Alice Chen            623   54,210   ████████████████████████
  🥈   Bob Martinez          401   18,940   ████████████████░░░░░░░░
  🥉   Carol Kim             223    9,871   █████████░░░░░░░░░░░░░░░

─────────────────────── Hottest Files ─────────────────────────
  🔴  src/core/engine.py      89   ████████████████████████
  🟡  tests/test_core.py      55   ██████████████░░░░░░░░░░
  🟢  docs/api.md             21   █████░░░░░░░░░░░░░░░░░░░

─────────────────────── Project Insights ──────────────────────
  📅  This project spans 2y 4mo of development.
  🚀  High velocity! Averaging 52.3 commits/month.
  🔥  Longest active streak: 47 consecutive days!
  🔧  Healthy churn ratio — 37% of changes are removals (good sign!).
  🏢  Team project with 8 contributors.
  📊  Peak productivity: 2024-03 with 98 commits.
```

---

## HTML Report Preview

The `--html` flag generates a dark-themed, self-contained HTML report with:

- **Summary cards** — 8 key metrics at a glance
- **Commit timeline** — SVG bar chart (last 24 months)
- **Contributor table** — with inline progress bars
- **Language donut chart** — SVG, no external libraries
- **Hottest files table** — with heat indicators (🔴🟡🟢)
- **Insights grid** — auto-generated observations

All SVG charts are rendered inline — the report is a single `.html` file you can share, email, or commit.

---

## How It Works

### 1. Git Data Extraction (`analyzer.py`)

Chronicle runs a single `git log` command with the `--numstat` flag to get both commit metadata and per-file change statistics in one pass:

```
git log --format="HASH|||AUTHOR|||EMAIL|||DATE|||SUBJECT" --numstat
```

The output is streamed and parsed line-by-line:
- Lines containing `|||` → commit header (hash, author, date, message)
- Lines matching `\d+\s+\d+\s+filename` → file change stats (insertions, deletions, path)

### 2. Statistics Aggregation

From the raw `List[Commit]`, Chronicle computes:

| Metric | Method |
|--------|--------|
| Commit timeline | Group commits by `YYYY-MM` key |
| Hot files | Count how many commits touched each file |
| Contributor stats | Sum commits & lines per author name |
| Streak | Sort unique commit days, count consecutive runs |
| Language breakdown | `git ls-files` → count by file extension |

### 3. Rendering

Two rendering modes:

**Terminal** (`render_terminal`) uses `rich.Console` to compose:
- Panels for stat cards (`rich.panel.Panel`)
- Tables with inline progress bars (`rich.table.Table`)
- Rule separators (`rich.rule.Rule`)
- Colour-coded ASCII bar charts (pure string math)

**HTML** (`render_html`) generates a self-contained page:
- Dark-theme CSS with CSS variables
- SVG bar chart (coordinate math, no JS)
- SVG donut chart (polar-to-Cartesian arc math)
- Inline styles — zero external resources

---

## Extending Chronicle

Chronicle is designed to be extended. Add new analysis to `analyzer.py` and new visualizations to `renderer.py`:

```python
# Example: add "most active day of week" to RepoStats
from collections import Counter

def _busiest_weekday(commits):
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    counts = Counter(c.date.weekday() for c in commits)
    top = counts.most_common(1)[0]
    return days[top[0]], top[1]
```

Then wire it into `analyze()` and add a row in `_generate_insights()`.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `rich` | ≥ 13.0 | Terminal colours, tables, panels |
| `click` | ≥ 8.0 | CLI argument parsing |
| Python stdlib | — | `subprocess`, `datetime`, `pathlib`, `collections`, `dataclasses` |

No network access, no API keys, no accounts required.

---

## License

MIT — do whatever you like with it.

---

*Built with [Chronicle](https://github.com/kareemrt/clauder) • Git Repository Historian*
