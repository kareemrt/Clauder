"""Core simulation engine for Particle Life.

Particles live on a unit torus (positions wrap around in [0, 1)).  Each particle
belongs to a "species" (an integer type). The force that one particle exerts on
another depends only on their two species and the distance between them, via an
attraction matrix. The resulting pairwise rule is enough to produce cells,
swarms, chases, and chains -- complex emergent structure from one simple law.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimulationConfig:
    """Tunable parameters of a Particle Life simulation."""

    num_particles: int
    attraction_matrix: np.ndarray
    r_max: float = 0.10
    beta: float = 0.3
    friction: float = 0.85
    force_factor: float = 8.0
    dt: float = 0.02

    @property
    def num_types(self) -> int:
        return self.attraction_matrix.shape[0]


def _pairwise_force(r_norm: np.ndarray, attraction: np.ndarray, beta: float) -> np.ndarray:
    """Force magnitude for normalized distances ``r_norm`` (distance / r_max).

    - Inside the repulsion core (``r_norm < beta``) every pair repels, regardless
      of species, to keep particles from collapsing onto each other.
    - Between ``beta`` and ``1`` the force ramps from 0 up to ``attraction`` and
      back down to 0, so species-dependent attraction/repulsion acts only in a
      mid-range "social" band.
    - Beyond ``r_max`` (``r_norm >= 1``) there is no interaction.
    """
    core = r_norm / beta - 1.0
    social = attraction * (1.0 - np.abs(2.0 * r_norm - 1.0 - beta) / (1.0 - beta))
    return np.where(r_norm < beta, core, np.where(r_norm < 1.0, social, 0.0))


class ParticleSystem:
    """A self-contained Particle Life world."""

    def __init__(self, config: SimulationConfig, seed: int | None = None):
        self.config = config
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.positions = rng.random((config.num_particles, 2))
        self.velocities = np.zeros((config.num_particles, 2))
        self.types = rng.integers(0, config.num_types, config.num_particles)

    def step(self) -> None:
        """Advance the simulation by one timestep ``dt``."""
        cfg = self.config
        pos = self.positions

        # Pairwise displacement on the torus, wrapped to the shortest vector.
        delta = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]
        delta -= np.round(delta)

        dist = np.linalg.norm(delta, axis=-1)
        # A particle never interacts with itself. Use a large finite value (not
        # inf) so the force formula below stays finite and produces no NaNs.
        np.fill_diagonal(dist, 1e6)

        r_norm = dist / cfg.r_max
        attraction = cfg.attraction_matrix[self.types[:, np.newaxis], self.types[np.newaxis, :]]

        mag = _pairwise_force(r_norm, attraction, cfg.beta)
        mag = np.where(r_norm < 1.0, mag, 0.0)

        direction = delta / dist[..., np.newaxis]
        force = (mag[..., np.newaxis] * direction).sum(axis=1) * cfg.force_factor

        self.velocities = (self.velocities + force * cfg.dt) * cfg.friction
        self.positions = (pos + self.velocities * cfg.dt) % 1.0

    def run(self, steps: int) -> None:
        for _ in range(steps):
            self.step()
