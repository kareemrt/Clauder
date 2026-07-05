"""
Scene presets — initial conditions for various gravitational configurations.

All positions in AU, velocities in AU/year, masses in solar masses.
"""

import math
import random
from typing import List

from .bodies import CelestialBody


def _v_circ(a: float, m_central: float = 1.0) -> float:
    """Circular orbital speed at semi-major axis a around mass m_central."""
    return math.sqrt(4.0 * math.pi ** 2 * m_central / a)


def solar_system() -> List[CelestialBody]:
    """
    Inner solar system + Jupiter using Keplerian circular orbits.
    Masses from NASA Planetary Fact Sheets; orbital periods from Kepler's third law.
    """
    return [
        CelestialBody("Sun",     1.000000, 0.000, 0.0, 0.000, 0.000,             "bright_yellow", "★", 0),
        CelestialBody("Mercury", 1.652e-7, 0.387, 0.0, 0.000, _v_circ(0.387),   "grey70",        "·", 40),
        CelestialBody("Venus",   2.448e-6, 0.723, 0.0, 0.000, _v_circ(0.723),   "yellow",        "○", 55),
        CelestialBody("Earth",   3.003e-6, 1.000, 0.0, 0.000, _v_circ(1.000),   "bright_cyan",   "⊕", 65),
        CelestialBody("Mars",    3.213e-7, 1.524, 0.0, 0.000, _v_circ(1.524),   "bright_red",    "○", 75),
        CelestialBody("Jupiter", 9.543e-4, 5.203, 0.0, 0.000, _v_circ(5.203),   "orange1",       "◉", 80),
    ]


def binary_star() -> List[CelestialBody]:
    """
    Binary star system with a circumbinary planet (Tatooine configuration).

    Two equal half-solar-mass stars orbit their common centre at ±0.5 AU.
    Total mass ≈ 1 M☉ → binary period = 1 year by Kepler's third law.
    The circumbinary planet lives at 3 AU, well beyond the 2–3× stability limit.
    """
    v_star = math.pi          # 2π × 0.5 AU / 1 year
    v_planet = _v_circ(3.0)   # ~3.63 AU/yr around total mass ≈ 1 M☉
    return [
        CelestialBody("Star α",   0.5,   -0.5, 0.0, 0.0,  v_star,    "bright_yellow", "★", 50),
        CelestialBody("Star β",   0.5,    0.5, 0.0, 0.0, -v_star,    "white",         "✦", 50),
        CelestialBody("Tatooine", 1e-6,   3.0, 0.0, 0.0,  v_planet,  "bright_cyan",   "⊕", 90),
    ]


def figure_eight() -> List[CelestialBody]:
    """
    Choreographic figure-8 three-body solution (Chenciner & Montgomery, 2000).

    Original ICs are in units where G = 1, m = 1.
    Converted to G = 4π², m = 0.01 M☉ by rescaling velocities:
      v_new = v_old × √(G_new × m_new) = v_old × 2π × 0.1 ≈ v_old × 0.6283
    Period in new units ≈ 10.07 years (about 6.33 original × 1.59 time scale).
    """
    s = math.sqrt(4.0 * math.pi ** 2 * 0.01)   # ≈ 0.6283
    return [
        CelestialBody("α", 0.01, -0.97000436,  0.24308753,  0.46620369 * s,  0.43236573 * s, "bright_red",   "●", 150),
        CelestialBody("β", 0.01,  0.97000436, -0.24308753,  0.46620369 * s,  0.43236573 * s, "bright_green", "●", 150),
        CelestialBody("γ", 0.01,  0.0,         0.0,        -0.93240737 * s, -0.86473146 * s, "bright_blue",  "●", 150),
    ]


def chaotic_cluster() -> List[CelestialBody]:
    """
    Seven bodies on a ring that quickly destabilises into gravitational chaos.

    Bodies are equally spaced on a 1.5 AU ring with velocities ≈1.2× circular,
    producing a richly unstable configuration: close encounters, ejections,
    and temporary captures all emerge within a few simulated years.
    """
    n = 7
    ring_r = 1.5
    total_mass = 0.7   # M☉ (≈0.1 each)
    colors = ["bright_red", "bright_green", "bright_cyan",
              "bright_magenta", "yellow", "white", "orange1"]
    symbols = ["●", "○", "◉", "◎", "◈", "◆", "·"]

    random.seed(42)
    bodies = []
    for i in range(n):
        angle = 2.0 * math.pi * i / n
        r = ring_r * (0.9 + 0.2 * random.random())
        m = total_mass / n * (0.8 + 0.4 * random.random())
        v_c = _v_circ(r, total_mass)
        speed = v_c * (1.1 + 0.3 * random.random())   # slightly super-circular
        # tangential velocity with small radial kick
        kick = (random.random() - 0.5) * v_c * 0.2
        vx = -speed * math.sin(angle) + kick * math.cos(angle)
        vy =  speed * math.cos(angle) + kick * math.sin(angle)
        bodies.append(CelestialBody(
            f"Body {i + 1}", m,
            r * math.cos(angle), r * math.sin(angle),
            vx, vy,
            colors[i], symbols[i], 70,
        ))
    return bodies
