import math

import pytest

from fractal_garden.lsystem import LSystem, bounding_box, interpret


def test_expand_algae():
    # Lindenmayer's classic algae system: A -> AB, B -> A
    lsystem = LSystem(
        name="algae",
        description="",
        axiom="A",
        rules={"A": "AB", "B": "A"},
        angle=0,
    )
    assert lsystem.expand(0) == "A"
    assert lsystem.expand(1) == "AB"
    assert lsystem.expand(2) == "ABA"
    assert lsystem.expand(3) == "ABAAB"
    assert lsystem.expand(4) == "ABAABABA"


def test_expand_rejects_negative_iterations():
    lsystem = LSystem(name="x", description="", axiom="A", rules={}, angle=0)
    with pytest.raises(ValueError):
        lsystem.expand(-1)


def test_interpret_draws_unit_square():
    # F+F+F+F+ with a 90 degree turn traces a closed unit square.
    lsystem = LSystem(
        name="square",
        description="",
        axiom="F+F+F+F+",
        rules={},
        angle=90,
        start_heading=0,
    )
    segments = interpret(lsystem.expand(0), lsystem, step=1.0)

    assert len(segments) == 4
    # Each segment should have unit length.
    for seg in segments:
        length = math.hypot(seg.x2 - seg.x1, seg.y2 - seg.y1)
        assert length == pytest.approx(1.0)

    # The path should return to its starting point.
    assert (segments[-1].x2, segments[-1].y2) == pytest.approx((segments[0].x1, segments[0].y1))


def test_interpret_branching_with_stack():
    # F[+F]F branches off a single segment and rejoins the main stem.
    lsystem = LSystem(
        name="branch",
        description="",
        axiom="F[+F]F",
        rules={},
        angle=90,
        start_heading=90,
    )
    segments = interpret(lsystem.expand(0), lsystem, step=1.0)

    assert len(segments) == 3
    assert segments[0].depth == 0
    assert segments[1].depth == 1  # the branch inside [ ]
    assert segments[2].depth == 0  # back on the main stem after ]

    # The branch starts where the first segment ended.
    assert (segments[1].x1, segments[1].y1) == pytest.approx((segments[0].x2, segments[0].y2))
    # The final stem segment continues from the end of the first segment too.
    assert (segments[2].x1, segments[2].y1) == pytest.approx((segments[0].x2, segments[0].y2))


def test_interpret_non_drawing_move_and_about_face():
    lsystem = LSystem(
        name="move",
        description="",
        axiom="f|F",
        rules={},
        angle=0,
        start_heading=0,
    )
    segments = interpret(lsystem.expand(0), lsystem, step=2.0)

    assert len(segments) == 1
    seg = segments[0]
    # 'f' moves 2 units forward without drawing, '|' turns around 180 degrees,
    # then 'F' draws back toward the origin.
    assert (seg.x1, seg.y1) == pytest.approx((2.0, 0.0))
    assert (seg.x2, seg.y2) == pytest.approx((0.0, 0.0))


def test_bounding_box_empty_and_nonempty():
    assert bounding_box([]) == (0.0, 0.0, 0.0, 0.0)

    lsystem = LSystem(name="line", description="", axiom="FF", rules={}, angle=0, start_heading=0)
    segments = interpret(lsystem.expand(0), lsystem, step=1.0)
    assert bounding_box(segments) == (0.0, 0.0, 2.0, 0.0)
