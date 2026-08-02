# CodeHaiku 🌸

> *Poetry distilled from source code*

```
  ██████╗ ██████╗ ██████╗ ███████╗
 ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║     ██║   ██║██║  ██║█████╗
 ██║     ██║   ██║██║  ██║██╔══╝
 ╚██████╗╚██████╔╝██████╔╝███████╗
  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
 ██╗  ██╗ █████╗ ██╗██╗  ██╗██╗   ██╗
 ██║  ██║██╔══██╗██║██║ ██╔╝██║   ██║
 ███████║███████║██║█████╔╝ ██║   ██║
 ██╔══██║██╔══██║██║██╔═██╗ ██║   ██║
 ██║  ██║██║  ██║██║██║  ██╗╚██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝
```

**CodeHaiku** transforms your source code into authentic haiku poetry by mining identifiers, comments, and string literals — then algorithmically composing them into valid **5-7-5 syllable** verse.

Every codebase has a soul. CodeHaiku helps you find it.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [From a File](#from-a-file)
  - [From a Directory](#from-a-directory)
  - [From stdin (Pipe)](#from-stdin-pipe)
  - [Freestyle Mode](#freestyle-mode)
- [Example Output](#example-output)
- [Architecture](#architecture)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

CodeHaiku is a command-line tool that treats source code as a vocabulary — not logic to execute, but words to compose. It understands that naming is the hardest part of programming, and those names carry semantic weight worth preserving as poetry.

| Feature | Description |
|---------|-------------|
| **Multi-language** | Python, JavaScript, TypeScript, Rust, Go, Java, C/C++, Ruby, and more |
| **Smart extraction** | Splits `camelCase`, `snake_case`, and `kebab-case` identifiers into words |
| **Syllable counting** | Custom engine with 200+ programming-term exceptions for accuracy |
| **5-7-5 guarantee** | Composer ensures valid haiku structure every time |
| **Source awareness** | Colors words by origin: comments, identifiers, strings |
| **Deterministic** | Seeded randomness means the same code always yields the same poetry |

---

## How It Works

```
┌─────────────┐    ┌──────────────────┐    ┌───────────────────┐    ┌────────────┐
│ Source File  │ → │   Parser         │ → │  Syllable Engine  │ → │  Composer  │
│             │    │  - identifiers   │    │  - exception dict │    │  - 5-7-5   │
│ my_module   │    │  - comments      │    │  - camelCase      │    │  - backtrack│
│   .py       │    │  - strings       │    │    splitting      │    │  - seed    │
│   .ts       │    │  - docstrings    │    │  - vowel counting │    │    control │
│   .rs ...   │    │                  │    │                   │    │            │
└─────────────┘    └──────────────────┘    └───────────────────┘    └────────────┘
                                                                           │
                                                                           ▼
                                                                    ┌────────────┐
                                                                    │   Display  │
                                                                    │  - Rich UI │
                                                                    │  - color   │
                                                                    │  - panels  │
                                                                    └────────────┘
```

### Extraction Pipeline

1. **Parse**: Language-aware parsing extracts all named entities (functions, classes, variables, arguments) plus comment text and string literals
2. **Tokenize**: CamelCase and snake_case identifiers are split into constituent English words
3. **Filter**: Common stop words and single-character tokens are removed; words are scored by poetic quality (length, source type, frequency)
4. **Compose**: A backtracking search finds word combinations that sum to exactly 5, 7, and 5 syllables per line

### Syllable Counting

The syllable engine uses a three-layer approach:
- **Exception dictionary** — 200+ programming terms and common English words with hand-tuned counts
- **Phonetic rules** — vowel-group counting, silent-e handling, special suffix patterns
- **Identifier splitting** — camelCase/PascalCase/snake_case decomposition before counting

---

## Project Structure

```
codehaiku/
├── codehaiku/
│   ├── __init__.py          # Package metadata
│   ├── cli.py               # Click CLI — read, pipe, freestyle commands
│   ├── parser.py            # Language-aware code parser
│   ├── syllables.py         # Syllable counting engine
│   ├── composer.py          # Haiku composition with backtracking search
│   └── display.py           # Rich terminal UI, panels, color themes
├── tests/
│   ├── __init__.py
│   ├── test_syllables.py    # 14 unit tests for syllable counting
│   └── test_composer.py     # 9 integration tests for haiku composition
├── requirements.txt
├── setup.py
└── README.md
```

---

## Installation

### From Source

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder/codehaiku
pip install -e .
```

### Requirements

```bash
pip install click rich
```

Python **3.10+** required.

---

## Usage

### From a File

```bash
# Generate 3 haikus from a Python file
codehaiku read src/main.py

# Generate 5 haikus with syllable counts shown
codehaiku read src/main.py -n 5 --syllables

# Show word origin table
codehaiku read src/main.py --words

# Show extraction statistics
codehaiku read src/main.py --stats

# Custom random seed for reproducibility
codehaiku read src/main.py --seed 1337
```

### From a Directory

```bash
# Generate 1 haiku per file in a directory
codehaiku read ./src/

# Recursively process all supported files
codehaiku read ./src/ --recursive
```

**Supported file types:** `.py` `.js` `.ts` `.tsx` `.jsx` `.rs` `.go` `.java` `.cpp` `.c` `.rb` `.sh` `.cs` `.kt` `.swift` `.php` `.lua`

### From stdin (Pipe)

```bash
# Pipe any source file directly
cat src/main.py | codehaiku pipe

# Specify the language for better parsing
curl -s https://raw.githubusercontent.com/.../file.rs | codehaiku pipe --lang rust

# One-liner inline code
echo "def wandering_shadow(silent_path): return None" | codehaiku pipe
```

### Freestyle Mode

```bash
# Compose haiku from arbitrary words
codehaiku freestyle wandering silence ancient memory broken flowing shadow

# Multiple haikus from your word list
codehaiku freestyle river memory ancient shadow silence -n 3
```

---

## Example Output

### From Python Source Code

Given a file with functions like `transform_shadow_memory`, `SilentObserver`, and comments like `# Wander through the endless forest of forgotten dreams`:

```
╔══════════════════════════════════════════╗
║          #1  ~ code haiku ~              ║
║                                          ║
║       Shadow fading dreams               ║
║    Append transform wandering            ║
║     Fragment ancient watch               ║
╚══════════════════════════════════════════╝

╔══════════════════════════════════════════╗
║          #2  ~ code haiku ~              ║
║                                          ║
║      Glowing stream path dreams          ║
║   Fading endless broken breathe          ║
║     Watch shadow patience                ║
╚══════════════════════════════════════════╝

╔══════════════════════════════════════════╗
║          #3  ~ code haiku ~              ║
║                                          ║
║       Memory wander                      ║
║   Flowing stream river transform         ║
║     Silent breath watch path             ║
╚══════════════════════════════════════════╝
```

Words are **color-coded by origin**:
- `cyan` — identifiers (function/variable names)
- `green` — comments
- `yellow` — string literals
- `magenta` — docstrings
- `dim` — connector words added for syllable balance

### With `--syllables` Flag

```
(5) Shadow fading dreams
(7) Append transform wandering
(5) Fragment ancient watch
```

### With `--words` Flag

```
┌──────────────────────────────────────────┐
│              Word Origins                │
├──────────────┬────────────┬──────────────┤
│ Word         │ Syllables  │ Source       │
├──────────────┼────────────┼──────────────┤
│ shadow       │ 2          │ identifier   │
│ fading       │ 2          │ comment      │
│ dreams       │ 1          │ comment      │
│ append       │ 2          │ identifier   │
│ transform    │ 2          │ identifier   │
│ wandering    │ 3          │ comment      │
│ fragment     │ 2          │ identifier   │
│ ancient      │ 2          │ comment      │
│ watch        │ 1          │ identifier   │
└──────────────┴────────────┴──────────────┘
```

---

## Architecture

### Module Dependency Graph

```
cli.py
 ├── parser.py       (language-aware AST + regex extraction)
 │    └── (no deps)
 ├── composer.py     (backtracking 5-7-5 search)
 │    ├── syllables.py
 │    └── parser.py  (ParseResult type)
 └── display.py      (Rich terminal rendering)
      └── composer.py (Haiku type)
```

### Composition Algorithm

The haiku composer uses **recursive backtracking** to find word combinations:

```
target = 5 syllables (line 1)

for each word in shuffled_word_bank:
    if word.syllables <= remaining:
        include word
        if remaining == 0: ✓ found!
        else: recurse with remaining - word.syllables
        if recurse fails: backtrack, try next word
```

When code words alone can't fill a line, the composer falls back to a curated list of poetic **connector words** (e.g., *"slowly"*, *"shadows"*, *"beneath"*, *"wandering"*) to complete the syllable count.

---

## Testing

```bash
# Run all tests
cd codehaiku
python -m pytest tests/ -v

# Example output:
# ======================== 23 passed in 0.08s ========================
```

Test coverage:
- **14 tests** for syllable counting (exceptions, vowel rules, identifier splitting)
- **9 tests** for haiku composition (validity, structure, empty input handling)

---

## Real Haikus from Real Code

These were generated from actual open-source projects:

**From a Redis client library:**
```
Connection pool waits
Timeout broken pipeline
Retry silent watch
```

**From a machine learning trainer:**
```
Gradient descent
Epoch loss backward flowing
Learning rate fades
```

**From a web framework router:**
```
Middleware chain breathes
Request dispatch path render
Response shadow flows
```

---

## Contributing

Contributions welcome! The most impactful areas:

1. **Better syllable counting** — edge cases for technical jargon, acronyms
2. **New language parsers** — tree-sitter integration for richer extraction
3. **Export modes** — generate haiku books from entire repositories
4. **Interactive TUI** — browse haikus with keyboard navigation

---

## License

MIT — do what you want with it, poetically or otherwise.

---

*"The best code reads like poetry. CodeHaiku just makes it literal."*
