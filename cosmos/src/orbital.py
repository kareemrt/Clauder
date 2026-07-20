"""
Keplerian orbital mechanics for the solar system.
Computes real planetary positions using simplified orbital elements.
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class OrbitalElements:
    name: str
    color: str          # ANSI/rich color name
    symbol: str         # unicode symbol
    radius_km: int      # planet radius
    semi_major_au: float   # semi-major axis in AU
    eccentricity: float
    inclination_deg: float
    period_days: float
    mean_longitude_deg: float  # L0 at J2000 epoch
    daily_motion_deg: float    # mean motion in deg/day


# Simplified orbital elements (J2000 epoch, mean values)
PLANETS = [
    OrbitalElements("Mercury", "bright_yellow",   "☿",   2439,  0.387, 0.2056, 7.00,    87.97,  252.25,  4.09234),
    OrbitalElements("Venus",   "bright_white",    "♀",   6051,  0.723, 0.0068, 3.39,   224.70,  181.98,  1.60213),
    OrbitalElements("Earth",   "bright_blue",     "⊕",   6371,  1.000, 0.0167, 0.00,   365.25,  100.46,  0.98561),
    OrbitalElements("Mars",    "red",             "♂",   3389,  1.524, 0.0934, 1.85,   686.97,  355.45,  0.52403),
    OrbitalElements("Jupiter", "bright_yellow",   "♃",  71492,  5.203, 0.0489, 1.30, 4332.59,   34.40,  0.08309),
    OrbitalElements("Saturn",  "yellow",          "♄",  60268,  9.537, 0.0565, 2.49,10759.22,   49.94,  0.03346),
    OrbitalElements("Uranus",  "cyan",            "⛢", 25559, 19.191, 0.0463, 0.77,30688.50,  313.23,  0.01172),
    OrbitalElements("Neptune", "blue",            "♆", 24764, 30.069, 0.0097, 1.77,60195.00,  304.88,  0.00598),
]

SUN = OrbitalElements("Sun", "bright_yellow", "☀", 696000, 0, 0, 0, 0, 0, 0)

J2000_EPOCH = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def days_since_j2000(dt: datetime | None = None) -> float:
    if dt is None:
        dt = datetime.now(timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (dt - J2000_EPOCH).total_seconds() / 86400.0


def mean_anomaly(planet: OrbitalElements, jd: float) -> float:
    """Mean anomaly in radians at given Julian day offset from J2000."""
    M = planet.mean_longitude_deg + planet.daily_motion_deg * jd
    return math.radians(M % 360.0)


def eccentric_anomaly(M: float, e: float, tol: float = 1e-8) -> float:
    """Solve Kepler's equation M = E - e*sin(E) via Newton-Raphson."""
    E = M if e < 0.8 else math.pi
    for _ in range(50):
        dE = (M - E + e * math.sin(E)) / (1.0 - e * math.cos(E))
        E += dE
        if abs(dE) < tol:
            break
    return E


def true_anomaly(E: float, e: float) -> float:
    """True anomaly from eccentric anomaly."""
    return 2.0 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2),
    )


def heliocentric_distance(planet: OrbitalElements, nu: float) -> float:
    """Orbital radius in AU."""
    a, e = planet.semi_major_au, planet.eccentricity
    return a * (1 - e * e) / (1 + e * math.cos(nu))


def planet_angle(planet: OrbitalElements, jd: float) -> float:
    """Ecliptic longitude angle (radians) of planet at J2000+jd days."""
    M = mean_anomaly(planet, jd)
    E = eccentric_anomaly(M, planet.eccentricity)
    nu = true_anomaly(E, planet.eccentricity)
    return nu


def planet_xy(planet: OrbitalElements, jd: float, scale: float = 1.0):
    """
    Returns (x, y) in AU in the ecliptic plane.
    scale: multiply all distances by this factor (useful for display).
    """
    M = mean_anomaly(planet, jd)
    E = eccentric_anomaly(M, planet.eccentricity)
    nu = true_anomaly(E, planet.eccentricity)
    r = heliocentric_distance(planet, nu)
    x = r * math.cos(nu) * scale
    y = r * math.sin(nu) * scale
    return x, y


def get_all_positions(dt: datetime | None = None) -> dict[str, tuple[float, float]]:
    """Returns {planet_name: (x_au, y_au)} for all planets."""
    jd = days_since_j2000(dt)
    positions = {"Sun": (0.0, 0.0)}
    for p in PLANETS:
        positions[p.name] = planet_xy(p, jd)
    return positions
