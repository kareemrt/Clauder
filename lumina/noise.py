"""Value noise and fractal Brownian motion for procedural generation."""
import numpy as np


def _smoothstep(t: np.ndarray) -> np.ndarray:
    return t * t * (3 - 2 * t)


def value_noise(width: int, height: int, scale: float, rng: np.random.Generator) -> np.ndarray:
    """Generate smooth value noise using bilinear interpolation."""
    grid_w = int(np.ceil(width / scale)) + 2
    grid_h = int(np.ceil(height / scale)) + 2
    grid = rng.random((grid_h, grid_w))

    xs = np.linspace(0, grid_w - 2, width)
    ys = np.linspace(0, grid_h - 2, height)
    xi = xs.astype(int)
    yi = ys.astype(int)
    xf = _smoothstep(xs - xi)
    yf = _smoothstep(ys - yi)

    xi = np.clip(xi, 0, grid_w - 2)
    yi = np.clip(yi, 0, grid_h - 2)

    xf2d = xf[np.newaxis, :]
    yf2d = yf[:, np.newaxis]

    v00 = grid[yi[:, np.newaxis], xi[np.newaxis, :]]
    v10 = grid[yi[:, np.newaxis], (xi + 1)[np.newaxis, :]]
    v01 = grid[(yi + 1)[:, np.newaxis], xi[np.newaxis, :]]
    v11 = grid[(yi + 1)[:, np.newaxis], (xi + 1)[np.newaxis, :]]

    top = v00 * (1 - xf2d) + v10 * xf2d
    bot = v01 * (1 - xf2d) + v11 * xf2d
    return top * (1 - yf2d) + bot * yf2d


def fbm(width: int, height: int, octaves: int, lacunarity: float,
        gain: float, base_scale: float, rng: np.random.Generator) -> np.ndarray:
    """Fractal Brownian Motion — layered noise for organic textures."""
    result = np.zeros((height, width))
    amplitude = 1.0
    scale = base_scale
    total_amplitude = 0.0
    for _ in range(octaves):
        result += amplitude * value_noise(width, height, scale, rng)
        total_amplitude += amplitude
        amplitude *= gain
        scale /= lacunarity
    return result / total_amplitude
