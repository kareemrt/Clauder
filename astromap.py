#!/usr/bin/env python3
"""
AstroMap - Personal Star Map Generator
Renders a beautiful, astronomically accurate SVG star map for any
location on Earth at any date and time.

Usage:
    python astromap.py                                         # now, NYC
    python astromap.py --lat 51.5 --lon -0.1                 # London, now
    python astromap.py --lat 35.7 --lon 139.7 --date "2025-01-01 00:00"
    python astromap.py --lat 40.7 --lon -74.0 --title "Our First Night" --out sky.svg
"""

import math
import argparse
import sys
from datetime import datetime, timezone, timedelta

# ── Star Catalog ─────────────────────────────────────────────────────────────
# (name, ra_degrees, dec_degrees, visual_magnitude)
STARS = [
    # Negative magnitude
    ("Sirius",           101.287, -16.716, -1.46),
    ("Canopus",           95.988, -52.696, -0.72),
    # mag 0
    ("Rigil Kentaurus",  219.900, -60.834, -0.27),
    ("Arcturus",         213.915,  19.182, -0.04),
    ("Vega",             279.235,  38.784,  0.03),
    ("Capella",           79.172,  45.998,  0.08),
    ("Rigel",             78.634,  -8.202,  0.12),
    ("Procyon",          114.825,   5.225,  0.34),
    ("Achernar",          24.429, -57.237,  0.46),
    ("Betelgeuse",        88.793,   7.407,  0.42),
    ("Hadar",            210.956, -60.373,  0.61),
    ("Altair",           297.696,   8.868,  0.76),
    ("Aldebaran",         68.980,  16.509,  0.85),
    ("Acrux",            186.650, -63.099,  0.87),
    # mag 1
    ("Spica",            201.298, -11.161,  1.04),
    ("Antares",          247.352, -26.432,  1.06),
    ("Pollux",           116.329,  28.026,  1.14),
    ("Fomalhaut",        344.413, -29.622,  1.16),
    ("Deneb",            310.358,  45.280,  1.25),
    ("Mimosa",           191.930, -59.689,  1.25),
    ("Regulus",          152.093,  11.967,  1.36),
    ("Adhara",           104.657, -28.972,  1.50),
    ("Castor",           113.650,  31.888,  1.58),
    ("Gacrux",           187.791, -57.113,  1.59),
    ("Shaula",           263.402, -37.104,  1.62),
    ("Bellatrix",         81.283,   6.350,  1.64),
    ("Elnath",            81.573,  28.608,  1.65),
    ("Alnilam",           84.053,  -1.202,  1.70),
    ("Alnitak",           85.190,  -1.943,  1.74),
    ("Gamma Velorum",    122.383, -47.337,  1.75),
    ("Alioth",           193.508,  55.960,  1.76),
    ("Dubhe",            165.932,  61.751,  1.79),
    ("Mirfak",            51.080,  49.861,  1.79),
    ("Wezen",            107.098, -26.393,  1.83),
    ("Kaus Australis",   276.043, -34.384,  1.85),
    ("Alkaid",           206.885,  49.313,  1.86),
    ("Avior",            125.629, -59.509,  1.86),
    ("Sargas",           264.330, -42.998,  1.87),
    ("Menkalinan",        89.882,  44.948,  1.90),
    ("Atria",            252.166, -69.028,  1.91),
    ("Delta Velorum",    131.176, -54.709,  1.93),
    ("Alhena",            99.428,  16.399,  1.93),
    ("Peacock",          306.412, -56.735,  1.94),
    ("Mirzam",            95.675, -17.956,  1.98),
    ("Miaplacidus",      138.300, -69.717,  1.67),
    ("Polaris",           37.954,  89.264,  1.97),
    ("Alphard",          141.897,  -8.659,  1.98),
    # mag 2
    ("Hamal",             31.793,  23.463,  2.00),
    ("Diphda",            10.897, -17.987,  2.02),
    ("Nunki",            283.816, -26.297,  2.05),
    ("Menkent",          211.670, -36.370,  2.06),
    ("Saiph",             86.939,  -9.670,  2.07),
    ("Alpheratz",          2.097,  29.091,  2.07),
    ("Mirach",            17.433,  35.620,  2.07),
    ("Almach",            30.975,  42.330,  2.10),
    ("Denebola",         177.265,  14.572,  2.14),
    ("Mintaka",           83.002,  -0.299,  2.23),
    ("Schedar",           10.127,  56.537,  2.23),
    ("Sadr",             305.557,  40.257,  2.23),
    ("Naos",             120.896, -40.003,  2.25),
    ("Caph",               2.295,  59.150,  2.27),
    ("Mizar",            200.981,  54.925,  2.27),
    ("Albireo",          292.680,  27.960,  3.05),
    ("Epsilon Sco",      252.967, -34.293,  2.29),
    ("Dschubba",         240.083, -22.622,  2.29),
    ("Algol",             47.042,  40.956,  2.09),
    ("Enif",             326.046,   9.875,  2.40),
    ("Merak",            165.460,  56.383,  2.37),
    ("Algenib",            3.309,  15.184,  2.83),
    ("Scheat",           345.944,  28.083,  2.44),
    ("Phecda",           178.457,  53.694,  2.44),
    ("Alderamin",        319.645,  62.585,  2.45),
    ("Gienah Cyg",       311.553,  33.971,  2.46),
    ("Gamma Cas",         14.177,  60.717,  2.47),
    ("Markab",           346.190,  15.205,  2.49),
    ("Algieba",          154.993,  19.842,  2.61),
    ("Graffias",         241.359, -19.806,  2.62),
    ("Ruchbah",           21.454,  60.235,  2.68),
    ("Kaus Media",       275.248, -29.828,  2.70),
    ("Lesath",           264.866, -37.296,  2.70),
    ("Izar",             221.247,  27.074,  2.70),
    ("Tau Sco",          248.971, -28.216,  2.82),
    ("Alcyone",           56.871,  24.105,  2.87),
    ("Delta Cyg",        296.244,  45.131,  2.89),
    ("Kappa Sco",        265.622, -39.030,  2.41),
    ("Zosma",            168.527,  20.524,  2.56),
    # mag 3
    ("Meissa",            83.858,   9.934,  3.39),
    ("Megrez",           183.857,  57.033,  3.31),
    ("Segin",             28.599,  63.670,  3.35),
    ("Mebsuda",          100.983,  25.131,  3.06),
    ("Sadalsuud",        322.890,  -5.571,  2.91),
    ("Deneb Algedi",     321.668, -22.411,  2.85),
]

