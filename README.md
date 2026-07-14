# Clauder — The Autonomous Code Healer

<div align="center">

```
  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
 ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
 ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝
 ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗
 ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║
  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
```

**The Autonomous Code Healer — Powered by Claude**

[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Claude](https://img.shields.io/badge/powered%20by-Claude%20AI-orange?style=flat-square)](https://anthropic.com)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-13%20passing-brightgreen?style=flat-square)](#)

*Run your tests. Watch Claude fix them. Go get coffee.*

</div>

---

## What Is Clauder?

Clauder is a CLI tool that uses **Claude** as an autonomous debugging agent. It runs your test suite, intercepts failures, sends them to Claude with full context, applies the suggested fixes, and loops — until all tests are green or it hits your iteration limit.

Think of it as a pair-programmer who never sleeps and only needs your test failures as instructions.

---

## Features

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDER COMMANDS                         │
├──────────────────┬──────────────────────────────────────────────┤
│  clauder heal    │  Autonomous test-fix loop with Claude        │
│  clauder analyze │  Bug & code smell analysis for any .py file  │
│  clauder explain │  Plain-English traceback explanations        │
└──────────────────┴──────────────────────────────────────────────┘
```

- **`heal`** — Runs your test command, parses pytest failures, sends each to Claude, applies fixes, re-runs, repeats
- **`analyze`** — Deep static analysis with severity rankings and actionable suggestions
- **`explain`** — Turns cryptic tracebacks into plain-English breakdowns you can act on
- Rich terminal UI with colorized diffs, syntax-highlighted code, and progress panels
- Configurable model (any Claude model), iteration count, and working directory
- `--dry-run` mode to preview fixes without touching files
- `--no-auto` mode for interactive fix-by-fix approval

---

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│  Your Tests │────▶│  Clauder     │────▶│  Claude API         │
│  (pytest)   │     │  Runner      │     │  (Analyze + Fix)    │
└─────────────┘     └──────┬───────┘     └──────────┬──────────┘
                           │  FAILURES               │  FIXED CODE
                           │◀────────────────────────┘
                           │
                    ┌──────▼───────┐
                    │  Apply Diff  │
                    │  Re-run Tests│
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  All Green?  │──YES──▶  Done! ✓
                    └──────┬───────┘
                           │ NO (loop up to N times)
                           └──────▶  Repeat
```

### The Heal Loop in Detail

1. **Run** your test command (`pytest -v` by default)
2. **Parse** structured failure blocks — test ID, file, line, error type, traceback
3. **Read** the relevant source file
4. **Prompt** Claude with full context: failure, traceback, source code
5. **Extract** the fixed code from Claude's response
6. **Diff** original vs. fixed, display in the terminal
7. **Apply** the fix (or skip in `--dry-run`)
8. **Re-run** tests and check if the failure is resolved
9. **Repeat** until all tests pass or max iterations reached

---

## Installation

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install (editable mode recommended for development)
pip install -e .

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here
```

**Requirements:** Python 3.11+, an [Anthropic API key](https://console.anthropic.com/)

---

## Usage

### `clauder heal` — Fix Failing Tests

```bash
# Basic: run pytest in current directory, loop up to 5 times
clauder heal

# Custom test command and iteration limit
clauder heal --cmd "pytest tests/ -x" --iterations 3

# Preview fixes without applying them
clauder heal --dry-run

# Approve each fix interactively
clauder heal --no-auto

# Use a specific Claude model
clauder heal --model claude-opus-4-8

# Heal a project in another directory
clauder heal --dir /path/to/project
```

**Terminal output (example):**

```
  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
  ... (banner) ...

  ─────────────────── 🩺  Heal Mode ───────────────────
  ℹ  Working directory: /home/user/myproject
  ℹ  Test command:      pytest -v
  ℹ  Max iterations:    5

  ℹ  Iteration 1/5 — running tests…
  ⚠  2 test(s) failing.

  🤔  Analyzing failure: test_subtract
  🤔  Asking Claude for a fix…

  ╭──────────── Proposed Fix ────────────╮
  │ --- a/math.py                        │
  │ +++ b/math.py                        │
  │ @@ -4,3 +4,3 @@                     │
  │  def subtract(a, b):                 │
  │ -    return a + b   # Bug!           │
  │ +    return a - b                    │
  ╰──────────────────────────────────────╯

  ✓  Fix applied to math.py

  ℹ  Iteration 2/5 — running tests…
  ✓  All tests pass! (after 1 fix)

  ──────────────── 📋  Results ────────────────

  ┃  Iterations       2
  ┃  Tests Fixed      1
  ┃  Remaining        0
```

---

### `clauder analyze` — Code Analysis

```bash
# Analyze a Python file
clauder analyze my_module.py

# Show source code alongside findings
clauder analyze app/utils.py --show-code
```

**Sample output:**

```
  ─────────────────── 🔬  Analyze Mode ───────────────────
  ℹ  Analyzing utils.py …

  ─────────────────── 📌  4 Finding(s) ───────────────────
  ╭──────┬──────────┬──────────────────────────┬─────────────────────────────╮
  │ Line │ Severity │ Issue                    │ Suggestion                  │
  ├──────┼──────────┼──────────────────────────┼─────────────────────────────┤
  │  12  │ HIGH     │ SQL injection via f-str  │ Use parameterized queries   │
  │  28  │ MEDIUM   │ Bare except clause       │ Catch specific exceptions   │
  │  41  │ LOW      │ Unused variable `tmp`    │ Remove or use the variable  │
  │  55  │ INFO     │ Missing type hints       │ Add PEP 484 annotations     │
  ╰──────┴──────────┴──────────────────────────┴─────────────────────────────╯

  ⚠  1 HIGH severity issue(s) found — please review.
```

---

### `clauder explain` — Traceback Explainer

```bash
# Pipe pytest output directly
pytest 2>&1 | clauder explain

# Explain from a saved file
clauder explain --file error.txt

# Pass as a string
clauder explain "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

**Sample output:**

```
  ─────────────────── 💬  Explain Mode ───────────────────
  ℹ  Sending traceback to Claude…

  ─────────────────── 🧠  Explanation ───────────────────

  **What went wrong**
  Python tried to add an integer and a string, which isn't allowed.

  **Why it happened**
  The function `process_items` at line 34 receives `count` as a string
  from the HTTP query parameter but tries to add it directly to an
  integer. Python's `+` operator doesn't coerce types automatically.

  **How to fix it**
  - Cast the parameter on input: `count = int(request.args.get('count', 0))`
  - Or convert at the point of use: `total = items + int(count)`
  - Add input validation to reject non-numeric values early
```

---

## Project Structure

```
clauder/
├── clauder/
│   ├── __init__.py       # Version and package metadata
│   ├── cli.py            # Click CLI — heal, analyze, explain commands
│   ├── healer.py         # Healing loop: run → diagnose → fix → repeat
│   ├── runner.py         # Test runner — subprocess + pytest output parsing
│   ├── analyzer.py       # Claude-powered analysis and traceback explainer
│   └── ui.py             # Rich terminal UI components
├── tests/
│   ├── test_runner.py    # Unit tests for the failure parser
│   └── test_healer.py    # Unit tests for prompt building and code extraction
├── examples/
│   ├── buggy_math.py     # Demo module with intentional bugs
│   └── test_buggy_math.py# Tests to heal with `clauder heal`
├── pyproject.toml        # Package config and dependencies
└── README.md
```

---

## Demo: Healing the Example

```bash
# The examples/ directory contains a buggy module and its tests
cd /path/to/clauder

# Run the broken tests to see what fails
pytest examples/test_buggy_math.py -v
# 4 tests FAIL (subtract, multiply, divide, factorial)

# Let Clauder heal them
clauder heal --cmd "pytest examples/test_buggy_math.py -v" --dir .
# Claude will fix: subtract (wrong operator), multiply (copies first arg),
#                  divide (no ZeroDivisionError guard), factorial (missing base case)
```

---

## Configuration

All options can be passed as CLI flags. Common combinations:

| Goal | Command |
|------|---------|
| Quick fix, auto-apply | `clauder heal` |
| Safe preview first | `clauder heal --dry-run` |
| One shot, fail fast | `clauder heal --iterations 1 --cmd "pytest -x"` |
| Review each fix | `clauder heal --no-auto` |
| Fastest model | `clauder heal --model claude-haiku-4-5-20251001` |
| Best quality | `clauder heal --model claude-opus-4-8` |

---

## Requirements

| Dependency | Purpose |
|-----------|---------|
| `anthropic >= 0.40` | Claude API client |
| `rich >= 13` | Terminal UI — panels, diffs, tables |
| `click >= 8.1` | CLI argument parsing |
| Python `>= 3.11` | Structural pattern matching, `X \| Y` type hints |

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with [Claude](https://anthropic.com) · Made to make debugging less painful

</div>
