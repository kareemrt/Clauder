import numpy as np

from bloom.kernel import build_kernel, growth, ring_kernel


def test_ring_kernel_normalizes_to_one():
    k = ring_kernel(27, [(0.5, 0.15, 1.0)])
    np.testing.assert_allclose(k.sum(), 1.0, atol=1e-9)


def test_ring_kernel_is_radially_symmetric():
    k = ring_kernel(21, [(0.5, 0.15, 1.0)])
    np.testing.assert_allclose(k, np.flipud(k))
    np.testing.assert_allclose(k, np.fliplr(k))


def test_build_kernel_fft_has_expected_shape():
    fft = build_kernel((64, 64), radius=10, shells=[(0.5, 0.15, 1.0)])
    assert fft.shape == (64, 64)
    assert np.iscomplexobj(fft)


def test_growth_peaks_at_mu():
    u = np.linspace(0.0, 1.0, 1001)
    g = growth(u, mu=0.3, sigma=0.05)
    assert abs(u[np.argmax(g)] - 0.3) < 0.01


def test_growth_is_bounded():
    u = np.linspace(-5.0, 5.0, 200)
    g = growth(u, mu=0.3, sigma=0.05)
    assert g.max() <= 1.0 + 1e-9
    assert g.min() >= -1.0 - 1e-9
