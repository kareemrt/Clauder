import os
import sys
import numpy as np

# ---------------------------------------------------------------------------
# ANSI helpers
# ---------------------------------------------------------------------------

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"

FG = {
    "blue":           "\033[34m",
    "bright_yellow":  "\033[93m",
    "bright_cyan":    "\033[96m",
    "bright_red":     "\033[91m",
    "bright_green":   "\033[92m",
    "bright_magenta": "\033[95m",
    "bright_white":   "\033[97m",
    "yellow":         "\033[33m",
    "cyan":           "\033[36m",
    "magenta":        "\033[35m",
    "white":          "\033[37m",
}

BODY_SYMBOLS = ["●", "★", "◆", "▲", "♦", "✦", "⊕", "⊗"]
BODY_COLORS  = [
    FG["bright_yellow"],
    FG["bright_cyan"],
    FG["bright_red"],
    FG["bright_green"],
    FG["bright_magenta"],
    FG["bright_white"],
    FG["yellow"],
    FG["cyan"],
]
TRAIL_CHARS = ["●", "·", "·", ".", " "]  # index 0 = newest trail point


def _term_size() -> tuple[int, int]:
    try:
        c, r = os.get_terminal_size()
        return c, r
    except OSError:
        return 120, 40


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

class Renderer:
    """
    Maps simulation world-coordinates to a fixed-size terminal grid and
    emits a full-screen ANSI frame on each call to render().
    """

    _HEADER = 2
    _FOOTER = 3

    def __init__(self, width: int | None = None, height: int | None = None):
        tw, th = _term_size()
        self.width  = width  or (tw - 2)
        self.height = height or (th - self._HEADER - self._FOOTER - 2)
        self._frame = 0

    # ------------------------------------------------------------------
    # Coordinate mapping
    # ------------------------------------------------------------------

    def _viewport(self, bodies):
        """Return (cx, cy, scale) that fits all bodies + recent trails."""
        pts = [b.pos for b in bodies]
        for b in bodies:
            pts.extend(b.trail[-20:])

        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx = (min(xs) + max(xs)) / 2
        cy = (min(ys) + max(ys)) / 2

        span_x = max(xs) - min(xs) or 1.0
        span_y = max(ys) - min(ys) or 1.0
        # Terminal cells are ~2× taller than wide; compensate with 0.5 factor
        scale = min(
            (self.width  - 4) / span_x,
            (self.height - 2) / (span_y * 0.5),
        ) * 0.85
        return cx, cy, scale

    def _to_screen(self, wx, wy, cx, cy, scale) -> tuple[int, int]:
        sx = int((wx - cx) * scale        + self.width  / 2)
        sy = int((cy - wy) * scale * 0.5  + self.height / 2)  # flip Y
        return sx, sy

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, sim, fps: float = 0.0):
        bodies = sim.bodies
        cx, cy, scale = self._viewport(bodies)

        chars      = [[" "] * self.width for _ in range(self.height)]
        color_grid = [[""  ] * self.width for _ in range(self.height)]

        # Draw trails (oldest first so newer overwrites)
        for body in bodies:
            n = len(body.trail)
            for t, tp in enumerate(body.trail):
                sx, sy = self._to_screen(tp[0], tp[1], cx, cy, scale)
                if 0 <= sx < self.width and 0 <= sy < self.height:
                    age_ratio = t / max(n - 1, 1)  # 0=oldest, 1=newest
                    ci = int((1 - age_ratio) * (len(TRAIL_CHARS) - 1))
                    chars[sy][sx]       = TRAIL_CHARS[ci]
                    color_grid[sy][sx]  = FG["blue"]

        # Draw bodies (on top of trails)
        for i, body in enumerate(bodies):
            sx, sy = self._to_screen(body.pos[0], body.pos[1], cx, cy, scale)
            if 0 <= sx < self.width and 0 <= sy < self.height:
                chars[sy][sx]      = BODY_SYMBOLS[i % len(BODY_SYMBOLS)]
                color_grid[sy][sx] = BODY_COLORS [i % len(BODY_COLORS)]

        # Build output buffer
        buf: list[str] = []
        buf.append(
            f"{BOLD}{FG['bright_cyan']}"
            f"  ✦ NEBULA — N-Body Gravitational Simulator  "
            f"│ t={sim.time:8.3f} │ step={sim.steps:6d} │ fps={fps:5.1f}"
            f"{RESET}"
        )
        buf.append(FG["blue"] + "─" * self.width + RESET)

        for row_chars, row_cols in zip(chars, color_grid):
            line = ""
            for ch, col in zip(row_chars, row_cols):
                line += (col + ch + RESET) if col else ch
            buf.append(line)

        buf.append(FG["blue"] + "─" * self.width + RESET)

        stat_parts = []
        for i, body in enumerate(bodies):
            col  = BODY_COLORS[i % len(BODY_COLORS)]
            sym  = BODY_SYMBOLS[i % len(BODY_SYMBOLS)]
            spd  = float(np.linalg.norm(body.vel))
            name = body.name or f"Body {i+1}"
            stat_parts.append(f"{col}{sym} {name:<8s} m={body.mass:<5.1f} v={spd:.3f}{RESET}")
        buf.append("  " + "  │  ".join(stat_parts))

        ke = sim.kinetic_energy()
        pe = sim.potential_energy()
        buf.append(
            f"  {FG['bright_cyan']}KE={ke:9.4f}  PE={pe:9.4f}  "
            f"E={ke + pe:9.4f}{RESET}   {DIM}Ctrl-C to quit{RESET}"
        )

        sys.stdout.write("\033[H\033[2J" + "\n".join(buf) + "\n")
        sys.stdout.flush()
        self._frame += 1
