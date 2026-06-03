# Clauder

```
 ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝
██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗
╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
```

**Multi-Agent AI Repository Intelligence powered by Claude**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Powered by Claude](https://img.shields.io/badge/powered%20by-Claude-orange.svg)](https://anthropic.com)

Clauder sends **five specialized AI agents** to analyze any GitHub repository simultaneously, then synthesizes their findings into a single, actionable health report. Point it at a repo, get back a grade.

---

## What It Does

```
clauder analyze anthropics/anthropic-sdk-python
```

```
 ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
...

Repository: anthropics/anthropic-sdk-python
Model:      claude-opus-4-8
Max files:  60

✓ Fetched 60 files from anthropics/anthropic-sdk-python (Python)

⠿ 🔭 Scout Agent — done  (score: 91/100)          0:18
⠿ 🔒 Security Agent — done  (score: 88/100)        0:21
⠿ ✨ Quality Agent — done  (score: 84/100)          0:19
⠿ 🏛️  Architecture Agent — done  (score: 90/100)   0:22
⠿ 📚 Docs Agent — done  (score: 78/100)             0:17

⠿ 🧠 Synthesizer — complete                        0:14

════════════════════ ANALYSIS COMPLETE ════════════════════

Overall Score                                          Grade
[████████████████████░░░░] 86/100                     ✅ B

Agent Scores
 Agent          Score    Bar                       Summary
 🔭 Scout        91/100  [████████████████████░░]  Well-organized Python SDK with clear…
 🔒 Security     88/100  [██████████████████░░░░]  No hardcoded secrets found. Minor…
 ✨ Quality       84/100  [█████████████████░░░░░]  Strong typing throughout. Some comp…
 🏛️  Architecture 90/100  [██████████████████████]  Clean layered design. Async/sync…
 📚 Docs          78/100  [████████████████░░░░░░]  Good README. Several public methods…

Executive Summary
┌──────────────────────────────────────────────────────────────────────┐
│ The anthropic-sdk-python is a well-structured, production-quality    │
│ SDK with strong type safety and comprehensive async support. The     │
│ main areas for improvement are documentation coverage on internal    │
│ modules and a few complex methods that could benefit from           │
│ decomposition.                                                       │
└──────────────────────────────────────────────────────────────────────┘

💪 Strengths
  ✓ Consistent use of Python type hints throughout
  ✓ Clear separation between sync and async interfaces
  ✓ Comprehensive test fixtures and mocking patterns
  ✓ Well-defined retry and backoff logic

🗺️ Action Roadmap
  1. Add docstrings to 12 undocumented public methods in _client.py
  2. Decompose _make_request() — currently 80+ lines
  3. Add ADR for the sync/async dual-interface design decision
  4. Increase test coverage on edge cases in streaming module
  5. Document the internal pagination iterator API
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDER PIPELINE                         │
└─────────────────────────────────────────────────────────────────┘

   GitHub Repo
        │
        ▼
┌──────────────┐     Fetches up to N files,
│  RepoFetcher │     prioritizing source code
│  (httpx)     │     over config/binary files
└──────┬───────┘
       │
       │  RepoData
       │  (file tree + contents)
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                     Orchestrator                          │
│                                                          │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│   │  🔭Scout │  │ 🔒Security│  │ ✨Quality │  ···       │
│   │  Agent   │  │  Agent   │  │  Agent   │             │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│        │              │              │                   │
│        └──────────────┴──────────────┘                  │
│                       │  asyncio.gather                  │
│                       ▼                                  │
│              ┌─────────────────┐                        │
│              │  🧠 Synthesizer  │                        │
│              │     Agent       │                        │
│              └────────┬────────┘                        │
└───────────────────────┼─────────────────────────────────┘
                        │
                        ▼
               SynthesisReport
               (terminal + .md)
```

### The Agents

| Agent | Emoji | Focus |
|-------|-------|-------|
| **Scout** | 🔭 | Tech stack detection, project structure, entry points, build systems |
| **Security** | 🔒 | Vulnerabilities, hardcoded secrets, injection flaws, auth issues |
| **Quality** | ✨ | Complexity, DRY violations, error handling, test coverage, naming |
| **Architecture** | 🏛️ | Design patterns, coupling/cohesion, SOLID principles, API design |
| **Docs** | 📚 | README quality, docstrings, onboarding experience, outdated comments |
| **Synthesizer** | 🧠 | Combines all reports → overall score, grade, executive summary |

All five specialist agents run **in parallel** via `asyncio.gather`, then the Synthesizer collects their JSON reports and produces the final grade.

---

## Installation

### From PyPI *(coming soon)*
```bash
pip install clauder
```

### From Source
```bash
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .
```

### Requirements
- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com)
- A GitHub token (optional, but prevents rate limiting)

