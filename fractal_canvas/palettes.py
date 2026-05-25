"""
Color palettes and ASCII character sets for fractal rendering.
"""

from typing import List


def _fg(n: int) -> str:
    """ANSI 256-color foreground escape code."""
    return f"\033[38;5;{n}m"


RESET = "\033[0m"
BOLD  = "\033[1m"


# Character sets ordered dense → sparse (more ink = lower iteration counts)
CHAR_SETS: dict = {
    "ultra":    list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "),
    "standard": list("@#S%?*+;:,. "),
    "blocks":   ["█", "▓", "▒", "░", " "],
    "braille":  ["⣿", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾", "⣶", "⣮", "⣬", "⣤", "⣀", "⡀", " "],
    "minimal":  list("#. "),
    "binary":   list("10 "),
}

COLOR_PALETTES: dict = {
    "fire":   [_fg(c) for c in [52, 88, 124, 160, 196, 202, 208, 214, 220, 226, 229, 231]],
    "ocean":  [_fg(c) for c in [17, 18, 19, 20, 21, 27, 33, 39, 45, 51, 87, 123, 159, 195, 231]],
    "forest": [_fg(c) for c in [22, 28, 34, 40, 46, 82, 118, 154, 190, 226, 228, 231]],
    "violet": [_fg(c) for c in [17, 54, 90, 126, 162, 198, 207, 213, 219, 225, 231]],
    "ice":    [_fg(c) for c in [17, 18, 19, 20, 21, 27, 33, 51, 87, 195, 231]],
    "gold":   [_fg(c) for c in [52, 58, 94, 130, 136, 172, 178, 214, 220, 226, 231]],
    "neon":   [_fg(c) for c in [46, 47, 48, 49, 50, 51, 45, 39, 33, 27, 21]],
    "mono":   [""],
}

# Per-root color palettes for Newton fractal basin colorization
NEWTON_ROOT_PALETTES: List[List[str]] = [
    [_fg(c) for c in [196, 202, 208, 214, 220, 226]],  # root 1 — red/orange
    [_fg(c) for c in [21,  27,  33,  39,  45,  51]],   # root 2 — blue/cyan
    [_fg(c) for c in [46,  82, 118, 154, 190, 226]],   # root 3 — green/yellow
]


def map_to_char(value: float, max_val: float, char_set: List[str]) -> str:
    if value >= max_val:
        return " "
    idx = int(value / max_val * (len(char_set) - 1))
    return char_set[min(idx, len(char_set) - 1)]


def map_to_color(value: float, max_val: float, palette: List[str]) -> str:
    if not palette or not palette[0]:
        return ""
    if value >= max_val:
        return ""
    idx = int(value / max_val * (len(palette) - 1))
    return palette[min(idx, len(palette) - 1)]