# ── Constellation Lines ───────────────────────────────────────────────────────
# Each entry: list of (star_name_a, star_name_b) line segments
CONSTELLATIONS = {
    "Orion": [
        ("Meissa", "Betelgeuse"),
        ("Meissa", "Bellatrix"),
        ("Betelgeuse", "Alnilam"),
        ("Bellatrix", "Mintaka"),
        ("Mintaka", "Alnilam"),
        ("Alnilam", "Alnitak"),
        ("Alnitak", "Saiph"),
        ("Mintaka", "Rigel"),
        ("Alnitak", "Rigel"),
        ("Rigel", "Saiph"),
    ],
    "Ursa Major": [
        ("Dubhe", "Merak"),
        ("Merak", "Phecda"),
        ("Phecda", "Megrez"),
        ("Megrez", "Dubhe"),
        ("Megrez", "Alioth"),
        ("Alioth", "Mizar"),
        ("Mizar", "Alkaid"),
    ],
    "Cassiopeia": [
        ("Caph", "Schedar"),
        ("Schedar", "Gamma Cas"),
        ("Gamma Cas", "Ruchbah"),
        ("Ruchbah", "Segin"),
    ],
    "Scorpius": [
        ("Graffias", "Dschubba"),
        ("Dschubba", "Antares"),
        ("Antares", "Tau Sco"),
        ("Tau Sco", "Epsilon Sco"),
        ("Epsilon Sco", "Sargas"),
        ("Sargas", "Kappa Sco"),
        ("Kappa Sco", "Shaula"),
        ("Shaula", "Lesath"),
    ],
    "Cygnus": [
        ("Deneb", "Sadr"),
        ("Sadr", "Albireo"),
        ("Sadr", "Gienah Cyg"),
        ("Sadr", "Delta Cyg"),
    ],
    "Leo": [
        ("Regulus", "Algieba"),
        ("Algieba", "Zosma"),
        ("Zosma", "Denebola"),
        ("Regulus", "Eta Leo"),  # sickle
    ],
    "Gemini": [
        ("Castor", "Mebsuda"),
        ("Pollux", "Alhena"),
        ("Mebsuda", "Alhena"),
        ("Castor", "Pollux"),
    ],
    "Taurus": [
        ("Aldebaran", "Elnath"),
        ("Aldebaran", "Alcyone"),
    ],
    "Andromeda": [
        ("Alpheratz", "Mirach"),
        ("Mirach", "Almach"),
    ],
    "Perseus": [
        ("Mirfak", "Algol"),
        ("Mirfak", "Menkalinan"),
    ],
    "Pegasus": [
        ("Markab", "Scheat"),
        ("Scheat", "Alpheratz"),
        ("Alpheratz", "Algenib"),
        ("Algenib", "Markab"),
        ("Markab", "Enif"),
    ],
    "Sagittarius": [
        ("Kaus Australis", "Kaus Media"),
        ("Kaus Media", "Nunki"),
        ("Kaus Australis", "Nunki"),
    ],
    "Aquarius": [
        ("Sadalsuud", "Deneb Algedi"),
        ("Sadalsuud", "Enif"),
    ],
}

