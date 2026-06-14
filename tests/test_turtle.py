import math
import random

import pytest

from fractal_garden.turtle import Segment, TurtleConfig, run


def test_square_returns_to_start():
    config = TurtleConfig(angle=90, step=1.0, start_heading=0)
    segments = run("F+F+F+F", config)
    assert len(segments) == 4
    # The path is a closed unit square: last point equals first point.
    assert segments[0].x1 == pytest.approx(segments[-1].x2, abs=1e-9)
    assert segments[0].y1 == pytest.approx(segments[-1].y2, abs=1e-9)


def test_move_without_drawing():
    config = TurtleConfig(angle=90, step=1.0, start_heading=0)
    segments = run("Ff", config)
    assert len(segments) == 1
    assert segments[0] == Segment(0.0, 0.0, 1.0, 0.0, 0)


def test_brackets_save_and_restore_state():
    config = TurtleConfig(angle=90, step=1.0, start_heading=0)
    # Branch off, then come back to the trunk and continue straight.
    segments = run("F[+F]F", config)
    assert len(segments) == 3
    trunk_start, branch, trunk_end = segments
    assert trunk_start.depth == 0
    assert branch.depth == 1
    assert trunk_end.depth == 0
    # The second trunk segment continues from where the first left off,
    # unaffected by the branch.
    assert trunk_end.x1 == pytest.approx(trunk_start.x2)
    assert trunk_end.y1 == pytest.approx(trunk_start.y2)
    assert trunk_end.x2 == pytest.approx(2.0)


def test_unbalanced_bracket_raises():
    config = TurtleConfig(angle=90, step=1.0)
    with pytest.raises(ValueError):
        run("F]", config)


def test_angle_jitter_is_seed_reproducible():
    config = TurtleConfig(angle=20, step=1.0, angle_jitter=10)
    a = run("F+F+F", config, random.Random(7))
    b = run("F+F+F", config, random.Random(7))
    assert a == b


def test_heading_starts_from_configured_value():
    config = TurtleConfig(angle=90, step=2.0, start_heading=90)
    segments = run("F", config)
    seg = segments[0]
    assert seg.x2 == pytest.approx(0.0, abs=1e-9)
    assert seg.y2 == pytest.approx(2.0, abs=1e-9)
