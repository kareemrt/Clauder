"""Preset N-body scenarios for Nebula."""
from __future__ import annotations

import math
import random as _random

import numpy as np

from .physics import Body, Simulation


def _b(mass: float, pos, vel, name: str = "") -> Body:
    return Body(mass, pos, vel, name)


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

def figure_eight() -> Simulation:
    """
    Chenciner & Montgomery (2000) figure-8 choreography.
    Three equal masses perpetually chase each other in a figure-8 orbit.
    These are the exact initial conditions from the original paper.
    """
    x1 = np.array([-0.97000436,  0.24308753])
    v3 = np.array([-0.93240737, -0.86473146])
    v1 = -v3 / 2
    return Simulation(
        [
            _b(1.0,  x1,          v1,     "Alpha"),
            _b(1.0, -x1,          v1,     "Beta"),
            _b(1.0,  np.zeros(2), v3,     "Gamma"),
        ],
        G=1.0, dt=0.002,
    )


def binary_stars() -> Simulation:
    """Unequal binary star pair with a tiny test planetoid."""
    return Simulation(
        [
            _b(5.0,  [-1.5, 0.0], [0.0,  0.6],  "Castor"),
            _b(3.0,  [ 1.5, 0.0], [0.0, -1.0],  "Pollux"),
            _b(0.01, [ 0.0, 3.5], [1.2,  0.0],  "Pebble"),
        ],
        G=1.0, dt=0.003,
    )


def solar_system() -> Simulation:
    """Scaled inner Solar System: Sun + Mercury, Venus, Earth, Mars."""
    AU = 5.0   # 1 AU in simulation length units
    M  = 1000.0

    def v_circ(r: float) -> float:
        return math.sqrt(M / r)

    return Simulation(
        [
            _b(M,    [0.0,       0.0], [0.0,           0.0],  "Sun"),
            _b(0.01, [0.39 * AU, 0.0], [0.0, v_circ(0.39*AU)], "Mercury"),
            _b(0.01, [0.72 * AU, 0.0], [0.0, v_circ(0.72*AU)], "Venus"),
            _b(0.01, [1.00 * AU, 0.0], [0.0, v_circ(1.00*AU)], "Earth"),
            _b(0.01, [1.52 * AU, 0.0], [0.0, v_circ(1.52*AU)], "Mars"),
        ],
        G=1.0, dt=0.001,
    )


def galaxy_merger() -> Simulation:
    """
    Two mini-galaxies (each: 1 massive core + 8 orbiting stars) on a
    collision course. Produces beautiful chaotic slingshot dynamics.
    """
    rng = _random.Random(42)
    bodies: list[Body] = []

    for cx, cvx in [(-8.0, 1.5), (8.0, -1.5)]:
        core_mass = 20.0
        bodies.append(_b(core_mass, [cx, 0.0], [cvx, 0.0], "Core"))
        for _ in range(8):
            angle = rng.uniform(0, 2 * math.pi)
            r     = rng.uniform(1.5, 3.5)
            vc    = math.sqrt(core_mass / r)
            bodies.append(_b(
                0.1,
                [cx + r * math.cos(angle), r * math.sin(angle)],
                [cvx - vc * math.sin(angle), vc * math.cos(angle)],
                "Star",
            ))

    return Simulation(bodies, G=1.0, dt=0.005)


def random_cluster(n: int = 6, seed: int = 0) -> Simulation:
    """N random bodies with zero net linear momentum."""
    rng = _random.Random(seed)
    bodies = [
        _b(
            rng.uniform(0.5, 3.0),
            [rng.uniform(-5.0, 5.0), rng.uniform(-5.0, 5.0)],
            [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)],
            f"B{i + 1}",
        )
        for i in range(n)
    ]
    # Remove net momentum so the system doesn't drift off-screen
    total = sum(b.mass for b in bodies)
    net_p = sum(b.mass * b.vel for b in bodies)
    for b in bodies:
        b.vel -= net_p / total
    return Simulation(bodies, G=1.0, dt=0.003)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

SCENARIOS: dict[str, callable] = {
    "figure8": figure_eight,
    "binary":  binary_stars,
    "solar":   solar_system,
    "galaxy":  galaxy_merger,
    "random":  random_cluster,
}

SCENARIO_DESCRIPTIONS: dict[str, str] = {
    "figure8": "Chenciner–Montgomery figure-8 three-body choreography",
    "binary":  "Unequal binary star system with an orbiting planetoid",
    "solar":   "Scaled inner Solar System (Sun + 4 planets)",
    "galaxy":  "Two mini-galaxies on a collision course",
    "random":  "N random bodies with zero net momentum",
}
