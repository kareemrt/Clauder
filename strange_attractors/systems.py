"""Definitions of classic chaotic dynamical systems (strange attractors).

Each system is an autonomous ODE dx/dt = f(x, y, z; params) in three dimensions.
They are deterministic, yet long-term behavior is unpredictable and exponentially
sensitive to initial conditions — the defining signature of chaos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

DerivFn = Callable[[np.ndarray, dict], np.ndarray]


@dataclass
class AttractorSystem:
    name: str
    description: str
    params: dict
    deriv: DerivFn
    state0: tuple
    dt: float
    steps: int
    projection: tuple = ("x", "z")

    def f(self, state: np.ndarray) -> np.ndarray:
        return self.deriv(state, self.params)


def _lorenz(state, p):
    x, y, z = state
    return np.array([
        p["sigma"] * (y - x),
        x * (p["rho"] - z) - y,
        x * y - p["beta"] * z,
    ])


def _rossler(state, p):
    x, y, z = state
    return np.array([
        -y - z,
        x + p["a"] * y,
        p["b"] + z * (x - p["c"]),
    ])


def _aizawa(state, p):
    x, y, z = state
    a, b, c, d, e, f = p["a"], p["b"], p["c"], p["d"], p["e"], p["f"]
    return np.array([
        (z - b) * x - d * y,
        d * x + (z - b) * y,
        c + a * z - z ** 3 / 3 - (x ** 2 + y ** 2) * (1 + e * z) + f * z * x ** 3,
    ])


def _thomas(state, p):
    x, y, z = state
    b = p["b"]
    return np.array([
        np.sin(y) - b * x,
        np.sin(z) - b * y,
        np.sin(x) - b * z,
    ])


def _chen(state, p):
    x, y, z = state
    a, b, c = p["a"], p["b"], p["c"]
    return np.array([
        a * (y - x),
        (c - a) * x - x * z + c * y,
        x * y - b * z,
    ])


def _halvorsen(state, p):
    x, y, z = state
    a = p["a"]
    return np.array([
        -a * x - 4 * y - 4 * z - y ** 2,
        -a * y - 4 * z - 4 * x - z ** 2,
        -a * z - 4 * x - 4 * y - x ** 2,
    ])


def _dadras(state, p):
    x, y, z = state
    a, b, c, d, e = p["a"], p["b"], p["c"], p["d"], p["e"]
    return np.array([
        y - a * x + b * y * z,
        c * y - x * z + z,
        d * x * y - e * z,
    ])


SYSTEMS: dict[str, AttractorSystem] = {
    "lorenz": AttractorSystem(
        name="Lorenz",
        description="The original 1963 chaotic system, derived from a simplified model of atmospheric convection.",
        params=dict(sigma=10.0, rho=28.0, beta=8.0 / 3.0),
        deriv=_lorenz,
        state0=(0.1, 0.0, 0.0),
        dt=0.008,
        steps=20000,
        projection=("x", "z"),
    ),
    "rossler": AttractorSystem(
        name="Rössler",
        description="A simpler chaotic flow than Lorenz, with a single sheet of folded trajectories.",
        params=dict(a=0.2, b=0.2, c=5.7),
        deriv=_rossler,
        state0=(1.0, 1.0, 1.0),
        dt=0.02,
        steps=20000,
        projection=("x", "y"),
    ),
    "aizawa": AttractorSystem(
        name="Aizawa",
        description="A spherical, ribbon-like attractor that winds and twists around a central core.",
        params=dict(a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1),
        deriv=_aizawa,
        state0=(0.1, 0.0, 0.0),
        dt=0.01,
        steps=30000,
        projection=("x", "y"),
    ),
    "thomas": AttractorSystem(
        name="Thomas",
        description="A cyclically symmetric attractor driven purely by sine feedback — labyrinthine chaos.",
        params=dict(b=0.19),
        deriv=_thomas,
        state0=(0.1, 0.0, 0.0),
        dt=0.05,
        steps=40000,
        projection=("x", "y"),
    ),
    "chen": AttractorSystem(
        name="Chen",
        description="A double-scroll chaotic attractor closely related to Lorenz, but with sharper folds.",
        params=dict(a=35.0, b=3.0, c=28.0),
        deriv=_chen,
        state0=(-0.1, 0.5, -0.6),
        dt=0.0025,
        steps=30000,
        projection=("x", "z"),
    ),
    "halvorsen": AttractorSystem(
        name="Halvorsen",
        description="A cyclically symmetric attractor with three-fold rotational structure.",
        params=dict(a=1.4),
        deriv=_halvorsen,
        state0=(1.0, 0.0, 0.0),
        dt=0.005,
        steps=20000,
        projection=("x", "y"),
    ),
    "dadras": AttractorSystem(
        name="Dadras",
        description="A four-wing chaotic attractor discovered by Dadras & Momeni, with two interleaved wings.",
        params=dict(a=3.0, b=2.7, c=1.7, d=2.0, e=9.0),
        deriv=_dadras,
        state0=(1.0, 1.0, 1.0),
        dt=0.005,
        steps=20000,
        projection=("x", "y"),
    ),
}
