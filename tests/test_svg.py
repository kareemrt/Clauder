import pytest

from lsystems.svg import segments_to_svg
from lsystems.turtle import Segment


def test_empty_segments_raises():
    with pytest.raises(ValueError):
        segments_to_svg([])


def test_output_is_well_formed_svg_with_expected_line_count():
    segments = [Segment(0, 0, 1, 0), Segment(1, 0, 1, 1)]
    svg = segments_to_svg(segments, width=100)
    assert svg.startswith("<svg")
    assert svg.count("<line") == 2
    assert "</svg>" in svg


def test_width_is_respected():
    segments = [Segment(0, 0, 10, 0)]
    svg = segments_to_svg(segments, width=200)
    assert 'width="200"' in svg


def test_single_point_segment_does_not_crash():
    # Degenerate input: a single zero-length segment must not divide by zero.
    segments = [Segment(0, 0, 0, 0)]
    svg = segments_to_svg(segments, width=100)
    assert "<svg" in svg
