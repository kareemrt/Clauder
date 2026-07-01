"""
Color palettes for fractal rendering.

Each palette maps a normalized [0, 1] value to an (R, G, B) tuple.
"""

import math
from typing import Tuple

RGB = Tuple[int, int, int]


def _lerp_color(t: float, stops: list) -> RGB:
    """Linearly interpolate between color stops. stops = [(pos, (r,g,b)), ...]"""
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= t <= p1:
            f = (t - p0) / (p1 - p0) if p1 > p0 else 0.0
            return tuple(int(c0[j] + f * (c1[j] - c0[j])) for j in range(3))
    return stops[-1][1]


def fire(t: float) -> RGB:
    stops = [
        (0.0,  (0,   0,   0)),
        (0.25, (128, 0,   0)),
        (0.5,  (255, 80,  0)),
        (0.75, (255, 220, 0)),
        (1.0,  (255, 255, 255)),
    ]
    return _lerp_color(t, stops)


def ice(t: float) -> RGB:
    stops = [
        (0.0,  (0,   0,   32)),
        (0.3,  (0,   64,  128)),
        (0.6,  (0,   180, 220)),
        (0.85, (180, 230, 255)),
        (1.0,  (255, 255, 255)),
    ]
    return _lerp_color(t, stops)


def electric(t: float) -> RGB:
    stops = [
        (0.0,  (0,   0,   0)),
        (0.2,  (20,  0,   80)),
        (0.5,  (80,  0,   200)),
        (0.7,  (0,   140, 255)),
        (0.9,  (180, 255, 255)),
        (1.0,  (255, 255, 255)),
    ]
    return _lerp_color(t, stops)


def gold(t: float) -> RGB:
    stops = [
        (0.0,  (0,   0,   0)),
        (0.3,  (80,  30,  0)),
        (0.6,  (200, 140, 0)),
        (0.85, (255, 220, 80)),
        (1.0,  (255, 255, 220)),
    ]
    return _lerp_color(t, stops)


def neon(t: float) -> RGB:
    # Cycling through vivid hues
    hue = (t * 4.0) % 1.0
    r = int(127 + 127 * math.cos(2 * math.pi * hue))
    g = int(127 + 127 * math.cos(2 * math.pi * (hue + 0.333)))
    b = int(127 + 127 * math.cos(2 * math.pi * (hue + 0.667)))
    # Fade to black near interior (t → 1 means interior)
    brightness = 1.0 - t ** 3
    return (int(r * brightness), int(g * brightness), int(b * brightness))


def classic(t: float) -> RGB:
    """The timeless blue-gold Mandelbrot palette."""
    stops = [
        (0.0,  (0,   7,   100)),
        (0.16, (32,  107, 203)),
        (0.42, (237, 255, 255)),
        (0.6425,(255, 170, 0)),
        (0.8575,(0,   2,   0)),
        (1.0,  (0,   7,   100)),
    ]
    return _lerp_color(t % 1.0, stops)


def aurora(t: float) -> RGB:
    stops = [
        (0.0,  (0,   0,   20)),
        (0.2,  (0,   40,  80)),
        (0.45, (0,   180, 120)),
        (0.7,  (100, 255, 180)),
        (0.9,  (200, 255, 240)),
        (1.0,  (255, 255, 255)),
    ]
    return _lerp_color(t, stops)


def sunset(t: float) -> RGB:
    stops = [
        (0.0,  (20,  0,   40)),
        (0.25, (120, 0,   80)),
        (0.5,  (220, 60,  20)),
        (0.75, (255, 140, 20)),
        (1.0,  (255, 220, 120)),
    ]
    return _lerp_color(t, stops)


PALETTES = {
    "fire":     fire,
    "ice":      ice,
    "electric": electric,
    "gold":     gold,
    "neon":     neon,
    "classic":  classic,
    "aurora":   aurora,
    "sunset":   sunset,
}
