import xml.etree.ElementTree as ET

import pytest

from lsystemgarden.render_svg import render
from lsystemgarden.turtle import interpret


def _make_segments():
    return interpret("F[+F]F[-F]F", angle=25, step=10.0, start_heading=90.0)


def test_render_produces_well_formed_xml():
    svg = render(_make_segments())
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg")


def test_render_includes_one_line_per_segment():
    segments = _make_segments()
    svg = render(segments)
    assert svg.count("<line") == len(segments)


def test_render_respects_canvas_dimensions():
    svg = render(_make_segments(), width=321, height=654)
    assert 'width="321"' in svg
    assert 'height="654"' in svg


def test_render_uses_background_color():
    svg = render(_make_segments(), background="#abcdef")
    assert "#abcdef" in svg


def test_render_rejects_empty_segments():
    with pytest.raises(ValueError):
        render([])


def test_render_gradient_endpoints_present_for_multi_depth_shape():
    segments = _make_segments()
    svg = render(segments, start_color="#ff0000", end_color="#0000ff")
    # depth-0 segments should be tinted exactly start_color
    assert "#ff0000" in svg.lower() or "#ff0000" in svg
