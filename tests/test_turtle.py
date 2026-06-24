import math

import pytest

from lsystemgarden.turtle import bounding_box, interpret


def test_single_forward_draws_one_segment():
    segments = interpret("F", angle=90, step=2.0, start_heading=0.0)
    assert len(segments) == 1
    seg = segments[0]
    assert seg.x1 == pytest.approx(0.0)
    assert seg.y1 == pytest.approx(0.0)
    assert seg.x2 == pytest.approx(2.0)
    assert seg.y2 == pytest.approx(0.0)
    assert seg.depth == 0


def test_turning_changes_heading():
    segments = interpret("F+F", angle=90, step=1.0, start_heading=0.0)
    second = segments[1]
    assert second.x2 == pytest.approx(second.x1)
    assert second.y2 == pytest.approx(second.y1 + 1.0)


def test_lowercase_f_moves_without_drawing():
    segments = interpret("FfF", angle=90, step=1.0, start_heading=0.0)
    assert len(segments) == 2
    assert segments[1].x1 == pytest.approx(2.0)


def test_brackets_save_and_restore_state():
    segments = interpret("F[+F]F", angle=90, step=1.0, start_heading=0.0)
    # The second F (after the bracket pops) must resume from where the
    # first F ended, heading unchanged by the branch.
    branch_end = segments[1]
    resumed = segments[2]
    assert resumed.x1 == pytest.approx(1.0)
    assert resumed.y1 == pytest.approx(0.0)
    assert resumed.x2 == pytest.approx(2.0)
    assert resumed.y2 == pytest.approx(0.0)
    assert branch_end.depth == 1
    assert resumed.depth == 0


def test_unmatched_closing_bracket_raises():
    with pytest.raises(ValueError):
        interpret("F]", angle=90, step=1.0, start_heading=0.0)


def test_unclosed_bracket_raises():
    with pytest.raises(ValueError):
        interpret("[F", angle=90, step=1.0, start_heading=0.0)


def test_ignored_symbols_have_no_turtle_effect():
    a = interpret("F", angle=90, step=1.0, start_heading=0.0)
    b = interpret("FXY", angle=90, step=1.0, start_heading=0.0)
    assert a == b


def test_unknown_draw_chars_can_be_customized():
    segments = interpret("G", angle=90, step=1.0, start_heading=0.0, draw_chars=frozenset({"G"}))
    assert len(segments) == 1


def test_bounding_box_of_square_path():
    segments = interpret("F+F+F+F", angle=90, step=1.0, start_heading=0.0)
    min_x, min_y, max_x, max_y = bounding_box(segments)
    assert min_x == pytest.approx(0.0)
    assert min_y == pytest.approx(0.0)
    assert max_x == pytest.approx(1.0)
    assert max_y == pytest.approx(1.0)


def test_bounding_box_requires_segments():
    with pytest.raises(ValueError):
        bounding_box([])


def test_diagonal_heading_uses_trigonometry():
    segments = interpret("F", angle=90, step=1.0, start_heading=45.0)
    seg = segments[0]
    expected = 1.0 * math.cos(math.radians(45.0))
    assert seg.x2 == pytest.approx(expected)
