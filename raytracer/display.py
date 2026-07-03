"""Terminal display: convert float pixels → ASCII art with optional ANSI color."""

import sys
import os
from .vector import Vec3

# Characters ordered dark → bright (physically: low → high luminance)
_RAMP_DARK  = " .,:;+*?%S#@"
_RAMP_DENSE = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

GAMMA = 2.2


def _gamma_correct(v: Vec3, gamma: float = GAMMA) -> Vec3:
    exp = 1.0 / gamma
    return Vec3(v.x ** exp, v.y ** exp, v.z ** exp)


def _to_ansi_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


RESET = "\033[0m"


class AsciiDisplay:
    def __init__(self, ramp: str = _RAMP_DENSE, color: bool = True):
        self.ramp = ramp
        self.color = color and _supports_color()

    # ── public API ─────────────────────────────────────────────────────────

    def frame_to_str(self, pixels: list) -> str:
        """Convert a 2-D list of Vec3 → printable string."""
        lines = []
        for row in pixels:
            parts = []
            for pixel in row:
                pixel = _gamma_correct(pixel)
                lum = pixel.luminance()
                ch = self._lum_to_char(lum)
                if self.color:
                    r = int(pixel.x * 255)
                    g = int(pixel.y * 255)
                    b = int(pixel.z * 255)
                    parts.append(f"{_to_ansi_fg(r, g, b)}{ch}{ch}{RESET}")
                else:
                    parts.append(ch + ch)  # doubled for aspect ratio
            lines.append("".join(parts))
        return "\n".join(lines)

    def print_frame(self, pixels: list, clear: bool = False) -> None:
        if clear:
            # move cursor to top-left without clearing (flicker-free)
            rows = len(pixels)
            sys.stdout.write(f"\033[{rows}A\r")
        sys.stdout.write(self.frame_to_str(pixels) + "\n")
        sys.stdout.flush()

    # ── private ────────────────────────────────────────────────────────────

    def _lum_to_char(self, lum: float) -> str:
        lum = max(0.0, min(1.0, lum))
        idx = int(lum * (len(self.ramp) - 1))
        return self.ramp[idx]


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
