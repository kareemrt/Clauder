import random

import pytest

from lsystem_garden import presets
from lsystem_garden.render import render_svg
from lsystem_garden.turtle import walk


@pytest.mark.parametrize("name", presets.names())
def test_every_preset_grows_and_renders(name):
    system = presets.get(name)
    grown = system.expand(3, rng=random.Random(0))
    assert grown  # never empty

    segments = walk(grown, angle=system.angle, step=4.0)
    assert segments, f"{name} produced no drawable segments"

    svg = render_svg(segments, background=system.background, trunk_color=system.seed_color)
    assert svg.startswith("<?xml")


def test_get_unknown_preset_raises_with_helpful_message():
    with pytest.raises(KeyError, match="unknown preset 'nope'"):
        presets.get("nope")


def test_names_are_sorted_and_unique():
    all_names = presets.names()
    assert all_names == sorted(set(all_names))
