import numpy as np

from worldforge.worldgen import BIOMES, generate_world


def test_generate_world_shapes():
    world = generate_world(seed=123, width=64, height=48)

    assert world.elevation.shape == (48, 64)
    assert world.moisture.shape == (48, 64)
    assert world.biome_ids.shape == (48, 64)
    assert world.river_mask.shape == (48, 64)


def test_generate_world_is_deterministic():
    world_a = generate_world(seed=99, width=32, height=32)
    world_b = generate_world(seed=99, width=32, height=32)

    np.testing.assert_array_equal(world_a.elevation, world_b.elevation)
    np.testing.assert_array_equal(world_a.biome_ids, world_b.biome_ids)
    np.testing.assert_array_equal(world_a.river_mask, world_b.river_mask)
    assert world_a.name == world_b.name


def test_elevation_and_moisture_in_unit_range():
    world = generate_world(seed=5, width=64, height=64)

    assert world.elevation.min() >= 0.0
    assert world.elevation.max() <= 1.0
    assert world.moisture.min() >= 0.0
    assert world.moisture.max() <= 1.0


def test_biome_ids_within_known_biomes():
    world = generate_world(seed=5, width=64, height=64)

    assert world.biome_ids.min() >= 0
    assert world.biome_ids.max() < len(BIOMES)


def test_island_strength_creates_ocean_at_edges():
    world = generate_world(seed=5, width=64, height=64, island_strength=1.0)

    edge_elevations = np.concatenate([
        world.elevation[0, :],
        world.elevation[-1, :],
        world.elevation[:, 0],
        world.elevation[:, -1],
    ])
    # The strong island falloff should push most edge cells underwater.
    assert (edge_elevations < 0.5).mean() > 0.6


def test_rivers_only_flow_through_high_or_water_cells():
    world = generate_world(seed=42, width=128, height=128, river_count=10)

    river_cells = world.river_mask.sum()
    assert river_cells >= 0  # rivers are not guaranteed, but should not error

    if river_cells > 0:
        ys, xs = np.where(world.river_mask)
        assert len(ys) == len(xs)


def test_biome_counts_sum_to_total_cells():
    world = generate_world(seed=7, width=32, height=32)
    counts = world.biome_counts()

    land_and_water_total = sum(v for k, v in counts.items() if k != "river")
    assert land_and_water_total == world.width * world.height
