import numpy as np

from fractalforge.ifs import barnsley_fern_points, koch_snowflake_points, sierpinski_points


def test_sierpinski_points_shape_and_bounds():
    points = sierpinski_points(num_points=1000, seed=1)
    assert points.shape == (1000, 2)
    # Every point must lie within the bounding triangle's bounding box.
    assert points[:, 0].min() >= -0.01
    assert points[:, 0].max() <= 1.01
    assert points[:, 1].min() >= -0.01
    assert points[:, 1].max() <= np.sqrt(3) / 2 + 0.01


def test_sierpinski_points_reproducible_with_seed():
    a = sierpinski_points(num_points=500, seed=7)
    b = sierpinski_points(num_points=500, seed=7)
    assert np.array_equal(a, b)


def test_barnsley_fern_points_shape_and_bounds():
    points = barnsley_fern_points(num_points=1000, seed=1)
    assert points.shape == (1000, 2)
    # The classic Barnsley fern fits within roughly x in [-3, 3], y in [0, 10].
    assert points[:, 0].min() >= -3.0
    assert points[:, 0].max() <= 3.0
    assert points[:, 1].min() >= 0.0
    assert points[:, 1].max() <= 10.0


def test_koch_snowflake_returns_closed_loop():
    points = koch_snowflake_points(order=2)
    # The path should start and end at the same vertex.
    assert np.allclose(points[0], points[-1])
    assert len(points) > 3


def test_koch_snowflake_grows_with_order():
    low = koch_snowflake_points(order=1)
    high = koch_snowflake_points(order=3)
    assert len(high) > len(low)
