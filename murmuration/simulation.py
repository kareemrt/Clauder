"""Vectorized boids flocking simulation with optional predator-prey dynamics.

Implements Craig Reynolds' three classic steering rules (separation,
alignment, cohesion) plus predator avoidance and soft boundary steering,
all computed with numpy broadcasting so the whole flock updates in a
handful of array operations per step.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimulationConfig:
    width: float = 100.0
    height: float = 100.0

    num_boids: int = 120
    num_predators: int = 2

    perception_radius: float = 9.0
    separation_radius: float = 3.0
    separation_weight: float = 1.6
    alignment_weight: float = 1.0
    cohesion_weight: float = 1.0

    max_speed: float = 1.6
    min_speed: float = 0.6
    max_force: float = 0.12

    predator_avoid_radius: float = 12.0
    predator_avoid_weight: float = 3.0

    predator_chase_radius: float = 30.0
    predator_chase_weight: float = 1.0
    predator_separation_radius: float = 8.0
    predator_separation_weight: float = 1.2
    predator_max_speed: float = 1.9
    predator_max_force: float = 0.1

    boundary_margin: float = 8.0
    boundary_weight: float = 2.5

    seed: int | None = None


def _clamp_magnitude(vectors: np.ndarray, max_value: float) -> np.ndarray:
    """Scale rows of `vectors` so no row exceeds `max_value` in magnitude."""
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        scale = np.minimum(1.0, max_value / norms)
    scale = np.where(norms > 1e-9, scale, 1.0)
    return vectors * scale


def _boundary_force(positions: np.ndarray, width: float, height: float, margin: float) -> np.ndarray:
    """Steer agents away from world edges before they reach them."""
    force = np.zeros_like(positions)
    x, y = positions[:, 0], positions[:, 1]

    force[:, 0] += np.clip((margin - x) / margin, 0, None)
    force[:, 0] -= np.clip((margin - (width - x)) / margin, 0, None)
    force[:, 1] += np.clip((margin - y) / margin, 0, None)
    force[:, 1] -= np.clip((margin - (height - y)) / margin, 0, None)
    return force


class FlockSimulation:
    """A self-contained, steppable boids + predator-prey world."""

    def __init__(self, config: SimulationConfig | None = None):
        self.config = config or SimulationConfig()
        self.rng = np.random.default_rng(self.config.seed)
        self.step_count = 0

        c = self.config
        self.positions = self.rng.uniform([0, 0], [c.width, c.height], size=(c.num_boids, 2))
        angles = self.rng.uniform(0, 2 * np.pi, size=c.num_boids)
        speeds = self.rng.uniform(c.min_speed, c.max_speed, size=c.num_boids)
        self.velocities = np.stack([np.cos(angles), np.sin(angles)], axis=1) * speeds[:, None]

        self.predator_positions = self.rng.uniform([0, 0], [c.width, c.height], size=(c.num_predators, 2))
        p_angles = self.rng.uniform(0, 2 * np.pi, size=c.num_predators)
        self.predator_velocities = np.stack([np.cos(p_angles), np.sin(p_angles)], axis=1) * c.predator_max_speed

    def _flock_acceleration(self) -> np.ndarray:
        c = self.config
        pos, vel = self.positions, self.velocities
        n = pos.shape[0]

        delta = pos[None, :, :] - pos[:, None, :]  # delta[i, j] = pos[j] - pos[i]
        dist = np.linalg.norm(delta, axis=-1)
        np.fill_diagonal(dist, np.inf)

        neighbor_mask = dist < c.perception_radius
        neighbor_counts = neighbor_mask.sum(axis=1)
        has_neighbors = neighbor_counts > 0

        # Alignment: steer toward the average heading of nearby flockmates.
        avg_vel = (neighbor_mask[:, :, None] * vel[None, :, :]).sum(axis=1)
        alignment = np.zeros((n, 2))
        alignment[has_neighbors] = (
            avg_vel[has_neighbors] / neighbor_counts[has_neighbors, None] - vel[has_neighbors]
        )

        # Cohesion: steer toward the centroid of nearby flockmates.
        avg_pos = (neighbor_mask[:, :, None] * pos[None, :, :]).sum(axis=1)
        cohesion = np.zeros((n, 2))
        cohesion[has_neighbors] = (
            avg_pos[has_neighbors] / neighbor_counts[has_neighbors, None] - pos[has_neighbors]
        )

        # Separation: steer away from flockmates that are too close, weighted by closeness.
        close_mask = (dist < c.separation_radius) & np.isfinite(dist)
        push = np.divide(-delta, (dist**2)[..., None], out=np.zeros_like(delta), where=dist[..., None] > 1e-9)
        separation = (close_mask[..., None] * push).sum(axis=1)

        acc = (
            c.alignment_weight * alignment
            + c.cohesion_weight * cohesion
            + c.separation_weight * separation
        )

        if c.num_predators:
            to_predator = pos[:, None, :] - self.predator_positions[None, :, :]
            p_dist = np.linalg.norm(to_predator, axis=-1)
            danger_mask = p_dist < c.predator_avoid_radius
            flee = np.divide(
                to_predator,
                (p_dist**2)[..., None],
                out=np.zeros_like(to_predator),
                where=p_dist[..., None] > 1e-9,
            )
            acc += c.predator_avoid_weight * (danger_mask[..., None] * flee).sum(axis=1)

        acc += c.boundary_weight * _boundary_force(pos, c.width, c.height, c.boundary_margin)
        return _clamp_magnitude(acc, c.max_force)

    def _predator_acceleration(self) -> np.ndarray:
        c = self.config
        ppos, pvel = self.predator_positions, self.predator_velocities
        m = ppos.shape[0]
        acc = np.zeros((m, 2))

        to_prey = self.positions[None, :, :] - ppos[:, None, :]
        prey_dist = np.linalg.norm(to_prey, axis=-1)
        chase_mask = prey_dist < c.predator_chase_radius
        chase_counts = chase_mask.sum(axis=1)
        hunting = chase_counts > 0
        if hunting.any():
            target = np.zeros((m, 2))
            target[hunting] = (chase_mask[hunting, :, None] * to_prey[hunting]).sum(axis=1) / chase_counts[
                hunting, None
            ]
            acc[hunting] += c.predator_chase_weight * target[hunting]

        if m > 1:
            delta = ppos[None, :, :] - ppos[:, None, :]
            dist = np.linalg.norm(delta, axis=-1)
            np.fill_diagonal(dist, np.inf)
            close_mask = dist < c.predator_separation_radius
            push = np.divide(-delta, (dist**2)[..., None], out=np.zeros_like(delta), where=dist[..., None] > 1e-9)
            acc += c.predator_separation_weight * (close_mask[..., None] * push).sum(axis=1)

        acc += c.boundary_weight * _boundary_force(ppos, c.width, c.height, c.boundary_margin)
        return _clamp_magnitude(acc, c.predator_max_force)

    def step(self, dt: float = 1.0) -> None:
        c = self.config

        boid_acc = self._flock_acceleration()
        self.velocities = _clamp_magnitude(self.velocities + boid_acc * dt, c.max_speed)
        speeds = np.linalg.norm(self.velocities, axis=-1)
        too_slow = speeds < c.min_speed
        if too_slow.any():
            directions = np.divide(
                self.velocities[too_slow],
                speeds[too_slow, None],
                out=np.zeros_like(self.velocities[too_slow]),
                where=speeds[too_slow, None] > 1e-9,
            )
            self.velocities[too_slow] = directions * c.min_speed
        self.positions = np.clip(self.positions + self.velocities * dt, [0, 0], [c.width, c.height])

        if c.num_predators:
            predator_acc = self._predator_acceleration()
            self.predator_velocities = _clamp_magnitude(
                self.predator_velocities + predator_acc * dt, c.predator_max_speed
            )
            self.predator_positions = np.clip(
                self.predator_positions + self.predator_velocities * dt, [0, 0], [c.width, c.height]
            )

        self.step_count += 1

    def run(self, num_steps: int, dt: float = 1.0) -> list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
        """Advance the simulation and return a per-frame history for rendering."""
        frames = []
        for _ in range(num_steps):
            self.step(dt)
            frames.append(
                (
                    self.positions.copy(),
                    self.velocities.copy(),
                    self.predator_positions.copy(),
                    self.predator_velocities.copy(),
                )
            )
        return frames
