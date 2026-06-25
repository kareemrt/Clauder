import unittest

from fractalis import colormaps


class ColormapsTest(unittest.TestCase):
    def test_all_cmaps_return_valid_rgb_across_range(self):
        for name, fn in colormaps.CMAPS.items():
            for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                with self.subTest(cmap=name, t=t):
                    r, g, b = fn(t)
                    for channel in (r, g, b):
                        self.assertIsInstance(channel, int)
                        self.assertGreaterEqual(channel, 0)
                        self.assertLessEqual(channel, 255)

    def test_gradient_clamps_out_of_range_input(self):
        self.assertEqual(colormaps.grayscale(-5.0), colormaps.grayscale(0.0))
        self.assertEqual(colormaps.grayscale(5.0), colormaps.grayscale(1.0))

    def test_get_unknown_cmap_raises(self):
        with self.assertRaises(ValueError):
            colormaps.get("does-not-exist")

    def test_get_returns_callable_for_known_name(self):
        fn = colormaps.get("fire")
        self.assertEqual(fn, colormaps.fire)


if __name__ == "__main__":
    unittest.main()
