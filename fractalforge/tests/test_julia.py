"""Tests for julia module."""

import pytest
from fractalforge import julia


def test_compute_returns_correct_dimensions():
    grid = julia.compute(width=20, height=10)
    assert len(grid) == 10
    assert all(len(row) == 20 for row in grid)


def test_smooth_values_in_range():
    grid = julia.compute(width=50, height=30, max_iter=128)
    for row in grid:
        for val in row:
            assert 0.0 <= val <= 1.0, f"Out-of-range value: {val}"


def test_all_presets_compute():
    for name, preset in julia.PRESETS.items():
        grid = julia.compute(width=20, height=10, **preset, max_iter=64)
        assert len(grid) == 10, f"Failed for preset '{name}'"


def test_dendrite_has_in_set_points():
    # c=(0,1) creates a dendrite with interior points
    grid = julia.compute(width=40, height=30, cx=0.0, cy=1.0, max_iter=256)
    in_set = sum(1 for row in grid for v in row if v == 0.0)
    assert in_set > 0


def test_different_c_values_differ():
    g1 = julia.compute(width=30, height=20, cx=-0.7, cy=0.27, max_iter=64)
    g2 = julia.compute(width=30, height=20, cx=0.285, cy=0.01, max_iter=64)
    assert g1 != g2
