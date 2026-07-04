"""TerminalQuest entry point."""

import curses
import sys


def main() -> None:
    """Launch TerminalQuest."""
    try:
        curses.wrapper(_run)
    except KeyboardInterrupt:
        pass
    except curses.error as exc:
        print(f"Terminal error: {exc}", file=sys.stderr)
        print("Resize your terminal to at least 85 × 28 and try again.", file=sys.stderr)
        sys.exit(1)


def _run(stdscr: object) -> None:
    from .game import Game

    game = Game(stdscr)
    game.run()


if __name__ == "__main__":
    main()
