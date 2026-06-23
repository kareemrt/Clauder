"""Demonstrate sensitive dependence on initial conditions (the 'butterfly effect').

Two trajectories are started a tiny distance `eps` apart and integrated with
identical dynamics. Their separation grows exponentially while it remains
small, at a rate set by the system's largest Lyapunov exponent. Plotting
log(separation) against time reveals a straight line whose slope estimates
that exponent.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .integrator import rk4_step
from .systems import AttractorSystem


def divergence_run(system: AttractorSystem, eps: float = 1e-8, dt=None, steps=None):
    dt = system.dt if dt is None else dt
    steps = system.steps if steps is None else steps

    state_a = np.array(system.state0, dtype=float)
    direction = np.array([1.0, 0.0, 0.0])
    state_b = state_a + eps * direction

    times = np.arange(steps) * dt
    separation = np.empty(steps)

    for i in range(steps):
        separation[i] = np.linalg.norm(state_a - state_b)
        state_a = rk4_step(system.f, state_a, dt)
        state_b = rk4_step(system.f, state_b, dt)

    return times, separation


def lyapunov_benettin(
    system: AttractorSystem, eps: float = 1e-8, dt=None, steps=None, renorm_every: int = 10
) -> float:
    """Estimate the largest Lyapunov exponent via Benettin's renormalization method.

    A perturbation vector is repeatedly grown for `renorm_every` steps and then
    rescaled back to length `eps`, pointing it along the locally fastest-growing
    direction. Averaging log(growth factor) / time over many renormalizations
    converges to the leading Lyapunov exponent, avoiding the saturation bias of
    a single unrenormalized two-trajectory run.
    """
    dt = system.dt if dt is None else dt
    steps = system.steps if steps is None else steps

    state = np.array(system.state0, dtype=float)
    perturbed = state + eps * np.array([1.0, 0.0, 0.0])

    log_growth_sum = 0.0
    n_renorms = 0
    for i in range(steps):
        state = rk4_step(system.f, state, dt)
        perturbed = rk4_step(system.f, perturbed, dt)
        if (i + 1) % renorm_every == 0:
            delta = perturbed - state
            distance = np.linalg.norm(delta)
            log_growth_sum += np.log(distance / eps)
            n_renorms += 1
            perturbed = state + (delta / distance) * eps

    total_time = n_renorms * renorm_every * dt
    return float(log_growth_sum / total_time)


def plot_divergence(system: AttractorSystem, eps: float = 1e-8, dt=None, steps=None):
    times, separation = divergence_run(system, eps=eps, dt=dt, steps=steps)
    lyap = lyapunov_benettin(system, eps=eps, dt=dt, steps=steps)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=150, facecolor="black")
    ax.set_facecolor("black")
    ax.semilogy(times, separation, color="#39ff88", linewidth=1.5)
    ax.axhline(eps, color="#888888", linestyle="--", linewidth=0.8)
    ax.set_xlabel("time", color="white", fontfamily="monospace")
    ax.set_ylabel("separation |Δstate|  (log scale)", color="white", fontfamily="monospace")
    ax.set_title(
        f"{system.name}: divergence of two trajectories {eps:g} apart\n"
        f"estimated largest Lyapunov exponent ≈ {lyap:.3f}",
        color="white",
        fontfamily="monospace",
        fontsize=11,
    )
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#444444")
    fig.tight_layout()
    return fig, ax, lyap
