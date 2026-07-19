#!/usr/bin/env python3
"""
life — Conway's Game of Life with Evolutionary Pattern Discovery
================================================================
Usage:
  python -m life demo                # watch a classic pattern menagerie
  python -m life evolve              # run the genetic algorithm
  python -m life random              # random soup simulation
  python -m life pattern <name>      # run a specific named pattern
  python -m life list                # list available patterns
"""
from __future__ import annotations

import argparse
import sys
import time

import numpy as np
from rich.console import Console
from rich.table import Table
from rich import box
from rich.live import Live
from rich.columns import Columns

from life.board import Board
from life.patterns import PATTERNS, PATTERN_INFO
from life.renderer import (
    console,
    render_board_simple,
    render_board_gradient,
    render_stats,
    render_evolution_bar,
    print_header,
)
from life.evolution import Evolution, Individual

# ── default dimensions ────────────────────────────────────────────────────────
DEFAULT_W = 60
DEFAULT_H = 30


# ── helpers ───────────────────────────────────────────────────────────────────
def _centre_pattern(board: Board, pattern: np.ndarray) -> None:
    ph, pw = pattern.shape
    row = max(0, (board.height - ph) // 2)
    col = max(0, (board.width  - pw) // 2)
    board.load(pattern, row, col)


def _run_board(
    board: Board,
    max_gens: int = 300,
    delay: float = 0.07,
    title: str = "",
    color: str = "bright_cyan",
    silent: bool = False,
) -> None:
    age_grid = board.grid.copy().astype(np.int32)

    with Live(console=console, refresh_per_second=20) as live:
        for _ in range(max_gens):
            panel = render_board_gradient(
                board.grid, age_grid=age_grid,
                title=f"[bold]{title}[/bold]  gen=[cyan]{board.generation}[/cyan]  pop=[green]{board.population()}[/green]",
            )
            stats = render_stats(
                board.generation, board.population()
            )
            live.update(Columns([panel, stats]))

            if board.is_dead():
                break

            prev = board.grid.copy()
            board.step()
            age_grid = np.where(prev & board.grid, age_grid + 1, board.grid.astype(np.int32))

            if board.is_stable(window=10):
                break
            time.sleep(delay)


# ── commands ──────────────────────────────────────────────────────────────────
def cmd_list(_args: argparse.Namespace) -> None:
    print_header()
    t = Table(title="Built-in Patterns", box=box.ROUNDED, border_style="cyan")
    t.add_column("Name", style="bold bright_cyan", no_wrap=True)
    t.add_column("Description", style="white")
    for name, desc in PATTERN_INFO.items():
        t.add_row(name, desc)
    console.print(t)


def cmd_pattern(args: argparse.Namespace) -> None:
    name = args.name
    if name not in PATTERNS:
        console.print(f"[red]Unknown pattern '{name}'. Run `life list` to see all.[/red]")
        sys.exit(1)

    print_header()
    console.print(f"  [dim]{PATTERN_INFO.get(name, '')}[/dim]\n")

    board = Board(DEFAULT_W, DEFAULT_H)
    _centre_pattern(board, PATTERNS[name])
    _run_board(board, max_gens=args.gens, delay=args.delay, title=name)


def cmd_demo(args: argparse.Namespace) -> None:
    print_header()
    sequence = [
        ("glider_gun",     "bright_cyan",    200),
        ("pulsar",         "bright_green",   120),
        ("pentadecathlon", "bright_yellow",  120),
        ("lwss",           "bright_magenta", 100),
    ]
    for name, color, gens in sequence:
        console.print(f"\n  [bold]{name}[/bold]  [dim]— {PATTERN_INFO[name]}[/dim]")
        board = Board(DEFAULT_W, DEFAULT_H)
        _centre_pattern(board, PATTERNS[name])
        _run_board(board, max_gens=gens, delay=args.delay, title=name, color=color)
        time.sleep(0.5)


def cmd_random(args: argparse.Namespace) -> None:
    print_header()
    console.print(f"  [dim]Random soup · density={args.density:.2f}[/dim]\n")
    board = Board(DEFAULT_W, DEFAULT_H)
    board.randomize(density=args.density, seed=args.seed)
    _run_board(board, max_gens=args.gens, delay=args.delay, title="Random Soup")


def cmd_evolve(args: argparse.Namespace) -> None:
    print_header()
    console.print(
        f"  [dim]Evolving interesting Life configurations · "
        f"pop={args.pop}  evo_gens={args.evo_gens}  eval_gens={args.eval_gens}[/dim]\n"
    )

    evo = Evolution(
        pop_size=args.pop,
        board_width=args.width,
        board_height=args.height,
        eval_gens=args.eval_gens,
    )

    best_fitness_history: list[float] = []
    mean_fitness_history: list[float] = []

    with Live(console=console, refresh_per_second=4) as live:
        for gen in range(1, args.evo_gens + 1):
            best = evo.step()
            log  = evo.log[-1]
            best_fitness_history.append(log["best_fitness"])
            mean_fitness_history.append(log["mean_fitness"])
            bar = render_evolution_bar(gen, args.evo_gens, log["best_fitness"], log["mean_fitness"])
            live.update(bar)

    assert evo.best is not None
    b = evo.best

    console.print(
        f"\n  [bold bright_green]Evolution complete![/bold bright_green]  "
        f"Best fitness = [bold]{b.fitness:.4f}[/bold]"
    )
    console.print(
        f"  Alive for [cyan]{b.metadata.get('alive_gens', '?')}[/cyan] generations · "
        f"[cyan]{b.metadata.get('unique_states', '?')}[/cyan] unique states · "
        f"max pop [cyan]{b.metadata.get('max_pop', '?')}[/cyan]\n"
    )

    # Replay the evolved champion
    console.print("  [dim]Replaying evolved champion…[/dim]\n")
    board = Board(args.width, args.height)
    board.grid = b.genome.copy()
    _run_board(board, max_gens=args.replay, delay=args.delay, title="Evolved Champion", color="bright_magenta")


# ── entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="life",
        description="Conway's Game of Life — with an evolutionary twist",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    sub.add_parser("list", help="List all built-in patterns")

    # pattern
    p_pat = sub.add_parser("pattern", help="Run a named pattern")
    p_pat.add_argument("name", help="Pattern name (see `life list`)")
    p_pat.add_argument("--gens",  type=int,   default=300,  help="Max generations")
    p_pat.add_argument("--delay", type=float, default=0.07, help="Frame delay in seconds")

    # demo
    p_demo = sub.add_parser("demo", help="Showcase a curated pattern sequence")
    p_demo.add_argument("--delay", type=float, default=0.06, help="Frame delay in seconds")

    # random
    p_rnd = sub.add_parser("random", help="Run a random initial soup")
    p_rnd.add_argument("--density", type=float, default=0.30, help="Starting density 0–1")
    p_rnd.add_argument("--seed",    type=int,   default=None, help="RNG seed for reproducibility")
    p_rnd.add_argument("--gens",    type=int,   default=500,  help="Max generations")
    p_rnd.add_argument("--delay",   type=float, default=0.05, help="Frame delay in seconds")

    # evolve
    p_evo = sub.add_parser("evolve", help="Breed interesting patterns via genetic algorithm")
    p_evo.add_argument("--pop",       type=int,   default=24,   help="Population size")
    p_evo.add_argument("--evo-gens",  type=int,   default=15,   help="Evolutionary generations")
    p_evo.add_argument("--eval-gens", type=int,   default=150,  help="Simulation steps per fitness evaluation")
    p_evo.add_argument("--width",     type=int,   default=DEFAULT_W, help="Board width")
    p_evo.add_argument("--height",    type=int,   default=DEFAULT_H, help="Board height")
    p_evo.add_argument("--replay",    type=int,   default=300,  help="Replay generations for champion")
    p_evo.add_argument("--delay",     type=float, default=0.06, help="Frame delay during replay")

    args = parser.parse_args()

    dispatch = {
        "list":    cmd_list,
        "pattern": cmd_pattern,
        "demo":    cmd_demo,
        "random":  cmd_random,
        "evolve":  cmd_evolve,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
