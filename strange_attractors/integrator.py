"""Fixed-step RK4 integration of autonomous 3D ODE systems."""

from __future__ import annotations

import numpy as np

from .systems import AttractorSystem


def rk4_step(f, state: np.ndarray, dt: float) -> np.ndarray:
    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate(
    system: AttractorSystem,
    state0: tuple | np.ndarray | None = None,
    dt: float | None = None,
    steps: int | None = None,
    discard: int = 500,
) -> np.ndarray:
    """Integrate `system` forward and return an (steps, 3) trajectory array.

    The first `discard` steps are dropped so the trajectory has settled onto
    the attractor before any returned point, avoiding transient outliers.
    """
    state = np.array(state0 if state0 is not None else system.state0, dtype=float)
    dt = system.dt if dt is None else dt
    steps = system.steps if steps is None else steps

    for _ in range(discard):
        state = rk4_step(system.f, state, dt)

    trajectory = np.empty((steps, 3))
    for i in range(steps):
        trajectory[i] = state
        state = rk4_step(system.f, state, dt)
    return trajectory
