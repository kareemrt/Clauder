import math

import pytest

from lsystem_garden.turtle import Segment, bounds, walk


def test_forward_draws_segment_in_heading_direction():
    # Heading 0 means pointing along +x (screen coordinates: y grows downward).
    segments = walk("F", angle=90, step=10, start_heading=0)
    assert len(segments) == 1
    seg = segments[0]
    assert seg.x1 == pytest.approx(0)
    assert seg.y1 == pytest.approx(0)
    assert seg.x2 == pytest.approx(10)
    assert seg.y2 == pytest.approx(0)
    assert seg.depth == 0


def test_pen_up_move_does_not_draw():
    segments = walk("fF", angle=90, step=5, start_heading=0)
    assert len(segments) == 1
    seg = segments[0]
    # The turtle moved 5 units before drawing, so the segment starts at x=5.
    assert seg.x1 == pytest.approx(5)
    assert seg.x2 == pytest.approx(10)


def test_turns_change_heading_by_the_given_angle():
    segments = walk("F+F", angle=90, step=1, start_heading=0)
    first, second = segments
    # Turning left (+) by 90 degrees from heading 0 points the turtle "up" on screen (-y).
    assert second.x2 == pytest.approx(first.x2)
    assert second.y2 == pytest.approx(first.y2 - 1)


def test_scaled_turn_multiplies_base_angle():
    plain = walk("F+F", angle=30, step=1, start_heading=0)
    scaled = walk("F+(3)F", angle=30, step=1, start_heading=0)
    # +(3) should turn 3x as far as a bare '+'
    angle_plain = math.degrees(math.atan2(-(plain[1].y2 - plain[1].y1), plain[1].x2 - plain[1].x1))
    angle_scaled = math.degrees(math.atan2(-(scaled[1].y2 - scaled[1].y1), scaled[1].x2 - scaled[1].x1))
    assert angle_scaled == pytest.approx(angle_plain * 3, abs=1e-6)


def test_brackets_push_and_pop_state_and_depth():
    segments = walk("F[+F]F", angle=90, step=1, start_heading=0)
    trunk_a, branch, trunk_b = segments
    assert trunk_a.depth == 0
    assert branch.depth == 1
    assert trunk_b.depth == 0
    # The second trunk segment continues from where the first left off,
    # not from the branch tip — proving the state was restored on ']'.
    assert trunk_b.x1 == pytest.approx(trunk_a.x2)
    assert trunk_b.y1 == pytest.approx(trunk_a.y2)


def test_unbalanced_closing_bracket_raises():
    with pytest.raises(ValueError):
        walk("F]", angle=90, step=1)


def test_unknown_symbols_are_ignored():
    segments = walk("XFY", angle=90, step=1, start_heading=0)
    assert len(segments) == 1


def test_bounds_of_empty_segments():
    assert bounds([]) == (0.0, 0.0, 0.0, 0.0)


def test_bounds_covers_all_endpoints():
    segs = [Segment(0, 0, 3, 4, 0), Segment(-2, 5, 1, -1, 1)]
    assert bounds(segs) == (-2, -1, 3, 5)
