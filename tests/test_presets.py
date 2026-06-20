import pytest

from lsystems.presets import PRESETS, get
from lsystems.svg import segments_to_svg
from lsystems.turtle import TurtleInterpreter


@pytest.mark.parametrize("name", sorted(PRESETS))
def test_every_preset_expands_and_renders_without_error(name):
    preset = get(name)
    # Cap iterations for the test so dragon-curve / fractal-plant stay fast.
    iterations = min(preset.iterations, 4)
    instructions = preset.lsystem.expand(iterations)
    segments = TurtleInterpreter(
        angle=preset.angle, start_heading=preset.start_heading, draw_chars=preset.draw_chars
    ).interpret(instructions)
    assert len(segments) > 0
    svg = segments_to_svg(segments)
    assert svg.startswith("<svg")


def test_get_unknown_preset_raises_with_helpful_message():
    with pytest.raises(KeyError, match="unknown preset"):
        get("not-a-real-preset")
