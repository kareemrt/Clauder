# Clauder: The Oracle ✦

> *"Ancient wisdom meets modern code. The Oracle sees all."*

**Clauder** is an AI-powered code review CLI tool with a mystical oracle personality. It uses Claude to analyze your source code and deliver technically precise feedback wrapped in dramatic, insightful commentary — scoring quality, security, readability, and performance with flair.

---

## ✦ Demo

```
  ╔═══════════════════════════════════════════════════════════════╗
  ║    ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗   ║
  ║   ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗  ║
  ║   ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝  ║
  ║   ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗  ║
  ║   ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║  ║
  ║    ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝  ║
  ║                   ✦  T H E   O R A C L E  ✦                  ║
  ╚═══════════════════════════════════════════════════════════════╝
```

```
╭─────────────────────────────────────────────────────────────────╮
│  ✦  Oracle's Vision  ✦                                          │
│                                                                 │
│  "This code walks through shadows — functional on the surface,  │
│   yet carrying the weight of ancient sins: plaintext passwords, │
│   SQL conjured from raw strings, and errors swallowed whole     │
│   like offerings to a forgotten god."                           │
╰─────────────────────────────────────────────────────────────────╯

╔═══════════════════════════════════════════════════════════════╗
║         The Oracle's Verdict for example_code.py             ║
║                                                               ║
║        ☠  CURSED  ☠                                          ║
║                                                               ║
║        OVERALL SCORE: 18/100                                  ║
╚═══════════════════════════════════════════════════════════════╝

✦  The Four Runes  ✦
──────────────────────────────────────────────────────────────────
◈  Quality      ██████░░░░░░░░░░░░░░░  30/100
🔒 Security     ██░░░░░░░░░░░░░░░░░░░   8/100
◉  Readability  █████████░░░░░░░░░░░░  45/100
⚡ Performance  ████████░░░░░░░░░░░░░  40/100
```

---

## ✦ Features

| Feature | Description |
|---|---|
| **Full Review** | Deep AI analysis of any source file with scored feedback |
| **Four Runes** | Quality, Security, Readability & Performance scores |
| **Prophecies** | Categorized issues: `CRITICAL`, `WARNING`, `INFO`, `WISDOM` |
| **Oracle Vision** | Dramatic opening statement that captures the code's essence |
| **Verdicts** | `TRANSCENDENT` → `BLESSED` → `ENCHANTED` → `MUNDANE` → `CURSED` |
| **Code Metrics** | Static analysis: complexity, line count, function count, etc. |
| **Closing Haiku** | Every review ends with a 5-7-5 haiku about your code |
| **JSON Export** | Save reviews to JSON for tracking and CI integration |
| **Directory Scan** | Scan all Python files in a directory with a summary table |
| **Quick Prophecy** | One-paragraph piercing insight for a snippet |
| **Multi-Language** | Python, JS, TS, Go, Rust, Java, C/C++, Ruby, and more |

---

## ✦ Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

---

## ✦ Usage

### Review a file

```bash
python main.py review path/to/your/code.py
```

### Review and save the report

```bash
python main.py review myfile.py --save report.json
```

### Scan all Python files in a directory

```bash
python main.py scan
```

### Get a quick prophecy for a code snippet

```bash
python main.py prophecy "def foo(x): return eval(x)"
```

### Pipe code via stdin

```bash
cat myfile.py | python main.py prophecy -
```

---

## ✦ Architecture

```
clauder/
├── main.py                  ← CLI entry point (Click)
│
├── clauder/
│   ├── __init__.py
│   ├── analyzer.py          ← Static code analysis & metrics
│   ├── oracle.py            ← Claude API integration
│   ├── display.py           ← Rich terminal UI rendering
│   └── prompts.py           ← Oracle system prompts
│
├── examples/
│   └── example_code.py      ← Demo file with intentional issues
│
└── requirements.txt
```

### Data Flow

```
  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
  │  Source File │────▶│   Analyzer   │────▶│  CodeMetrics    │
  └─────────────┘     └──────────────┘     └────────┬────────┘
                                                     │
                                                     ▼
  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
  │  Rich  UI   │◀────│    Display   │◀────│  Oracle Review  │
  └─────────────┘     └──────────────┘     └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │   Claude API    │
                                           │  (The Oracle)   │
                                           └─────────────────┘
```

---

## ✦ Verdict System

The Oracle assigns one of five verdicts based on the overall score:

```
Score    Verdict         Symbol   Meaning
──────   ─────────────   ──────   ────────────────────────────────────
90-100   TRANSCENDENT    ✦        Near-perfect, production-grade code
70-89    BLESSED         ☽        Good code with minor opportunities
50-69    ENCHANTED       ◈        Mixed — real strengths and real flaws
30-49    MUNDANE         ○        Mediocre, needs significant rework
 0-29    CURSED          ☠        Serious issues — bugs, security, chaos
```

---

## ✦ Prophecy Severities

Each identified issue is classified by severity:

| Severity | Icon | Meaning |
|---|---|---|
| `CRITICAL` | ⚠ | Security vulnerabilities, crashes, data loss risks |
| `WARNING` | ⚡ | Bad practices, potential bugs, missing error handling |
| `INFO` | ◉ | Style issues, minor improvements, best practices |
| `WISDOM` | ✦ | Architectural suggestions, deeper patterns |

---

## ✦ Example: What The Oracle Catches

The Oracle reviews code like a senior engineer with thousands of years of experience. Given `example_code.py`, it will detect:

- **🔒 CRITICAL** — Plaintext password storage
- **🔒 CRITICAL** — SQL injection via string concatenation  
- **⚠ WARNING** — Bare `except:` clauses swallowing all errors
- **⚠ WARNING** — Hardcoded API secrets in source code
- **⚠ WARNING** — Division by zero in `calculate_stats()`
- **◉ INFO** — Use of `type()` instead of `isinstance()`
- **✦ WISDOM** — Structural suggestions for the `UserManager` class

---

## ✦ Requirements

- Python 3.9+
- Anthropic API key
- `rich` — terminal UI
- `click` — CLI framework  
- `anthropic` — Claude API client
- `pygments` — syntax highlighting

---

## ✦ Configuration

| Environment Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) |

The `--api-key` flag can also be passed directly to any command.

---

## ✦ Philosophy

Code review is often dry, generic, and easy to ignore. The Oracle gives feedback that's memorable and precise — not because the mystical framing is the point, but because **personality makes insight stick**. Every prophecy is technically grounded. Every verdict is earned.

The Oracle doesn't flatter. It doesn't sugarcoat. It sees the code as it truly is.

---

## ✦ License

MIT — use freely, review wisely.

---

*"The Oracle has spoken. The rest is up to you."* ✦
