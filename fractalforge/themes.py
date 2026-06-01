"""Color themes: gradient stop tables and ANSI true-color helpers."""

import math

# Each theme: list of (position, (R, G, B)) gradient stops + interior color.
THEMES: dict = {
    "fire": {
        "stops": [
            (0.00, (10, 0, 20)),
            (0.06, (70, 0, 30)),
            (0.20, (160, 20, 0)),
            (0.40, (220, 80, 0)),
            (0.60, (255, 160, 0)),
            (0.80, (255, 230, 80)),
            (1.00, (255, 255, 220)),
        ],
        "interior": (5, 0, 10),
    },
    "ocean": {
        "stops": [
            (0.00, (0, 0, 20)),
            (0.15, (0, 15, 90)),
            (0.35, (0, 55, 170)),
            (0.55, (0, 115, 205)),
            (0.75, (35, 175, 225)),
            (1.00, (185, 235, 255)),
        ],
        "interior": (0, 0, 12),
    },
    "neon": {
        "stops": [
            (0.00, (5, 0, 30)),
            (0.15, (90, 0, 190)),
            (0.30, (210, 0, 255)),
            (0.50, (255, 50, 110)),
            (0.70, (255, 205, 0)),
            (0.85, (100, 255, 100)),
            (1.00, (0, 255, 235)),
        ],
        "interior": (0, 0, 20),
    },
    "plasma": {
        "stops": [
            (0.00, (13, 8, 135)),
            (0.25, (126, 3, 168)),
            (0.50, (204, 71, 120)),
            (0.75, (248, 149, 64)),
            (1.00, (240, 249, 33)),
        ],
        "interior": (5, 2, 60),
    },
    "matrix": {
        "stops": [
            (0.00, (0, 5, 0)),
            (0.20, (0, 45, 0)),
            (0.50, (0, 125, 0)),
            (0.80, (0, 205, 30)),
            (1.00, (155, 255, 155)),
        ],
        "interior": (0, 2, 0),
    },
    "ice": {
        "stops": [
            (0.00, (0, 10, 35)),
            (0.25, (20, 85, 150)),
            (0.50, (105, 185, 225)),
            (0.75, (205, 235, 252)),
            (1.00, (245, 252, 255)),
        ],
        "interior": (0, 5, 18),
    },
    "mono": {
        "stops": [
            (0.00, (12, 12, 12)),
            (0.50, (125, 125, 125)),
            (1.00, (255, 255, 255)),
        ],
        "interior": (0, 0, 0),
    },
}

# Colors assigned to each Newton root (red, green, blue)
NEWTON_ROOT_COLORS = [
    (220, 60, 60),
    (60, 200, 60),
    (60, 100, 230),
]


def _lerp_stops(t: float, stops: list) -> tuple:
    """Linearly interpolate within a list of (position, color) stops."""
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for k in range(len(stops) - 1):
        t0, c0 = stops[k]
        t1, c1 = stops[k + 1]
        if t0 <= t <= t1:
            alpha = (t - t0) / (t1 - t0)
            return tuple(int(a + alpha * (b - a)) for a, b in zip(c0, c1))
    return stops[-1][1]


def get_color(t: float, theme_name: str) -> tuple:
    """Map a normalized value t in [0, 1] to an RGB tuple for the given theme."""
    theme = THEMES.get(theme_name, THEMES["fire"])
    return _lerp_stops(t, theme["stops"])


def get_interior(theme_name: str) -> tuple:
    """Return the interior (in-set) color for a theme."""
    return THEMES.get(theme_name, THEMES["fire"])["interior"]


# ── ANSI true-color helpers ──────────────────────────────────────────────────

def fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J\033[H"
BOLD = "\033[1m"
