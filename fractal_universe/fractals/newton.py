import numpy as np


def newton(width: int, height: int,
           x_min: float = -2.0, x_max: float = 2.0,
           y_min: float = -2.0, y_max: float = 2.0,
           max_iter: int = 64, tol: float = 1e-6) -> tuple[np.ndarray, np.ndarray]:
    """
    Newton fractal for f(z) = z^3 - 1.

    Returns (root_id, iteration) arrays of shape (height, width).
    root_id encodes which of the three cube roots z converged to (0,1,2).
    iteration holds the convergence speed (lower = faster convergence).
    """
    # The three cube roots of unity
    roots = np.array([1.0 + 0j,
                      -0.5 + 0.8660254j,
                      -0.5 - 0.8660254j])

    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    root_id = np.full(Z.shape, -1, dtype=np.int8)
    iteration = np.full(Z.shape, max_iter, dtype=np.float64)
    active = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z2 = Z[active] ** 2
        Z3 = Z2 * Z[active]
        # Newton step: z - f(z)/f'(z) = z - (z^3-1)/(3z^2) = (2z^3+1)/(3z^2)
        denom = 3 * Z2
        safe = np.abs(denom) > 1e-14
        idx = np.where(active)[0], np.where(active)[1]  # not used as tuple
        # work on the active flat slice
        step = np.where(safe, (Z3[safe] - 1) / denom[safe], 0)

        Z_active = Z[active]
        safe_mask = np.abs(3 * Z_active ** 2) > 1e-14
        Z_new = np.where(safe_mask, Z_active - (Z_active**3 - 1) / (3 * Z_active**2), Z_active)
        Z[active] = Z_new

        for r_idx, root in enumerate(roots):
            converged = active & (np.abs(Z - root) < tol)
            root_id[converged] = r_idx
            iteration[converged] = i
            active &= ~converged

        if not active.any():
            break

    return root_id, iteration
