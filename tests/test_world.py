import numpy as np
import pytest

from bloom.creatures import PRESETS
from bloom.world import World


def test_step_keeps_state_in_unit_range():
    world = World(48, 48, seed=0)
    world.seed_random(density=0.5, patch=30)
    for _ in range(50):
        world.step()
    assert world.state.min() >= 0.0
    assert world.state.max() <= 1.0
    assert np.isfinite(world.state).all()


def test_step_preserves_shape():
    world = World(32, 40, seed=0)
    world.seed_random(density=0.3)
    world.step()
    assert world.state.shape == (32, 40)


def test_place_wraps_around_edges():
    world = World(40, 40, radius=5, shells=[(0.5, 0.15, 1.0)], seed=0)
    pattern = np.ones((5, 5))
    world.place(pattern, row=0, col=0)
    assert world.state[0, 0] == 1.0
    assert world.state[-1, -1] == 1.0  # wrapped from the top-left corner


@pytest.mark.parametrize("name", list(PRESETS))
def test_every_preset_stays_alive(name):
    preset = PRESETS[name]
    world = World(
        80,
        80,
        radius=preset.radius,
        shells=preset.shells,
        mu=preset.mu,
        sigma=preset.sigma,
        dt=preset.dt,
        seed=0,
    )
    if preset.seed_kind == "random":
        world.seed_random(density=preset.density, patch=48)
    else:
        world.place(preset.pattern, 40, 40)

    for _ in range(200):
        world.step()

    assert world.mass() > 0.0, f"{name} died out"
    assert np.isfinite(world.state).all()
