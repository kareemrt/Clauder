"""Iterated function systems: Sierpinski triangle, Barnsley fern, Koch snowflake."""

import numpy as np


def sierpinski_points(num_points=100_000, seed=None):
    """Generate points on the Sierpinski triangle via the chaos game."""
    rng = np.random.default_rng(seed)
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
    choices = rng.integers(0, 3, size=num_points)

    points = np.empty((num_points, 2))
    point = np.array([0.5, 0.25])
    for i, choice in enumerate(choices):
        point = (point + vertices[choice]) / 2
        points[i] = point
    return points


def barnsley_fern_points(num_points=100_000, seed=None):
    """Generate points on the Barnsley fern via an affine iterated function system."""
    rng = np.random.default_rng(seed)
    rolls = rng.random(num_points)

    points = np.empty((num_points, 2))
    x, y = 0.0, 0.0
    for i, roll in enumerate(rolls):
        if roll < 0.01:
            x, y = 0.0, 0.16 * y
        elif roll < 0.86:
            x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif roll < 0.93:
            x, y = 0.20 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
        points[i] = (x, y)
    return points


def _koch_curve(p1, p2, order):
    """Recursively subdivide a segment into a Koch curve, returning leading points."""
    if order == 0:
        return [p1]

    p1 = np.asarray(p1, dtype=np.float64)
    p2 = np.asarray(p2, dtype=np.float64)
    delta = (p2 - p1) / 3.0
    a = p1 + delta
    b = p1 + 2 * delta

    angle = -np.pi / 3.0
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    peak = a + rotation @ delta

    points = []
    points += _koch_curve(p1, a, order - 1)
    points += _koch_curve(a, peak, order - 1)
    points += _koch_curve(peak, b, order - 1)
    points += _koch_curve(b, p2, order - 1)
    return points


def koch_snowflake_points(order=4):
    """Generate the closed outline of a Koch snowflake as an array of points."""
    p1 = np.array([0.0, 0.0])
    p2 = np.array([1.0, 0.0])
    p3 = np.array([0.5, np.sqrt(3) / 2])

    points = (
        _koch_curve(p1, p2, order)
        + _koch_curve(p2, p3, order)
        + _koch_curve(p3, p1, order)
    )
    points.append(p1)
    return np.array(points)
