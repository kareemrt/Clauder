#!/usr/bin/env python3
"""
Labyrinthine — A Procedural Maze Universe Explorer

Generate, solve, and explore mazes using multiple algorithms.
"""
import argparse
import sys
import time
import os
from src.maze import Maze, ALGORITHMS
from src.solver import SOLVERS, AStarSolver, BFSSolver, DFSSolver
from src.renderer import render_maze, render_stats, Color, THEMES
from src.export import save_text, save_svg, maze_statistics


BANNER = r"""
  _       _    _                      _   _     _
 | |     | |  | |                    | | | |   (_)
 | |     | |  | |__  _   _ _ __ _   _| |_| |__  _ _ __   ___
 | |     | |  | '_ \| | | | '__| | | | __| '_ \| | '_ \ / _ \
 | |____ | |__| |_) | |_| | |  | |_| | |_| | | | | | | |  __/
 |______||____|_.__/ \__, |_|   \__, |\__|_| |_|_|_| |_|\___|
                      __/ |      __/ |
                     |___/      |___/
"""

def print_colored(text: str, color: str = "", bold: bool = False) -> None:
    prefix = Color.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Color.RESET}")


def animate_generation(maze: Maze, order, theme_name: str, delay: float = 0.002):
    """Animate maze generation step by step."""
    visited = []
    chunk = max(1, len(order) // 200)

    for i, cell in enumerate(order):
        visited.append(cell)
        if i % chunk == 0 or i == len(order) - 1:
            rendered = render_maze(maze, theme_name=theme_name,
                                   visited=visited, color=True)
            lines = rendered.split("\n")
            # Move cursor up to redraw
            if i > 0:
                sys.stdout.write(f"\033[{len(lines)}A")
            print(rendered)
            sys.stdout.flush()
            time.sleep(delay)


def animate_solve(maze: Maze, result, theme_name: str, delay: float = 0.005):
    """Animate solver exploration, then reveal the path."""
    # Show visited cells growing
    chunk = max(1, len(result.visited) // 100)
    for i in range(0, len(result.visited), chunk):
        rendered = render_maze(maze, theme_name=theme_name,
                               visited=result.visited[:i], color=True)
        lines = rendered.split("\n")
        if i > 0:
            sys.stdout.write(f"\033[{len(lines)}A")
        print(rendered)
        sys.stdout.flush()
        time.sleep(delay)

    # Flash the final path
    for _ in range(3):
        rendered = render_maze(maze, theme_name=theme_name,
                               visited=result.visited, path=result.path, color=True)
        lines = rendered.split("\n")
        sys.stdout.write(f"\033[{len(lines)}A")
        print(rendered)
        sys.stdout.flush()
        time.sleep(0.15)
        rendered2 = render_maze(maze, theme_name=theme_name,
                                visited=result.visited, color=True)
        sys.stdout.write(f"\033[{len(lines)}A")
        print(rendered2)
        sys.stdout.flush()
        time.sleep(0.1)

    # Final stable render
    rendered = render_maze(maze, theme_name=theme_name,
                           visited=result.visited, path=result.path, color=True)
    lines = rendered.split("\n")
    sys.stdout.write(f"\033[{len(lines)}A")
    print(rendered)


def cmd_generate(args):
    algo_cls = ALGORITHMS.get(args.algorithm, ALGORITHMS["recursive"])
    maze = Maze(args.rows, args.cols)

    print_colored(BANNER, Color.BRIGHT_CYAN)
    print_colored(f"  Algorithm : {algo_cls.name}", Color.BRIGHT_YELLOW)
    print_colored(f"  Size      : {args.rows} × {args.cols}", Color.BRIGHT_YELLOW)
    print_colored(f"  Theme     : {args.theme}", Color.BRIGHT_YELLOW)
    print_colored(f"  Seed      : {args.seed if args.seed else 'random'}\n", Color.BRIGHT_YELLOW)

    t0 = time.time()
    if args.animate:
        order = algo_cls.generate(maze, seed=args.seed)
        # Print empty maze first
        print(render_maze(maze, theme_name=args.theme, color=True))
    else:
        order = algo_cls.generate(maze, seed=args.seed)

    gen_time = time.time() - t0

    if not args.animate:
        print(render_maze(maze, theme_name=args.theme, color=True))

    print()
    print_colored(f"  Generated in {gen_time*1000:.1f}ms", Color.DIM)

    if args.solve:
        solver_cls = SOLVERS.get(args.solver, SOLVERS["astar"])
        print_colored(f"\n  Solving with {solver_cls.name}...\n", Color.BRIGHT_CYAN)
        t0 = time.time()
        result = solver_cls.solve(maze)
        solve_time = time.time() - t0

        if args.animate:
            animate_solve(maze, result, args.theme)
        else:
            print(render_maze(maze, theme_name=args.theme,
                              visited=result.visited, path=result.path, color=True))

        print()
        print(render_stats(maze, result, theme_name=args.theme, color=True))
        print_colored(f"\n  Solved in {solve_time*1000:.1f}ms", Color.DIM)
    else:
        print(render_stats(maze, theme_name=args.theme, color=True))

    if args.export_txt:
        result_obj = result if args.solve else None
        path_data = result_obj.path if result_obj else None
        save_text(maze, args.export_txt, path=path_data, theme_name=args.theme)
        print_colored(f"\n  Saved to {args.export_txt}", Color.BRIGHT_GREEN)

    if args.export_svg:
        result_obj = result if args.solve else None
        path_data = result_obj.path if result_obj else None
        save_svg(maze, args.export_svg, path=path_data)
        print_colored(f"  Saved SVG to {args.export_svg}", Color.BRIGHT_GREEN)


def cmd_compare(args):
    """Compare all 4 algorithms on the same maze."""
    print_colored(BANNER, Color.BRIGHT_CYAN)
    print_colored("  ALGORITHM COMPARISON\n", Color.BOLD + Color.BRIGHT_YELLOW)

    results_table = []
    for name, algo_cls in ALGORITHMS.items():
        maze = Maze(args.rows, args.cols)
        t0 = time.time()
        algo_cls.generate(maze, seed=args.seed)
        gen_time = time.time() - t0

        solver_cls = SOLVERS.get(args.solver, SOLVERS["astar"])
        t0 = time.time()
        result = solver_cls.solve(maze)
        solve_time = time.time() - t0

        stats = maze_statistics(maze, result)
        results_table.append({
            "name": algo_cls.name,
            "gen_ms": gen_time * 1000,
            "solve_ms": solve_time * 1000,
            **stats,
        })

    # Print table
    header = f"{'Algorithm':<24} {'Dead Ends':>10} {'Junctions':>10} {'Path Len':>10} {'Visited':>10} {'Eff %':>8}"
    print_colored(header, Color.BRIGHT_WHITE + Color.BOLD)
    print_colored("─" * len(header), Color.DIM)
    for row in results_table:
        eff = row.get('efficiency', 0) * 100
        line = (f"{row['name']:<24} {row['dead_ends']:>10} {row['junctions']:>10} "
                f"{row['path_length']:>10} {row['cells_visited']:>10} {eff:>7.1f}%")
        print_colored(line, Color.BRIGHT_CYAN)

    print()
    for row in results_table:
        print_colored(f"  {row['name']}: generated in {row['gen_ms']:.1f}ms, "
                      f"solved in {row['solve_ms']:.1f}ms", Color.DIM)


def cmd_explore(args):
    """Launch interactive exploration mode."""
    try:
        import curses
    except ImportError:
        print_colored("  curses not available on this platform.", Color.RED)
        return

    algo_cls = ALGORITHMS.get(args.algorithm, ALGORITHMS["recursive"])
    maze = Maze(args.rows, args.cols)
    algo_cls.generate(maze, seed=args.seed)

    print_colored(BANNER, Color.BRIGHT_CYAN)
    print_colored("  Launching interactive mode...", Color.BRIGHT_YELLOW)
    print_colored("  Controls: WASD or Arrow Keys to move", Color.DIM)
    print_colored("  H = toggle solution hint  |  Q = quit\n", Color.DIM)
    time.sleep(1)

    from src.interactive import run_interactive
    run_interactive(maze, fog=not args.no_fog, reveal_radius=args.fog_radius)
    print_colored("\n  Thanks for playing Labyrinthine!\n", Color.BRIGHT_CYAN)


def main():
    parser = argparse.ArgumentParser(
        description="Labyrinthine — Procedural Maze Universe Explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py generate -r 20 -c 40 --solve --animate
  python main.py generate -r 30 -c 60 -a wilsons --theme neon --export-svg maze.svg
  python main.py compare -r 25 -c 25
  python main.py explore -r 20 -c 40 --algorithm recursive
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # ── generate ──
    gen = subparsers.add_parser("generate", help="Generate and optionally solve a maze")
    gen.add_argument("-r", "--rows",      type=int, default=15)
    gen.add_argument("-c", "--cols",      type=int, default=30)
    gen.add_argument("-a", "--algorithm", choices=list(ALGORITHMS.keys()), default="recursive")
    gen.add_argument("-s", "--seed",      type=int, default=None)
    gen.add_argument("--solve",           action="store_true")
    gen.add_argument("--solver",          choices=list(SOLVERS.keys()), default="astar")
    gen.add_argument("--theme",           choices=list(THEMES.keys()), default="neon")
    gen.add_argument("--animate",         action="store_true")
    gen.add_argument("--export-txt",      metavar="FILE", default=None)
    gen.add_argument("--export-svg",      metavar="FILE", default=None)

    # ── compare ──
    cmp = subparsers.add_parser("compare", help="Compare all generation algorithms side-by-side")
    cmp.add_argument("-r", "--rows",   type=int, default=20)
    cmp.add_argument("-c", "--cols",   type=int, default=20)
    cmp.add_argument("-s", "--seed",   type=int, default=42)
    cmp.add_argument("--solver",       choices=list(SOLVERS.keys()), default="astar")

    # ── explore ──
    exp = subparsers.add_parser("explore", help="Explore a maze interactively")
    exp.add_argument("-r", "--rows",       type=int, default=20)
    exp.add_argument("-c", "--cols",       type=int, default=40)
    exp.add_argument("-a", "--algorithm",  choices=list(ALGORITHMS.keys()), default="recursive")
    exp.add_argument("-s", "--seed",       type=int, default=None)
    exp.add_argument("--no-fog",           action="store_true")
    exp.add_argument("--fog-radius",       type=int, default=4)

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "explore":
        cmd_explore(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
