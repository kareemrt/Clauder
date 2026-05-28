"""Color palettes and gradient mapping for fractal rendering."""

import math
import colorsys
from dataclasses import dataclass


@dataclass
class Color:
    r: int
    g: int
    b: int

    def to_ansi_fg(self) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m"

    def to_ansi_bg(self) -> str:
        return f"\033[48;2;{self.r};{self.g};{self.b}m"


RESET = "\033[0m"


def _lerp_color(a: Color, b: Color, t: float) -> Color:
    t = max(0.0, min(1.0, t))
    return Color(
        int(a.r + (b.r - a.r) * t),
        int(a.g + (b.g - a.g) * t),
        int(a.b + (b.b - a.b) * t),
    )


def _gradient(stops: list[tuple[float, Color]], t: float) -> Color:
    """Interpolate along a multi-stop gradient; t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            local = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
            return _lerp_color(c0, c1, local)
    return stops[-1][1]


# ── Palette functions: (smooth_val, max_iter) → Color ─────────────────────────

def fire(smooth: float, max_iter: int) -> Color:
    """Incandescent fire — black → red → orange → yellow → white."""
    if smooth == 0.0:
        return Color(0, 0, 0)
    t = (smooth % max_iter) / max_iter
    stops = [
        (0.00, Color(0, 0, 0)),
        (0.25, Color(128, 0, 0)),
        (0.50, Color(255, 64, 0)),
        (0.70, Color(255, 180, 0)),
        (0.85, Color(255, 255, 100)),
        (1.00, Color(255, 255, 255)),
    ]
    return _gradient(stops, t)


def ocean(smooth: float, max_iter: int) -> Color:
    """Deep ocean — midnight blue → teal → cyan → white foam."""
    if smooth == 0.0:
        return Color(0, 5, 30)
    t = (smooth % max_iter) / max_iter
    stops = [
        (0.00, Color(0, 0, 50)),
        (0.30, Color(0, 50, 130)),
        (0.55, Color(0, 140, 180)),
        (0.75, Color(0, 210, 220)),
        (0.90, Color(100, 240, 240)),
        (1.00, Color(255, 255, 255)),
    ]
    return _gradient(stops, t)


def galaxy(smooth: float, max_iter: int) -> Color:
    """Cosmic nebula — deep purple → violet → blue → starlight."""
    if smooth == 0.0:
        return Color(2, 0, 10)
    t = (smooth % max_iter) / max_iter
    stops = [
        (0.00, Color(5, 0, 20)),
        (0.20, Color(60, 0, 80)),
        (0.40, Color(120, 0, 160)),
        (0.60, Color(80, 80, 220)),
        (0.80, Color(140, 180, 255)),
        (1.00, Color(255, 255, 255)),
    ]
    return _gradient(stops, t)


def psychedelic(smooth: float, max_iter: int) -> Color:
    """Cycling rainbow hues — full HSV spectrum rotation."""
    if smooth == 0.0:
        return Color(0, 0, 0)
    hue = (smooth * 0.05) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return Color(int(r * 255), int(g * 255), int(b * 255))


def electric(smooth: float, max_iter: int) -> Color:
    """Electric cyan on black — lightning bolt aesthetic."""
    if smooth == 0.0:
        return Color(0, 0, 0)
    t = math.sin((smooth / max_iter) * math.pi * 6) * 0.5 + 0.5
    stops = [
        (0.00, Color(0, 0, 0)),
        (0.30, Color(0, 40, 80)),
        (0.60, Color(0, 160, 220)),
        (0.85, Color(80, 240, 255)),
        (1.00, Color(255, 255, 255)),
    ]
    return _gradient(stops, t)


def newton_palette(smooth: float, max_iter: int) -> Color:
    """Three-basin coloring for Newton fractals."""
    if smooth == 0.0:
        return Color(10, 10, 10)
    basin = int(smooth / 100.0) % 3
    speed = (smooth % 100.0) / 100.0
    base_colors = [
        (Color(180, 20, 20), Color(255, 120, 120)),   # red root
        (Color(20, 140, 20), Color(120, 255, 120)),   # green root
        (Color(20, 60, 200), Color(120, 160, 255)),   # blue root
    ]
    dark, light = base_colors[basin]
    return _lerp_color(dark, light, speed)


def monochrome(smooth: float, max_iter: int) -> Color:
    """Classic black-and-white with smooth shading."""
    if smooth == 0.0:
        return Color(0, 0, 0)
    t = (smooth % max_iter) / max_iter
    v = int(t * 255)
    return Color(v, v, v)


PALETTES: dict[str, callable] = {
    "fire": fire,
    "ocean": ocean,
    "galaxy": galaxy,
    "psychedelic": psychedelic,
    "electric": electric,
    "newton": newton_palette,
    "mono": monochrome,
}
