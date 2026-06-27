"""Rendering: static maze images, animated GIFs of a search in progress, and a
bar chart comparing algorithms — all drawn with Pillow, no plotting library."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from mazecraft.maze import DELTA, EAST, Maze, NORTH, SOUTH, WEST

BG = (255, 255, 255)
WALL = (30, 30, 36)
UNVISITED = (255, 255, 255)
VISITED = (173, 216, 230)
FRONTIER = (255, 206, 84)
PATH = (231, 76, 60)
START = (46, 204, 113)
END = (155, 89, 182)

ALGO_COLORS = {
    "BFS": (52, 152, 219),
    "DFS": (230, 126, 34),
    "Dijkstra": (155, 89, 182),
    "A*": (231, 76, 60),
}


def _font(size: int):
    try:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size
        )
    except OSError:
        return ImageFont.load_default()


def _cell_box(cell: tuple, cell_size: int, margin: int) -> tuple:
    r, c = cell
    x0 = margin + c * cell_size
    y0 = margin + r * cell_size
    return x0, y0, x0 + cell_size, y0 + cell_size


def _draw_walls(draw: ImageDraw.ImageDraw, maze: Maze, cell_size: int, margin: int, wall_width: int) -> None:
    for cell in maze.passages:
        x0, y0, x1, y1 = _cell_box(cell, cell_size, margin)
        open_dirs = maze.passages[cell]
        if NORTH not in open_dirs:
            draw.line([(x0, y0), (x1, y0)], fill=WALL, width=wall_width)
        if WEST not in open_dirs:
            draw.line([(x0, y0), (x0, y1)], fill=WALL, width=wall_width)
        if cell[0] == maze.rows - 1 and SOUTH not in open_dirs:
            draw.line([(x0, y1), (x1, y1)], fill=WALL, width=wall_width)
        if cell[1] == maze.cols - 1 and EAST not in open_dirs:
            draw.line([(x1, y0), (x1, y1)], fill=WALL, width=wall_width)


def _base_image(maze: Maze, cell_size: int, margin: int):
    width = maze.cols * cell_size + 2 * margin
    height = maze.rows * cell_size + 2 * margin
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    for cell in maze.passages:
        draw.rectangle(_cell_box(cell, cell_size, margin), fill=UNVISITED)
    _draw_walls(draw, maze, cell_size, margin, wall_width=max(2, cell_size // 8))
    return img, draw


def draw_static_maze(maze: Maze, cell_size: int = 20, margin: int = 10) -> Image.Image:
    """Render the bare maze with start/end markers, no search overlay."""
    img, draw = _base_image(maze, cell_size, margin)
    draw.rectangle(_cell_box(maze.start, cell_size, margin), fill=START)
    draw.rectangle(_cell_box(maze.end, cell_size, margin), fill=END)
    return img


def render_solution_gif(
    maze: Maze,
    result,
    out_path: str,
    cell_size: int = 20,
    margin: int = 10,
    target_frames: int = 70,
    hold_ms: int = 1400,
    frame_ms: int = 40,
) -> None:
    """Animate the order in which `result.visited_order` explored the maze,
    then reveal the final shortest path found, and hold on the last frame."""
    base, _ = _base_image(maze, cell_size, margin)
    frames = []

    batch = max(1, len(result.visited_order) // target_frames)
    visited_so_far = []
    for i, cell in enumerate(result.visited_order):
        visited_so_far.append(cell)
        if i % batch == 0 or i == len(result.visited_order) - 1:
            frame = base.copy()
            draw = ImageDraw.Draw(frame)
            for vc in visited_so_far:
                draw.rectangle(_cell_box(vc, cell_size, margin), fill=VISITED)
            draw.rectangle(_cell_box(visited_so_far[-1], cell_size, margin), fill=FRONTIER)
            draw.rectangle(_cell_box(maze.start, cell_size, margin), fill=START)
            draw.rectangle(_cell_box(maze.end, cell_size, margin), fill=END)
            frames.append(frame)

    # Final frames: full exploration shown, then the path drawn on top.
    final = base.copy()
    draw = ImageDraw.Draw(final)
    for vc in result.visited_order:
        draw.rectangle(_cell_box(vc, cell_size, margin), fill=VISITED)
    for pc in result.path:
        draw.rectangle(_cell_box(pc, cell_size, margin), fill=PATH)
    draw.rectangle(_cell_box(maze.start, cell_size, margin), fill=START)
    draw.rectangle(_cell_box(maze.end, cell_size, margin), fill=END)
    frames.append(final)

    durations = [frame_ms] * (len(frames) - 1) + [hold_ms]
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )


def render_comparison_chart(results: list, out_path: str, width: int = 760, height: int = 460) -> None:
    """Bar chart of cells explored per algorithm, annotated with path length
    and elapsed time so the trade-offs between algorithms are visible at a glance."""
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    title_font = _font(20)
    label_font = _font(14)
    small_font = _font(12)

    draw.text((20, 16), "Cells Explored by Algorithm", fill=(20, 20, 20), font=title_font)

    chart_top, chart_bottom = 70, height - 90
    chart_left, chart_right = 60, width - 40
    draw.line([(chart_left, chart_bottom), (chart_right, chart_bottom)], fill=(120, 120, 120), width=2)

    max_explored = max(r.nodes_explored for r in results) or 1
    n = len(results)
    gap = 30
    bar_width = (chart_right - chart_left - gap * (n + 1)) // n

    for i, r in enumerate(results):
        bar_h = int((chart_bottom - chart_top) * (r.nodes_explored / max_explored))
        x0 = chart_left + gap + i * (bar_width + gap)
        y0 = chart_bottom - bar_h
        x1 = x0 + bar_width
        color = ALGO_COLORS.get(r.name, (100, 100, 100))
        draw.rectangle([x0, y0, x1, chart_bottom], fill=color)
        draw.text((x0, y0 - 20), str(r.nodes_explored), fill=(20, 20, 20), font=label_font)
        draw.text((x0, chart_bottom + 10), r.name, fill=(20, 20, 20), font=title_font)
        draw.text(
            (x0, chart_bottom + 36),
            f"path: {r.path_length}",
            fill=(70, 70, 70),
            font=small_font,
        )
        draw.text(
            (x0, chart_bottom + 54),
            f"{r.elapsed_seconds * 1000:.2f} ms",
            fill=(70, 70, 70),
            font=small_font,
        )

    img.save(out_path)
