"""ANSI color palettes for fractal rendering."""

# 256-color ANSI escape
def fg(n: int) -> str:
    return f"\x1b[38;5;{n}m"

def bg(n: int) -> str:
    return f"\x1b[48;5;{n}m"

RESET = "\x1b[0m"

# Each palette maps escape count [0..1] -> (char, ansi_color_code)
# Characters ordered light -> dense for smooth gradients
CHARS_SMOOTH = " .:;+=xX$&#"
CHARS_FIRE   = " .,:-+*%@#"
CHARS_MATRIX = " ░▒▓█"
CHARS_MINIMAL = " .oO@"

def _interp(t: float, stops: list[int]) -> int:
    """Linearly interpolate through a list of 256-color indices."""
    if t <= 0:
        return stops[0]
    if t >= 1:
        return stops[-1]
    seg = t * (len(stops) - 1)
    lo = int(seg)
    hi = min(lo + 1, len(stops) - 1)
    frac = seg - lo
    # nearest-neighbor for 256-color (no true blending)
    return stops[hi] if frac >= 0.5 else stops[lo]

PALETTES: dict[str, dict] = {
    "cosmic": {
        "name": "Cosmic",
        "chars": CHARS_SMOOTH,
        "color_stops": [16, 17, 18, 19, 20, 21, 27, 33, 39, 45, 51, 87, 123, 159, 195, 231],
        "interior": (bg(16), " "),
    },
    "fire": {
        "name": "Fire",
        "chars": CHARS_FIRE,
        "color_stops": [16, 52, 88, 124, 160, 196, 202, 208, 214, 220, 226, 227, 228, 229, 230, 231],
        "interior": (bg(16), "█"),
    },
    "matrix": {
        "name": "Matrix",
        "chars": CHARS_MATRIX,
        "color_stops": [16, 22, 28, 34, 40, 46, 82, 118, 154, 190, 226, 231],
        "interior": (bg(16), " "),
    },
    "ocean": {
        "name": "Ocean",
        "chars": CHARS_SMOOTH,
        "color_stops": [16, 17, 18, 19, 24, 25, 26, 27, 32, 33, 38, 39, 44, 45, 50, 51],
        "interior": (bg(17), " "),
    },
    "neon": {
        "name": "Neon",
        "chars": CHARS_SMOOTH,
        "color_stops": [16, 90, 91, 92, 93, 99, 105, 111, 117, 123, 159, 195, 219, 213, 207, 201],
        "interior": (bg(16), " "),
    },
    "gold": {
        "name": "Gold",
        "chars": CHARS_SMOOTH,
        "color_stops": [16, 52, 58, 94, 100, 136, 172, 178, 214, 220, 226, 227, 228, 229, 230, 231],
        "interior": (bg(52), " "),
    },
}

def colorize(t: float, palette_name: str) -> str:
    """Return ANSI prefix for a normalized escape value t in [0,1]."""
    p = PALETTES[palette_name]
    stops = p["color_stops"]
    code = _interp(t, stops)
    n_chars = len(p["chars"])
    char_idx = min(int(t * n_chars), n_chars - 1)
    char = p["chars"][char_idx]
    return f"{fg(code)}{char}"
