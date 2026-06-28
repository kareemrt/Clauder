import numpy as np
import pytest

from murmuration.simulation import FlockSimulation, SimulationConfig


def make_sim(**overrides) -> FlockSimulation:
    defaults = dict(num_boids=40, num_predators=2, seed=123)
    defaults.update(overrides)
    return FlockSimulation(SimulationConfig(**defaults))


def test_initial_state_is_within_bounds():
    sim = make_sim()
    c = sim.config
    assert (sim.positions[:, 0] >= 0).all() and (sim.positions[:, 0] <= c.width).all()
    assert (sim.positions[:, 1] >= 0).all() and (sim.positions[:, 1] <= c.height).all()
    assert sim.positions.shape == (c.num_boids, 2)
    assert sim.predator_positions.shape == (c.num_predators, 2)


def test_positions_stay_within_bounds_after_many_steps():
    sim = make_sim()
    for _ in range(200):
        sim.step()
    c = sim.config
    assert (sim.positions[:, 0] >= -1e-9).all() and (sim.positions[:, 0] <= c.width + 1e-9).all()
    assert (sim.positions[:, 1] >= -1e-9).all() and (sim.positions[:, 1] <= c.height + 1e-9).all()
    assert (sim.predator_positions[:, 0] >= -1e-9).all() and (sim.predator_positions[:, 0] <= c.width + 1e-9).all()


def test_speed_is_clamped_between_min_and_max():
    sim = make_sim()
    for _ in range(100):
        sim.step()
    speeds = np.linalg.norm(sim.velocities, axis=-1)
    assert (speeds >= sim.config.min_speed - 1e-6).all()
    assert (speeds <= sim.config.max_speed + 1e-6).all()

    predator_speeds = np.linalg.norm(sim.predator_velocities, axis=-1)
    assert (predator_speeds <= sim.config.predator_max_speed + 1e-6).all()


def test_same_seed_is_deterministic():
    sim_a = make_sim()
    sim_b = make_sim()
    for _ in range(50):
        sim_a.step()
        sim_b.step()
    np.testing.assert_allclose(sim_a.positions, sim_b.positions)
    np.testing.assert_allclose(sim_a.velocities, sim_b.velocities)


def test_different_seeds_diverge():
    sim_a = make_sim(seed=1)
    sim_b = make_sim(seed=2)
    for _ in range(20):
        sim_a.step()
        sim_b.step()
    assert not np.allclose(sim_a.positions, sim_b.positions)


def test_run_returns_one_frame_per_step():
    sim = make_sim()
    frames = sim.run(10)
    assert len(frames) == 10
    boid_pos, boid_vel, pred_pos, pred_vel = frames[-1]
    assert boid_pos.shape == (sim.config.num_boids, 2)
    assert pred_pos.shape == (sim.config.num_predators, 2)
    assert sim.step_count == 10


def test_works_with_zero_predators():
    sim = make_sim(num_predators=0)
    for _ in range(30):
        sim.step()
    assert sim.predator_positions.shape == (0, 2)


def _mean_nearest_neighbor_distance(positions: np.ndarray) -> float:
    diff = positions[:, None, :] - positions[None, :, :]
    dist = np.linalg.norm(diff, axis=-1)
    np.fill_diagonal(dist, np.inf)
    return dist.min(axis=1).mean()


def test_flock_converges_toward_local_clusters():
    """With cohesion/alignment active and no predators, boids should end up
    much closer to their nearest flockmate than a uniform random start."""
    sim = make_sim(num_predators=0, num_boids=60, seed=99)
    initial_nn_distance = _mean_nearest_neighbor_distance(sim.positions)
    for _ in range(150):
        sim.step()
    final_nn_distance = _mean_nearest_neighbor_distance(sim.positions)
    assert final_nn_distance < initial_nn_distance
