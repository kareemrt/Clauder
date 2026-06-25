import unittest

from fractalis.mandelbrot import render_mandelbrot
from fractalis.julia import render_julia
from fractalis.burning_ship import render_burning_ship


class EscapeTimeTest(unittest.TestCase):
    def test_mandelbrot_origin_is_in_set(self):
        # c = 0 never escapes, so the center pixel of a symmetric view
        # around the origin should be colored black (in-set).
        pixels = render_mandelbrot(width=3, height=3,
                                    bounds=(-1, 1, -1, 1), max_iter=50)
        center_offset = (1 * 3 + 1) * 3
        self.assertEqual(tuple(pixels[center_offset:center_offset + 3]), (0, 0, 0))

    def test_mandelbrot_far_point_escapes_quickly(self):
        # c = 10 escapes on the very first iteration, so it should not be
        # colored black like an in-set point.
        pixels = render_mandelbrot(width=1, height=1, bounds=(10, 10, 0, 0),
                                    max_iter=50)
        self.assertNotEqual(tuple(pixels[0:3]), (0, 0, 0))

    def test_output_buffer_size_matches_dimensions(self):
        for renderer in (render_mandelbrot, render_julia, render_burning_ship):
            with self.subTest(renderer=renderer.__name__):
                pixels = renderer(width=10, height=7, max_iter=20)
                self.assertEqual(len(pixels), 10 * 7 * 3)


if __name__ == "__main__":
    unittest.main()
