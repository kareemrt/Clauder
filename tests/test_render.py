import numpy as np

from fractalforge.escape_time import mandelbrot
from fractalforge.ifs import koch_snowflake_points, sierpinski_points
from fractalforge.render import render_escape_grid, render_point_cloud, render_polyline


def test_render_escape_grid_size_and_mode():
    grid = mandelbrot(20, 15, max_iter=30)
    img = render_escape_grid(grid, "fire")
    assert img.size == (20, 15)
    assert img.mode == "RGB"


def test_render_point_cloud_size_and_mode():
    points = sierpinski_points(num_points=500, seed=3)
    img = render_point_cloud(points, 30, 25, "electric")
    assert img.size == (30, 25)
    assert img.mode == "RGB"


def test_render_polyline_size_and_mode():
    points = koch_snowflake_points(order=2)
    img = render_polyline(points, 40, 40)
    assert img.size == (40, 40)
    assert img.mode == "RGB"


def test_render_escape_grid_inside_color():
    grid = np.array([[1.0, 0.0]])
    img = render_escape_grid(grid, "fire", inside_color=(9, 9, 9))
    pixels = np.array(img)
    assert tuple(pixels[0, 0]) == (9, 9, 9)
