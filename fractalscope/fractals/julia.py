import numpy as np


# Visually striking presets — (real, imag)
PRESETS = {
    "dendrite":   (-0.0,    1.0),
    "douady_rabbit": (-0.123, 0.745),
    "san_marco":  (-0.75,   0.0),
    "siegel_disk": (-0.391, -0.587),
    "seahorse":   (-0.75,   0.13),
    "spiral":     (0.285,   0.01),
    "lightning":  (-0.7269, 0.1889),
}


def julia(
    width: int,
    height: int,
    x_min: float = -1.8,
    x_max: float = 1.8,
    y_min: float = -1.8,
    y_max: float = 1.8,
    max_iter: int = 256,
    c_real: float = -0.7269,
    c_imag: float = 0.1889,
) -> np.ndarray:
    """
    Compute Julia set escape-time values for the map z -> z² + c.

    Returns a (height, width) float array in [0, 1].
    """
    c = complex(c_real, c_imag)
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    escaped = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        newly_escaped = mask & (np.abs(Z) > 2.0)
        escaped[newly_escaped] = i + 1 - np.log2(np.log2(np.abs(Z[newly_escaped])))
        mask[newly_escaped] = False

    result = np.where(mask, 0.0, escaped / max_iter)
    return result.clip(0.0, 1.0)