# Remove Leo constellation reference to "Eta Leo" since it's not in catalog
CONSTELLATIONS["Leo"] = [
    ("Regulus", "Algieba"),
    ("Algieba", "Zosma"),
    ("Zosma", "Denebola"),
]

# Label bright stars (shown on map)
LABEL_MAG_LIMIT = 1.5


# ── Astronomy Math ────────────────────────────────────────────────────────────

def julian_day(dt: datetime) -> float:
    """Julian Day Number from a UTC datetime."""
    dt = dt.astimezone(timezone.utc)
    y, m, d = dt.year, dt.month, dt.day
    h = dt.hour + dt.minute / 60 + dt.second / 3600
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + h / 24 + B - 1524.5


def gmst_degrees(jd: float) -> float:
    """Greenwich Mean Sidereal Time in degrees."""
    T = (jd - 2451545.0) / 36525.0
    gmst = (280.46061837
            + 360.98564736629 * (jd - 2451545.0)
            + T * T * (0.000387933 - T / 38710000.0))
    return gmst % 360


def equatorial_to_horizontal(ra: float, dec: float,
                              lat: float, lon: float, jd: float):
    """Convert RA/Dec (degrees) to Altitude/Azimuth (degrees).
    Returns (altitude, azimuth) where azimuth is N=0°, E=90°.
    """
    lst = (gmst_degrees(jd) + lon) % 360
    ha = (lst - ra) % 360           # Hour angle

    ha_r  = math.radians(ha)
    dec_r = math.radians(dec)
    lat_r = math.radians(lat)

    sin_alt = (math.sin(dec_r) * math.sin(lat_r)
               + math.cos(dec_r) * math.cos(lat_r) * math.cos(ha_r))
    alt = math.degrees(math.asin(max(-1.0, min(1.0, sin_alt))))

    cos_az = ((math.sin(dec_r) - math.sin(math.radians(alt)) * math.sin(lat_r))
              / (math.cos(math.radians(alt)) * math.cos(lat_r) + 1e-10))
    az = math.degrees(math.acos(max(-1.0, min(1.0, cos_az))))
    if math.sin(ha_r) > 0:
        az = 360.0 - az

    return alt, az


