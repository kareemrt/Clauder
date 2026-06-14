import pytest

from fractal_garden import garden, palette, svgrender


def test_render_svg_contains_one_line_per_segment():
    segments = garden.grow("koch", seed=0)
    svg = svgrender.render_svg(segments, palette=palette.resolve("spring"))
    assert svg.startswith("<svg")
    assert svg.count("<line") == len(segments)


def test_render_svg_rejects_empty_segments():
    with pytest.raises(ValueError):
        svgrender.render_svg([], palette=palette.resolve("spring"))


def test_render_garden_combines_multiple_plants():
    plants = [
        svgrender.GardenPlant(garden.grow("fern", seed=1), palette.resolve("spring")),
        svgrender.GardenPlant(garden.grow("bush", seed=2), palette.resolve("autumn")),
    ]
    svg = svgrender.render_garden(plants)
    assert svg.startswith("<svg")
    total_segments = sum(len(p.segments) for p in plants)
    assert svg.count("<line") == total_segments


def test_palette_interpolation_endpoints():
    assert palette.interpolate("#000000", "#ffffff", 0.0) == "#000000"
    assert palette.interpolate("#000000", "#ffffff", 1.0) == "#ffffff"
    assert palette.interpolate("#000000", "#ffffff", 0.5) == "#808080"


def test_unknown_palette_raises():
    with pytest.raises(ValueError):
        palette.resolve("not-a-palette")
