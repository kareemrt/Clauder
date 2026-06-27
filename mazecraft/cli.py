"""Command-line interface: generate a maze, race pathfinding algorithms on
it, and render the results as images/GIFs in an output directory."""

from __future__ import annotations

import argparse
import json
import os

from mazecraft.algorithms import ALGORITHMS
from mazecraft.maze import generate_maze
from mazecraft.render import draw_static_maze, render_comparison_chart, render_solution_gif


def parse_size(value: str) -> tuple:
    rows, _, cols = value.partition("x")
    if not cols:
        raise argparse.ArgumentTypeError("size must look like ROWSxCOLS, e.g. 25x25")
    return int(rows), int(cols)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mazecraft",
        description="Generate a maze and race pathfinding algorithms against each other.",
    )
    parser.add_argument("--size", type=parse_size, default=(25, 25), help="ROWSxCOLS, default 25x25")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducible mazes")
    parser.add_argument(
        "--algos",
        default="bfs,dfs,dijkstra,astar",
        help="comma-separated subset of: bfs,dfs,dijkstra,astar",
    )
    parser.add_argument("--out", default="assets", help="output directory for rendered assets")
    parser.add_argument("--cell-size", type=int, default=20, help="pixel size of each maze cell")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    rows, cols = args.size
    os.makedirs(args.out, exist_ok=True)

    maze = generate_maze(rows, cols, seed=args.seed)

    maze_path = os.path.join(args.out, "maze.png")
    draw_static_maze(maze, cell_size=args.cell_size).save(maze_path)
    print(f"maze:  {rows}x{cols}  seed={args.seed}  -> {maze_path}")

    names = [a.strip() for a in args.algos.split(",") if a.strip()]
    results = []
    for name in names:
        if name not in ALGORITHMS:
            raise SystemExit(f"unknown algorithm '{name}', choose from {sorted(ALGORITHMS)}")
        result = ALGORITHMS[name](maze)
        results.append(result)
        gif_path = os.path.join(args.out, f"{name}.gif")
        render_solution_gif(maze, result, gif_path, cell_size=args.cell_size)
        print(
            f"{result.name:<10} explored={result.nodes_explored:<6} "
            f"path_length={result.path_length:<6} time={result.elapsed_seconds * 1000:.3f}ms "
            f"-> {gif_path}"
        )

    if len(results) > 1:
        chart_path = os.path.join(args.out, "comparison.png")
        render_comparison_chart(results, chart_path)
        print(f"comparison chart -> {chart_path}")

    summary = {
        "rows": rows,
        "cols": cols,
        "seed": args.seed,
        "results": [
            {
                "name": r.name,
                "nodes_explored": r.nodes_explored,
                "path_length": r.path_length,
                "elapsed_seconds": r.elapsed_seconds,
            }
            for r in results
        ],
    }
    summary_path = os.path.join(args.out, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"summary -> {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
