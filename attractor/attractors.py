"""
Mathematical definitions for each strange attractor.

Each attractor is either:
  - Discrete (iterated map): x_{n+1} = f(x_n, y_n)
  - Continuous (ODE): dx/dt = f(x, y, z), integrated with RK4
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple


@dataclass
class AttractorDef:
    name: str
    description: str
    equations: List[str]
    default_params: Dict[str, float]
    kind: str  # "discrete" or "continuous"
    compute: Callable
    default_iterations: int = 2_000_000
    projection: str = "xy"  # which axes to project to 2D


# ── Discrete Attractors ────────────────────────────────────────────────────────

def _clifford(params: Dict, n: int) -> np.ndarray:
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = 0.0, 0.0
    pts = np.empty((n, 2), dtype=np.float32)
    for i in range(n):
        xn = np.sin(a * y) + c * np.cos(a * x)
        yn = np.sin(b * x) + d * np.cos(b * y)
        x, y = xn, yn
        pts[i, 0] = x
        pts[i, 1] = y
    return pts


def _dejong(params: Dict, n: int) -> np.ndarray:
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = 0.1, 0.1
    pts = np.empty((n, 2), dtype=np.float32)
    for i in range(n):
        xn = np.sin(a * y) - np.cos(b * x)
        yn = np.sin(c * x) - np.cos(d * y)
        x, y = xn, yn
        pts[i, 0] = x
        pts[i, 1] = y
    return pts


def _tinkerbell(params: Dict, n: int) -> np.ndarray:
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = -0.72, -0.64
    pts = np.empty((n, 2), dtype=np.float32)
    for i in range(n):
        xn = x * x - y * y + a * x + b * y
        yn = 2 * x * y + c * x + d * y
        x, y = xn, yn
        pts[i, 0] = x
        pts[i, 1] = y
    return pts


def _svensson(params: Dict, n: int) -> np.ndarray:
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = 0.0, 0.0
    pts = np.empty((n, 2), dtype=np.float32)
    for i in range(n):
        xn = d * np.sin(a * x) - np.sin(b * y)
        yn = c * np.cos(a * x) + np.cos(b * y)
        x, y = xn, yn
        pts[i, 0] = x
        pts[i, 1] = y
    return pts


# ── Continuous Attractors (RK4 integration) ─────────────────────────────────

def _rk4_integrate(deriv, x0, y0, z0, dt, n):
    pts = np.empty((n, 3), dtype=np.float32)
    x, y, z = x0, y0, z0
    for i in range(n):
        pts[i] = (x, y, z)
        k1x, k1y, k1z = deriv(x, y, z)
        k2x, k2y, k2z = deriv(x + dt/2*k1x, y + dt/2*k1y, z + dt/2*k1z)
        k3x, k3y, k3z = deriv(x + dt/2*k2x, y + dt/2*k2y, z + dt/2*k2z)
        k4x, k4y, k4z = deriv(x + dt*k3x,   y + dt*k3y,   z + dt*k3z)
        x += dt/6 * (k1x + 2*k2x + 2*k3x + k4x)
        y += dt/6 * (k1y + 2*k2y + 2*k3y + k4y)
        z += dt/6 * (k1z + 2*k2z + 2*k3z + k4z)
    return pts


def _lorenz(params: Dict, n: int) -> np.ndarray:
    s, r, b = params["sigma"], params["rho"], params["beta"]
    def deriv(x, y, z):
        return s*(y-x), x*(r-z)-y, x*y - b*z
    return _rk4_integrate(deriv, 0.1, 0.0, 0.0, 0.005, n)


def _aizawa(params: Dict, n: int) -> np.ndarray:
    a, b, c, d, e, f = (params["a"], params["b"], params["c"],
                         params["d"], params["e"], params["f"])
    def deriv(x, y, z):
        dx = (z - b) * x - d * y
        dy = d * x + (z - b) * y
        dz = c + a * z - z**3 / 3 - (x**2 + y**2) * (1 + e * z) + f * z * x**3
        return dx, dy, dz
    return _rk4_integrate(deriv, 0.1, 1.0, 0.01, 0.01, n)


def _halvorsen(params: Dict, n: int) -> np.ndarray:
    a = params["a"]
    def deriv(x, y, z):
        dx = -a * x - 4 * y - 4 * z - y**2
        dy = -a * y - 4 * z - 4 * x - z**2
        dz = -a * z - 4 * x - 4 * y - x**2
        return dx, dy, dz
    return _rk4_integrate(deriv, -5.0, 0.0, 0.0, 0.005, n)


def _thomas(params: Dict, n: int) -> np.ndarray:
    b = params["b"]
    def deriv(x, y, z):
        return np.sin(y) - b * x, np.sin(z) - b * y, np.sin(x) - b * z
    return _rk4_integrate(deriv, 0.1, 0.0, 0.0, 0.05, n)


# ── Registry ────────────────────────────────────────────────────────────────

ATTRACTORS: Dict[str, AttractorDef] = {
    "clifford": AttractorDef(
        name="Clifford",
        description="A 2D iterated map producing intricate lace-like patterns, discovered by Clifford Pickover.",
        equations=["x_{n+1} = sin(a·y_n) + c·cos(a·x_n)", "y_{n+1} = sin(b·x_n) + d·cos(b·y_n)"],
        default_params={"a": -1.4, "b": 1.6, "c": 1.0, "d": 0.7},
        kind="discrete",
        compute=_clifford,
        default_iterations=3_000_000,
    ),
    "dejong": AttractorDef(
        name="Peter de Jong",
        description="A 2D iterated map by Peter de Jong producing infinitely varied flowing forms.",
        equations=["x_{n+1} = sin(a·y_n) − cos(b·x_n)", "y_{n+1} = sin(c·x_n) − cos(d·y_n)"],
        default_params={"a": 1.641, "b": 1.902, "c": 0.316, "d": 1.525},
        kind="discrete",
        compute=_dejong,
        default_iterations=3_000_000,
    ),
    "tinkerbell": AttractorDef(
        name="Tinkerbell",
        description="A 2D map named whimsically for its fairy-like spiraling structure.",
        equations=["x_{n+1} = x² − y² + a·x + b·y", "y_{n+1} = 2xy + c·x + d·y"],
        default_params={"a": 0.9, "b": -0.6013, "c": 2.0, "d": 0.5},
        kind="discrete",
        compute=_tinkerbell,
        default_iterations=2_000_000,
    ),
    "svensson": AttractorDef(
        name="Svensson",
        description="A 2D iterated map by Johnny Svensson with sweeping, feather-like symmetry.",
        equations=["x_{n+1} = d·sin(a·x) − sin(b·y)", "y_{n+1} = c·cos(a·x) + cos(b·y)"],
        default_params={"a": 1.40, "b": 1.56, "c": 1.40, "d": -6.56},
        kind="discrete",
        compute=_svensson,
        default_iterations=3_000_000,
    ),
    "lorenz": AttractorDef(
        name="Lorenz",
        description="The archetypal chaotic system — the butterfly that started it all. Edward Lorenz, 1963.",
        equations=["dx/dt = σ(y − x)", "dy/dt = x(ρ − z) − y", "dz/dt = xy − βz"],
        default_params={"sigma": 10.0, "rho": 28.0, "beta": 8/3},
        kind="continuous",
        compute=_lorenz,
        default_iterations=500_000,
        projection="xz",
    ),
    "aizawa": AttractorDef(
        name="Aizawa",
        description="A 3D flow with a mesmerizing torus-knot-like structure and rich fine detail.",
        equations=["dx/dt = (z−b)x − dy", "dy/dt = dx + (z−b)y", "dz/dt = c + az − z³/3 − (x²+y²)(1+ez) + fzx³"],
        default_params={"a": 0.95, "b": 0.7, "c": 0.6, "d": 3.5, "e": 0.25, "f": 0.1},
        kind="continuous",
        compute=_aizawa,
        default_iterations=300_000,
        projection="xz",
    ),
    "halvorsen": AttractorDef(
        name="Halvorsen",
        description="A symmetric 3D flow with three intertwined spiraling arms in cyclic symmetry.",
        equations=["dx/dt = −a·x − 4y − 4z − y²", "dy/dt = −a·y − 4z − 4x − z²", "dz/dt = −a·z − 4x − 4y − x²"],
        default_params={"a": 1.89},
        kind="continuous",
        compute=_halvorsen,
        default_iterations=400_000,
        projection="xy",
    ),
    "thomas": AttractorDef(
        name="Thomas",
        description="René Thomas's dissipative system — a slow, languid dance along three axes.",
        equations=["dx/dt = sin(y) − b·x", "dy/dt = sin(z) − b·y", "dz/dt = sin(x) − b·z"],
        default_params={"b": 0.208186},
        kind="continuous",
        compute=_thomas,
        default_iterations=200_000,
        projection="xy",
    ),
}


def list_attractors() -> List[str]:
    return list(ATTRACTORS.keys())


def get_attractor(name: str) -> AttractorDef:
    key = name.lower()
    if key not in ATTRACTORS:
        raise ValueError(f"Unknown attractor '{name}'. Choose from: {', '.join(ATTRACTORS)}")
    return ATTRACTORS[key]


def compute_points(attractor_def: AttractorDef, iterations: int | None = None) -> np.ndarray:
    """
    Compute the 2D projected point cloud for a given attractor.
    Returns shape (N, 2) float32 array.
    """
    n = iterations or attractor_def.default_iterations
    raw = attractor_def.compute(attractor_def.default_params, n)

    axis_map = {"x": 0, "y": 1, "z": 2}
    p = attractor_def.projection
    a1, a2 = axis_map[p[0]], axis_map[p[1]]

    if raw.shape[1] == 2:
        return raw
    return raw[:, [a1, a2]]
