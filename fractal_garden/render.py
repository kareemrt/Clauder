"""Turn L-system segments into static images and growth animations."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import LineCollection  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from .lsystem import LSystem, Segment, bounding_box, interpret  # noqa: E402

BACKGROUND = "#0b0c10"
CMAP = "spring"


def _segments_to_lines(segments: list[Segment]) -> list:
    return [((s.x1, s.y1), (s.x2, s.y2)) for s in segments]


def _color_values(segments: list[Segment]) -> list[float]:
    """Pick a value in [0, 1] per segment to drive the colormap.

    Branching fractals (trees, plants) are colored by branch depth so that
    trunks and twigs stand apart. Non-branching curves (snowflakes, dragon
    curves, space-filling curves) have a constant depth of 0, so instead we
    color them by position along the path to produce a smooth gradient.
    """
    depths = [s.depth for s in segments]
    max_depth = max(depths) if depths else 0
    if max_depth > 0:
        return [d / max_depth for d in depths]
    n = len(segments)
    return [i / max(n - 1, 1) for i in range(n)]


def _style_axes(ax, facecolor: str = BACKGROUND) -> None:
    ax.set_facecolor(facecolor)
    ax.set_aspect("equal")
    ax.axis("off")


def render_image(
    lsystem: LSystem,
    iterations: int,
    output_path: str,
    *,
    cmap: str = CMAP,
    linewidth: float = 0.8,
    figsize: tuple[float, float] = (8, 8),
    dpi: int = 150,
    facecolor: str = BACKGROUND,
    title: bool = True,
) -> list[Segment]:
    """Render a single L-system iteration to an image file."""
    instructions = lsystem.expand(iterations)
    segments = interpret(instructions, lsystem)

    fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)
    _style_axes(ax, facecolor)

    if segments:
        lines = _segments_to_lines(segments)
        collection = LineCollection(lines, cmap=cmap, linewidths=linewidth)
        collection.set_array(_color_values(segments))
        ax.add_collection(collection)

        min_x, min_y, max_x, max_y = bounding_box(segments)
        pad_x = max((max_x - min_x) * 0.05, 0.5)
        pad_y = max((max_y - min_y) * 0.05, 0.5)
        ax.set_xlim(min_x - pad_x, max_x + pad_x)
        ax.set_ylim(min_y - pad_y, max_y + pad_y)

    if title:
        ax.set_title(
            f"{lsystem.name} (iteration {iterations})",
            color="white",
            fontsize=10,
            pad=10,
        )

    fig.tight_layout()
    fig.savefig(output_path, facecolor=facecolor, bbox_inches="tight")
    plt.close(fig)
    return segments


def render_animation(
    lsystem: LSystem,
    max_iterations: int,
    output_path: str,
    *,
    cmap: str = CMAP,
    linewidth: float = 0.8,
    figsize: tuple[float, float] = (6, 6),
    dpi: int = 100,
    facecolor: str = BACKGROUND,
    fps: int = 1,
    hold_last_frames: int = 2,
) -> None:
    """Render an animated GIF showing the fractal growing iteration by iteration."""
    final_instructions = lsystem.expand(max_iterations)
    final_segments = interpret(final_instructions, lsystem)
    min_x, min_y, max_x, max_y = bounding_box(final_segments)
    pad_x = max((max_x - min_x) * 0.05, 0.5)
    pad_y = max((max_y - min_y) * 0.05, 0.5)

    fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    frame_iterations = list(range(0, max_iterations + 1)) + [max_iterations] * hold_last_frames

    def draw_frame(iteration: int):
        ax.clear()
        _style_axes(ax, facecolor)
        ax.set_xlim(min_x - pad_x, max_x + pad_x)
        ax.set_ylim(min_y - pad_y, max_y + pad_y)
        ax.set_title(
            f"{lsystem.name} (iteration {iteration})",
            color="white",
            fontsize=10,
            pad=10,
        )

        instructions = lsystem.expand(iteration)
        segments = interpret(instructions, lsystem)
        if segments:
            lines = _segments_to_lines(segments)
            collection = LineCollection(lines, cmap=cmap, linewidths=linewidth)
            collection.set_array(_color_values(segments))
            ax.add_collection(collection)
        return ax.collections

    anim = FuncAnimation(fig, draw_frame, frames=frame_iterations, blit=False)
    anim.save(output_path, writer=PillowWriter(fps=fps), dpi=dpi)
    plt.close(fig)
