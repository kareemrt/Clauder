import math

from pytracer.vector import Vec3


def test_add_sub():
    a = Vec3(1, 2, 3)
    b = Vec3(4, 5, 6)
    assert a + b == Vec3(5, 7, 9)
    assert b - a == Vec3(3, 3, 3)


def test_scalar_mul():
    a = Vec3(1, -2, 3)
    assert a * 2 == Vec3(2, -4, 6)
    assert 2 * a == Vec3(2, -4, 6)


def test_dot_and_cross():
    x = Vec3(1, 0, 0)
    y = Vec3(0, 1, 0)
    assert x.dot(y) == 0
    assert x.cross(y) == Vec3(0, 0, 1)


def test_length_and_normalize():
    v = Vec3(3, 4, 0)
    assert v.length() == 5
    n = v.normalize()
    assert math.isclose(n.length(), 1.0)


def test_normalize_zero_vector_is_safe():
    zero = Vec3(0, 0, 0)
    assert zero.normalize() == zero


def test_reflect_off_flat_surface():
    incoming = Vec3(1, -1, 0).normalize()
    normal = Vec3(0, 1, 0)
    reflected = incoming.reflect(normal)
    assert math.isclose(reflected.x, incoming.x)
    assert math.isclose(reflected.y, -incoming.y)


def test_clamp_and_to_rgb():
    v = Vec3(1.5, -0.2, 0.5)
    assert v.clamp() == Vec3(1.0, 0.0, 0.5)
    assert v.to_rgb() == (255, 0, 128)
