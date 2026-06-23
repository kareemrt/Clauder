import numpy as np

from strange_attractors.integrator import integrate, rk4_step
from strange_attractors.systems import SYSTEMS
from strange_attractors.divergence import lyapunov_benettin


def test_rk4_matches_exponential_decay():
    # dx/dt = -x has the exact solution x(t) = x0 * exp(-t).
    state = np.array([1.0])
    dt = 0.01
    f = lambda s: -s
    for _ in range(1000):
        state = rk4_step(f, state, dt)
    expected = np.exp(-10.0)
    assert abs(state[0] - expected) < 1e-6


def test_integrate_returns_expected_shape():
    system = SYSTEMS["lorenz"]
    traj = integrate(system, steps=500)
    assert traj.shape == (500, 3)
    assert np.all(np.isfinite(traj))


def test_all_systems_remain_bounded():
    # A genuine attractor should not blow up to infinity over a moderate run.
    for key, system in SYSTEMS.items():
        traj = integrate(system, steps=2000)
        assert np.all(np.isfinite(traj)), f"{key} produced non-finite values"
        assert np.max(np.abs(traj)) < 1e4, f"{key} diverged"


def test_lorenz_has_positive_lyapunov_exponent():
    # Chaos is defined by sensitive dependence on initial conditions: lambda > 0.
    lyap = lyapunov_benettin(SYSTEMS["lorenz"], eps=1e-8, steps=8000)
    assert lyap > 0.3
