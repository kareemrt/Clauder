import numpy as np

from fracta.escape_fractals import render_julia, render_mandelbrot


def test_mandelbrot_shape_and_dtype():
    img = render_mandelbrot(width=40, height=30, max_iter=50)
    assert img.shape == (30, 40, 3)
    assert img.dtype == np.uint8


def test_mandelbrot_origin_is_inside_set():
    # The point c=0 never escapes, so a tight render centered there should
    # be dominated by the "inside" color (palette value at 0.0).
    img = render_mandelbrot(width=5, height=5, center=(0.0, 0.0), scale=0.001, max_iter=100)
    # All pixels should be identical since the region is entirely inside.
    assert np.all(img == img[0, 0])


def test_julia_shape_and_dtype():
    img = render_julia(width=32, height=24, max_iter=40)
    assert img.shape == (24, 32, 3)
    assert img.dtype == np.uint8
