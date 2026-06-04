"""
Rendering engine — converts a point cloud into a density image and applies color.

Two render paths:
  - render_image(): produces a PIL/matplotlib image saved to disk
  - render_ascii():  produces a terminal-printable ASCII art string
"""

import numpy as np
from pathlib import Path
from typing import Tuple

from .themes import get_theme


# ── Core density computation ─────────────────────────────────────────────────

def _build_density(pts: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Bin a (N, 2) point cloud into a (height, width) density histogram.
    Returns float32 array normalized to [0, 1].
    """
    x, y = pts[:, 0], pts[:, 1]

    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    margin_x = (x_max - x_min) * 0.02
    margin_y = (y_max - y_min) * 0.02
    x_min -= margin_x; x_max += margin_x
    y_min -= margin_y; y_max += margin_y

    xi = ((x - x_min) / (x_max - x_min) * (width  - 1)).astype(np.int32)
    yi = ((y - y_min) / (y_max - y_min) * (height - 1)).astype(np.int32)

    np.clip(xi, 0, width  - 1, out=xi)
    np.clip(yi, 0, height - 1, out=yi)

    density = np.zeros((height, width), dtype=np.float32)
    np.add.at(density, (yi, xi), 1)

    # Log-scale so dim regions are still visible
    density = np.log1p(density)

    max_d = density.max()
    if max_d > 0:
        density /= max_d

    return density


# ── Image renderer ───────────────────────────────────────────────────────────

def render_image(
    pts: np.ndarray,
    output_path: str | Path,
    width: int = 1920,
    height: int = 1080,
    theme: str = "plasma",
    dpi: int = 150,
    gamma: float = 0.5,
) -> Path:
    """
    Render a point cloud to a high-resolution PNG image.

    Args:
        pts:         (N, 2) float32 array of projected attractor points.
        output_path: Destination file path (PNG).
        width:       Image width in pixels.
        height:      Image height in pixels.
        theme:       Color theme name (see themes.py).
        dpi:         Resolution for matplotlib figure.
        gamma:       Gamma correction (< 1 brightens dim regions).

    Returns:
        Resolved Path to the saved image.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    bg_hex, cmap_name = get_theme(theme)

    density = _build_density(pts, width, height)
    density = np.power(density, gamma)

    cmap = plt.get_cmap(cmap_name)
    rgba = cmap(density)

    # Mask zero-density pixels as background color
    bg_rgb = mcolors.to_rgb(bg_hex)
    zero_mask = density == 0
    rgba[zero_mask, 0] = bg_rgb[0]
    rgba[zero_mask, 1] = bg_rgb[1]
    rgba[zero_mask, 2] = bg_rgb[2]
    rgba[zero_mask, 3] = 1.0

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    ax.imshow(rgba, origin="lower", aspect="auto", interpolation="nearest")
    ax.axis("off")
    plt.tight_layout(pad=0)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi, bbox_inches="tight", pad_inches=0, facecolor=bg_hex)
    plt.close(fig)
    return out


# ── ASCII renderer ───────────────────────────────────────────────────────────

_ASCII_PALETTE = " .:;+=xX$&#@"

_ANSI_THEMES = {
    "plasma":  ["\033[38;5;57m", "\033[38;5;93m", "\033[38;5;129m",
                "\033[38;5;165m", "\033[38;5;201m", "\033[38;5;207m",
                "\033[38;5;213m", "\033[38;5;220m", "\033[38;5;227m"],
    "ember":   ["\033[38;5;52m", "\033[38;5;88m", "\033[38;5;124m",
                "\033[38;5;160m", "\033[38;5;196m", "\033[38;5;202m",
                "\033[38;5;208m", "\033[38;5;214m", "\033[38;5;220m"],
    "galaxy":  ["\033[38;5;17m", "\033[38;5;18m", "\033[38;5;19m",
                "\033[38;5;25m", "\033[38;5;32m", "\033[38;5;39m",
                "\033[38;5;51m", "\033[38;5;195m", "\033[38;5;231m"],
    "forest":  ["\033[38;5;22m", "\033[38;5;28m", "\033[38;5;34m",
                "\033[38;5;40m", "\033[38;5;46m", "\033[38;5;82m",
                "\033[38;5;118m","\033[38;5;154m","\033[38;5;190m"],
}
_RESET = "\033[0m"


def render_ascii(
    pts: np.ndarray,
    width: int = 120,
    height: int = 40,
    theme: str = "plasma",
    color: bool = True,
) -> str:
    """
    Render a point cloud to a colored ASCII art string.

    Args:
        pts:    (N, 2) float32 array.
        width:  Character columns.
        height: Character rows.
        theme:  Color theme for ANSI coloring.
        color:  If False, skip ANSI codes (plain ASCII).

    Returns:
        Multi-line string suitable for print().
    """
    density = _build_density(pts, width, height)
    palette = _ASCII_PALETTE
    n_chars = len(palette)

    ansi_colors = _ANSI_THEMES.get(theme, _ANSI_THEMES["plasma"]) if color else None

    lines = []
    for row in reversed(range(height)):
        line = []
        for col in range(width):
            d = density[row, col]
            idx = int(d * (n_chars - 1))
            ch = palette[idx]
            if ansi_colors and d > 0:
                color_idx = min(int(d * (len(ansi_colors) - 1)), len(ansi_colors) - 1)
                ch = ansi_colors[color_idx] + ch + _RESET
            line.append(ch)
        lines.append("".join(line))

    return "\n".join(lines)
