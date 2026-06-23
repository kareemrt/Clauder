"""Render strange-attractor trajectories as glowing line-art on a dark canvas."""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from .systems import AttractorSystem

AXES = {"x": 0, "y": 1, "z": 2}


def _segments_2d(traj: np.ndarray, projection: tuple[str, str]) -> np.ndarray:
    i, j = AXES[projection[0]], AXES[projection[1]]
    points = traj[:, [i, j]]
    return np.concatenate([points[:-1, None, :], points[1:, None, :]], axis=1)


def _add_glow(ax, segments, cmap, lw_core=1.0, layers=4, base_alpha=0.10, **kw):
    n = len(segments)
    colors = plt.get_cmap(cmap)(np.linspace(0, 1, n))
    for layer in range(layers, 0, -1):
        lc = LineCollection(
            segments,
            colors=colors,
            linewidths=lw_core * layer * 1.8,
            alpha=base_alpha,
            **kw,
        )
        ax.add_collection(lc)
    lc = LineCollection(segments, colors=colors, linewidths=lw_core, alpha=0.95, **kw)
    ax.add_collection(lc)


def render_attractor(
    trajectory: np.ndarray,
    system: AttractorSystem,
    projection: tuple[str, str] | None = None,
    cmap: str = "plasma",
    figsize: tuple[float, float] = (8, 8),
    dpi: int = 160,
    title: bool = True,
):
    """Render a 2D projection of a trajectory with a neon glow effect."""
    projection = projection or system.projection
    segments = _segments_2d(trajectory, projection)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor="black")
    ax.set_facecolor("black")
    _add_glow(ax, segments, cmap)

    i, j = AXES[projection[0]], AXES[projection[1]]
    pad_x = 0.04 * (trajectory[:, i].max() - trajectory[:, i].min() or 1)
    pad_y = 0.04 * (trajectory[:, j].max() - trajectory[:, j].min() or 1)
    ax.set_xlim(trajectory[:, i].min() - pad_x, trajectory[:, i].max() + pad_x)
    ax.set_ylim(trajectory[:, j].min() - pad_y, trajectory[:, j].max() + pad_y)
    ax.set_aspect("equal")
    ax.axis("off")

    if title:
        ax.set_title(
            f"{system.name} Attractor",
            color="white",
            fontsize=14,
            fontfamily="monospace",
            pad=10,
        )
    fig.tight_layout()
    return fig, ax


def render_attractor_3d(
    trajectory: np.ndarray,
    system: AttractorSystem,
    elev: float = 25,
    azim: float = 45,
    cmap: str = "plasma",
    figsize: tuple[float, float] = (8, 8),
    dpi: int = 130,
):
    """Render a full 3D view of a trajectory, used for the rotation animation."""
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="black")
    ax = fig.add_subplot(111, projection="3d")
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    points = trajectory[:, None, :]
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    colors = plt.get_cmap(cmap)(np.linspace(0, 1, len(segments)))
    lc = Line3DCollection(segments, colors=colors, linewidths=0.8, alpha=0.9)
    ax.add_collection3d(lc)

    ax.set_xlim(trajectory[:, 0].min(), trajectory[:, 0].max())
    ax.set_ylim(trajectory[:, 1].min(), trajectory[:, 1].max())
    ax.set_zlim(trajectory[:, 2].min(), trajectory[:, 2].max())
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.tight_layout(pad=0)
    return fig, ax


def save_fig(fig, path: str, dpi: int | None = None):
    fig.savefig(path, facecolor="black", dpi=dpi, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
