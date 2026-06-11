import numpy as np

from fractalforge.escape_time import burning_ship, julia, mandelbrot


def test_mandelbrot_shape_and_range():
    grid = mandelbrot(40, 30, max_iter=50)
    assert grid.shape == (30, 40)
    assert grid.min() >= 0.0
    assert grid.max() <= 1.0


def test_mandelbrot_origin_is_inside_set():
    # The origin (0, 0) belongs to the Mandelbrot set, so z stays bounded
    # and the point should be classified as "inside" (value == 1.0).
    grid = mandelbrot(3, 3, max_iter=100, center=(0.0, 0.0), zoom=1e6)
    assert grid[1, 1] == 1.0


def test_mandelbrot_far_point_escapes_immediately():
    # A point far outside the set escapes on the very first iteration.
    grid = mandelbrot(3, 3, max_iter=100, center=(100.0, 100.0), zoom=1e6)
    assert grid[1, 1] < 1.0


def test_julia_shape_and_range():
    grid = julia(40, 30, complex(-0.7, 0.27015), max_iter=50)
    assert grid.shape == (30, 40)
    assert grid.min() >= 0.0
    assert grid.max() <= 1.0


def test_burning_ship_shape_and_range():
    grid = burning_ship(40, 30, max_iter=50)
    assert grid.shape == (30, 40)
    assert grid.min() >= 0.0
    assert grid.max() <= 1.0


def test_deep_zoom_inside_bulb_is_uniform():
    # At extreme zoom centered on the period-2 bulb (c = -1), the whole
    # viewport lies inside the set.
    grid = mandelbrot(40, 30, max_iter=50, center=(-1.0, 0.0), zoom=1e8)
    assert np.all(grid == 1.0)
