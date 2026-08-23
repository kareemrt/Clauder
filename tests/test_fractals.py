"""Tests for fractal computation correctness."""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from spectra.fractals import mandelbrot, julia, burning_ship, newton


def test_mandelbrot_shape():
    result = mandelbrot(100, 80, -2.5, 1.0, -1.25, 1.25, 64)
    assert result.shape == (80, 100)


def test_mandelbrot_origin_escapes():
    # z=0, c=2 should escape immediately → low iteration count
    result = mandelbrot(10, 10, 1.9, 2.1, -0.1, 0.1, 256)
    assert np.any(result > 0), "Points far outside should escape"


def test_mandelbrot_interior():
    # z=0, c=0 is in the Mandelbrot set (never escapes)
    result = mandelbrot(11, 11, -0.1, 0.1, -0.1, 0.1, 256)
    center = result[5, 5]
    assert center == 0.0, "Origin should be in the Mandelbrot set (never escape)"


def test_julia_shape():
    result = julia(120, 90, -2, 2, -2, 2, 64, c=-0.4 + 0.6j)
    assert result.shape == (90, 120)


def test_burning_ship_shape():
    result = burning_ship(100, 80, -2.5, 1.5, -2.0, 0.5, 64)
    assert result.shape == (80, 100)


def test_burning_ship_has_escapes():
    result = burning_ship(50, 50, -2.5, 1.5, -2.0, 0.5, 64)
    assert np.any(result > 0)


def test_newton_shape():
    root_map, speed_map = newton(60, 60, -2, 2, -2, 2, 64)
    assert root_map.shape == (60, 60)
    assert speed_map.shape == (60, 60)


def test_newton_three_roots():
    root_map, _ = newton(200, 200, -2, 2, -2, 2, 128)
    roots_found = set(root_map.flatten()) - {-1}
    assert len(roots_found) == 3, f"Expected 3 roots, found: {roots_found}"


def test_palette_output_shape():
    from spectra.palettes import apply_palette
    data = mandelbrot(50, 40, -2.5, 1.0, -1.25, 1.25, 64)
    rgb = apply_palette(data, palette_name="ocean", max_iter=64)
    assert rgb.shape == (40, 50, 3)
    assert rgb.dtype == np.uint8


def test_all_palettes_work():
    from spectra.palettes import apply_palette, list_palettes
    data = mandelbrot(20, 20, -2.5, 1.0, -1.25, 1.25, 32)
    for palette in list_palettes():
        rgb = apply_palette(data, palette_name=palette, max_iter=32)
        assert rgb.shape == (20, 20, 3), f"Palette {palette} failed"


if __name__ == "__main__":
    tests = [
        test_mandelbrot_shape,
        test_mandelbrot_origin_escapes,
        test_mandelbrot_interior,
        test_julia_shape,
        test_burning_ship_shape,
        test_burning_ship_has_escapes,
        test_newton_shape,
        test_newton_three_roots,
        test_palette_output_shape,
        test_all_palettes_work,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
