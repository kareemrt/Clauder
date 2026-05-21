"""Newton fractal: Newton's method applied to z^3 - 1 = 0"""

import numpy as np


# The three cube roots of unity
ROOTS = np.array([1.0 + 0j, -0.5 + 0.8660254j, -0.5 - 0.8660254j])
ROOT_COLORS = np.array([[1.0, 0.2, 0.2], [0.2, 1.0, 0.2], [0.2, 0.2, 1.0]])


def newton(
    width: int,
    height: int,
    x_min: float = -1.5,
    x_max: float = 1.5,
    y_min: float = -1.5,
    y_max: float = 1.5,
    max_iter: int = 64,
    tolerance: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the Newton fractal for f(z) = z^3 - 1.

    Returns:
        root_map: (H, W) int array indicating which root each point converged to
        speed_map: (H, W) float array of convergence speed, normalized to [0, 1]
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    convergence_iter = np.full(z.shape, max_iter, dtype=float)
    root_map = np.full(z.shape, -1, dtype=int)
    active = np.ones(z.shape, dtype=bool)

    for i in range(max_iter):
        if not np.any(active):
            break
        # Newton step for z^3 - 1: z_new = z - f(z)/f'(z) = z - (z^3-1)/(3z^2)
        z3 = z[active] ** 3
        z[active] = z[active] - (z3 - 1) / (3 * z[active] ** 2)

        for r_idx, root in enumerate(ROOTS):
            converged = active & (np.abs(z - root) < tolerance)
            root_map[converged] = r_idx
            convergence_iter[converged] = i
            active[converged] = False

    # Normalize convergence speed: fast convergence → bright
    speed_map = 1.0 - (convergence_iter / max_iter)
    return root_map, speed_map
