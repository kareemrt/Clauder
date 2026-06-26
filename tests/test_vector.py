import math
import unittest

from murmuration.vector import Vector2, distance, toroidal_delta


class TestVector2(unittest.TestCase):
    def test_add_sub(self):
        a, b = Vector2(1, 2), Vector2(3, 4)
        self.assertEqual(a + b, Vector2(4, 6))
        self.assertEqual(b - a, Vector2(2, 2))

    def test_scalar_mul_div(self):
        a = Vector2(2, 4)
        self.assertEqual(a * 2, Vector2(4, 8))
        self.assertEqual(2 * a, Vector2(4, 8))
        self.assertEqual(a / 2, Vector2(1, 2))

    def test_length(self):
        self.assertAlmostEqual(Vector2(3, 4).length(), 5.0)

    def test_normalized_unit_length(self):
        v = Vector2(5, 0).normalized()
        self.assertAlmostEqual(v.length(), 1.0)
        self.assertEqual(v, Vector2(1.0, 0.0))

    def test_normalized_zero_vector(self):
        self.assertEqual(Vector2(0, 0).normalized(), Vector2(0, 0))

    def test_limited_under_max_is_unchanged(self):
        v = Vector2(1, 1)
        self.assertEqual(v.limited(10), v)

    def test_limited_over_max_is_clamped(self):
        v = Vector2(10, 0).limited(3)
        self.assertAlmostEqual(v.length(), 3.0)

    def test_angle(self):
        self.assertAlmostEqual(Vector2(1, 0).angle(), 0.0)
        self.assertAlmostEqual(Vector2(0, 1).angle(), math.pi / 2)

    def test_distance(self):
        self.assertAlmostEqual(distance(Vector2(0, 0), Vector2(3, 4)), 5.0)

    def test_toroidal_delta_no_wrap(self):
        delta = toroidal_delta(Vector2(5, 5), Vector2(2, 2), width=100, height=100)
        self.assertEqual(delta, Vector2(3, 3))

    def test_toroidal_delta_wraps_shortest_path(self):
        # a is near the right edge, b is near the left edge of a width-10 world;
        # the true shortest displacement should wrap around, not cross the middle.
        delta = toroidal_delta(Vector2(9, 0), Vector2(1, 0), width=10, height=10)
        self.assertAlmostEqual(delta.x, -2.0)


if __name__ == "__main__":
    unittest.main()
