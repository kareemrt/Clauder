import numpy as np

from worldforge.noise import PerlinNoise, normalize


def test_noise_is_deterministic_for_seed():
    noise_a = PerlinNoise(seed=42)
    noise_b = PerlinNoise(seed=42)

    x = np.linspace(0, 5, 20)
    y = np.linspace(0, 5, 20)
    xx, yy = np.meshgrid(x, y)

    np.testing.assert_array_equal(noise_a.noise(xx, yy), noise_b.noise(xx, yy))


def test_noise_differs_for_different_seeds():
    noise_a = PerlinNoise(seed=1)
    noise_b = PerlinNoise(seed=2)

    x = np.linspace(0, 5, 20)
    y = np.linspace(0, 5, 20)
    xx, yy = np.meshgrid(x, y)

    assert not np.array_equal(noise_a.noise(xx, yy), noise_b.noise(xx, yy))


def test_noise_bounded_roughly_unit_range():
    noise = PerlinNoise(seed=7)
    x = np.linspace(0, 20, 200)
    y = np.linspace(0, 20, 200)
    xx, yy = np.meshgrid(x, y)

    values = noise.noise(xx, yy)
    assert values.min() >= -1.5
    assert values.max() <= 1.5


def test_fbm_normalize_range():
    noise = PerlinNoise(seed=3)
    x = np.linspace(0, 10, 64)
    y = np.linspace(0, 10, 64)
    xx, yy = np.meshgrid(x, y)

    fbm = noise.fbm(xx, yy, octaves=5)
    normalized = normalize(fbm)

    assert normalized.min() == 0.0
    assert normalized.max() == 1.0
    assert normalized.shape == fbm.shape


def test_normalize_handles_constant_array():
    constant = np.full((4, 4), 3.0)
    result = normalize(constant)
    assert np.all(result == 0)
