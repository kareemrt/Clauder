#!/usr/bin/env python3
"""
Clauder: Natural Language Shell

Type commands in plain English. Claude translates them to shell commands,
explains what they do, and runs them only after your approval.

Usage:
    python clauder.py

Environment:
    ANTHROPIC_API_KEY  Your Anthropic API key (required)
"""

import os
import subprocess
import sys
from typing import Optional

import anthropic

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"

SAFETY_COLOUR = {"safe": GREEN, "caution": YELLOW, "dangerous": RED}
SAFETY_ICON = {"safe": "✓", "caution": "⚠", "dangerous": "✗"}

# ── System prompt (cached) ────────────────────────────────────────────────────
SYSTEM_PROMPT = """\
You are a shell-command translator embedded in an interactive terminal tool called Clauder.
The user types requests in natural language; you respond by calling the `propose_command` tool
with a precise shell command that fulfils the request, an explanation a junior developer would
understand, and a safety assessment.

Rules:
- Always call `propose_command` — never respond with plain text alone.
- Prefer portable POSIX/bash commands. Avoid obscure flags unless necessary.
- For multi-step tasks, chain commands with && or write a concise one-liner.
- Set safety_level:
    "safe"      – purely read-only or trivially reversible (ls, cat, echo, grep…)
    "caution"   – writes new files, installs packages, or touches config
    "dangerous" – deletes files/data, modifies system state, or is irreversible
- Set can_be_undone to true only when the action is genuinely reversible (e.g. moves to trash,
  git operations, package installs that can be uninstalled).
- If the request is ambiguous, pick the safest reasonable interpretation and note it in the
  explanation.
- If the request is completely impossible to translate to a shell command (e.g. "how are you?"),
  call `propose_command` with an empty string for `command` and explain why in the `explanation`.
"""

# ── Tool definition ───────────────────────────────────────────────────────────
PROPOSE_COMMAND_TOOL = {
    "name": "propose_command",
    "description": "Propose a shell command that satisfies the user's natural language request.",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The exact shell command to run. Empty string if untranslatable.",
            },
            "explanation": {
                "type": "string",
                "description": "Plain-English explanation of what the command does and why.",
            },
            "safety_level": {
                "type": "string",
                "enum": ["safe", "caution", "dangerous"],
                "description": "Safety classification of the command.",
            },
            "can_be_undone": {
                "type": "boolean",
                "description": "Whether the action can be reasonably reversed.",
            },
        },
        "required": ["command", "explanation", "safety_level", "can_be_undone"],
    },
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def cprint(colour: str, text: str, **kwargs) -> None:
    print(f"{colour}{text}{RESET}", **kwargs)


def print_banner() -> None:
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════╗
║  Clauder · Natural Language Shell   ║
╚══════════════════════════════════════╝{RESET}
{DIM}Type a request in plain English.
Special commands: {BOLD}history{RESET}{DIM}, {BOLD}clear{RESET}{DIM}, {BOLD}help{RESET}{DIM}, {BOLD}exit{RESET}{DIM}
""")


def print_help() -> None:
    print(f"""
{BOLD}Usage:{RESET}
  Just describe what you want in plain English and press Enter.

{BOLD}Examples:{RESET}
  {CYAN}»{RESET} show me all Python files modified in the last 7 days
  {CYAN}»{RESET} count lines in every .py file in this directory
  {CYAN}»{RESET} find processes using port 8080
  {CYAN}»{RESET} compress the logs folder into a tarball

{BOLD}Special commands:{RESET}
  {BOLD}history{RESET}   Show the session's executed commands
  {BOLD}clear{RESET}     Clear the screen
  {BOLD}help{RESET}      Show this message
  {BOLD}exit{RESET}      Quit Clauder
""")


def confirm(prompt: str) -> bool:
    """Ask y/n; default no."""
    try:
        answer = input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return answer in ("y", "yes")


def run_command(command: str) -> tuple[int, str, str]:
    """Execute a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
    )
    return result.returncode, result.stdout, result.stderr


# ── Core translation via Claude ───────────────────────────────────────────────
def translate(
    client: anthropic.Anthropic,
    user_request: str,
    history: list[dict],
) -> Optional[dict]:
    """
    Send user_request to Claude and extract the proposed command dict.
    Returns None on API error.
    """
    history.append({"role": "user", "content": user_request})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=[PROPOSE_COMMAND_TOOL],
            tool_choice={"type": "auto"},
            messages=history,
        )
    except anthropic.APIError as exc:
        cprint(RED, f"\nAPI error: {exc}\n")
        history.pop()
        return None

    # Append assistant turn to history for context continuity
    history.append({"role": "assistant", "content": response.content})

    # Extract the tool call
    for block in response.content:
        if block.type == "tool_use" and block.name == "propose_command":
            return block.input

    return None


# ── Main REPL ─────────────────────────────────────────────────────────────────
def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        cprint(RED, "Error: ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    conversation_history: list[dict] = []
    executed_history: list[str] = []

    print_banner()

    while True:
        try:
            user_input = input(f"{BOLD}{BLUE}clauder{RESET} {CYAN}»{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            cprint(DIM, "Goodbye!")
            break

        if not user_input:
            continue

        lowered = user_input.lower()

        if lowered in ("exit", "quit", "q"):
            cprint(DIM, "Goodbye!")
            break

        if lowered == "clear":
            print("\033[2J\033[H", end="")
            continue

        if lowered == "help":
            print_help()
            continue

        if lowered == "history":
            if not executed_history:
                cprint(DIM, "\n  (no commands executed this session)\n")
            else:
                print()
                for i, cmd in enumerate(executed_history, 1):
                    print(f"  {DIM}{i:3}.{RESET} {cmd}")
                print()
            continue

        # ── Translate ──────────────────────────────────────────────────────
        cprint(DIM, "  thinking…")
        proposal = translate(client, user_input, conversation_history)

        if proposal is None:
            continue

        command: str = proposal.get("command", "").strip()
        explanation: str = proposal.get("explanation", "")
        safety: str = proposal.get("safety_level", "caution")
        undoable: bool = proposal.get("can_be_undone", False)

        # ── Display proposal ───────────────────────────────────────────────
        print()
        colour = SAFETY_COLOUR.get(safety, YELLOW)
        icon = SAFETY_ICON.get(safety, "?")

        if not command:
            cprint(YELLOW, f"  {icon}  {explanation}\n")
            continue

        cprint(BOLD + colour, f"  {icon}  [{safety.upper()}]  {'reversible' if undoable else 'irreversible'}")
        print(f"  {DIM}Explanation:{RESET} {explanation}")
        print(f"\n  {BOLD}$ {command}{RESET}\n")

        if safety == "dangerous":
            cprint(RED + BOLD, "  !! This command is potentially destructive. !!")

        # ── Confirm & run ──────────────────────────────────────────────────
        prompt_colour = colour
        run_it = confirm(f"  {prompt_colour}Run this command? [y/N]{RESET} ")

        if not run_it:
            cprint(DIM, "  Skipped.\n")
            continue

        print()
        returncode, stdout, stderr = run_command(command)
        executed_history.append(command)

        if stdout:
            print(stdout, end="" if stdout.endswith("\n") else "\n")
        if stderr:
            cprint(YELLOW, stderr, end="" if stderr.endswith("\n") else "\n")

        status_colour = GREEN if returncode == 0 else RED
        cprint(status_colour + DIM, f"  [exit {returncode}]\n")


if __name__ == "__main__":
    main()
