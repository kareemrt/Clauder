"""Tests for colormap and palette functionality."""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fractalforge.colormap import (
    apply_colormap,
    PALETTES,
    _interpolate_palette,
    iteration_to_ascii,
    ASCII_GRADIENT,
)


class TestPalettes:
    def test_all_palettes_present(self):
        expected = {"inferno", "ocean", "fire", "psychedelic", "grayscale", "copper"}
        assert expected.issubset(set(PALETTES.keys()))

    def test_interpolate_returns_256_colors(self):
        lut = _interpolate_palette(PALETTES["inferno"])
        assert lut.shape == (256, 3)
        assert lut.dtype == np.uint8

    def test_interpolate_all_values_in_range(self):
        for name, palette in PALETTES.items():
            lut = _interpolate_palette(palette)
            assert np.all(lut >= 0) and np.all(lut <= 255), f"Palette {name} out of range"


class TestApplyColormap:
    def test_output_shape_matches_input(self):
        counts = np.zeros((40, 80))
        rgb = apply_colormap(counts, max_iter=256)
        assert rgb.shape == (40, 80, 3)

    def test_interior_is_black(self):
        counts = np.full((10, 10), 256, dtype=float)
        rgb = apply_colormap(counts, max_iter=256)
        assert np.all(rgb == 0), "Interior points (max_iter) should be black"

    def test_escaping_points_get_color(self):
        counts = np.full((10, 10), 10.5)
        rgb = apply_colormap(counts, max_iter=256)
        assert np.any(rgb > 0), "Escaping points should have non-zero color"

    def test_all_palettes_run_without_error(self):
        counts = np.linspace(0, 256, 100).reshape(10, 10)
        for palette in PALETTES:
            rgb = apply_colormap(counts, max_iter=256, palette_name=palette)
            assert rgb.shape == (10, 10, 3)


class TestAsciiGradient:
    def test_max_iter_gives_space(self):
        assert iteration_to_ascii(256, 256) == " "

    def test_low_value_gives_darker_char(self):
        ch = iteration_to_ascii(1, 256)
        assert ch in ASCII_GRADIENT

    def test_gradient_covers_full_range(self):
        chars = set()
        for i in range(0, 256, 5):
            chars.add(iteration_to_ascii(i, 256))
        assert len(chars) > 3, "Gradient should span multiple characters"
