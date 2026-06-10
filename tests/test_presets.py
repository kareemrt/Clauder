import pytest

from fractal_garden.lsystem import bounding_box, interpret
from fractal_garden.presets import PRESETS, get_preset


@pytest.mark.parametrize("key", sorted(PRESETS))
def test_preset_expands_and_draws_something(key):
    lsystem = PRESETS[key]
    instructions = lsystem.expand(2)
    segments = interpret(instructions, lsystem)

    assert len(segments) > 0

    min_x, min_y, max_x, max_y = bounding_box(segments)
    # The fractal should occupy a non-degenerate area or line.
    assert (max_x - min_x) + (max_y - min_y) > 0


def test_get_preset_unknown_key_raises():
    with pytest.raises(KeyError):
        get_preset("does-not-exist")


def test_get_preset_returns_known_lsystem():
    lsystem = get_preset("koch-snowflake")
    assert lsystem.name == "Koch Snowflake"
