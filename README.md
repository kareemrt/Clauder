# Clauder

**Natural Language Shell** — type commands in plain English, get back shell commands with explanations, and run them with a single keystroke.

## What it does

Clauder sits between you and your terminal. You describe what you want in plain English; Claude translates it into a precise shell command, explains what it does, rates its safety, and only executes it after your explicit approval.

```
clauder » show me all Python files modified in the last 7 days
  thinking…

  ✓  [SAFE]  reversible
  Explanation: Uses `find` to list .py files whose modification time is within 7 days.

  $ find . -name "*.py" -mtime -7

  Run this command? [y/N] y

./clauder.py
./requirements.txt

  [exit 0]
```

## Features

- **Plain-English commands** — describe any shell task in natural language
- **Safety classification** — every command is rated `safe`, `caution`, or `dangerous`
- **Reversibility flag** — tells you upfront if an action can be undone
- **Session context** — Claude remembers earlier commands so you can say "now sort that by size"
- **Prompt caching** — system prompt is cached so repeated queries are fast and cheap
- **Command history** — type `history` to see everything you've run this session

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python clauder.py
```

## Special commands

| Command   | Action                              |
|-----------|-------------------------------------|
| `history` | Show all commands run this session  |
| `clear`   | Clear the screen                    |
| `help`    | Show usage examples                 |
| `exit`    | Quit                                |
