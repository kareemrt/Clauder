"""Rendering utilities: turn a FlockSimulation run into a GIF or a static plot."""

from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from murmuration.simulation import FlockSimulation

BACKGROUND = "#0b0f1a"
BOID_COLOR = "#7fdbff"
PREDATOR_COLOR = "#ff4d6d"


def _bare_axes(ax) -> None:
    ax.set_facecolor(BACKGROUND)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def render_gif(sim: FlockSimulation, num_steps: int, output_path: str, dt: float = 1.0, fps: int = 24) -> None:
    """Step `sim` forward `num_steps` times, saving each frame into an animated GIF."""
    c = sim.config
    fig, ax = plt.subplots(figsize=(7, 7), facecolor=BACKGROUND)
    _bare_axes(ax)
    ax.set_xlim(0, c.width)
    ax.set_ylim(0, c.height)

    boid_quiver = ax.quiver(
        sim.positions[:, 0],
        sim.positions[:, 1],
        sim.velocities[:, 0],
        sim.velocities[:, 1],
        color=BOID_COLOR,
        scale=22,
        width=0.004,
        pivot="mid",
    )
    predator_scatter = ax.scatter(
        sim.predator_positions[:, 0],
        sim.predator_positions[:, 1],
        c=PREDATOR_COLOR,
        s=140,
        marker="^",
        edgecolors="white",
        linewidths=0.6,
        zorder=5,
    )
    title = ax.set_title("", color="white", fontsize=11, family="monospace")

    def update(_frame_idx):
        sim.step(dt)
        boid_quiver.set_offsets(sim.positions)
        boid_quiver.set_UVC(sim.velocities[:, 0], sim.velocities[:, 1])
        if c.num_predators:
            predator_scatter.set_offsets(sim.predator_positions)
        title.set_text(f"step {sim.step_count:04d}")
        return boid_quiver, predator_scatter, title

    anim = FuncAnimation(fig, update, frames=num_steps, blit=False, interval=1000 / fps)
    anim.save(output_path, writer=PillowWriter(fps=fps))
    plt.close(fig)


def render_trajectories(
    sim: FlockSimulation,
    num_steps: int,
    output_path: str,
    dt: float = 1.0,
    trail_every: int = 1,
) -> None:
    """Run `sim` for `num_steps` and save a static plot of every agent's path."""
    history = sim.run(num_steps, dt)
    boid_traj = np.stack([frame[0] for frame in history])  # (steps, n_boids, 2)
    predator_traj = np.stack([frame[2] for frame in history]) if sim.config.num_predators else None

    fig, ax = plt.subplots(figsize=(8, 8), facecolor=BACKGROUND)
    _bare_axes(ax)
    ax.set_xlim(0, sim.config.width)
    ax.set_ylim(0, sim.config.height)

    for i in range(boid_traj.shape[1]):
        ax.plot(
            boid_traj[::trail_every, i, 0],
            boid_traj[::trail_every, i, 1],
            color=BOID_COLOR,
            alpha=0.25,
            linewidth=0.6,
        )
    ax.scatter(boid_traj[-1, :, 0], boid_traj[-1, :, 1], color=BOID_COLOR, s=10, zorder=4)

    if predator_traj is not None:
        for j in range(predator_traj.shape[1]):
            ax.plot(
                predator_traj[::trail_every, j, 0],
                predator_traj[::trail_every, j, 1],
                color=PREDATOR_COLOR,
                alpha=0.8,
                linewidth=1.4,
            )
        ax.scatter(
            predator_traj[-1, :, 0],
            predator_traj[-1, :, 1],
            color=PREDATOR_COLOR,
            s=80,
            marker="^",
            zorder=5,
            edgecolors="white",
            linewidths=0.6,
        )

    ax.set_title(
        f"{boid_traj.shape[1]} boids × {num_steps} steps",
        color="white",
        fontsize=11,
        family="monospace",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
