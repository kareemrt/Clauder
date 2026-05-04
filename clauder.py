#!/usr/bin/env python3
"""
Clauder — A beautiful terminal interface for Claude AI

Features:
  - Streaming responses with live markdown rendering
  - Adaptive thinking for complex queries
  - Prompt caching to reduce API costs
  - Multi-turn conversation history
  - Rich command system (/help, /clear, /think, /model, /save, …)
  - Per-session token usage tracking
"""

import os
import sys
import json
import datetime
from contextlib import contextmanager

import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.rule import Rule
from rich.align import Align

# ──────────────────────────────────────────────────────────────
# Global console (created once, used everywhere)
# ──────────────────────────────────────────────────────────────

console = Console()

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

VERSION = "1.0.0"

DEFAULT_MODEL = "claude-opus-4-7"

DEFAULT_SYSTEM = (
    "You are Claude, a helpful, harmless, and honest AI assistant. "
    "Be thorough but concise. When writing code, include comments and "
    "use modern best practices. Format your responses with markdown when "
    "it improves readability."
)

BANNER = r"""
   ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
  ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
  ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝
  ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗
  ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║
   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

COMMANDS = {
    "/help":           "Show this help message",
    "/clear":          "Clear conversation history",
    "/think [on|off]": "Toggle adaptive thinking (deeper reasoning)",
    "/model [name]":   "View or switch Claude model",
    "/system [text]":  "View or set the system prompt",
    "/tokens":         "Show cumulative token usage for this session",
    "/save [file]":    "Save conversation to a JSON file",
    "/history":        "Show conversation summary",
    "/exit":           "Exit Clauder",
}

AVAILABLE_MODELS = [
    "claude-opus-4-7",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "claude-haiku-4-5",
]


# ──────────────────────────────────────────────────────────────
# Streaming helper — keeps the anthropic stream alive during use
# ──────────────────────────────────────────────────────────────

@contextmanager
def managed_stream(client, **kwargs):
    with client.messages.stream(**kwargs) as stream:
        yield stream


# ──────────────────────────────────────────────────────────────
# Main application class
# ──────────────────────────────────────────────────────────────

class Clauder:
    def __init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            console.print(
                Panel(
                    "[red bold]ANTHROPIC_API_KEY environment variable is not set.[/]\n\n"
                    "Export it before running:\n"
                    "  [cyan]export ANTHROPIC_API_KEY=sk-ant-...[/]",
                    title="[red]Authentication Error[/]",
                    border_style="red",
                )
            )
            sys.exit(1)

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = DEFAULT_MODEL
        self.system_prompt = DEFAULT_SYSTEM
        self.history: list[dict] = []
        self.thinking_enabled = False
        self.session_start = datetime.datetime.now()

        # Cumulative token counters
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cache_read_tokens = 0
        self.total_cache_create_tokens = 0
        self.exchange_count = 0

    # ── Display helpers ────────────────────────────────────────

    def print_banner(self) -> None:
        console.print(Text(BANNER, style="bold cyan"), justify="center")
        console.print(
            Align.center(
                Text(
                    f"v{VERSION}  ·  Your intelligent terminal companion",
                    style="dim italic",
                )
            )
        )
        console.print()

        info = Table(
            box=box.ROUNDED,
            show_header=False,
            border_style="dim cyan",
            padding=(0, 1),
        )
        info.add_column("k", style="dim")
        info.add_column("v", style="cyan bold")
        info.add_row("Model",    self.model)
        info.add_row("Thinking", "[red]off[/]")
        info.add_row("Session",  self.session_start.strftime("%Y-%m-%d %H:%M"))
        info.add_row("Commands", "[dim]/help[/dim]")
        console.print(Align.center(info))
        console.print()
        console.print(Rule(style="dim cyan"))

    def print_help(self) -> None:
        t = Table(
            title="[bold cyan]Clauder Commands[/]",
            box=box.ROUNDED,
            border_style="cyan",
            title_style="bold cyan",
            show_lines=True,
        )
        t.add_column("Command", style="yellow", no_wrap=True)
        t.add_column("Description")
        for cmd, desc in COMMANDS.items():
            t.add_row(cmd, desc)
        console.print()
        console.print(t)
        console.print()

    def print_history(self) -> None:
        if not self.history:
            console.print("[dim]No conversation history yet.[/]")
            console.print()
            return
        t = Table(
            title="[bold]Conversation History[/]",
            box=box.SIMPLE_HEAVY,
            border_style="dim",
            show_lines=True,
        )
        t.add_column("#", style="dim", width=4)
        t.add_column("Role", width=12)
        t.add_column("Preview")
        for i, msg in enumerate(self.history, 1):
            role = msg["role"]
            preview = msg["content"]
            if len(preview) > 72:
                preview = preview[:72] + "…"
            color = "blue" if role == "user" else "green"
            t.add_row(str(i), f"[{color}]{role}[/]", f"[dim]{preview}[/dim]")
        console.print()
        console.print(t)
        console.print()

    def print_tokens(self) -> None:
        t = Table(
            title="[bold]Token Usage — Session[/]",
            box=box.ROUNDED,
            border_style="dim cyan",
        )
        t.add_column("Metric", style="dim")
        t.add_column("Tokens", style="cyan bold", justify="right")
        t.add_row("Input (uncached)",  f"{self.total_input_tokens:,}")
        t.add_row("Cache reads",        f"{self.total_cache_read_tokens:,}")
        t.add_row("Cache writes",       f"{self.total_cache_create_tokens:,}")
        t.add_row("Output",             f"{self.total_output_tokens:,}")
        t.add_row("[bold]Exchanges[/]", f"[bold]{self.exchange_count}[/bold]")
        console.print()
        console.print(t)
        console.print()

    # ── Core: streaming response ───────────────────────────────

    def stream_response(self, user_input: str) -> None:
        self.history.append({"role": "user", "content": user_input})

        # System prompt with prompt caching
        system = [
            {
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        thinking_param = (
            {"type": "adaptive"} if self.thinking_enabled else {"type": "disabled"}
        )

        console.print()
        console.print(
            Panel(
                Text("Claude", style="bold green"),
                expand=False,
                border_style="green",
                padding=(0, 1),
            )
        )

        full_response = ""
        thinking_text = ""

        try:
            with managed_stream(
                self.client,
                model=self.model,
                max_tokens=8192,
                system=system,
                thinking=thinking_param,
                messages=self.history,
            ) as stream:
                with Live(console=console, refresh_per_second=15) as live:
                    for event in stream:
                        etype = event.type

                        if etype == "content_block_start":
                            block_type = event.content_block.type
                            if block_type == "thinking":
                                live.update(
                                    Text("⟳ Thinking…", style="dim italic yellow")
                                )

                        elif etype == "content_block_delta":
                            dtype = event.delta.type
                            if dtype == "thinking_delta":
                                thinking_text += event.delta.thinking
                            elif dtype == "text_delta":
                                full_response += event.delta.text
                                try:
                                    live.update(Markdown(full_response))
                                except Exception:
                                    live.update(Text(full_response))

                # Get final message for usage stats (while stream is still open)
                final = stream.get_final_message()

            # Update cumulative counters
            usage = final.usage
            self.total_input_tokens        += usage.input_tokens
            self.total_output_tokens       += usage.output_tokens
            self.total_cache_read_tokens   += getattr(usage, "cache_read_input_tokens", 0) or 0
            self.total_cache_create_tokens += getattr(usage, "cache_creation_input_tokens", 0) or 0

        except anthropic.APIConnectionError:
            console.print("[red]Connection error — check your internet connection.[/]")
            self.history.pop()
            return
        except anthropic.AuthenticationError:
            console.print("[red]Authentication failed — check your ANTHROPIC_API_KEY.[/]")
            sys.exit(1)
        except anthropic.RateLimitError:
            console.print("[red]Rate limited — please wait a moment and try again.[/]")
            self.history.pop()
            return
        except anthropic.APIStatusError as exc:
            console.print(f"[red]API error ({exc.status_code}):[/] {exc.message}")
            self.history.pop()
            return

        console.print()

        # Show thinking summary (collapsed) when thinking was active
        if self.thinking_enabled and thinking_text:
            snippet = thinking_text[:300] + ("…" if len(thinking_text) > 300 else "")
            console.print(
                Panel(
                    Text(snippet, style="dim"),
                    title="[yellow dim]Thinking (excerpt)[/]",
                    border_style="yellow dim",
                    padding=(0, 1),
                )
            )
            console.print()

        # Per-exchange usage footer
        cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
        cache_hit_note = f"  [dim]💾 cache hit: {cache_read:,}[/dim]" if cache_read else ""
        console.print(
            f"  [dim]▸ in: {usage.input_tokens:,}  "
            f"out: {usage.output_tokens:,}{cache_hit_note}[/dim]"
        )
        console.print()

        self.history.append({"role": "assistant", "content": full_response})
        self.exchange_count += 1

    # ── Command dispatcher ─────────────────────────────────────

    def handle_command(self, raw: str) -> bool:
        """Process a slash command.  Returns False when the app should exit."""
        parts = raw.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd == "/help":
            self.print_help()

        elif cmd == "/clear":
            self.history.clear()
            console.print("[yellow]✓ Conversation history cleared.[/]")
            console.print()

        elif cmd == "/think":
            if arg.lower() in ("on", "1", "true"):
                self.thinking_enabled = True
            elif arg.lower() in ("off", "0", "false"):
                self.thinking_enabled = False
            else:
                self.thinking_enabled = not self.thinking_enabled

            state = "[bold green]ON[/]" if self.thinking_enabled else "[bold red]OFF[/]"
            console.print(f"[bold]Adaptive thinking:[/] {state}")
            if self.thinking_enabled:
                console.print(
                    "[dim]  Claude will reason carefully before answering.[/dim]"
                )
            console.print()

        elif cmd == "/model":
            if arg:
                self.model = arg
                console.print(f"[green]✓ Model switched to[/] [bold]{arg}[/]")
                console.print(
                    "[dim]  Conversation history is preserved; "
                    "prompt cache will be rebuilt on next message.[/dim]"
                )
            else:
                t = Table(box=box.SIMPLE, show_header=False, border_style="dim")
                t.add_column(width=2)
                t.add_column()
                for m in AVAILABLE_MODELS:
                    marker = "[cyan bold]▶[/]" if m == self.model else " "
                    t.add_row(marker, m)
                console.print()
                console.print(t)
            console.print()

        elif cmd == "/system":
            if arg:
                self.system_prompt = arg
                console.print("[green]✓ System prompt updated.[/]")
                console.print(
                    Panel(arg[:200], border_style="dim", title="[dim]New system prompt[/dim]")
                )
            else:
                console.print(
                    Panel(
                        self.system_prompt,
                        border_style="dim cyan",
                        title="[dim cyan]Current system prompt[/dim cyan]",
                    )
                )
            console.print()

        elif cmd == "/tokens":
            self.print_tokens()

        elif cmd == "/save":
            filename = (
                arg or f"clauder_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
            )
            payload = {
                "clauder_version": VERSION,
                "model":           self.model,
                "system_prompt":   self.system_prompt,
                "thinking":        self.thinking_enabled,
                "session_start":   self.session_start.isoformat(),
                "usage": {
                    "input_tokens":         self.total_input_tokens,
                    "output_tokens":        self.total_output_tokens,
                    "cache_read_tokens":    self.total_cache_read_tokens,
                    "cache_create_tokens":  self.total_cache_create_tokens,
                    "exchanges":            self.exchange_count,
                },
                "messages": self.history,
            }
            with open(filename, "w") as fh:
                json.dump(payload, fh, indent=2)
            console.print(f"[green]✓ Saved to[/] [cyan]{filename}[/]")
            console.print()

        elif cmd == "/history":
            self.print_history()

        elif cmd == "/exit":
            duration = datetime.datetime.now() - self.session_start
            mins, secs = divmod(int(duration.total_seconds()), 60)
            console.print()
            console.print(
                Panel(
                    f"[bold]Session complete[/]\n\n"
                    f"Duration:  [cyan]{mins}m {secs}s[/]\n"
                    f"Exchanges: [cyan]{self.exchange_count}[/]\n"
                    f"Model:     [cyan]{self.model}[/]\n\n"
                    f"[dim italic]Thanks for using Clauder![/]",
                    border_style="cyan",
                    title="[cyan]Goodbye[/]",
                    title_align="center",
                )
            )
            return False

        else:
            console.print(
                f"[red]Unknown command:[/] {cmd}  "
                f"— type [yellow]/help[/] for available commands."
            )
            console.print()

        return True

    # ── Main REPL loop ─────────────────────────────────────────

    def run(self) -> None:
        self.print_banner()

        while True:
            try:
                console.print(Rule(style="dim"))
                prompt_color = "yellow" if self.thinking_enabled else "blue"
                user_input = Prompt.ask(
                    f"\n[{prompt_color} bold]You[/]"
                ).strip()

                if not user_input:
                    continue

                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue

                self.stream_response(user_input)

            except KeyboardInterrupt:
                console.print(
                    "\n[dim]Interrupted — type [yellow]/exit[/] to quit "
                    "or keep chatting.[/]"
                )
                console.print()
            except EOFError:
                break


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────

def main() -> None:
    app = Clauder()
    app.run()


if __name__ == "__main__":
    main()