def stereographic_project(alt: float, az: float, cx: float, cy: float, r: float):
    """Azimuthal equidistant projection: zenith=center, N=top, horizon=edge."""
    rho = (90.0 - alt) / 90.0      # 0 at zenith, 1 at horizon
    az_r = math.radians(az)
    x = cx + rho * r * math.sin(az_r)
    y = cy - rho * r * math.cos(az_r)
    return x, y


# ── Colour helpers ────────────────────────────────────────────────────────────

def star_color(vmag: float) -> str:
    """Return a warm-white/blue-white CSS colour based on magnitude."""
    if vmag < 0.5:
        return "#cce8ff"   # brilliant blue-white
    elif vmag < 1.5:
        return "#dff0ff"   # white-blue
    elif vmag < 2.5:
        return "#f0f8ff"   # alice blue
    elif vmag < 3.5:
        return "#fffaf0"   # warm white
    else:
        return "#ffeedd"   # dim warm


def star_radius(vmag: float) -> float:
    """SVG circle radius scaled by brightness (inverse-log)."""
    return max(0.6, 4.5 - vmag * 0.9)


def star_glow(vmag: float) -> float:
    """Glow filter intensity."""
    return max(1.0, 3.5 - vmag * 0.5)


# ── SVG Generation ────────────────────────────────────────────────────────────

SVG_SIZE = 800
MARGIN   = 60
RADIUS   = (SVG_SIZE - 2 * MARGIN) // 2
CX       = SVG_SIZE // 2
CY       = SVG_SIZE // 2

