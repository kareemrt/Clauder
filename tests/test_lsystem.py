import unittest

from fractalis.lsystem import PRESETS, expand, rasterize, render_lsystem, turtle_segments


class LSystemTest(unittest.TestCase):
    def test_expand_applies_rules_iteratively(self):
        result = expand("F", {"F": "F+F"}, iterations=2)
        # iter 0: F  |  iter 1: F+F  |  iter 2: F+F+F+F
        self.assertEqual(result, "F+F+F+F")

    def test_expand_zero_iterations_is_identity(self):
        self.assertEqual(expand("ABC", {"A": "X"}, iterations=0), "ABC")

    def test_turtle_draws_unit_square_with_right_angles(self):
        segments = turtle_segments("F+F+F+F", angle=90, step=1.0, heading=0)
        self.assertEqual(len(segments), 4)
        # A closed unit square returns to (0, 0).
        self.assertAlmostEqual(segments[-1][2], 0.0, places=9)
        self.assertAlmostEqual(segments[-1][3], 0.0, places=9)

    def test_brackets_save_and_restore_turtle_state(self):
        segments = turtle_segments("F[+F]F", angle=90, step=1.0, heading=0)
        # Two forward moves along the main stem are colinear on the x-axis,
        # regardless of the branched segment drawn in between.
        self.assertEqual(len(segments), 3)
        main_stem_end = segments[2]
        self.assertAlmostEqual(main_stem_end[3], 0.0, places=9)

    def test_every_preset_expands_and_rasterizes(self):
        for name, spec in PRESETS.items():
            with self.subTest(preset=name):
                instructions = expand(spec["axiom"], spec["rules"], iterations=2)
                segments = turtle_segments(instructions, spec["angle"],
                                            heading=spec["heading"])
                self.assertGreater(len(segments), 0)
                pixels = rasterize(segments, width=20, height=20)
                self.assertEqual(len(pixels), 20 * 20 * 3)

    def test_render_lsystem_unknown_preset_raises(self):
        with self.assertRaises(KeyError):
            render_lsystem("not-a-real-preset")


if __name__ == "__main__":
    unittest.main()
