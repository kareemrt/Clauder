# Clauder

```
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 | |    | |/ _` | | | |/ _` |/ _ \ '__|
 | |____| | (_| | |_| | (_| |  __/ |
  \_____|_|\__,_|\__,_|\__,_|\___|_|
```

**AI-Powered Code Review Dashboard** — Powered by [Claude](https://www.anthropic.com/claude) (Anthropic)

> Feed Clauder a Python file or an entire project and get a stunning terminal dashboard with quality grades, bug detection, security alerts, complexity hotspots, documentation gaps, and AI-generated git insights — all in seconds.

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
  - [review](#review)
  - [chat](#chat)
  - [insights](#insights)
  - [scan](#scan)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Example Output](#example-output)
- [Requirements](#requirements)

---

## Features

| Category | What Clauder Does |
|---|---|
| 🏆 **Quality Grading** | A+–F letter grade + 0–10 quality score per file |
| 🐛 **Bug Detection** | Finds real bugs with line numbers, severity, and fix suggestions |
| 🔒 **Security Audit** | Flags injection risks, credential leaks, unsafe deserialization, and more |
| 🔥 **Complexity Hotspots** | Identifies overly-complex functions with refactoring suggestions |
| 📝 **Documentation Gaps** | Spots missing docstrings, type hints, and module docs |
| ✨ **Strengths** | Highlights what's done well — not just problems |
| 🔀 **Git Intelligence** | AI-generated narrative of your project's commit history |
| 📊 **Project Dashboard** | Multi-file summary with per-file scores in a single view |
| 💬 **Chat Mode** | Interactive Claude chat about any Python file |
| ⚡ **Fast Scan** | Zero-AI metrics scan for a quick project overview |

---

## Demo

### Single-file Review

```
clauder review my_module.py
```

```
   _____ _                 _
  / ____| |               | |
 | |    | | __ _ _   _  __| | ___ _ __
 ...

─────────────────── Analysis: my_module.py ───────────────────

 ╭──────────╮   Quality: ████████████████░░░░  8.2/10
 │          │
 │    B+    │   Well-structured module with clean separation of concerns.
 │          │   Minor documentation gaps in public functions; one potential
 ╰──────────╯   security concern with unvalidated user input on line 47.

 ┌──────┐ ┌──────┐ ┌───────────┐ ┌─────────┐ ┌──────────┐
 │Lines │ │Code  │ │Functions  │ │Classes  │ │Comments  │
 │  142 │ │  118 │ │    8      │ │    2    │ │    12    │
 └──────┘ └──────┘ └───────────┘ └─────────┘ └──────────┘

╭─── Bugs & Issues (2) ──────────────────────────────────────────────────╮
│ Severity    │ Line │ Description                  │ Suggested Fix      │
│ 🟡 MEDIUM   │  47  │ Unvalidated input passed...  │ Add input.strip()  │
│ ⚪ LOW      │  89  │ Bare except catches all...   │ Use except ValueError│
╰────────────────────────────────────────────────────────────────────────╯

╭─── Strengths ──────────────╮  ╭─── Improvements ───────────────────────╮
│ ✓ Clear function naming    │  │ → Add type hints to public functions    │
│ ✓ Good use of dataclasses  │  │ → Extract magic numbers into constants  │
│ ✓ Consistent error raising │  │ → Add module-level docstring            │
╰────────────────────────────╯  ╰─────────────────────────────────────────╯
```

### Project Dashboard

```
clauder review ./myproject --max-files 20
```

```
───────────────── 📊 Project Summary Dashboard ──────────────────

 ╭──────────────╮  ╭──────────────────────────╮  ╭────────────────╮  ╭──────────╮
 │     12       │  │ ████████████░░░░ 7.6/10  │  │  18 bugs found │  │  2847    │
 │ files review │  │  average quality         │  │ (3 high/crit.) │  │  total   │
 ╰──────────────╯  ╰──────────────────────────╯  ╰────────────────╯  ╰──────────╯

╭─── Per-File Scores ────────────────────────────────────────────────────────────────╮
│ File             │ Grade │ Score                   │ Bugs │ Security │  LOC │
│ models.py        │  A+   │ ████████████████████ 9.4│  0   │    0     │  156 │
│ utils.py         │  A    │ ████████████████░░░░ 8.7│  1   │    0     │   89 │
│ auth.py          │  B+   │ ██████████████░░░░░░ 7.8│  2   │    2     │  203 │
│ api_client.py    │  B    │ ████████████░░░░░░░░ 7.1│  3   │    1     │  318 │
│ legacy_parser.py │  D    │ ██████░░░░░░░░░░░░░░ 3.9│  8   │    0     │  421 │
╰────────────────────────────────────────────────────────────────────────────────────╯
```

### Git Intelligence

```
clauder insights .
```

```
──────────────────────── 🔀 Git Intelligence ────────────────────────────

╭─── Repository Info ─────────────────────────────────────────────────╮
│ Branch: main   Total commits: 147   Remote: github.com/user/project  │
╰─────────────────────────────────────────────────────────────────────╯

╭─── AI-Generated Commit Insights ──────────────────────────────────────────╮
│                                                                            │
│ This codebase tells the story of rapid iteration — the first 30 commits   │
│ show a team establishing foundations, followed by a burst of feature work  │
│ around the auth module. The high churn in `legacy_parser.py` (touched in  │
│ 23% of all commits) suggests it may be a candidate for a full rewrite...  │
│                                                                            │
╰────────────────────────────────────────────────────────────────────────────╯
```

---

## Installation

### From source

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements.txt
```

### Set your API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

> Get your key at [console.anthropic.com](https://console.anthropic.com)

---

## Quick Start

```bash
# Review a single file
python main.py review path/to/script.py

# Review your whole project (up to 10 files)
python main.py review ./src

# Review with higher file limit
python main.py review ./src --max-files 25

# Chat interactively with Claude about a file
python main.py chat path/to/complex_module.py

# Get AI git insights for your repo
python main.py insights .

# Quick metrics scan (no API key needed)
python main.py scan ./src
```

---

## Commands

### `review`

Deep AI-powered code review of a file or directory.

```
Usage: main.py review [OPTIONS] [PATH]

  Review a Python file or directory with Claude AI.

Options:
  --no-banner            Suppress the ASCII banner
  --max-files INTEGER    Max files to review in directory mode  [default: 10]
  --help                 Show this message and exit.
```

**Output includes:**
- Letter grade (A+ → F) and quality score (0–10)
- Executive summary from Claude
- Bugs table with severity, line numbers, and fix suggestions
- Security concerns with severity ratings
- Strengths vs. improvements side-by-side
- Complexity hotspots
- Documentation gaps
- Design patterns detected

---

### `chat`

Interactive Claude conversation about any Python file.

```
Usage: main.py chat [OPTIONS] PATH

  Interactive AI chat about a Python file.

Options:
  --help  Show this message and exit.
```

Claude loads the file as context and you can ask anything:

```
You > What does the process_batch function do?
You > Are there any thread-safety issues in this class?
You > How would you refactor this to use async/await?
You > exit
```

---

### `insights`

AI-powered git history analysis.

```
Usage: main.py insights [OPTIONS] [PATH]

  Show AI-powered git commit insights for a repository.

Options:
  --no-ai   Show raw git log without AI narrative
  --help    Show this message and exit.
```

**Output includes:**
- Repository metadata (branch, total commits, remote)
- AI-generated narrative about development patterns and velocity
- Recent commits table

---

### `scan`

Fast metrics scan — no API key required.

```
Usage: main.py scan [OPTIONS] [PATH]

  Quick metrics scan — no AI required.

Options:
  --help  Show this message and exit.
```

Shows a table with total/code/blank/comment lines, function count, class count, import count, and max line length for every Python file found.

---

## Project Structure

```
clauder/
│
├── main.py                   # Entry point
├── requirements.txt          # anthropic, rich, click, gitpython
│
└── clauder/
    ├── __init__.py           # Version and metadata
    ├── analyzer.py           # Claude API integration (tool-use structured output)
    ├── scanner.py            # File system + git utilities
    ├── reporter.py           # Rich terminal UI components
    └── cli.py                # Click CLI (review / chat / insights / scan)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        clauder CLI                          │
│              (Click-based, 4 commands)                      │
└────────────┬──────────────┬──────────────┬─────────────────┘
             │              │              │
      ┌──────▼──────┐ ┌─────▼─────┐ ┌────▼─────────┐
      │  analyzer   │ │  scanner  │ │   reporter   │
      │             │ │           │ │              │
      │ ClaudeAnalyzer│ scan_python│ Rich panels,  │
      │ - tool_use  │ │ get_stats  │ tables, rules │
      │ - chat      │ │ git utils  │ progress bars │
      │ - git NLP   │ │           │ │              │
      └──────┬──────┘ └───────────┘ └──────────────┘
             │
    ┌────────▼──────────┐
    │  Anthropic API    │
    │                   │
    │  claude-sonnet-4-6│
    │  tool_use output  │
    │  structured JSON  │
    └───────────────────┘
```

**Key design decisions:**

- **Tool use for structured output** — Rather than asking Claude to return JSON and parsing it, Clauder uses Claude's [tool use](https://docs.anthropic.com/en/docs/tool-use) feature with a strict schema. This guarantees well-typed, reliable analysis data every time.
- **Single model call per file** — One `claude-sonnet-4-6` call with a rich schema produces all dimensions of analysis simultaneously, minimising latency and cost.
- **Rich for terminal UI** — [`rich`](https://github.com/Textualize/rich) renders beautiful panels, tables, progress bars, and colour-coded output without any extra configuration.
- **Separation of concerns** — `analyzer.py` owns the AI logic, `scanner.py` owns I/O, and `reporter.py` owns presentation. `cli.py` orchestrates them.

---

## Configuration

| Environment Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes (AI commands) | Your Anthropic API key |

The `scan` command works entirely offline — no API key required.

---

## Requirements

```
python >= 3.11
anthropic >= 0.100.0
rich >= 15.0.0
click >= 8.0.0
gitpython >= 3.1.0
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with ❤️ and Claude by Clauder.*
