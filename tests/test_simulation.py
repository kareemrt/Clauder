import numpy as np
import pytest

from particle_life.presets import PRESETS, get_preset
from particle_life.simulation import ParticleSystem, SimulationConfig, _pairwise_force


def make_system(num_particles=20, seed=0):
    matrix = PRESETS["cells"].matrix
    config = SimulationConfig(num_particles=num_particles, attraction_matrix=matrix)
    return ParticleSystem(config, seed=seed)


def test_initial_state_within_bounds():
    system = make_system()
    assert system.positions.shape == (20, 2)
    assert np.all(system.positions >= 0.0)
    assert np.all(system.positions < 1.0)
    assert np.all(system.velocities == 0.0)
    assert set(np.unique(system.types)) <= set(range(system.config.num_types))


def test_step_keeps_positions_on_torus():
    system = make_system()
    for _ in range(50):
        system.step()
    assert np.all(system.positions >= 0.0)
    assert np.all(system.positions < 1.0)
    assert np.all(np.isfinite(system.positions))
    assert np.all(np.isfinite(system.velocities))


def test_step_is_deterministic_given_seed():
    a = make_system(seed=42)
    b = make_system(seed=42)
    a.run(10)
    b.run(10)
    np.testing.assert_array_equal(a.positions, b.positions)
    np.testing.assert_array_equal(a.velocities, b.velocities)


def test_different_seeds_diverge():
    a = make_system(seed=1)
    b = make_system(seed=2)
    a.run(5)
    b.run(5)
    assert not np.array_equal(a.positions, b.positions)


@pytest.mark.parametrize(
    "r_norm, attraction, beta, expected",
    [
        (0.0, 1.0, 0.3, -1.0),  # at the center, pure repulsion regardless of attraction
        (0.3, 1.0, 0.3, 0.0),  # at the repulsion boundary, force is zero
        (0.65, 1.0, 0.3, 1.0),  # at the midpoint of the social band, full attraction
        (1.0, 1.0, 0.3, 0.0),  # outside r_max, no force
    ],
)
def test_pairwise_force_shape(r_norm, attraction, beta, expected):
    result = _pairwise_force(np.array([r_norm]), np.array([attraction]), beta)
    assert result[0] == pytest.approx(expected, abs=1e-9)


def test_get_preset_known_and_unknown():
    preset = get_preset("cells")
    assert preset.matrix.shape[0] == len(preset.colors)

    with pytest.raises(KeyError):
        get_preset("does-not-exist")


def test_all_presets_have_square_matrices_with_matching_colors():
    for preset in PRESETS.values():
        n = preset.matrix.shape
        assert n[0] == n[1], preset.name
        assert n[0] == len(preset.colors), preset.name
