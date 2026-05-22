"""Tests for the fractal computation engine."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fractalforge.core import (
    compute_mandelbrot,
    compute_julia,
    compute_burning_ship,
    compute_tricorn,
    zoom_region,
)


class TestMandelbrot:
    def test_output_shape(self):
        result = compute_mandelbrot(80, 40)
        assert result.shape == (40, 80)

    def test_interior_points_reach_max_iter(self):
        # The origin (0+0j) is well inside the Mandelbrot set
        result = compute_mandelbrot(11, 11, x_min=-0.1, x_max=0.1, y_min=-0.1, y_max=0.1, max_iter=100)
        center = result[5, 5]
        assert center == 100, f"Expected 100, got {center}"

    def test_exterior_points_escape(self):
        # Far-right region is entirely outside the set
        result = compute_mandelbrot(10, 10, x_min=3.0, x_max=5.0, y_min=-1.0, y_max=1.0, max_iter=100)
        assert np.all(result < 100)

    def test_smooth_coloring_fractional(self):
        # Smooth coloring should produce non-integer values for escaping points
        result = compute_mandelbrot(100, 50, max_iter=256)
        escaping = result[result < 256]
        if len(escaping) > 0:
            fractional = escaping % 1
            assert np.any(fractional > 0), "Smooth coloring should yield fractional values"


class TestJulia:
    def test_output_shape(self):
        result = compute_julia(60, 60)
        assert result.shape == (60, 60)

    def test_different_params_give_different_results(self):
        r1 = compute_julia(50, 50, c=-0.7269 + 0.1889j, max_iter=100)
        r2 = compute_julia(50, 50, c=0.285 + 0.01j, max_iter=100)
        assert not np.array_equal(r1, r2)

    def test_symmetric_about_origin(self):
        # Julia sets are symmetric under 180-degree rotation for z² + c
        result = compute_julia(101, 101, c=-0.4 + 0.6j, max_iter=150)
        # Compare (row, col) with (H-1-row, W-1-col) — should be approximately equal
        flipped = np.rot90(result, 2)
        np.testing.assert_allclose(result, flipped, atol=1.0)


class TestBurningShip:
    def test_output_shape(self):
        result = compute_burning_ship(80, 60)
        assert result.shape == (60, 80)

    def test_has_interior_and_exterior(self):
        result = compute_burning_ship(100, 80, max_iter=128)
        assert np.any(result == 128), "Should have interior points"
        assert np.any(result < 128), "Should have escaping points"


class TestTricorn:
    def test_output_shape(self):
        result = compute_tricorn(80, 60)
        assert result.shape == (60, 80)

    def test_has_interior_and_exterior(self):
        result = compute_tricorn(100, 80, max_iter=128)
        assert np.any(result == 128)
        assert np.any(result < 128)


class TestZoomRegion:
    def test_zoom_1_gives_reasonable_bounds(self):
        x_min, x_max, y_min, y_max = zoom_region(0.0, 0.0, 1.0)
        assert x_min < 0 < x_max
        assert y_min < 0 < y_max

    def test_higher_zoom_gives_smaller_region(self):
        b1 = zoom_region(0.0, 0.0, 1.0)
        b2 = zoom_region(0.0, 0.0, 10.0)
        width1 = b1[1] - b1[0]
        width2 = b2[1] - b2[0]
        assert width2 < width1

    def test_center_is_preserved(self):
        cx, cy = -0.5, 0.3
        x_min, x_max, y_min, y_max = zoom_region(cx, cy, 5.0)
        assert abs((x_min + x_max) / 2 - cx) < 1e-9
        assert abs((y_min + y_max) / 2 - cy) < 1e-9
