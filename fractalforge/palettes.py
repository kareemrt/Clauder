"""Color palettes for fractal rendering."""

from colorama import Fore, Back, Style

# Each palette maps an iteration ratio [0.0, 1.0] to an ANSI color + character.
# Palettes are lists of (threshold, fg_color, char) tuples, sorted ascending.

CHARS_DENSE  = " .:-=+*#%@"
CHARS_BLOCKS = " ░▒▓█"
CHARS_MATH   = " .,;:!|/\\(){}[]"

def _gradient(colors, n):
    """Interpolate a list of ANSI colors into n steps."""
    result = []
    buckets = len(colors) - 1
    for i in range(n):
        idx = int(i / n * buckets)
        result.append(colors[min(idx, buckets - 1)])
    return result


PALETTES = {
    "fire": [
        Fore.WHITE, Fore.YELLOW, Fore.YELLOW, Fore.RED, Fore.RED,
        Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.WHITE, Fore.BLACK,
    ],
    "ocean": [
        Fore.WHITE, Fore.CYAN, Fore.CYAN, Fore.BLUE, Fore.BLUE,
        Fore.MAGENTA, Fore.WHITE, Fore.CYAN, Fore.BLUE, Fore.BLACK,
    ],
    "neon": [
        Fore.WHITE, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA,
        Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLACK,
    ],
    "grayscale": [
        Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE,
        Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.BLACK,
    ],
    "rainbow": [
        Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN,
        Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.YELLOW,
        Fore.WHITE, Fore.BLACK,
    ],
    "matrix": [
        Fore.GREEN, Fore.GREEN, Fore.GREEN, Fore.GREEN,
        Fore.GREEN, Fore.GREEN, Fore.GREEN, Fore.GREEN,
        Fore.WHITE, Fore.BLACK,
    ],
}


def color_for_iters(iters, max_iters, palette_name="fire"):
    """Return (ansi_color, char) for a given iteration count."""
    palette = PALETTES.get(palette_name, PALETTES["fire"])
    chars = CHARS_DENSE

    if iters == max_iters:
        return Fore.BLACK, " "

    ratio = iters / max_iters
    bucket = min(int(ratio * (len(palette) - 1)), len(palette) - 2)
    color = palette[bucket]

    char_idx = min(int(ratio * (len(chars) - 1)), len(chars) - 1)
    char = chars[char_idx]

    return color, char


def list_palettes():
    return list(PALETTES.keys())
