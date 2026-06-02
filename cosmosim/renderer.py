from __future__ import annotations
import sys
import shutil
import numpy as np
from typing import List, Tuple
from .bodies import Body

RST  = '\033[0m'
BOLD = '\033[1m'
DIM  = '\033[2m'

def fg256(n: int) -> str:
    return f'\033[38;5;{n}m'

# Border / UI colors
BORDER  = fg256(39)   # bright cyan
TITLE   = fg256(87)   # light blue
STAT    = fg256(250)  # light grey
ENERGY  = fg256(220)  # gold

TRAIL_DENSITY = ['.', '·', '•', '◦', '○']


class Renderer:
    def __init__(self, scale: float = 1.0):
        self.view_scale = scale

    def _term_size(self) -> Tuple[int, int]:
        sz = shutil.get_terminal_size((120, 40))
        w = min(sz.columns, 200)
        h = max(sz.lines - 8, 20)
        return w, h

    def _to_screen(self, pos: np.ndarray, cx: float, cy: float,
                   w: int, h: int) -> Tuple[int, int]:
        # x is squeezed by 0.5 because terminal chars are ~2× taller than wide
        sx = int((pos[0] - cx) * self.view_scale * 0.5 + w // 2)
        sy = int((pos[1] - cy) * self.view_scale + h // 2)
        return sx, sy

    def render(self, bodies: List[Body], step: int, t: float,
               name: str, com: np.ndarray, energy: float) -> None:
        w, h = self._term_size()
        cx, cy = float(com[0]), float(com[1])

        # char + color grids
        chars  = [[' '] * w for _ in range(h)]
        colors = [[''] * w for _ in range(h)]

        # Trails (dim, fading from old → new)
        for body in bodies:
            n = len(body.trail)
            for i, pos in enumerate(body.trail):
                sx, sy = self._to_screen(pos, cx, cy, w, h)
                if 0 <= sx < w and 0 <= sy < h:
                    frac = i / max(n - 1, 1)
                    idx  = min(int(frac * len(TRAIL_DENSITY)), len(TRAIL_DENSITY) - 1)
                    chars[sy][sx]  = TRAIL_DENSITY[idx]
                    colors[sy][sx] = DIM + body.color

        # Bodies (on top of trails)
        for body in bodies:
            sx, sy = self._to_screen(body.pos, cx, cy, w, h)
            if 0 <= sx < w and 0 <= sy < h:
                chars[sy][sx]  = body.symbol
                colors[sy][sx] = BOLD + body.color

        # ── Compose output buffer ────────────────────────────────────────────
        out: List[str] = ['\033[H']  # cursor → home (no flicker vs. clear)

        bar = '━' * w
        out.append(f'{BOLD}{BORDER}{bar}{RST}')

        title_str = f'  ✦ COSMOSIM  │  {name}  │  t = {t:9.3f}  │  step {step:>8d}  '
        out.append(f'{BOLD}{TITLE}{title_str:^{w}}{RST}')
        out.append(f'{BOLD}{BORDER}{bar}{RST}')

        for y, (char_row, color_row) in enumerate(zip(chars, colors)):
            line = ''
            for ch, col in zip(char_row, color_row):
                if ch != ' ':
                    line += col + ch + RST
                else:
                    line += ' '
            out.append(line)

        out.append(f'{BOLD}{BORDER}{bar}{RST}')

        # Legend line
        legend = '  '.join(
            f'{b.color}{b.symbol}{RST} {b.name}' for b in bodies[:10]
        )
        e_str = f'{ENERGY}E={energy:+.1f}{RST}'
        footer = f'{STAT}  ▸ {legend}   {e_str}   [Ctrl+C to quit]{RST}'
        out.append(footer)

        sys.stdout.write('\n'.join(out) + '\n')
        sys.stdout.flush()
