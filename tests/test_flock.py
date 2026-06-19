import numpy as np
import pytest

from boids.flock import Flock


def test_positions_stay_within_bounds_after_many_steps():
    flock = Flock(n_boids=40, width=200, height=150, n_predators=3, seed=0)
    for _ in range(50):
        flock.step()

    assert np.all(flock.positions[:, 0] >= 0) and np.all(flock.positions[:, 0] < 200)
    assert np.all(flock.positions[:, 1] >= 0) and np.all(flock.positions[:, 1] < 150)
    assert np.all(flock.predator_positions[:, 0] >= 0) and np.all(flock.predator_positions[:, 0] < 200)


def test_velocities_never_exceed_max_speed():
    flock = Flock(n_boids=60, width=300, height=300, n_predators=2, max_speed=3.5, seed=1)
    for _ in range(80):
        flock.step()

    speeds = np.linalg.norm(flock.velocities, axis=1)
    assert np.all(speeds <= flock.max_speed + 1e-6)

    predator_speeds = np.linalg.norm(flock.predator_velocities, axis=1)
    assert np.all(predator_speeds <= flock.predator_max_speed + 1e-6)


def test_separation_pushes_overlapping_boids_apart():
    flock = Flock(n_boids=2, width=500, height=500, n_predators=0, seed=2)
    flock.positions = np.array([[100.0, 100.0], [101.0, 100.0]])
    flock.velocities = np.zeros((2, 2))

    force = flock._flocking_forces()

    # The two boids are far closer than separation_radius, so each one should
    # be steered away from the other along the x-axis.
    assert force[0, 0] < 0
    assert force[1, 0] > 0


def test_toroidal_wraparound_is_seamless():
    flock = Flock(n_boids=2, width=100, height=100, n_predators=0, seed=3)
    # Two boids on opposite sides of the same seam are effectively adjacent.
    flock.positions = np.array([[1.0, 50.0], [99.0, 50.0]])
    flock.velocities = np.zeros((2, 2))

    delta = flock._toroidal_delta(flock.positions, flock.positions, flock.width, flock.height)
    distance = np.linalg.norm(delta[0, 1])

    assert distance < 5.0


def test_predators_chase_the_nearest_boid():
    flock = Flock(n_boids=3, width=1000, height=1000, n_predators=1, seed=4)
    flock.positions = np.array([[5.0, 5.0], [620.0, 620.0], [625.0, 625.0]])
    flock.velocities = np.zeros((3, 2))
    flock.predator_positions = np.array([[600.0, 600.0]])
    flock.predator_velocities = np.zeros((1, 2))

    flock._step_predators(dt=1.0)

    # The (620,620)/(625,625) cluster is much nearer than the far corner
    # boid, so the predator should have moved toward it.
    assert flock.predator_positions[0, 0] > 600
    assert flock.predator_positions[0, 1] > 600


@pytest.mark.parametrize("n_boids", [0, 1, 5])
def test_handles_small_flocks_without_error(n_boids):
    flock = Flock(n_boids=n_boids, width=200, height=200, n_predators=1, seed=5)
    flock.step()
    assert flock.positions.shape == (n_boids, 2)
