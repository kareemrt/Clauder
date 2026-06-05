"""Color palettes and ANSI terminal color utilities."""

import math
from typing import Tuple

Rgb = Tuple[int, int, int]

RESET = "\033[0m"
BOLD  = "\033[1m"


def ansi_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def ansi_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


def _clamp(v: float) -> int:
    return max(0, min(255, int(v)))


def palette_fire(t: float) -> Rgb:
    r = _clamp(t * 3 * 255)
    g = _clamp(t * 3 * 255 - 255)
    b = _clamp(t * 3 * 255 - 510)
    return r, g, b


def palette_ocean(t: float) -> Rgb:
    return _clamp(t * 30), _clamp(100 + t * 155), _clamp(150 + t * 105)


def palette_matrix(t: float) -> Rgb:
    return 0, _clamp(t * 255), _clamp(t * 80)


def palette_plasma(t: float) -> Rgb:
    r = _clamp(127.5 + 127.5 * math.sin(t * math.pi * 2))
    g = _clamp(127.5 + 127.5 * math.sin(t * math.pi * 2 + 2.094))
    b = _clamp(127.5 + 127.5 * math.sin(t * math.pi * 2 + 4.189))
    return r, g, b


def palette_gold(t: float) -> Rgb:
    return _clamp(min(255, t * 2 * 255)), _clamp(t * 1.5 * 200), _clamp(t * 50)


def palette_neon(t: float) -> Rgb:
    r = _clamp(127.5 + 127.5 * math.sin(t * math.pi * 4))
    g = _clamp(50 + 205 * t)
    b = _clamp(200 + 55 * math.sin(t * math.pi * 6))
    return r, g, b


PALETTES: dict = {
    "fire":   palette_fire,
    "ocean":  palette_ocean,
    "matrix": palette_matrix,
    "plasma": palette_plasma,
    "gold":   palette_gold,
    "neon":   palette_neon,
}

ASCII_SETS: dict = {
    "dense":   list("@#S%?*+;:,. "),
    "blocks":  list("█▓▒░ "),
    "dots":    list("●◉◎○ "),
    "classic": list("@%#*+=-:. "),
    "simple":  list("#. "),
}


def iter_to_char(iters: int, max_iters: int, charset: str = "dense") -> str:
    chars = ASCII_SETS.get(charset, ASCII_SETS["dense"])
    if iters == max_iters:
        return chars[-1]
    t = iters / max_iters
    idx = int(t * (len(chars) - 1))
    return chars[idx]


def iter_to_color(iters: int, max_iters: int, palette: str = "plasma") -> Rgb:
    fn = PALETTES.get(palette, palette_plasma)
    if iters == max_iters:
        return 0, 0, 0
    t = iters / max_iters
    # Smooth coloring: use log for nicer gradients
    smooth_t = (t + 0.5 * math.sin(t * math.pi * 8)) % 1.0
    return fn(smooth_t)
