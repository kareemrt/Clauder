import numpy as np
import pytest

from primordia.presets import PRESETS, get_preset
from primordia.simulation import ParticleLife, SimulationConfig


def test_initial_state_shapes():
    sim = ParticleLife(SimulationConfig(num_particles=50, num_types=3, seed=0))
    assert sim.positions.shape == (50, 2)
    assert sim.velocities.shape == (50, 2)
    assert sim.types.shape == (50,)
    assert sim.rules.shape == (3, 3)


def test_positions_stay_in_bounds_after_steps():
    sim = ParticleLife(SimulationConfig(num_particles=80, num_types=4, seed=1))
    sim.run(20)
    assert np.all(sim.positions >= 0)
    assert sim.positions[:, 0].max() < sim.config.width
    assert sim.positions[:, 1].max() < sim.config.height


def test_step_is_deterministic_given_seed():
    sim_a = ParticleLife(SimulationConfig(num_particles=30, num_types=3, seed=42))
    sim_b = ParticleLife(SimulationConfig(num_particles=30, num_types=3, seed=42))

    sim_a.run(10)
    sim_b.run(10)

    np.testing.assert_allclose(sim_a.positions, sim_b.positions)
    np.testing.assert_allclose(sim_a.velocities, sim_b.velocities)


def test_step_count_increments():
    sim = ParticleLife(SimulationConfig(num_particles=10, num_types=2, seed=0))
    sim.run(5)
    assert sim.step_count == 5


def test_explicit_rules_shape_validation():
    bad_rules = np.zeros((2, 2))
    sim_config = SimulationConfig(num_particles=10, num_types=3, rules=bad_rules, seed=0)
    with pytest.raises(ValueError):
        ParticleLife(sim_config)


@pytest.mark.parametrize("name", sorted(PRESETS))
def test_all_presets_run(name):
    config = get_preset(name, seed=0)
    sim = ParticleLife(config)
    sim.run(5)
    assert np.all(np.isfinite(sim.positions))
    assert np.all(np.isfinite(sim.velocities))


def test_unknown_preset_raises():
    with pytest.raises(KeyError):
        get_preset("does-not-exist")
