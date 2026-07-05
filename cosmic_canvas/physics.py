"""
Leapfrog (Störmer-Verlet) N-body integrator.

Units: AU, years, solar masses
  G = 4π² AU³ yr⁻² M☉⁻¹  (exact in Gaussian gravitational units)
"""

import math
from typing import List, Tuple

from .bodies import CelestialBody

G: float = 4.0 * math.pi ** 2   # AU³ yr⁻² M☉⁻¹
SOFTENING: float = 0.005         # AU — prevents force singularity at close approach


def _accelerations(bodies: List[CelestialBody]) -> List[Tuple[float, float]]:
    """Compute gravitational acceleration on each body (O(N²))."""
    n = len(bodies)
    accels: List[Tuple[float, float]] = [(0.0, 0.0)] * n
    for i in range(n):
        ax = ay = 0.0
        bi = bodies[i]
        for j in range(n):
            if i == j:
                continue
            bj = bodies[j]
            dx = bj.x - bi.x
            dy = bj.y - bi.y
            r2 = dx * dx + dy * dy + SOFTENING ** 2
            r = math.sqrt(r2)
            a = G * bj.mass / r2
            ax += a * dx / r
            ay += a * dy / r
        accels[i] = (ax, ay)
    return accels


def step(bodies: List[CelestialBody], dt: float) -> None:
    """
    Advance bodies by one timestep using leapfrog integration.

    This scheme is symplectic: it conserves a modified energy exactly,
    so long-term energy drift is negligible compared to simple Euler.
    """
    a0 = _accelerations(bodies)

    # Half-step velocity kick
    hvx = [b.vx + 0.5 * a[0] * dt for b, a in zip(bodies, a0)]
    hvy = [b.vy + 0.5 * a[1] * dt for b, a in zip(bodies, a0)]

    # Full position drift
    for i, b in enumerate(bodies):
        b.x += hvx[i] * dt
        b.y += hvy[i] * dt
        b.record_position()

    # Recompute forces, second half-kick
    a1 = _accelerations(bodies)
    for i, b in enumerate(bodies):
        b.vx = hvx[i] + 0.5 * a1[i][0] * dt
        b.vy = hvy[i] + 0.5 * a1[i][1] * dt


def total_energy(bodies: List[CelestialBody]) -> float:
    """Return total mechanical energy (KE + PE) in natural units."""
    ke = sum(0.5 * b.mass * b.speed ** 2 for b in bodies)
    pe = 0.0
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            r = math.sqrt(dx * dx + dy * dy + SOFTENING ** 2)
            pe -= G * bodies[i].mass * bodies[j].mass / r
    return ke + pe