---

## Usage

### Analyze a repository

```bash
# Set your API key first
export ANTHROPIC_API_KEY=sk-ant-...
export GITHUB_TOKEN=ghp_...   # optional but recommended

# By owner/name
clauder analyze torvalds/linux

# By full URL
clauder analyze https://github.com/django/django

# Save report to a Markdown file
clauder analyze pallets/flask --output flask-report.md

# Use a faster/cheaper model
clauder analyze fastapi/fastapi --model claude-haiku-4-5-20251001

# Run only specific agents
clauder analyze myorg/myrepo --agents security,quality

# Increase file coverage for large repos
clauder analyze kubernetes/kubernetes --max-files 100
```

### List available models

```bash
clauder models
```

```
         Available Models
┌────────────────────────────┬───────────┬─────────────────────────┬──────────┐
│ Model ID                   │ Name      │ Best For                │ Est.Time │
├────────────────────────────┼───────────┼─────────────────────────┼──────────┤
│ claude-opus-4-8            │ Opus 4.8  │ Most capable, best      │ ~60s     │
│                            │           │ analysis                │          │
│ claude-sonnet-4-6          │ Sonnet4.6 │ Balanced speed/quality  │ ~25s     │
│ claude-haiku-4-5-20251001  │ Haiku 4.5 │ Fastest, lightweight    │ ~10s     │
└────────────────────────────┴───────────┴─────────────────────────┴──────────┘
```

---

## Output

### Terminal (default)
Rich, colorized output with score bars, severity-sorted findings table, and the executive summary.

### Markdown report (`--output report.md`)

The saved report includes:
- Overall score bar and letter grade
- Executive summary
- Critical issues list
- Strengths
- Prioritized action roadmap
- Per-agent breakdown with full findings tables

---

## Scoring

Each agent rates its domain 0–100. The Synthesizer computes a weighted overall score (security issues count more than documentation gaps) and assigns a letter grade:

```
Score   Grade   Meaning
90–100    A     Production-ready, excellent health
75–89     B     Good codebase, minor improvements needed
60–74     C     Functional but significant issues present
45–59     D     Serious problems requiring attention
0–44      F     Critical failures, major rework needed
```

---

## Project Structure

```
clauder/
├── clauder/
│   ├── __init__.py          # Package version
│   ├── cli.py               # Typer CLI entry point
│   ├── models.py            # Pydantic data models
│   ├── github.py            # GitHub API fetcher (httpx)
│   ├── orchestrator.py      # Parallel agent runner + Rich live UI
│   ├── reporter.py          # Terminal display + Markdown generation
│   └── agents/
│       ├── base.py          # AgentBase: shared Claude call + JSON parsing
│       ├── scout.py         # Structure & tech stack agent
│       ├── security.py      # Security & vulnerability agent
│       ├── quality.py       # Code quality & tests agent
│       ├── architecture.py  # Design patterns & coupling agent
│       ├── docs.py          # Documentation coverage agent
│       └── synthesizer.py   # Final synthesis & grading agent
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_reporter.py
│   └── test_github.py
├── pyproject.toml
└── requirements.txt
```

---

## Development

```bash
# Install with dev extras
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check clauder/

# Type check
mypy clauder/
```

### Adding a New Agent

1. Create `clauder/agents/my_agent.py` extending `AgentBase`
2. Set `name`, `emoji`, `description`, `system_prompt` as class attributes
3. Register it in `clauder/agents/__init__.py` under `AGENT_REGISTRY`
4. The orchestrator picks it up automatically

```python
from clauder.agents.base import AgentBase

class PerformanceAgent(AgentBase):
    name = "Performance"
    emoji = "⚡"
    description = "Identifies bottlenecks and optimization opportunities"
    system_prompt = """You are the Performance Agent..."""
```

---

## Architecture Decisions

**Why parallel agents?**  
Each agent has its own specialized system prompt and perspective. Running them concurrently cuts wall-clock time from ~5× sequential to ~1×, and prevents cross-contamination — the Security agent doesn't unconsciously weight findings toward whatever the Quality agent noticed first.

**Why JSON output from agents?**  
Structured JSON lets us sort findings by severity, de-duplicate, render tables, and feed the exact data model into the Synthesizer. Plain prose would require another LLM call to parse.

**Why Pydantic models throughout?**  
Validation catches malformed agent responses before they propagate. `AgentReport.score` is validated to be 0–100; `Finding.severity` is a literal union. Bad Claude output → clear error, not a mystery crash downstream.

---

## License

MIT — see [LICENSE](LICENSE).

---

*Built with [Claude](https://anthropic.com) by [kareemrt](https://github.com/kareemrt)*
