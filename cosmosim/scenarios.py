"""
Pre-built gravitational scenarios.
All use G=1 normalized units.
"""
from __future__ import annotations
import numpy as np
from .bodies import Body

# ── ANSI 256-color helpers ───────────────────────────────────────────────────
def fg(n: int) -> str:
    return f'\033[38;5;{n}m'

YELLOW  = fg(226)
ORANGE  = fg(214)
RED     = fg(196)
BLUE    = fg(33)
CYAN    = fg(51)
GREEN   = fg(46)
MAGENTA = fg(201)
WHITE   = fg(231)
GOLD    = fg(220)
PINK    = fg(213)
PURPLE  = fg(129)
TEAL    = fg(37)
LIME    = fg(154)
CORAL   = fg(203)


# ── Scenario factories ────────────────────────────────────────────────────────

def solar_system() -> list:
    """Sun + 5 planets in stable circular orbits."""
    M_sun = 12000.0
    bodies = [
        Body("Sol", M_sun, np.array([0.0, 0.0]), np.array([0.0, 0.0]),
             YELLOW, '★', max_trail=8),
    ]
    # (name, mass, orbital_radius, color, symbol, angle_offset)
    planets = [
        ("Mercury", 30,    7.0,  WHITE,   '●', 0.0),
        ("Venus",   60,   12.0,  ORANGE,  '●', 1.1),
        ("Earth",   80,   18.0,  BLUE,    '◉', 2.3),
        ("Mars",    40,   26.0,  RED,     '●', 0.7),
        ("Jupiter", 400,  44.0,  GOLD,    '◎', 3.9),
    ]
    for name, mass, r, color, sym, a0 in planets:
        v_circ = np.sqrt(M_sun / r)  # circular orbit speed (G=1)
        pos = np.array([r * np.cos(a0), r * np.sin(a0)])
        vel = np.array([-v_circ * np.sin(a0), v_circ * np.cos(a0)])
        bodies.append(Body(name, mass, pos, vel, color, sym, max_trail=60))
    return bodies


def binary_stars() -> list:
    """Two massive stars in mutual orbit, with a smaller companion."""
    M = 4000.0
    sep = 20.0        # centre-to-centre separation
    r = sep / 2.0     # each star orbits at r from CoM

    # v² = G*M / (4*r)  →  from centripetal balance for equal masses
    v = np.sqrt(G_val(M, r))
    bodies = [
        Body("Sirius A", M, np.array([-r, 0.0]), np.array([0.0, -v]),
             CYAN, '★', max_trail=120),
        Body("Sirius B", M, np.array([r, 0.0]),  np.array([0.0,  v]),
             MAGENTA, '★', max_trail=120),
    ]
    # Distant companion in wider orbit
    R3 = 55.0
    v3 = np.sqrt(2 * M / R3)
    bodies.append(Body("Companion", 80, np.array([0.0, -R3]), np.array([v3, 0.0]),
                       LIME, '◉', max_trail=200))
    return bodies


def G_val(M: float, r: float) -> float:
    """Circular orbit speed² for a test body around mass M at distance r (G=1)."""
    return M / (4 * r)


def three_body_figure_eight() -> list:
    """
    Chenciner-Montgomery figure-eight choreography.
    Three equal masses chase each other along a figure-eight curve.
    Positions scaled ×18, velocities scaled to match.
    """
    M = 1.0
    s_pos = 18.0   # spatial scale
    s_vel = 1.45   # velocity scale (tuned empirically for this unit system)

    # Normalized IC from the original paper
    x1 = np.array([-0.97000436,  0.24308753]) * s_pos
    x2 = np.array([ 0.0,         0.0       ]) * s_pos
    x3 = np.array([ 0.97000436, -0.24308753]) * s_pos

    v3 = np.array([-0.93240737, -0.86473146]) * s_vel
    v1 = np.array([ 0.46620368,  0.43236573]) * s_vel
    v2 = np.array([ 0.46620368,  0.43236573]) * s_vel

    return [
        Body("Alpha", M, x1.copy(), v1.copy(), RED,    '★', max_trail=300),
        Body("Beta",  M, x2.copy(), v2.copy(), CYAN,   '★', max_trail=300),
        Body("Gamma", M, x3.copy(), v3.copy(), GOLD,   '★', max_trail=300),
    ]


def galaxy_collision() -> list:
    """Two mini-galaxies (core + disk stars) on a collision course."""
    rng = np.random.default_rng(7)
    bodies: list = []

    def make_galaxy(cx: float, cy: float,
                    drift_vx: float, drift_vy: float,
                    core_mass: float, n_stars: int,
                    star_color: str, core_color: str,
                    core_sym: str, label: str) -> None:
        center = np.array([cx, cy])
        drift  = np.array([drift_vx, drift_vy])
        bodies.append(Body(label, core_mass, center.copy(), drift.copy(),
                           core_color, core_sym, max_trail=40))
        for _ in range(n_stars):
            r     = rng.uniform(6, 28)
            angle = rng.uniform(0, 2 * np.pi)
            pos   = center + np.array([r * np.cos(angle), r * np.sin(angle)])
            v_orb = np.sqrt(core_mass / r)
            v_tan = np.array([-v_orb * np.sin(angle), v_orb * np.cos(angle)])
            bodies.append(Body("*", 20, pos, v_tan + drift,
                               star_color, '·', max_trail=25))

    make_galaxy(-38, 12,  7, -1.5, 9000, 18, CYAN,    BLUE,   '◎', "Andromeda")
    make_galaxy( 38,-12, -7,  1.5, 7000, 14, MAGENTA, PURPLE, '◎', "Milky Way")
    return bodies


def chaotic_cluster() -> list:
    """Dense cluster of stars — chaotic many-body dynamics."""
    rng = np.random.default_rng(42)
    bodies: list = []
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, MAGENTA, WHITE, GOLD, PINK]
    for i in range(12):
        r     = rng.uniform(2, 18)
        angle = rng.uniform(0, 2 * np.pi)
        pos   = np.array([r * np.cos(angle), r * np.sin(angle)])
        speed = rng.uniform(0.5, 3.0)
        v_ang = rng.uniform(0, 2 * np.pi)
        vel   = np.array([speed * np.cos(v_ang), speed * np.sin(v_ang)])
        mass  = rng.uniform(200, 1200)
        col   = colors[i % len(colors)]
        bodies.append(Body(f"S{i+1}", mass, pos, vel, col, '★', max_trail=80))
    return bodies


# ── Registry ─────────────────────────────────────────────────────────────────
# (factory, display_name, dt, view_scale, steps_per_frame)
SCENARIOS: dict = {
    'solar':   (solar_system,           'Solar System',            0.004,  0.9, 12),
    'binary':  (binary_stars,           'Binary Stars',            0.012,  0.8,  6),
    'figure8': (three_body_figure_eight,'Figure-Eight Choreography',0.0004, 0.9, 10),
    'galaxy':  (galaxy_collision,       'Galaxy Collision',        0.012,  0.55, 6),
    'cluster': (chaotic_cluster,        'Chaotic Star Cluster',    0.006,  1.4,  6),
}
