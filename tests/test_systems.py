import numpy as np

from strange_attractors.systems import SYSTEMS


def test_registry_not_empty():
    assert len(SYSTEMS) >= 5


def test_each_system_has_valid_derivative_at_its_initial_state():
    for key, system in SYSTEMS.items():
        state0 = np.array(system.state0, dtype=float)
        derivative = system.f(state0)
        assert derivative.shape == (3,), f"{key} derivative has wrong shape"
        assert np.all(np.isfinite(derivative)), f"{key} derivative is not finite"


def test_fixed_point_origin_for_thomas_when_b_nonzero():
    # Thomas' system has sin(0)=0 at the origin, so the origin is a fixed point.
    system = SYSTEMS["thomas"]
    derivative = system.f(np.array([0.0, 0.0, 0.0]))
    assert np.allclose(derivative, 0.0)
