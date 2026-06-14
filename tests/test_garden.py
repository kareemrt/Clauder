import pytest

from fractal_garden import garden
from fractal_garden.species import SPECIES


@pytest.mark.parametrize("key", sorted(SPECIES))
def test_every_species_grows_segments(key):
    segments = garden.grow(key, seed=1)
    assert len(segments) > 0


@pytest.mark.parametrize("key", sorted(SPECIES))
def test_growth_is_seed_reproducible(key):
    a = garden.grow(key, seed=42)
    b = garden.grow(key, seed=42)
    assert a == b


def test_unknown_species_raises():
    with pytest.raises(ValueError):
        garden.grow("not-a-species")


def test_iterations_override_changes_detail():
    small = garden.grow("koch", iterations=1, seed=0)
    large = garden.grow("koch", iterations=3, seed=0)
    assert len(large) > len(small)
