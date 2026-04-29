"""Tests for mandelbrot module."""

import pytest
from fractalforge import mandelbrot


def test_compute_returns_correct_dimensions():
    grid = mandelbrot.compute(width=20, height=10)
    assert len(grid) == 10
    assert all(len(row) == 20 for row in grid)


def test_in_set_returns_zero():
    # Point (0, 0) is well inside the set
    grid = mandelbrot.compute(width=100, height=100,
                              x_min=-0.01, x_max=0.01,
                              y_min=-0.01, y_max=0.01,
                              max_iter=256)
    assert grid[50][50] == 0.0


def test_outside_set_returns_positive():
    # Point (2.5, 0) is clearly outside
    grid = mandelbrot.compute(width=10, height=10,
                              x_min=2.4, x_max=2.6,
                              y_min=-0.1, y_max=0.1,
                              max_iter=64)
    assert any(grid[row][col] > 0 for row in range(10) for col in range(10))


def test_smooth_values_in_range():
    grid = mandelbrot.compute(width=50, height=30, max_iter=128)
    for row in grid:
        for val in row:
            assert 0.0 <= val <= 1.0, f"Out-of-range value: {val}"


def test_presets_exist():
    for name, preset in mandelbrot.PRESETS.items():
        assert "x_min" in preset
        assert "x_max" in preset
        assert "y_min" in preset
        assert "y_max" in preset
        assert "max_iter" in preset


def test_all_presets_compute():
    for name, preset in mandelbrot.PRESETS.items():
        grid = mandelbrot.compute(width=20, height=10, **preset)
        assert len(grid) == 10, f"Failed for preset '{name}'"
