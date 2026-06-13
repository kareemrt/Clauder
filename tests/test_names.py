from worldforge.names import generate_world_name


def test_name_is_deterministic():
    assert generate_world_name(42) == generate_world_name(42)


def test_name_contains_epithet():
    name = generate_world_name(1)
    assert ", the " in name


def test_different_seeds_usually_differ():
    names = {generate_world_name(seed) for seed in range(10)}
    assert len(names) > 1
