# Clauder

```
   ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
  ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
  ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝
  ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗
  ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║
   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
```

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Anthropic](https://img.shields.io/badge/powered%20by-Claude%20AI-orange?style=flat-square)](https://www.anthropic.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Rich](https://img.shields.io/badge/terminal%20UI-Rich-purple?style=flat-square)](https://github.com/Textualize/rich)

**Clauder** is a beautiful, feature-rich terminal interface for Claude AI. Stream responses in real time, toggle deep reasoning, track token usage, and hold multi-turn conversations — all from your terminal.

---

## Features

| Feature | Description |
|---|---|
| **Streaming responses** | Live token-by-token output rendered as beautiful markdown |
| **Adaptive thinking** | Toggle Claude's extended reasoning for complex problems |
| **Prompt caching** | Ephemeral cache on the system prompt reduces API costs over a session |
| **Multi-turn history** | Full conversation context preserved across every exchange |
| **Token tracking** | Per-exchange and cumulative usage stats (input, output, cache reads/writes) |
| **Rich command system** | `/help`, `/think`, `/model`, `/save`, `/history`, and more |
| **Model switching** | Switch between Claude models mid-conversation |
| **Conversation export** | Save full sessions to JSON for analysis or sharing |

---

## Installation

### Prerequisites

- Python 3.10 or later
- An [Anthropic API key](https://console.anthropic.com/)

### Setup

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Launch Clauder
python clauder.py
```

---

## Usage

When you launch Clauder, you'll see the banner and an info table showing your current model, session time, and thinking status. Type any message to start chatting, or use a slash command.

```
┌─────────────────────────────────────┐
│ Model    claude-opus-4-7            │
│ Thinking off                        │
│ Session  2025-01-01 09:00           │
│ Commands /help                      │
└─────────────────────────────────────┘

──────────────────────────────────────

You › Explain the difference between TCP and UDP in one paragraph.

╭── Claude ────────────────────────────╮
│ TCP (Transmission Control Protocol) │
│ guarantees delivery, ordering, and  │
│ error-checking through handshaking  │
│ and acknowledgments — ideal for     │
│ web pages, emails, and file         │
│ transfers. UDP (User Datagram       │
│ Protocol) skips that overhead,      │
│ trading reliability for speed —     │
│ perfect for live video, gaming, and │
│ DNS lookups where a dropped packet  │
│ is better than a late one.          │
╰──────────────────────────────────────╯

  ▸ in: 312  out: 89
```

---

## Commands

| Command | Description |
|---|---|
| `/help` | Show this command reference |
| `/clear` | Clear conversation history |
| `/think [on\|off]` | Toggle adaptive thinking (deeper, slower reasoning) |
| `/model [name]` | View or switch the Claude model |
| `/system [text]` | View or update the system prompt |
| `/tokens` | Show cumulative token usage for this session |
| `/save [file]` | Save full conversation to a JSON file |
| `/history` | Show a tabular summary of the conversation so far |
| `/exit` | Exit with a session summary |

### Tip: Adaptive Thinking

When you `/think on`, Claude reasons step-by-step before responding. The prompt color shifts to yellow as a reminder. Use it for math, logic puzzles, code debugging, or any problem that benefits from careful deliberation.

```
You › /think on
Adaptive thinking: ON
  Claude will reason carefully before answering.

You [thinking mode] › Prove that √2 is irrational.
```

---

## Available Models

| Model | ID | Best For |
|---|---|---|
| Claude Opus 4.7 | `claude-opus-4-7` | Most capable, complex tasks |
| Claude Opus 4.6 | `claude-opus-4-6` | High capability, reliable |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Balanced speed and quality |
| Claude Haiku 4.5 | `claude-haiku-4-5` | Fastest, cost-efficient |

Switch models with `/model claude-sonnet-4-6`.

---

## Architecture

```
clauder.py
├── console           Global Rich Console (module-level)
├── managed_stream    Context manager — keeps stream alive for get_final_message()
└── Clauder (class)
    ├── __init__      API client, model config, history, token counters
    ├── print_banner  ASCII logo + session info table
    ├── print_help    Command reference table
    ├── print_history Conversation summary table
    ├── print_tokens  Cumulative token usage table
    ├── stream_response
    │   ├── Appends user turn to history
    │   ├── Builds system block with cache_control
    │   ├── Streams with Live + Markdown rendering
    │   ├── Calls get_final_message() for usage stats
    │   └── Appends assistant turn to history
    ├── handle_command Slash command dispatcher
    └── run            REPL loop (Prompt.ask → dispatch)
```

### Key Design Decisions

- **Prompt caching** — The system prompt is tagged with `cache_control: {type: "ephemeral"}`. After the first exchange, Claude reads the prompt from cache rather than re-tokenizing it, reducing costs on long sessions.
- **Adaptive thinking** — Uses `thinking: {type: "adaptive"}` (not a fixed budget). Claude decides dynamically how much to think based on query complexity.
- **Stream context manager** — `managed_stream` wraps `client.messages.stream()` so `get_final_message()` can be called after iterating events without the stream closing early.
- **Single global console** — One `rich.Console` instance is shared across all rendering so output is always synchronized.

---

## Token Usage

After each response, Clauder shows a compact usage footer:

```
  ▸ in: 1,204  out: 347  💾 cache hit: 890
```

View cumulative session stats at any time with `/tokens`:

```
╭──────────────────────────────╮
│ Token Usage — Session        │
├──────────────────┬───────────┤
│ Input (uncached) │     2,108 │
│ Cache reads      │     4,460 │
│ Cache writes     │       890 │
│ Output           │     1,203 │
│ Exchanges        │         5 │
╰──────────────────┴───────────╯
```

---

## Saving Conversations

```bash
# Auto-named by session timestamp
/save

# Custom filename
/save my_research_session.json
```

The saved JSON contains the model, system prompt, thinking state, full usage stats, and every message in the conversation.

---

## License

MIT — see [LICENSE](LICENSE) for details.