def build_svg(visible_stars: list, constellation_segments: list,
              title: str, subtitle: str, lat: float, lon: float) -> str:
    """Assemble the complete SVG document."""

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'width="{SVG_SIZE}" height="{SVG_SIZE + 80}" '
                 f'viewBox="0 0 {SVG_SIZE} {SVG_SIZE + 80}">')

    # ── Defs: gradients, filters ──────────────────────────────────────────────
    lines.append("""  <defs>
    <radialGradient id="skyGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#0a0a2e"/>
      <stop offset="60%"  stop-color="#050520"/>
      <stop offset="100%" stop-color="#010112"/>
    </radialGradient>
    <radialGradient id="horizonGlow" cx="50%" cy="50%" r="50%">
      <stop offset="70%"  stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#1a3a6a" stop-opacity="0.4"/>
    </radialGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="1.8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="bigGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="labelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#000033" flood-opacity="0.9"/>
    </filter>
    <clipPath id="skyClip">
      <circle cx="{cx}" cy="{cy}" r="{r}"/>
    </clipPath>
  </defs>""".format(cx=CX, cy=CY, r=RADIUS))

    # ── Background ────────────────────────────────────────────────────────────
    lines.append(f'  <rect width="{SVG_SIZE}" height="{SVG_SIZE + 80}" fill="#000005"/>')
    lines.append(f'  <circle cx="{CX}" cy="{CY}" r="{RADIUS}" fill="url(#skyGrad)"/>')

    # ── Grid rings ────────────────────────────────────────────────────────────
    lines.append('  <g clip-path="url(#skyClip)" opacity="0.18">')
    for alt_line in [0, 15, 30, 45, 60, 75]:
        rho = (90 - alt_line) / 90 * RADIUS
        lines.append(f'    <circle cx="{CX}" cy="{CY}" r="{rho:.1f}" '
                     f'fill="none" stroke="#4488cc" stroke-width="0.4"/>')
    # Azimuth spokes
    for az_deg in range(0, 360, 30):
        az_r = math.radians(az_deg)
        x2 = CX + RADIUS * math.sin(az_r)
        y2 = CY - RADIUS * math.cos(az_r)
        lines.append(f'    <line x1="{CX}" y1="{CY}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="#4488cc" stroke-width="0.4"/>')
    lines.append('  </g>')

    # ── Milky Way (artistic approximation: arc band) ─────────────────────────
    mw_path = _milky_way_path()
    if mw_path:
        lines.append(f'  <g clip-path="url(#skyClip)">{mw_path}</g>')

    # ── Constellation lines ───────────────────────────────────────────────────
    lines.append('  <g clip-path="url(#skyClip)" opacity="0.55" '
                 'stroke="#4a90d9" stroke-width="0.8" stroke-dasharray="4,3">')
    for (x1, y1, x2, y2) in constellation_segments:
        lines.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" '
                     f'x2="{x2:.1f}" y2="{y2:.1f}"/>')
    lines.append('  </g>')

    # ── Stars ─────────────────────────────────────────────────────────────────
    lines.append('  <g clip-path="url(#skyClip)">')
    for name, vmag, x, y in sorted(visible_stars, key=lambda s: -s[1]):
        r  = star_radius(vmag)
        sc = star_color(vmag)
        fid = "bigGlow" if vmag < 1.0 else "glow"
        lines.append(f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" '
                     f'fill="{sc}" filter="url(#{fid})" opacity="0.95"/>')
        # Halo for very bright stars
        if vmag < 0.5:
            lines.append(f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="{r*3.5:.2f}" '
                         f'fill="{sc}" opacity="0.08"/>')
    lines.append('  </g>')

    # ── Star labels ───────────────────────────────────────────────────────────
    lines.append('  <g clip-path="url(#skyClip)" filter="url(#labelShadow)">')
    for name, vmag, x, y in visible_stars:
        if vmag <= LABEL_MAG_LIMIT:
            lx = x + star_radius(vmag) + 3
            ly = y - 2
            fs = max(7, int(10 - vmag * 1.5))
            lines.append(f'    <text x="{lx:.1f}" y="{ly:.1f}" '
                         f'font-family="Georgia, serif" font-size="{fs}" '
                         f'fill="#aaccff" opacity="0.85">{name}</text>')
    lines.append('  </g>')

    # ── Horizon circle ────────────────────────────────────────────────────────
    lines.append(f'  <circle cx="{CX}" cy="{CY}" r="{RADIUS}" '
                 f'fill="none" stroke="#2255aa" stroke-width="1.5" opacity="0.7"/>')
    lines.append(f'  <circle cx="{CX}" cy="{CY}" r="{RADIUS}" fill="url(#horizonGlow)"/>')

    # ── Cardinal labels ───────────────────────────────────────────────────────
    offsets = {"N": (0, -1, 0, -8), "S": (0, 1, 0, 14),
               "E": (1, 0, 10, 4), "W": (-1, 0, -14, 4)}
    for label, (sx, sy, ox, oy) in offsets.items():
        cx2 = CX + sx * (RADIUS + 18) + ox
        cy2 = CY + sy * (RADIUS + 18) + oy
        lines.append(f'  <text x="{cx2:.0f}" y="{cy2:.0f}" text-anchor="middle" '
                     f'font-family="monospace" font-size="13" font-weight="bold" '
                     f'fill="#6699cc" letter-spacing="1">{label}</text>')

    # ── Altitude labels ───────────────────────────────────────────────────────
    for alt_line in [30, 60]:
        rho = (90 - alt_line) / 90 * RADIUS
        lines.append(f'  <text x="{CX + 3:.0f}" y="{CY - rho + 10:.0f}" '
                     f'font-family="monospace" font-size="8" fill="#336699" '
                     f'opacity="0.6">{alt_line}°</text>')

    # ── Title block ───────────────────────────────────────────────────────────
    ty = SVG_SIZE + 25
    lines.append(f'  <text x="{CX}" y="{ty}" text-anchor="middle" '
                 f'font-family="Georgia, \'Times New Roman\', serif" font-size="22" '
                 f'font-weight="bold" fill="#d0e8ff" letter-spacing="2">{title}</text>')
    lines.append(f'  <text x="{CX}" y="{ty + 24}" text-anchor="middle" '
                 f'font-family="Georgia, \'Times New Roman\', serif" font-size="12" '
                 f'fill="#6688aa" letter-spacing="1">{subtitle}</text>')
    coord_str = f"{abs(lat):.2f}°{'N' if lat >= 0 else 'S'}  {abs(lon):.2f}°{'E' if lon >= 0 else 'W'}"
    lines.append(f'  <text x="{CX}" y="{ty + 45}" text-anchor="middle" '
                 f'font-family="monospace" font-size="10" fill="#445566">{coord_str}</text>')

    lines.append('</svg>')
    return '\n'.join(lines)


