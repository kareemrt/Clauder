"""Core simulation: Reynolds' boids (separation, alignment, cohesion) plus
an optional predator/prey dynamic, fully vectorized with NumPy.
"""
from __future__ import annotations

import numpy as np


class Flock:
    """A flock of boids and an optional set of predators on a toroidal plane.

    The plane wraps at its edges (a torus) so boids never "hit a wall" and
    the flock reads as a single continuous swarm even near the borders.
    """

    def __init__(
        self,
        n_boids: int,
        width: float,
        height: float,
        *,
        perception: float = 75.0,
        max_speed: float = 3.0,
        max_force: float = 0.06,
        separation_radius: float = 20.0,
        separation_weight: float = 1.4,
        alignment_weight: float = 1.0,
        cohesion_weight: float = 1.0,
        n_predators: int = 0,
        predator_perception: float = 120.0,
        predator_max_speed: float = 3.6,
        predator_avoid_weight: float = 0.9,
        predator_chase_weight: float = 0.3,
        seed: int | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.perception = perception
        self.max_speed = max_speed
        self.max_force = max_force
        self.separation_radius = separation_radius
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        self.n_predators = n_predators
        self.predator_perception = predator_perception
        self.predator_max_speed = predator_max_speed
        self.predator_avoid_weight = predator_avoid_weight
        self.predator_chase_weight = predator_chase_weight

        rng = np.random.default_rng(seed)
        self.positions = rng.random((n_boids, 2)) * [width, height]
        angles = rng.random(n_boids) * 2 * np.pi
        self.velocities = np.column_stack([np.cos(angles), np.sin(angles)]) * max_speed * 0.5

        self.predator_positions = rng.random((n_predators, 2)) * [width, height]
        p_angles = rng.random(n_predators) * 2 * np.pi
        self.predator_velocities = (
            np.column_stack([np.cos(p_angles), np.sin(p_angles)]) * predator_max_speed * 0.5
        )

    @staticmethod
    def _toroidal_delta(from_points: np.ndarray, to_points: np.ndarray, width: float, height: float) -> np.ndarray:
        """Shortest displacement from each ``from_points[i]`` to each ``to_points[j]``,
        taking the torus seams into account.

        Returns an (n_from, n_to, 2) tensor where ``result[i, j]`` is the vector that,
        added to ``from_points[i]``, points at ``to_points[j]``.
        """
        delta = to_points[None, :, :] - from_points[:, None, :]
        delta[..., 0] -= width * np.round(delta[..., 0] / width)
        delta[..., 1] -= height * np.round(delta[..., 1] / height)
        return delta

    def _clamp(self, vectors: np.ndarray, max_magnitude: float) -> np.ndarray:
        magnitudes = np.linalg.norm(vectors, axis=1)
        nonzero = magnitudes > 1e-12
        scales = np.ones_like(magnitudes)
        too_fast = nonzero & (magnitudes > max_magnitude)
        scales[too_fast] = max_magnitude / magnitudes[too_fast]
        return vectors * scales[:, None]

    def _flocking_forces(self) -> np.ndarray:
        pos = self.positions
        # to_neighbor[i, j] is the vector from boid i to boid j.
        to_neighbor = self._toroidal_delta(pos, pos, self.width, self.height)
        dist = np.linalg.norm(to_neighbor, axis=-1)
        np.fill_diagonal(dist, np.inf)

        neighbor_mask = dist < self.perception
        neighbor_counts = np.maximum(neighbor_mask.sum(axis=1), 1)

        # Cohesion: steer toward the average position of neighbors.
        masked_delta = np.where(neighbor_mask[..., None], to_neighbor, 0.0)
        cohesion = masked_delta.sum(axis=1) / neighbor_counts[:, None]

        # Alignment: steer toward the average heading of neighbors.
        masked_vel = np.where(neighbor_mask[..., None], self.velocities[None, :, :], 0.0)
        avg_velocity = masked_vel.sum(axis=1) / neighbor_counts[:, None]
        alignment = avg_velocity - self.velocities

        # Separation: steer away from boids that are too close (away from to_neighbor).
        close_mask = dist < self.separation_radius
        repulsion = np.where(close_mask[..., None], -to_neighbor / (dist[..., None] ** 2 + 1e-6), 0.0)
        separation = repulsion.sum(axis=1)

        force = (
            self.cohesion_weight * cohesion
            + self.alignment_weight * alignment
            + self.separation_weight * separation
        )
        return self._clamp(force, self.max_force)

    def _predator_interaction(self) -> np.ndarray:
        if self.n_predators == 0:
            return np.zeros_like(self.positions)

        # to_predator[b, p] is the vector from boid b to predator p.
        to_predator = self._toroidal_delta(self.positions, self.predator_positions, self.width, self.height)
        dist = np.linalg.norm(to_predator, axis=-1)
        threatened = dist < self.predator_perception

        flee = np.where(threatened[..., None], -to_predator / (dist[..., None] ** 2 + 1e-6), 0.0)
        avoidance = flee.sum(axis=1)
        return self._clamp(avoidance, self.max_force) * self.predator_avoid_weight

    def _step_predators(self, dt: float) -> None:
        if self.n_predators == 0:
            return

        if len(self.positions) == 0:
            chase = np.zeros_like(self.predator_positions)
        else:
            # to_boid[p, b] is the vector from predator p to boid b.
            to_boid = self._toroidal_delta(self.predator_positions, self.positions, self.width, self.height)
            dist = np.linalg.norm(to_boid, axis=-1)
            nearest = np.argmin(dist, axis=1)
            chase_target = to_boid[np.arange(self.n_predators), nearest]
            chase = self._clamp(chase_target, self.max_force) * self.predator_chase_weight

        self.predator_velocities = self._clamp(
            self.predator_velocities + chase, self.predator_max_speed
        )
        self.predator_positions = (self.predator_positions + self.predator_velocities * dt) % [
            self.width,
            self.height,
        ]

    def step(self, dt: float = 1.0) -> None:
        """Advance the simulation by one tick."""
        force = self._flocking_forces() + self._predator_interaction()
        self.velocities = self._clamp(self.velocities + force, self.max_speed)
        self.positions = (self.positions + self.velocities * dt) % [self.width, self.height]
        self._step_predators(dt)
