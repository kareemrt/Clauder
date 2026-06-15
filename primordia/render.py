"""Rendering helpers: static snapshots and animated GIFs."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # safe for headless environments

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from primordia.presets import PALETTE
from primordia.simulation import ParticleLife


def _setup_axes(ax, sim: ParticleLife) -> None:
    ax.set_xlim(0, sim.config.width)
    ax.set_ylim(0, sim.config.height)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("#0b0b16")
    for spine in ax.spines.values():
        spine.set_visible(False)


def save_snapshot(sim: ParticleLife, path: str | Path, dpi: int = 150) -> None:
    """Render the current state of ``sim`` to a static PNG."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _setup_axes(ax, sim)

    colors = [PALETTE[t % len(PALETTE)] for t in sim.types]
    ax.scatter(
        sim.positions[:, 0],
        sim.positions[:, 1],
        c=colors,
        s=8,
        linewidths=0,
    )

    fig.tight_layout(pad=0)
    fig.savefig(path, dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_animation(
    sim: ParticleLife,
    path: str | Path,
    frames: int = 200,
    steps_per_frame: int = 1,
    fps: int = 30,
    dpi: int = 100,
    warmup_steps: int = 0,
) -> None:
    """Run ``sim`` forward and save the result as an animated GIF.

    Parameters
    ----------
    frames:
        Number of frames to capture.
    steps_per_frame:
        Simulation steps advanced between each captured frame.
    warmup_steps:
        Steps to run (and discard) before recording begins, useful for
        letting the system settle into its characteristic pattern.
    """
    for _ in range(warmup_steps):
        sim.step()

    fig, ax = plt.subplots(figsize=(6, 6))
    _setup_axes(ax, sim)

    colors = [PALETTE[t % len(PALETTE)] for t in sim.types]
    scatter = ax.scatter(
        sim.positions[:, 0],
        sim.positions[:, 1],
        c=colors,
        s=8,
        linewidths=0,
    )

    def update(_frame_index: int):
        for _ in range(steps_per_frame):
            sim.step()
        scatter.set_offsets(sim.positions)
        return (scatter,)

    anim = animation.FuncAnimation(fig, update, frames=frames, blit=True)
    anim.save(path, writer=animation.PillowWriter(fps=fps), dpi=dpi)
    plt.close(fig)
