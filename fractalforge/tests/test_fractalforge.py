import os
import struct
import tempfile
import unittest
import zlib

from fractalforge import palettes
from fractalforge.fractals import Viewport, escape_value
from fractalforge.png import write_png
from fractalforge.render import render_grid


class ViewportTests(unittest.TestCase):
    def test_centre_pixel_maps_to_centre_point(self):
        vp = Viewport(width=100, height=100, center=complex(-0.5, 0.25), scale=1.0)
        # Pixel (50, 50) sits exactly on the viewport's centre.
        point = vp.to_complex(50, 50)
        self.assertAlmostEqual(point.real, -0.5)
        self.assertAlmostEqual(point.imag, 0.25)

    def test_wider_aspect_stretches_real_axis(self):
        vp = Viewport(width=200, height=100, center=0j, scale=1.0)
        left = vp.to_complex(0, 50)
        right = vp.to_complex(200, 50)
        # width/height = 2, so the real span should be twice the imaginary span.
        self.assertAlmostEqual(right.real - left.real, 4.0)


class EscapeValueTests(unittest.TestCase):
    def test_origin_is_inside_mandelbrot(self):
        self.assertIsNone(escape_value("mandelbrot", 0j, 100))

    def test_far_point_escapes_immediately(self):
        value = escape_value("mandelbrot", complex(10, 10), 100)
        self.assertIsNotNone(value)
        self.assertLess(value, 2.0)

    def test_julia_requires_constant(self):
        with self.assertRaises(ValueError):
            escape_value("julia", 0j, 50)

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            escape_value("sierpinski", 0j, 50)

    def test_all_known_families_compute(self):
        for family in ("mandelbrot", "burningship", "tricorn"):
            self.assertIsNone(escape_value(family, 0j, 50))
        julia = escape_value("julia", complex(2, 2), 50, julia_c=complex(-0.7, 0.27015))
        self.assertIsInstance(julia, float)


class PaletteTests(unittest.TestCase):
    def test_endpoints_match_stops(self):
        first_stop_colour = palettes.PALETTES["inferno"][0][1]
        last_stop_colour = palettes.PALETTES["inferno"][-1][1]
        self.assertEqual(palettes.colour_at("inferno", 0.0), first_stop_colour)
        self.assertEqual(palettes.colour_at("inferno", 1.0), last_stop_colour)

    def test_interpolation_is_between_neighbours(self):
        colour = palettes.colour_at("ocean", 0.15)
        c0 = palettes.PALETTES["ocean"][0][1]
        c1 = palettes.PALETTES["ocean"][1][1]
        for channel in range(3):
            lo, hi = sorted((c0[channel], c1[channel]))
            self.assertLessEqual(lo, colour[channel])
            self.assertLessEqual(colour[channel], hi)

    def test_unknown_palette_raises(self):
        with self.assertRaises(KeyError):
            palettes.colour_at("nonexistent", 0.5)


class RenderGridTests(unittest.TestCase):
    def test_grid_dimensions_match_viewport(self):
        vp = Viewport(width=12, height=8, center=complex(-0.5, 0), scale=1.5)
        grid = render_grid("mandelbrot", vp, max_iter=25, palette="inferno")
        self.assertEqual(len(grid), 8)
        self.assertTrue(all(len(row) == 12 for row in grid))

    def test_inside_point_uses_inside_colour(self):
        vp = Viewport(width=4, height=4, center=0j, scale=0.01)
        grid = render_grid("mandelbrot", vp, max_iter=64, palette="inferno")
        # At this tight zoom around the origin, every sample is inside the set.
        self.assertTrue(all(px == palettes.INSIDE_COLOUR for row in grid for px in row))

    def test_rejects_unknown_fractal(self):
        vp = Viewport(width=2, height=2, center=0j, scale=1.0)
        with self.assertRaises(ValueError):
            render_grid("not-a-fractal", vp, max_iter=10, palette="inferno")

    def test_rejects_unknown_palette(self):
        vp = Viewport(width=2, height=2, center=0j, scale=1.0)
        with self.assertRaises(ValueError):
            render_grid("mandelbrot", vp, max_iter=10, palette="not-a-palette")


class PngWriterTests(unittest.TestCase):
    def test_written_file_round_trips_through_zlib(self):
        pixels = [
            [(255, 0, 0), (0, 255, 0)],
            [(0, 0, 255), (255, 255, 255)],
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.png")
            write_png(path, pixels)

            with open(path, "rb") as fh:
                data = fh.read()

            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")

            # Walk the chunks: IHDR must report the right geometry, and the
            # IDAT payload must inflate back to filter-byte-prefixed rows.
            offset = 8
            chunks = {}
            while offset < len(data):
                (length,) = struct.unpack(">I", data[offset : offset + 4])
                tag = data[offset + 4 : offset + 8]
                body = data[offset + 8 : offset + 8 + length]
                chunks[tag] = body
                offset += 12 + length

            width, height, depth, colour_type = struct.unpack(">IIBB", chunks[b"IHDR"][:10])
            self.assertEqual((width, height, depth, colour_type), (2, 2, 8, 2))

            raw = zlib.decompress(chunks[b"IDAT"])
            expected_row_len = 1 + width * 3
            self.assertEqual(len(raw), expected_row_len * height)
            self.assertEqual(raw[0], 0)  # filter byte for row 0
            self.assertEqual(raw[1:4], bytes((255, 0, 0)))


if __name__ == "__main__":
    unittest.main()
