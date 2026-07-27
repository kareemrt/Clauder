# 🤖 Clauder

> **AI-powered code review for your git workflow — powered by Claude.**

[![CI](https://github.com/kareemrt/clauder/actions/workflows/ci.yml/badge.svg)](https://github.com/kareemrt/clauder/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Clauder reviews your code changes using Claude and outputs structured, actionable feedback — in your terminal, as Markdown, or as JSON. It works with staged changes, branch diffs, specific commits, and GitHub PRs.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-source review** | Staged changes, branch diffs, commits, or GitHub PRs |
| **5 review modes** | `full`, `security`, `performance`, `style`, `bugs` |
| **3 output formats** | Terminal (Rich), Markdown, JSON |
| **Structured findings** | Per-file, per-line comments with severity levels |
| **GitHub Actions** | Automatic PR reviews posted as comments |
| **CI/CD ready** | Exit codes and JSON output for pipeline integration |

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      clauder CLI                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  review  │  │  branch  │  │    pr    │  │ staged │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       └─────────────┴─────────────┴─────────────┘       │
│                           │                             │
│                    ┌──────▼──────┐                      │
│                    │ diff_parser │  parse unified diff  │
│                    └──────┬──────┘                      │
│                           │ ParsedDiff                  │
│                    ┌──────▼──────┐                      │
│                    │  reviewer   │  Claude API call     │
│                    └──────┬──────┘                      │
│                           │ ReviewResult                │
│              ┌────────────┼─────────────┐               │
│       ┌──────▼───┐  ┌─────▼────┐  ┌────▼──────┐        │
│       │ Terminal │  │ Markdown │  │   JSON    │        │
│       │  (Rich)  │  │          │  │           │        │
│       └──────────┘  └──────────┘  └───────────┘        │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

```bash
# Install from source
git clone https://github.com/kareemrt/clauder
cd clauder
pip install -e .

# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 📖 Usage

### Review a diff file

```bash
# From a file
clauder review changes.diff

# From stdin
git diff main | clauder review

# Security-focused review, output Markdown
git diff main | clauder review --mode security --format markdown --output review.md
```

### Review branch changes

```bash
# Compare your feature branch against main
clauder branch main feature/my-feature

# Compare HEAD against develop, bugs mode
clauder branch develop HEAD --mode bugs
```

### Review staged changes

```bash
# Review what's about to be committed
git add -p
clauder staged

# Security check before pushing
clauder staged --mode security --format json
```

### Review a commit

```bash
# Last commit
clauder commit

# Specific commit hash
clauder commit abc1234f

# Last 3 commits combined
clauder commit -n 3
```

### Review a GitHub PR

```bash
# Review PR #42 in owner/repo
clauder pr owner/repo 42

# With explicit token
clauder pr owner/repo 42 --token ghp_xxx

# Output as Markdown
clauder pr owner/repo 42 --format markdown --output pr_review.md
```

---

## 🎨 Output Modes

### Terminal (default)

```
   ______ __    ___   __  ______  ______  ____
  / ____// /   /   | / / / / __ \/ ____/ / __ \
 / /    / /   / /| |/ / / / / / / __/   / /_/ /
/ /___ / /___/ ___ / /_/ / /_/ / /___  / _, _/
\____//_____/_/  |_\____/_____/_____/ /_/ |_|
                                     AI Code Reviewer

Overall Score: [████████████████░░░░] 82/100

┌──────────────────────────────────────────────────────────────┐
│ Summary                                                      │
│ The changes introduce bcrypt hashing and parameterized       │
│ queries, fixing critical security issues in the auth layer.  │
│ A few style improvements remain.                            │
└──────────────────────────────────────────────────────────────┘

🚨 critical: 1  |  🟡 medium: 2  |  🔵 low: 1

╭────────┬──────────────┬──────┬──────────────────────────────╮
│ Sev    │ File         │ Line │ Message                       │
├────────┼──────────────┼──────┼──────────────────────────────┤
│ 🚨     │ src/auth.py  │  15  │ MD5 is cryptographically      │
│ critical│             │      │ broken for password hashing.  │
│        │              │      │ 💡 Use bcrypt or argon2       │
╰────────┴──────────────┴──────┴──────────────────────────────╯
```

### Markdown

```markdown
# 🤖 Clauder AI Code Review

**Overall Score:** `82/100`

## Summary
The changes introduce bcrypt hashing...

## Issue Breakdown
🚨 **critical**: 1 | 🟡 **medium**: 2 | 🔵 **low**: 1

## Comments
### 🚨 CRITICAL — `src/auth.py` line 15
**Category:** security

MD5 is cryptographically broken for password hashing.

> 💡 **Suggestion:** Use bcrypt or argon2id instead.
```

### JSON (for CI pipelines)

```json
{
  "summary": "The changes introduce bcrypt hashing...",
  "overall_score": 82,
  "model": "claude-opus-5",
  "usage": { "input_tokens": 1847, "output_tokens": 412 },
  "comments": [
    {
      "file": "src/auth.py",
      "line": 15,
      "severity": "critical",
      "category": "security",
      "message": "MD5 is cryptographically broken for password hashing.",
      "suggestion": "Use bcrypt or argon2id instead."
    }
  ]
}
```

---

## 🔍 Review Modes

| Mode | Focus |
|---|---|
| `full` *(default)* | Correctness, security, performance, readability, maintainability |
| `security` | OWASP Top 10, injection, auth flaws, cryptography, secrets |
| `performance` | Algorithmic complexity, N+1 queries, blocking I/O, caching |
| `style` | Naming, function length, complexity, documentation, dead code |
| `bugs` | Off-by-one, null access, race conditions, exception gaps |

---

## ⚠️ Severity Levels

```
🚨 critical  →  Must fix before merging (data loss, security vuln, crash)
🔴 high      →  Should fix before merging (serious bug, major perf issue)
🟡 medium    →  Should address soon (code smell, minor bug risk)
🔵 low       →  Nice to have (style, naming improvements)
ℹ️  info      →  Observations and praise
```

---

## 🤖 GitHub Actions Integration

Add Clauder to your CI pipeline to automatically review every PR:

```yaml
# .github/workflows/review.yml
name: AI Code Review

on:
  pull_request:
    branches: [main]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Clauder
        run: pip install clauder

      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr.diff
          clauder review pr.diff --format markdown --output review.md

      - name: Post comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

---

## 🗂️ Project Structure

```
clauder/
├── clauder/
│   ├── __init__.py      # Package version
│   ├── cli.py           # Click CLI entry points
│   ├── config.py        # ReviewConfig, severity levels, mode prompts
│   ├── diff_parser.py   # Unified diff → ParsedDiff (no deps)
│   ├── git_utils.py     # Git & GitHub diff fetchers
│   ├── renderer.py      # Terminal / Markdown / JSON output
│   └── reviewer.py      # Claude API call & response parsing
├── tests/
│   ├── test_diff_parser.py
│   └── test_renderer.py
├── .github/
│   └── workflows/
│       └── ci.yml       # Tests + auto PR review
├── pyproject.toml
└── README.md
```

---

## 🛠️ Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint & format
ruff check clauder/ tests/
ruff format clauder/ tests/

# Type check
mypy clauder/
```

---

## 🗺️ Roadmap

- [ ] `--watch` mode: re-review on every save (via `watchfiles`)
- [ ] Review history stored in `.clauder/history/`
- [ ] GitHub App mode: webhook listener for automated PR comments
- [ ] `clauder init` to configure per-repo settings in `.clauder.toml`
- [ ] Support for other LLM backends (OpenAI, local Ollama)
- [ ] VS Code extension

---

## 📄 License

MIT © 2025 Kareem
