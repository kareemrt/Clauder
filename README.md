# ◈ Clauder — AI Repository Storyteller

> *Every codebase has a story. Clauder tells it.*

Clauder is a Python CLI tool that analyzes any GitHub repository and generates a **captivating documentary-style narrative** using Claude AI. It produces rich terminal output and a beautiful standalone HTML report — complete with contributor profiles, language breakdowns, commit timelines, and an AI-authored story in six chapters.

---

## ✦ What It Does

```
clauder story kareemrt/clauder --output story.html
```

```
  ◈ CLAUDER    Repository Storyteller

           kareemrt/clauder
  "Where Claude tells the story of code"

  ★ 0      ⑂ 0      ◈ Python      ⊕ 0
──────────────────────────────────────────────

  Language Breakdown
  ████████████████████████████░░░░ Python 92.1%   Shell 7.9%

  ┌─────────────────────────────────┐
  │ ★ The Origin                    │
  │                                 │
  │  In the summer of 2024, a       │
  │  developer set out to bridge    │
  │  the gap between raw git        │
  │  history and human narrative…   │
  └─────────────────────────────────┘
```

---

## ◆ Architecture

```
clauder/
├── clauder/
│   ├── __init__.py          # Package metadata
│   ├── cli.py               # Click CLI entry point (story, stats commands)
│   ├── github_client.py     # GitHub REST API wrapper
│   │                        #   → fetches commits, contributors,
│   │                        #     languages, issues, PRs
│   ├── storyteller.py       # Claude AI narrative engine
│   │                        #   → generate_story()  — 6-chapter documentary
│   │                        #   → generate_tagline() — punchy one-liner
│   ├── renderer.py          # Rich terminal rendering
│   │                        #   → header, language bar, contributor table,
│   │                        #     commit timeline, story panels
│   └── report.py            # Jinja2 HTML report generator
│                            #   → dark-mode GitHub-style HTML page
├── tests/
│   └── test_clauder.py      # Unit tests (7 tests, 100% pass)
├── pyproject.toml           # Package config + dependencies
└── README.md
```

### Data Flow

```
GitHub REST API
      │
      ▼
 GitHubClient              ← fetches repo metadata, commits (50),
      │                      contributors (20), languages, issues, PRs
      ▼
  RepoData
      │
      ├──► Storyteller  ──► Claude claude-sonnet-5  ──► story text (6 sections)
      │    (storyteller.py)  Claude claude-haiku-4-5 ──► tagline
      │
      ├──► StoryRenderer ──► Rich terminal panels, tables, timeline
      │    (renderer.py)
      │
      └──► generate_html_report ──► standalone HTML file
           (report.py)               (Jinja2 + embedded CSS)
```

---

## ◉ The Story Chapters

Each repository gets a **six-chapter documentary**, generated entirely by Claude:

| Chapter | Content |
|---------|---------|
| **★ The Origin** | What the project is, why it exists, the problem it solves |
| **◆ The Architects** | Key contributors as characters — their roles and contributions |
| **◈ The Journey** | Timeline narrative based on commit history — phases of development |
| **◉ The Technology** | Technical choices, language patterns, what they reveal about the team |
| **◎ The Current State** | Health, open questions, community activity |
| **◌ The Future** | Trajectory speculation based on current momentum |
| **✦ One-Line Story** | A single poetic sentence capturing the project's essence |

---

## ◎ Installation

**Requirements:** Python ≥ 3.11, an Anthropic API key, and optionally a GitHub token (for higher rate limits).

```bash
# Clone and install
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -e .

# Set your API keys
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."          # optional, but recommended
```

Or install directly:

```bash
pip install git+https://github.com/kareemrt/clauder.git
```

---

## ◌ Usage

### Generate a Story

```bash
# Terminal output only
clauder story torvalds/linux

# Terminal + save HTML report
clauder story kareemrt/clauder --output clauder_story.html

# HTML only (skip terminal rendering)
clauder story microsoft/vscode -o vscode.html --no-terminal

# Pass tokens explicitly
clauder story owner/repo \
  --github-token ghp_... \
  --anthropic-key sk-ant-...
```

### Quick Stats (no AI needed)

```bash
clauder stats kareemrt/clauder
```

```
  ╭──────────────────────────────────╮
  │      kareemrt/clauder            │
  ├──────────────────┬───────────────┤
  │ Description      │ Claude Bot    │
  │ Stars            │ 0             │
  │ Forks            │ 0             │
  │ Language         │ Python        │
  │ License          │ MIT           │
  │ Created          │ 2024-06-30    │
  ╰──────────────────┴───────────────╯
```

---

## ✦ HTML Report

The `--output` flag generates a **self-contained dark-mode HTML file** with:

- Animated language breakdown bar
- Contributor cards with avatars and commit share bars
- Commit timeline with branching connector lines
- Six color-coded story panels
- Fully responsive layout, no external dependencies

---

## ◆ Configuration

| Environment Variable | Description |
|----------------------|-------------|
| `ANTHROPIC_API_KEY` | Required — your Anthropic API key |
| `GITHUB_TOKEN` | Recommended — GitHub PAT for higher API rate limits |

---

## ◈ Development

```bash
# Run tests
pip install pytest
python -m pytest tests/ -v

# Lint
pip install ruff
ruff check clauder/
```

---

## ◎ License

MIT — see [LICENSE](LICENSE).

---

<div align="center">
<sub>Built by Claude, for humans who love code stories. Powered by <a href="https://anthropic.com">Anthropic Claude</a>.</sub>
</div>
