from __future__ import annotations
import numpy as np
from typing import List
from .bodies import Body

G = 1.0
SOFTENING = 0.8  # prevent force singularity when bodies get close


class Simulation:
    def __init__(self, bodies: List[Body], dt: float = 0.01):
        self.bodies = bodies
        self.dt = dt
        self.step_count = 0
        self.time = 0.0

    def _accelerations(self) -> List[np.ndarray]:
        n = len(self.bodies)
        a = [np.zeros(2) for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                r = self.bodies[j].pos - self.bodies[i].pos
                dist_sq = float(np.dot(r, r)) + SOFTENING ** 2
                dist = np.sqrt(dist_sq)
                f = G * r / (dist * dist_sq)  # G * r̂ / r²
                a[i] += f * self.bodies[j].mass
                a[j] -= f * self.bodies[i].mass
        return a

    def step(self) -> None:
        # Leapfrog (Störmer-Verlet) — energy-conserving for orbital mechanics
        a0 = self._accelerations()

        # Half-step velocities
        half_v = [b.vel + a0[i] * (self.dt * 0.5) for i, b in enumerate(self.bodies)]

        # Full-step positions
        for i, body in enumerate(self.bodies):
            body.record_trail()
            body.pos = body.pos + half_v[i] * self.dt

        # Accelerations at new positions
        a1 = self._accelerations()

        # Complete velocity step
        for i, body in enumerate(self.bodies):
            body.vel = half_v[i] + a1[i] * (self.dt * 0.5)

        self.step_count += 1
        self.time += self.dt

    def center_of_mass(self) -> np.ndarray:
        total = sum(b.mass for b in self.bodies)
        return sum(b.mass * b.pos for b in self.bodies) / total

    def total_energy(self) -> float:
        ke = sum(0.5 * b.mass * float(np.dot(b.vel, b.vel)) for b in self.bodies)
        pe = 0.0
        for i, bi in enumerate(self.bodies):
            for bj in self.bodies[i + 1:]:
                r = float(np.linalg.norm(bj.pos - bi.pos))
                pe -= G * bi.mass * bj.mass / max(r, SOFTENING)
        return ke + pe
