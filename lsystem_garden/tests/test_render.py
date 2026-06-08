import pytest

from lsystem_garden.render import gradient, render_svg
from lsystem_garden.turtle import Segment


def test_render_svg_rejects_empty_drawing():
    with pytest.raises(ValueError):
        render_svg([])


def test_render_svg_contains_expected_structure():
    segments = [Segment(0, 0, 10, 0, 0), Segment(10, 0, 10, 10, 1)]
    svg = render_svg(segments, title="Test Drawing")
    assert svg.startswith("<?xml")
    assert "<svg" in svg
    assert "<title>Test Drawing</title>" in svg
    assert svg.count("<line") == 2
    assert svg.strip().endswith("</svg>")


def test_render_svg_viewbox_accounts_for_padding_and_bounds():
    segments = [Segment(0, 0, 100, 50, 0)]
    svg = render_svg(segments, padding=10)
    assert 'viewBox="0 0 120.00 70.00"' in svg


def test_gradient_endpoints_match_palette():
    assert gradient(0, 4, start="#000000", end="#ffffff") == "#000000"
    assert gradient(4, 4, start="#000000", end="#ffffff") == "#ffffff"


def test_gradient_midpoint_is_blended():
    mid = gradient(2, 4, start="#000000", end="#ffffff")
    r, g, b = (int(mid[i : i + 2], 16) for i in (1, 3, 5))
    assert 100 < r < 156 and r == g == b


def test_gradient_handles_zero_max_depth():
    assert gradient(0, 0, start="#123456", end="#abcdef") == "#123456"


def test_taper_shrinks_stroke_width_with_depth():
    segments = [Segment(0, 0, 1, 0, 0), Segment(1, 0, 2, 0, 5)]
    svg = render_svg(segments, taper=True, stroke_width=2.0)
    widths = [line for line in svg.splitlines() if "<line" in line]
    assert 'stroke-width="2.00"' in widths[0]
    assert 'stroke-width="2.00"' not in widths[1]
