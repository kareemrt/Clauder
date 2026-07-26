"""Tests for the fractal computation modules."""

import pytest
from fractal_explorer.mandelbrot import compute_mandelbrot, _escape_count as mb_escape
from fractal_explorer.julia import compute_julia, _escape_count as jl_escape
from fractal_explorer.sierpinski import compute_sierpinski, compute_dragon_curve, render_dragon_to_grid
from fractal_explorer.renderer import render_grid, render_sierpinski, PALETTES, COLOR_SCHEMES


# ── Mandelbrot ────────────────────────────────────────────────────────────────

class TestMandelbrot:
    def test_returns_correct_shape(self):
        grid = compute_mandelbrot(10, 5)
        assert len(grid) == 5
        assert all(len(row) == 10 for row in grid)

    def test_origin_inside_set(self):
        """z=0 with c=0 never escapes — iteration count should be 0."""
        count = mb_escape(0.0, 0.0, max_iter=100)
        assert count == 0

    def test_far_point_escapes_quickly(self):
        """c=10 is far outside the set and should escape at iteration 1."""
        count = mb_escape(10.0, 0.0, max_iter=100)
        assert count == 1

    def test_iteration_counts_in_range(self):
        grid = compute_mandelbrot(20, 10, max_iter=50)
        for row in grid:
            for val in row:
                assert 0 <= val <= 50

    def test_negative_two_inside_set(self):
        """The point c=-2 is on the boundary but considered inside."""
        count = mb_escape(-2.0, 0.0, max_iter=200)
        assert count == 0


# ── Julia ─────────────────────────────────────────────────────────────────────

class TestJulia:
    def test_returns_correct_shape(self):
        grid = compute_julia(8, 6)
        assert len(grid) == 6
        assert all(len(row) == 8 for row in grid)

    def test_c_zero_origin_inside(self):
        """z=0 with c=0 stays at 0 forever — must be inside (count=0)."""
        count = jl_escape(0.0, 0.0, cx=0.0, cy=0.0, max_iter=100)
        assert count == 0

    def test_far_z_escapes(self):
        """z=10 escapes immediately for any reasonable c."""
        count = jl_escape(10.0, 0.0, cx=-0.7, cy=0.27015, max_iter=100)
        assert count == 1

    def test_all_values_bounded(self):
        grid = compute_julia(15, 8, max_iter=60)
        for row in grid:
            for val in row:
                assert 0 <= val <= 60


# ── Sierpinski ────────────────────────────────────────────────────────────────

class TestSierpinski:
    def test_size(self):
        rows = compute_sierpinski(16)
        assert len(rows) == 16
        assert all(len(r) == 16 for r in rows)

    def test_top_left_always_filled(self):
        """(0,0) should always be filled since 0 & 0 == 0."""
        rows = compute_sierpinski(8)
        assert rows[0][0] == "█"

    def test_contains_spaces(self):
        rows = compute_sierpinski(8)
        all_chars = "".join(rows)
        assert " " in all_chars


# ── Dragon curve ──────────────────────────────────────────────────────────────

class TestDragonCurve:
    def test_produces_points(self):
        pts = compute_dragon_curve(4)
        assert len(pts) > 0

    def test_point_count_grows_with_iterations(self):
        pts_4 = compute_dragon_curve(4)
        pts_8 = compute_dragon_curve(8)
        assert len(pts_8) > len(pts_4)

    def test_grid_shape(self):
        pts = compute_dragon_curve(6)
        grid = render_dragon_to_grid(pts, width=20, height=10)
        assert len(grid) == 10
        assert all(len(row) == 20 for row in grid)

    def test_grid_has_true_values(self):
        pts = compute_dragon_curve(6)
        grid = render_dragon_to_grid(pts, width=20, height=10)
        flat = [cell for row in grid for cell in row]
        assert any(flat)


# ── Renderer ──────────────────────────────────────────────────────────────────

class TestRenderer:
    def test_render_grid_returns_text(self):
        from rich.text import Text
        grid = compute_mandelbrot(5, 3, max_iter=10)
        t = render_grid(grid, max_iter=10)
        assert isinstance(t, Text)

    def test_all_palettes_work(self):
        grid = compute_mandelbrot(5, 3, max_iter=10)
        for palette in PALETTES:
            t = render_grid(grid, 10, palette_name=palette)
            assert len(str(t)) > 0

    def test_all_color_schemes_work(self):
        grid = compute_mandelbrot(5, 3, max_iter=10)
        for scheme in COLOR_SCHEMES:
            t = render_grid(grid, 10, color_scheme=scheme)
            assert len(str(t)) > 0

    def test_sierpinski_render(self):
        from rich.text import Text
        rows = compute_sierpinski(8)
        t = render_sierpinski(rows)
        assert isinstance(t, Text)
