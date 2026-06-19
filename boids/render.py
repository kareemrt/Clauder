"""Matplotlib rendering: boids drawn as arrows pointing along their heading,
exported as an animated GIF or a single PNG snapshot.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from boids.flock import Flock

BOID_COLOR = "#3FB8AF"
PREDATOR_COLOR = "#E84855"
BACKGROUND = "#0B132B"


def _make_figure(flock: Flock):
    fig, ax = plt.subplots(figsize=(6, 6), facecolor=BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.set_xlim(0, flock.width)
    ax.set_ylim(0, flock.height)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    boid_quiver = ax.quiver(
        flock.positions[:, 0],
        flock.positions[:, 1],
        flock.velocities[:, 0],
        flock.velocities[:, 1],
        color=BOID_COLOR,
        pivot="middle",
        scale=60,
        width=0.004,
        headwidth=4,
        headlength=5,
    )
    predator_quiver = ax.quiver(
        flock.predator_positions[:, 0],
        flock.predator_positions[:, 1],
        flock.predator_velocities[:, 0],
        flock.predator_velocities[:, 1],
        color=PREDATOR_COLOR,
        pivot="middle",
        scale=40,
        width=0.007,
        headwidth=4,
        headlength=5,
    )
    return fig, ax, boid_quiver, predator_quiver


def _sync_quivers(flock: Flock, boid_quiver, predator_quiver) -> None:
    boid_quiver.set_offsets(flock.positions)
    boid_quiver.set_UVC(flock.velocities[:, 0], flock.velocities[:, 1])
    if flock.n_predators:
        predator_quiver.set_offsets(flock.predator_positions)
        predator_quiver.set_UVC(flock.predator_velocities[:, 0], flock.predator_velocities[:, 1])


def render_gif(flock: Flock, path: str, *, frames: int = 200, dt: float = 1.0, fps: int = 30) -> None:
    """Run the simulation forward, saving every frame into an animated GIF."""
    fig, ax, boid_quiver, predator_quiver = _make_figure(flock)

    def update(_frame_index: int):
        flock.step(dt)
        _sync_quivers(flock, boid_quiver, predator_quiver)
        return boid_quiver, predator_quiver

    anim = FuncAnimation(fig, update, frames=frames, blit=False)
    anim.save(path, writer=PillowWriter(fps=fps))
    plt.close(fig)


def render_snapshot(flock: Flock, path: str, *, warmup_steps: int = 0, dt: float = 1.0) -> None:
    """Advance the simulation a number of steps, then save a single PNG frame."""
    for _ in range(warmup_steps):
        flock.step(dt)

    fig, ax, boid_quiver, predator_quiver = _make_figure(flock)
    _sync_quivers(flock, boid_quiver, predator_quiver)
    fig.savefig(path, dpi=150, facecolor=BACKGROUND)
    plt.close(fig)
