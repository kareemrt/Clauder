"""Export mazes to various formats."""
from typing import Optional, List, Tuple
from .maze import Maze, Wall
from .renderer import render_maze


def to_text(maze: Maze,
            path: Optional[List[Tuple[int, int]]] = None,
            theme_name: str = "classic") -> str:
    """Export maze as plain text (no ANSI codes)."""
    return render_maze(maze, theme_name=theme_name, path=path, color=False)


def to_svg(maze: Maze,
           path: Optional[List[Tuple[int, int]]] = None,
           cell_size: int = 20,
           wall_width: int = 2) -> str:
    """Export maze as an SVG file."""
    W = cell_size
    svg_w = maze.cols * W + wall_width
    svg_h = maze.rows * W + wall_width

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}">',
        f'  <rect width="{svg_w}" height="{svg_h}" fill="#1a1a2e"/>',
    ]

    # Draw walls
    stroke = f'stroke="#00ff96" stroke-width="{wall_width}" stroke-linecap="round"'

    for r in range(maze.rows):
        for c in range(maze.cols):
            x = c * W + wall_width // 2
            y = r * W + wall_width // 2

            if r == 0 or maze.has_wall(r, c, Wall.NORTH):
                lines.append(f'  <line x1="{x}" y1="{y}" x2="{x+W}" y2="{y}" {stroke}/>')
            if c == 0 or maze.has_wall(r, c, Wall.WEST):
                lines.append(f'  <line x1="{x}" y1="{y}" x2="{x}" y2="{y+W}" {stroke}/>')

    # Close right and bottom borders
    for r in range(maze.rows):
        x = maze.cols * W + wall_width // 2
        y = r * W + wall_width // 2
        if maze.has_wall(r, maze.cols - 1, Wall.EAST):
            lines.append(f'  <line x1="{x}" y1="{y}" x2="{x}" y2="{y+W}" {stroke}/>')
    for c in range(maze.cols):
        x = c * W + wall_width // 2
        y = maze.rows * W + wall_width // 2
        if maze.has_wall(maze.rows - 1, c, Wall.SOUTH):
            lines.append(f'  <line x1="{x}" y1="{y}" x2="{x+W}" y2="{y}" {stroke}/>')

    # Draw path
    if path:
        path_coords = " ".join(
            f"{c * W + W // 2 + wall_width // 2},{r * W + W // 2 + wall_width // 2}"
            for r, c in path
        )
        lines.append(
            f'  <polyline points="{path_coords}" fill="none" '
            f'stroke="#ffdd00" stroke-width="{wall_width + 1}" '
            f'stroke-linejoin="round" stroke-linecap="round" opacity="0.8"/>'
        )

    # Mark start and end
    sr, sc = maze.start
    er, ec = maze.end
    sx = sc * W + W // 2 + wall_width // 2
    sy = sr * W + W // 2 + wall_width // 2
    ex = ec * W + W // 2 + wall_width // 2
    ey = er * W + W // 2 + wall_width // 2
    r = W // 2 - 2
    lines.append(f'  <circle cx="{sx}" cy="{sy}" r="{r}" fill="#00ff60" opacity="0.9"/>')
    lines.append(f'  <circle cx="{ex}" cy="{ey}" r="{r}" fill="#ff4060" opacity="0.9"/>')

    lines.append('</svg>')
    return "\n".join(lines)


def save_text(maze: Maze, filepath: str, path=None, theme_name: str = "classic") -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(to_text(maze, path=path, theme_name=theme_name))


def save_svg(maze: Maze, filepath: str, path=None, cell_size: int = 20) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(to_svg(maze, path=path, cell_size=cell_size))


def maze_statistics(maze: Maze, result=None) -> dict:
    """Compute statistics about the maze structure."""
    dead_ends = 0
    junctions = 0
    total_passages = 0

    for r in range(maze.rows):
        for c in range(maze.cols):
            passage_count = sum(
                1 for d in (Wall.NORTH, Wall.SOUTH, Wall.EAST, Wall.WEST)
                if not maze.has_wall(r, c, d)
            )
            total_passages += passage_count
            if passage_count == 1:
                dead_ends += 1
            elif passage_count >= 3:
                junctions += 1

    stats = {
        "rows": maze.rows,
        "cols": maze.cols,
        "cells": maze.rows * maze.cols,
        "dead_ends": dead_ends,
        "junctions": junctions,
        "total_passages": total_passages // 2,
        "dead_end_ratio": dead_ends / (maze.rows * maze.cols),
    }

    if result:
        stats.update({
            "solver": result.algorithm,
            "path_length": result.path_length,
            "cells_visited": result.steps,
            "efficiency": result.path_length / max(result.steps, 1),
        })

    return stats
