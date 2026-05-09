# Clauder — AI Git Storyteller

```
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|

       AI-Powered Git Storyteller
       Powered by Claude ✦ Anthropic
```

> *Your git log is a novel waiting to be told.*

**Clauder** transforms any git repository's commit history into a vivid, living narrative — combining beautiful terminal visualizations with Claude-generated prose, haikus, and developer diaries.

---

## What It Does

```
git log --oneline    →    "47 commits. 3 contributors. 12,000 lines."
       ↓
   [ Clauder ]
       ↓
    A story.
```

Clauder does three things in one pass:

1. **Analyzes** your repository — commits, contributors, timelines, hotspot files
2. **Visualizes** the history as rich ASCII charts right in your terminal
3. **Narrates** the journey using Claude to write a developer diary, project haiku, and punchy tagline

---

## Features

| Feature | Description |
|---|---|
| Commit Timeline | ASCII bar chart of activity by month |
| Contributor Leaderboard | Color-coded horizontal bars per author |
| Most-Touched Files | Table of files that evolved the most |
| AI Tagline | One punchy line capturing the project's soul |
| AI Haiku | Three-line poem distilling the codebase's essence |
| Developer Diary | Full narrative story, streamed live in the terminal |
| Markdown Report | Exportable `.md` report with everything combined |

---

## Demo Output

```
╭─────────────────────── Repository Profile ──────────────────────╮
│   Total Commits      847                                        │
│   Contributors       Alice (412), Bob (291), Carol (144)        │
│   Lines Added        +148,203                                   │
│   Lines Removed      -61,940                                    │
│   Most Active Day    Wednesday                                  │
│   Born               Jan 05, 2023 — "initial scaffolding"       │
│   Latest             May 08, 2025 — "fix: race condition in..."  │
╰─────────────────────────────────────────────────────────────────╯

Commit Timeline
  2023-01  ████████████                          12
  2023-02  ████████████████████                  20
  2023-03  ██████████████████████████████        30
  2023-04  ████████████████████████████████████  36
  ...

Contributor Leaderboard
  Alice     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  412 commits
  Bob       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             291 commits
  Carol     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                     144 commits
```

### AI-Generated Output

```
╭──────────────── Project Tagline ────────────────╮
│  "The API that finally made async feel human."  │
╰─────────────────────────────────────────────────╯

╭────────── Project Haiku ──────────────╮
│   A thousand commits deep             │
│   bugs bloom and fade like seasons    │
│   Alice hits merge again              │
╰───────────────────────────────────────╯
```

Then the **Developer Diary** streams live — a vivid, markdown-formatted narrative of your project's entire journey, written as if the code itself is looking back on how it came to be.

---

## Project Structure

```
Clauder/
│
├── clauder/
│   ├── __init__.py         # Package metadata
│   ├── main.py             # CLI entry point (Click)
│   ├── git_analyzer.py     # Git history parsing (GitPython)
│   ├── storyteller.py      # Claude API integration (streaming)
│   ├── visualizer.py       # Rich terminal visualizations
│   └── report.py           # Markdown report export
│
├── requirements.txt
├── setup.py
└── README.md
```

### Module Responsibilities

```
 ┌──────────────────────────────────────────────────────┐
 │                     clauder/main.py                  │
 │             CLI orchestration & UX flow              │
 └──────────────┬──────────────┬───────────────┬────────┘
                │              │               │
                ▼              ▼               ▼
    git_analyzer.py   visualizer.py   storyteller.py
    ───────────────   ─────────────   ──────────────
    Parse git log     Rich tables,    Claude API,
    into structs      bars, banners   streaming prose
                              │
                              ▼
                          report.py
                      ─────────────────
                      Markdown export
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt

# (Optional) Install as a CLI tool
pip install -e .
```

---

## Usage

### Basic (stats + visualizations only)

```bash
python -m clauder.main /path/to/your/repo --no-story
```

### Full AI Story Mode

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

python -m clauder.main /path/to/your/repo
```

### Save a Markdown Report

```bash
python -m clauder.main /path/to/your/repo --save --output my_story.md
```

### All Options

```
Usage: python -m clauder.main [OPTIONS] [REPO_PATH]

  Clauder — Turn your git history into a living story.

Arguments:
  REPO_PATH  Path to git repository [default: .]

Options:
  --max-commits INTEGER  Max commits to analyze  [default: 200]
  --save                 Save a Markdown report to disk
  --output TEXT          Output file path for --save  [default: clauder_report.md]
  --no-story             Skip AI story generation (stats only)
  --help                 Show this message and exit.
```

---

## How It Works

```
  Your Repo                  Clauder                      Output
  ─────────                  ───────                      ──────
  git log    ──────────►  git_analyzer.py  ──────────►  Rich tables
  git blame              (RepoStats struct)              Timeline chart
  git diff                      │                        Leaderboard
                                │
                                ▼
                          storyteller.py
                       (Anthropic API call)
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                 Tagline      Haiku      Story
               (Haiku 4.5) (Haiku 4.5) (Sonnet 4.6
                                         streamed)
                                │
                                ▼
                           report.py
                        (Markdown file)
```

**Clauder uses two Claude models:**
- `claude-haiku-4-5` for fast, creative micro-outputs (tagline, haiku)
- `claude-sonnet-4-6` for the full developer diary narrative (streamed live)

---

## Example Story Output

> *Excerpt from a real Clauder run:*

---

### ✦ Birth in the Dark

*It began on a Monday in January 2023 — a single commit named "initial scaffolding," authored by Alice at 11:47 PM. The codebase was three files and a dream: an `__init__.py`, a `README` stub, and a requirements file with five dependencies listed with the audacity of someone who knows exactly where this is going...*

### ✦ The Surge

*March 2023 was the crucible. Thirty commits in a single month — the most the project would ever see. Bob arrived, quiet at first with a two-line fix to the auth flow, then increasingly bold. The commit messages shifted from careful ("add: user model") to caffeinated ("FIX THIS PLEASE IT'S 3AM")...*

### ✦ The Steady Hand

*By winter, Carol had quietly become the glue. Her commits were never flashy — "refactor: extract helper," "docs: clarify edge case" — but remove them from the log and the project's coherence unravels. The codebase owes its legibility to someone who never asked for credit...*

---

## Requirements

- Python 3.9+
- Git repository (at least 1 commit)
- `ANTHROPIC_API_KEY` environment variable (for AI features)

---

## Tech Stack

| Library | Purpose |
|---|---|
| [anthropic](https://github.com/anthropics/anthropic-sdk-python) | Claude API — story generation |
| [rich](https://github.com/Textualize/rich) | Terminal visualizations & formatting |
| [gitpython](https://github.com/gitpython-developers/GitPython) | Git repository parsing |
| [click](https://click.palletsprojects.com/) | CLI interface |

---

## License

MIT — do whatever you want with it, but let your git history speak.

---

*Generated by **Clauder** — AI Git Storyteller powered by [Claude](https://anthropic.com) ✦ Anthropic*
