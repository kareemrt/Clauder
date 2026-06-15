"""Core particle-life simulation.

The simulation models a set of particles, each belonging to one of
``num_types`` species. Every pair of species (i, j) has an interaction
strength ``rules[i, j]`` in roughly [-1, 1]:

* A positive value means particles of type ``i`` are *attracted* to
  particles of type ``j``.
* A negative value means they are *repelled*.

Regardless of the sign of ``rules``, particles always strongly repel
each other at very short range (so they don't collapse into a single
point). The force as a function of distance ``r`` is a "tent" function:

* ``r < beta``         -> strong, constant repulsion (collision avoidance)
* ``beta <= r <= r_max`` -> ramps linearly from 0 up to ``rules[i, j]``
                             at the midpoint and back down to 0
* ``r > r_max``        -> no force

This is the same family of rules popularized by Jeffrey Ventrella's
"Clusters" and the many "particle life" simulations it inspired. The
whole update is vectorized with numpy so a few hundred particles can be
simulated at interactive speed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimulationConfig:
    """Tunable parameters for a :class:`ParticleLife` simulation."""

    num_particles: int = 400
    num_types: int = 5
    rules: np.ndarray | None = None  # shape (num_types, num_types), values in [-1, 1]
    width: float = 1.0
    height: float = 1.0
    r_max: float = 0.08
    beta: float = 0.3  # fraction of r_max below which particles always repel
    friction: float = 0.85  # velocity retained each step (0..1)
    force_factor: float = 1.0
    dt: float = 0.02
    seed: int | None = None

    def resolved_rules(self, rng: np.random.Generator) -> np.ndarray:
        if self.rules is not None:
            rules = np.asarray(self.rules, dtype=np.float64)
            if rules.shape != (self.num_types, self.num_types):
                raise ValueError(
                    f"rules must have shape ({self.num_types}, {self.num_types}), "
                    f"got {rules.shape}"
                )
            return rules
        return rng.uniform(-1.0, 1.0, size=(self.num_types, self.num_types))


@dataclass
class ParticleLife:
    """A toroidal 2D particle-life simulation.

    Example
    -------
    >>> sim = ParticleLife(SimulationConfig(seed=0))
    >>> sim.step()
    >>> sim.positions.shape
    (400, 2)
    """

    config: SimulationConfig
    positions: np.ndarray = field(init=False)
    velocities: np.ndarray = field(init=False)
    types: np.ndarray = field(init=False)
    rules: np.ndarray = field(init=False)
    rng: np.random.Generator = field(init=False, repr=False)
    step_count: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.config.seed)
        cfg = self.config

        self.positions = self.rng.uniform(
            low=[0.0, 0.0], high=[cfg.width, cfg.height], size=(cfg.num_particles, 2)
        )
        self.velocities = np.zeros((cfg.num_particles, 2), dtype=np.float64)
        self.types = self.rng.integers(0, cfg.num_types, size=cfg.num_particles)
        self.rules = cfg.resolved_rules(self.rng)

    def step(self) -> None:
        """Advance the simulation by one time step (in place)."""
        cfg = self.config
        n = cfg.num_particles

        # Pairwise displacement with periodic (toroidal) wrap, using the
        # "minimum image" convention so particles interact with the
        # nearest copy of every other particle across the wrap boundary.
        delta = self.positions[None, :, :] - self.positions[:, None, :]
        delta[..., 0] -= cfg.width * np.round(delta[..., 0] / cfg.width)
        delta[..., 1] -= cfg.height * np.round(delta[..., 1] / cfg.height)

        dist = np.sqrt((delta ** 2).sum(axis=-1))
        np.fill_diagonal(dist, np.inf)  # ignore self-interaction

        # Strength matrix per ordered pair, looked up from the rule table.
        strength = self.rules[self.types[:, None], self.types[None, :]]

        force_mag = _force_profile(dist, strength, cfg.beta * cfg.r_max, cfg.r_max)

        # Direction unit vectors (avoid divide-by-zero for inf distances).
        with np.errstate(invalid="ignore", divide="ignore"):
            direction = delta / dist[..., None]
        direction = np.nan_to_num(direction, nan=0.0, posinf=0.0, neginf=0.0)

        total_force = (force_mag[..., None] * direction).sum(axis=1)
        total_force *= cfg.force_factor

        self.velocities = self.velocities * cfg.friction + total_force * cfg.dt
        self.positions += self.velocities * cfg.dt
        self.positions[:, 0] %= cfg.width
        self.positions[:, 1] %= cfg.height

        self.step_count += 1

    def run(self, steps: int) -> None:
        """Advance the simulation by ``steps`` time steps."""
        for _ in range(steps):
            self.step()


def _force_profile(
    dist: np.ndarray, strength: np.ndarray, beta_dist: float, r_max: float
) -> np.ndarray:
    """Piecewise "tent" force profile used by particle-life rules.

    Returns the (signed) force magnitude for every pairwise distance in
    ``dist``, given the per-pair rule ``strength`` in [-1, 1].
    """
    # Region 1: short range, always repulsive, independent of `strength`.
    repulsion = dist / beta_dist - 1.0

    # Region 2: the attraction/repulsion "tent" peaking at the midpoint
    # between beta_dist and r_max.
    mid = (beta_dist + r_max) / 2.0
    half_width = (r_max - beta_dist) / 2.0
    tent = strength * (1.0 - np.abs(dist - mid) / half_width)

    force = np.where(dist < beta_dist, repulsion, tent)
    force = np.where(dist > r_max, 0.0, force)
    return force
