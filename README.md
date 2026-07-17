# ☁ Clauder

> **AI-powered code review in your terminal, powered by Claude.**

```
╭──────────────────────────────╮
│      ☁  CLAUDER  ☁           │
│    AI-powered code review    │
╰──────────────────────────────╯
```

Clauder is a CLI tool that sends your git diffs or source files to Claude and
returns a structured, color-coded code review directly in your terminal — with
actionable feedback on bugs, security issues, performance, style, and documentation.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🐛 **Bug Detection** | Spot logic errors, off-by-ones, null dereferences |
| 🔒 **Security Scanning** | SQLi, XSS, hardcoded secrets, insecure patterns |
| ⚡ **Performance** | N+1 queries, unnecessary allocations, blocking calls |
| 🎨 **Style** | Magic numbers, inconsistent naming, dead code |
| 📝 **Docs** | Missing docstrings, outdated comments |
| 📊 **Scoring** | 0–100 quality score with visual progress bar |
| 🎯 **Multiple Inputs** | Staged diff, all changes, specific commit, branch diff, raw files |
| 📄 **Output Formats** | Terminal (colored), Markdown, JSON |
| 💾 **Save Reports** | Export to `.md` or `.json` for sharing or CI artifacts |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/kareemrt/Clauder.git
cd Clauder

# Install dependencies
pip install -r requirements.txt

# Or install as a CLI tool
pip install -e .
```

### Set your API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Get a key at [console.anthropic.com](https://console.anthropic.com).

### Run your first review

```bash
# Review staged git changes
clauder review

# Review everything (staged + unstaged)
clauder review --all

# Review a specific commit
clauder review --commit abc1234

# Review changes vs main branch
clauder review --branch main

# Review specific files
clauder review src/auth.py src/db.py

# Save a markdown report
clauder review --all --save report.md
```

---

## 📸 Example Output

```
╭──────────────────────────────────────────────────────────╮
│                     ☁  CLAUDER  ☁                        │
│                  AI-powered code review                   │
╰──────────────────────────────────────────────────────────╯

╭─────────────────────────── Review Score ─────────────────╮
│                                                           │
│  42/100  ████████░░░░░░░░░░░░                             │
│                                                           │
│  2 critical  1 high  1 medium  2 low                      │
│                                                           │
│  This diff adds a user authentication endpoint. The       │
│  implementation works but contains a SQL injection        │
│  vulnerability and stores passwords in plaintext.         │
│                                                           │
╰───────────────────────────────────────────────────────────╯

───────────────────── ✓ Highlights ──────────────────────────
  ✓ Good use of try/except for error handling
  ✓ Clear separation of the login and register routes

──────────────────────── Issues Found ───────────────────────

🔒  SECURITY  (2 issues)
  ● CRITICAL  auth/db.py:47  SQL Injection via string interpolation
    User input is interpolated directly into an SQL query string.
    → Use parameterized queries: cursor.execute('SELECT * ...', (email,))

  ● CRITICAL  auth/models.py:23  Plaintext password storage
    Passwords are stored as raw strings in the database.
    → Use bcrypt: password_hash = bcrypt.hashpw(password.encode(), ...)

🐛  BUGS  (1 issue)
  ● HIGH  auth/middleware.py:61-68  Token expiry not validated
    JWT tokens are decoded but 'exp' claim is never checked.
    → Add: if payload['exp'] < time.time(): raise TokenExpiredError()

⚡  PERFORMANCE  (1 issue)
  ● MEDIUM  auth/views.py:89  N+1 query in user lookup
    Each login check fires an additional SELECT for roles.
    → Use a JOIN to fetch user + roles in a single query.

 Lines reviewed: 312   Total issues: 6
```

---

## 🛠 Usage Reference

```
Usage: clauder review [OPTIONS] [FILES]...

  Review code changes with Claude AI.

Options:
  --staged / --no-staged    Review only staged git changes
  --all                     Review all changes (staged + unstaged)
  --commit SHA              Review a specific commit
  --branch BASE             Review changes vs a base branch (default: main)
  -o, --output FORMAT       Output format: terminal | markdown | json
  -s, --save FILE           Save report to a file (.md or .json)
  -c, --context TEXT        Optional context about what this change is for
  --model MODEL             Override Claude model
  --help                    Show this message and exit.
```

### Extra Commands

```bash
# Show current branch and recent commits
clauder status

# Show version
clauder --version
```

---

## 🔧 Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `CLAUDER_MODEL` | `claude-sonnet-5` | Claude model to use |

### Use as a pre-commit hook

Add Clauder as a git pre-commit hook to gate commits on code quality:

```bash
# .git/hooks/pre-commit
#!/bin/sh
clauder review --staged --output terminal
if [ $? -ne 0 ]; then
  echo "❌ Clauder found critical/high issues. Fix them before committing."
  exit 1
fi
```

### Use in CI/CD (GitHub Actions)

```yaml
# .github/workflows/review.yml
name: AI Code Review
on: [pull_request]

jobs:
  clauder:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: clauder review --branch ${{ github.base_ref }} --output markdown --save review.md
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - uses: actions/upload-artifact@v4
        with:
          name: code-review
          path: review.md
```

---

## 📁 Project Structure

```
Clauder/
├── clauder/
│   ├── __init__.py       # Package metadata
│   ├── cli.py            # Click CLI — entry point and commands
│   ├── reviewer.py       # Claude API integration + response parsing
│   ├── formatter.py      # Rich terminal, Markdown, and JSON rendering
│   ├── git_utils.py      # Git diff extraction helpers
│   └── config.py         # Configuration via environment variables
├── examples/
│   └── demo.py           # Demo script (no API key required)
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🏗 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                        YOU                              │
│              clauder review --all                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   git_utils.py                          │
│   Extract diff via git diff / git show / file read      │
└────────────────────────┬────────────────────────────────┘
                         │  raw diff text
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   reviewer.py                           │
│   Build structured prompt → call Claude API             │
│   Parse JSON response → ReviewResult dataclass          │
└────────────────────────┬────────────────────────────────┘
                         │  ReviewResult
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   formatter.py                          │
│   Render as colored terminal / Markdown / JSON          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              YOUR TERMINAL / FILE / CI LOG              │
└─────────────────────────────────────────────────────────┘
```

Claude receives:
1. A structured **system prompt** describing its role and the exact JSON schema to return
2. The **diff or file content** as the user message

The response is parsed into a typed `ReviewResult` with `Issue` objects sorted by severity.

---

## 🧪 Running the Demo

No API key needed to see the UI:

```bash
python examples/demo.py
```

This renders a pre-baked review result showing all severity levels, categories, and formatting.

---

## 🤝 Contributing

1. Fork and clone the repo
2. `pip install -e ".[dev]"` (or `pip install -r requirements.txt`)
3. Make your changes
4. Test: `python examples/demo.py`
5. Open a PR

---

## 📜 License

MIT — see [LICENSE](LICENSE).

---

*Built with [Claude](https://anthropic.com) · Powered by [Rich](https://github.com/Textualize/rich) · Made for developers who care about code quality*
