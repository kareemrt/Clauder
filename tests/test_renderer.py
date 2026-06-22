from pytracer.presets import showcase
from pytracer.renderer import render, trace
from pytracer.ray import Ray
from pytracer.vector import Vec3


def test_trace_background_when_nothing_hit():
    camera, scene = showcase(width=8, height=8)
    ray = Ray(Vec3(0, 100, 0), Vec3(0, 1, 0))
    color = trace(ray, scene)
    assert color == scene.background(ray.direction)


def test_render_produces_full_grid_of_pixels():
    camera, scene = showcase(width=8, height=6)
    rows = render(camera, scene, samples=1, max_depth=1, workers=1)
    assert set(rows.keys()) == set(range(6))
    for pixels in rows.values():
        assert len(pixels) == 8
        for r, g, b in pixels:
            assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255


def test_render_has_visual_variety_not_a_flat_color():
    camera, scene = showcase(width=16, height=12)
    rows = render(camera, scene, samples=1, max_depth=2, workers=1)
    all_pixels = {pixel for row in rows.values() for pixel in row}
    assert len(all_pixels) > 1
