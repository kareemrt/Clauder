import numpy as np

SOFTENING = 0.1  # Prevents singularities when bodies get very close


class Body:
    """A point mass with position, velocity, and an optional trail."""

    def __init__(self, mass: float, pos, vel, name: str = ""):
        self.mass = float(mass)
        self.pos  = np.array(pos, dtype=float)
        self.vel  = np.array(vel, dtype=float)
        self.name = name
        self.trail: list[np.ndarray] = []
        self.max_trail = 100

    def record_trail(self):
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)


class Simulation:
    """Velocity Verlet N-body integrator."""

    def __init__(self, bodies: list[Body], G: float = 1.0, dt: float = 0.005):
        self.bodies = bodies
        self.G      = G
        self.dt     = dt
        self.time   = 0.0
        self.steps  = 0

    # ------------------------------------------------------------------

    def _accelerations(self) -> list[np.ndarray]:
        n   = len(self.bodies)
        acc = [np.zeros(2) for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                bi, bj  = self.bodies[i], self.bodies[j]
                r       = bj.pos - bi.pos
                dist_sq = r @ r + SOFTENING ** 2
                factor  = self.G / (dist_sq * dist_sq ** 0.5)  # G / r^3
                acc[i] += factor * bj.mass * r
                acc[j] -= factor * bi.mass * r
        return acc

    def step(self):
        """Advance simulation by one timestep using Velocity Verlet."""
        acc0 = self._accelerations()
        for i, body in enumerate(self.bodies):
            body.record_trail()
            body.pos += body.vel * self.dt + 0.5 * acc0[i] * self.dt ** 2

        acc1 = self._accelerations()
        for i, body in enumerate(self.bodies):
            body.vel += 0.5 * (acc0[i] + acc1[i]) * self.dt

        self.time  += self.dt
        self.steps += 1

    # ------------------------------------------------------------------

    def kinetic_energy(self) -> float:
        return sum(0.5 * b.mass * float(b.vel @ b.vel) for b in self.bodies)

    def potential_energy(self) -> float:
        pe = 0.0
        for i, bi in enumerate(self.bodies):
            for bj in self.bodies[i + 1:]:
                dist = float(np.linalg.norm(bj.pos - bi.pos)) + SOFTENING
                pe  -= self.G * bi.mass * bj.mass / dist
        return pe

    def total_energy(self) -> float:
        return self.kinetic_energy() + self.potential_energy()

    def center_of_mass(self) -> np.ndarray:
        total_mass = sum(b.mass for b in self.bodies)
        return sum(b.mass * b.pos for b in self.bodies) / total_mass
