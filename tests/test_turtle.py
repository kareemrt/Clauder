import math

import pytest

from lsystems.turtle import Segment, TurtleInterpreter


def test_forward_draws_one_segment_along_heading():
    turtle = TurtleInterpreter(angle=90, step=2.0, start_heading=0)
    segments = turtle.interpret("F")
    assert segments == [Segment(0.0, 0.0, 2.0, 0.0)]


def test_move_without_draw_produces_no_segment():
    turtle = TurtleInterpreter(angle=90, step=1.0, start_heading=0)
    segments = turtle.interpret("f")
    assert segments == []


def test_turning_changes_heading_of_next_segment():
    turtle = TurtleInterpreter(angle=90, step=1.0, start_heading=0)
    segments = turtle.interpret("F+F")
    assert segments[0] == Segment(0.0, 0.0, 1.0, 0.0)
    second = segments[1]
    assert second.x1 == pytest.approx(1.0)
    assert second.y1 == pytest.approx(0.0)
    assert second.x2 == pytest.approx(1.0)
    assert second.y2 == pytest.approx(1.0)


def test_right_turn_is_opposite_of_left_turn():
    left = TurtleInterpreter(angle=45, step=1.0, start_heading=0).interpret("F+F")
    right = TurtleInterpreter(angle=45, step=1.0, start_heading=0).interpret("F-F")
    assert left[1].y2 > left[1].y1
    assert right[1].y2 < right[1].y1


def test_push_and_pop_restore_state():
    turtle = TurtleInterpreter(angle=90, step=1.0, start_heading=0)
    segments = turtle.interpret("F[+F]F")
    assert segments[0] == Segment(0.0, 0.0, 1.0, 0.0)
    # branch goes up from (1, 0)
    assert segments[1].x1 == pytest.approx(1.0)
    assert segments[1].y1 == pytest.approx(0.0)
    # after popping, the trunk continues straight from (1, 0) along heading 0
    assert segments[2] == Segment(1.0, 0.0, 2.0, 0.0)


def test_unbalanced_pop_raises():
    turtle = TurtleInterpreter(angle=90, step=1.0)
    with pytest.raises(ValueError):
        turtle.interpret("]")


def test_unbalanced_push_raises():
    turtle = TurtleInterpreter(angle=90, step=1.0)
    with pytest.raises(ValueError):
        turtle.interpret("[F")


def test_koch_curve_single_iteration_geometry():
    # F -> F+F--F+F at 60 degrees is one iteration of a Koch curve segment.
    turtle = TurtleInterpreter(angle=60, step=1.0, start_heading=0)
    segments = turtle.interpret("F+F--F+F")
    assert len(segments) == 4
    # The path should return close to the same horizontal span as a straight
    # line of length 4, net horizontal displacement should equal 4 units.
    total_dx = sum(s.x2 - s.x1 for s in segments)
    assert total_dx == pytest.approx(3.0)