def _milky_way_path() -> str:
    """Returns an artistic SVG blob representing the Milky Way band."""
    # Pre-rendered as a soft elliptical arc through the sky dome
    # (stylistic, not astrometrically precise — shifts with season/location)
    return (
        '<ellipse cx="400" cy="400" rx="320" ry="95" '
        'transform="rotate(35 400 400)" '
        'fill="none" stroke="#ffffff" stroke-width="55" '
        'opacity="0.03" stroke-opacity="0.06"/>'
        '<ellipse cx="400" cy="400" rx="310" ry="80" '
        'transform="rotate(35 400 400)" '
        'fill="none" stroke="#aaccff" stroke-width="30" '
        'opacity="0.025" stroke-opacity="0.04"/>'
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="AstroMap — generate a beautiful SVG star map",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--lat",   type=float, default=40.7128,
                   help="Observer latitude  (default 40.71 = New York)")
    p.add_argument("--lon",   type=float, default=-74.0060,
                   help="Observer longitude (default -74.01 = New York)")
    p.add_argument("--date",  default=None,
                   help="UTC date/time 'YYYY-MM-DD HH:MM' (default: now)")
    p.add_argument("--title", default="The Night Sky",
                   help="Map title text")
    p.add_argument("--out",   default="starmap.svg",
                   help="Output SVG filename (default: starmap.svg)")
    p.add_argument("--min-alt", type=float, default=-5.0,
                   help="Minimum altitude to plot (default -5° for horizon stars)")
    p.add_argument("--mag-limit", type=float, default=4.0,
                   help="Faintest magnitude to plot (default 4.0)")
    return p.parse_args()


def main():
    args = parse_args()

    if args.date:
        try:
            dt = datetime.strptime(args.date, "%Y-%m-%d %H:%M")
            dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Error: --date must be 'YYYY-MM-DD HH:MM' (got '{args.date}')",
                  file=sys.stderr)
            sys.exit(1)
    else:
        dt = datetime.now(timezone.utc)

    jd   = julian_day(dt)
    lat  = args.lat
    lon  = args.lon

    # ── Build star index for constellation lookups ────────────────────────────
    star_index = {name: (ra, dec, vmag) for name, ra, dec, vmag in STARS}

    # ── Compute visible stars ─────────────────────────────────────────────────
    visible_stars = []
    star_positions = {}   # name → (x, y) for constellation lines

    for name, ra, dec, vmag in STARS:
        if vmag > args.mag_limit:
            continue
        alt, az = equatorial_to_horizontal(ra, dec, lat, lon, jd)
        if alt < args.min_alt:
            continue
        x, y = stereographic_project(alt, az, CX, CY, RADIUS)
        visible_stars.append((name, vmag, x, y))
        star_positions[name] = (x, y)

    # ── Build constellation segments ──────────────────────────────────────────
    segments = []
    for const_name, pairs in CONSTELLATIONS.items():
        for s1, s2 in pairs:
            if s1 not in star_positions or s2 not in star_positions:
                continue
            x1, y1 = star_positions[s1]
            x2, y2 = star_positions[s2]
            segments.append((x1, y1, x2, y2))

    # ── Format subtitle ───────────────────────────────────────────────────────
    subtitle = dt.strftime("%B %-d, %Y  ·  %H:%M UTC")

    # ── Render ───────────────────────────────────────────────────────────────
    svg = build_svg(visible_stars, segments, args.title, subtitle, lat, lon)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"✓  {len(visible_stars)} stars plotted  ·  {len(segments)} constellation segments")
    print(f"✓  Saved → {args.out}")


if __name__ == "__main__":
    main()
