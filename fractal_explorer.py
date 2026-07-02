#!/usr/bin/env python3
"""
MandelCLI — Terminal Fractal Explorer

An animated deep-dive into the Mandelbrot set, rendered with half-block Unicode
characters (▀▄) for 2× vertical resolution and 24-bit terminal color.

Usage:
    python3 fractal_explorer.py [--scheme SCHEME] [--target TARGET] [--fps FPS]
    python3 fractal_explorer.py --julia -0.7269 0.1889
    python3 fractal_explorer.py --list-targets
"""

import math
import sys
import time
import argparse
from typing import Tuple

import numpy as np
from rich.live import Live
from rich.console import Console
from rich.text import Text
from rich.panel import Panel


# ─── Color Schemes ────────────────────────────────────────────────────────────

def _make_colormap(n: int, recipe) -> np.ndarray:
    """Build an (N, 3) uint8 colormap from a callable recipe(t_array)."""
    t = np.linspace(0, 1, n)
    rgb = recipe(t)
    return np.clip(rgb, 0, 255).astype(np.uint8)


def _cm_psychedelic(t):
    freq = 6.0
    r = (0.5 + 0.5 * np.sin(freq * np.pi * t + 0.0)) * 255
    g = (0.5 + 0.5 * np.sin(freq * np.pi * t + 2.094)) * 255
    b = (0.5 + 0.5 * np.sin(freq * np.pi * t + 4.189)) * 255
    return np.stack([r, g, b], axis=-1)


def _cm_fire(t):
    r = np.clip(t * 3, 0, 1) * 255
    g = np.clip(t * 3 - 1, 0, 1) * 255
    b = np.clip(t * 3 - 2, 0, 1) * 255
    return np.stack([r, g, b], axis=-1)


def _cm_ocean(t):
    r = np.clip(t * 2 - 1, 0, 1) * 80
    g = np.clip(t * 3 - 1, 0, 1) * 200
    b = np.clip(t * 2, 0, 1) * 255
    return np.stack([r, g, b], axis=-1)


def _cm_gold(t):
    r = np.clip(t * 1.5, 0, 1) * 255
    g = np.clip(t * 2.5 - 0.8, 0, 1) * 200
    b = np.clip(t * 4 - 3.0, 0, 1) * 150
    return np.stack([r, g, b], axis=-1)


def _cm_ice(t):
    r = np.clip(t * 3 - 2, 0, 1) * 255
    g = np.clip(t * 2 - 0.5, 0, 1) * 240
    b = np.clip(t + 0.2, 0, 1) * 255
    return np.stack([r, g, b], axis=-1)


def _cm_plasma(t):
    r = (0.5 + 0.5 * np.sin(5 * np.pi * t + 0.5)) * 255
    g = (0.3 + 0.7 * t) * 255
    b = (0.5 + 0.5 * np.cos(4 * np.pi * t)) * 255
    return np.stack([r, g, b], axis=-1)


_CM_SIZE = 2048

COLORMAPS = {
    "psychedelic": _make_colormap(_CM_SIZE, _cm_psychedelic),
    "fire":        _make_colormap(_CM_SIZE, _cm_fire),
    "ocean":       _make_colormap(_CM_SIZE, _cm_ocean),
    "gold":        _make_colormap(_CM_SIZE, _cm_gold),
    "ice":         _make_colormap(_CM_SIZE, _cm_ice),
    "plasma":      _make_colormap(_CM_SIZE, _cm_plasma),
}


# ─── Fractal Computation ──────────────────────────────────────────────────────

def compute_mandelbrot(
    pixel_w: int,
    pixel_h: int,
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    max_iter: int,
) -> np.ndarray:
    """
    Vectorized Mandelbrot iteration.
    Returns smooth escape values in [0, 1]; 0 = interior (never escaped).
    """
    re = np.linspace(x_min, x_max, pixel_w, dtype=np.float64)
    im = np.linspace(y_max, y_min, pixel_h, dtype=np.float64)   # flip y
    C = re[np.newaxis, :] + 1j * im[:, np.newaxis]

    Z = np.zeros_like(C)
    escape = np.full(C.shape, max_iter, dtype=np.float64)
    active = np.ones(C.shape, dtype=bool)

    for n in range(max_iter):
        Z[active] = Z[active] ** 2 + C[active]
        just_escaped = active & (Z.real**2 + Z.imag**2 > 4.0)
        escape[just_escaped] = n
        active[just_escaped] = False
        if not np.any(active):
            break

    # Smooth coloring (eliminates banding bands)
    interior = escape >= max_iter
    abs_sq = Z.real**2 + Z.imag**2
    abs_sq = np.where(abs_sq > 1.0, abs_sq, 1.001)
    log_zn = np.log(abs_sq) * 0.5
    nu = np.log(np.maximum(log_zn / math.log(2), 1e-10)) / math.log(2)
    smooth = np.where(interior, 0.0, (escape + 1.0 - nu) / max_iter)

    return smooth.astype(np.float32)


def compute_julia(
    pixel_w: int,
    pixel_h: int,
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    c_re: float, c_im: float,
    max_iter: int,
) -> np.ndarray:
    """Vectorized Julia set for parameter c = c_re + c_im*j."""
    re = np.linspace(x_min, x_max, pixel_w, dtype=np.float64)
    im = np.linspace(y_max, y_min, pixel_h, dtype=np.float64)
    Z = re[np.newaxis, :] + 1j * im[:, np.newaxis]
    C = complex(c_re, c_im)

    escape = np.full(Z.shape, max_iter, dtype=np.float64)
    active = np.ones(Z.shape, dtype=bool)

    for n in range(max_iter):
        Z[active] = Z[active] ** 2 + C
        just_escaped = active & (Z.real**2 + Z.imag**2 > 4.0)
        escape[just_escaped] = n
        active[just_escaped] = False
        if not np.any(active):
            break

    interior = escape >= max_iter
    abs_sq = Z.real**2 + Z.imag**2
    abs_sq = np.where(abs_sq > 1.0, abs_sq, 1.001)
    log_zn = np.log(abs_sq) * 0.5
    nu = np.log(np.maximum(log_zn / math.log(2), 1e-10)) / math.log(2)
    smooth = np.where(interior, 0.0, (escape + 1.0 - nu) / max_iter)

    return smooth.astype(np.float32)


def apply_colormap(values: np.ndarray, cmap: np.ndarray) -> np.ndarray:
    """Map float32 [0,1] escape values → RGB uint8 (H×W×3)."""
    n = len(cmap)
    indices = (values * (n - 1)).astype(np.int32)
    indices = np.clip(indices, 0, n - 1)
    rgb = cmap[indices]
    # Interior (value == 0) → pitch black
    rgb[values == 0.0] = 0
    return rgb


# ─── Terminal Rendering ───────────────────────────────────────────────────────

def rgb_to_rich_text(rgb: np.ndarray) -> Text:
    """
    Convert (pixel_h, pixel_w, 3) RGB array to a Rich Text object.

    Uses Unicode half-block characters (▀ upper, ▄ lower) so each terminal
    row encodes TWO pixel rows, giving 2× vertical resolution.
    """
    pixel_h, pixel_w, _ = rgb.shape
    term_rows = pixel_h // 2
    text = Text()

    for row in range(term_rows):
        upper = rgb[row * 2]        # (W, 3)
        lower = rgb[row * 2 + 1]    # (W, 3)

        for col in range(pixel_w):
            ur, ug, ub = int(upper[col, 0]), int(upper[col, 1]), int(upper[col, 2])
            lr, lg, lb = int(lower[col, 0]), int(lower[col, 1]), int(lower[col, 2])

            u_dark = ur + ug + ub < 3
            l_dark = lr + lg + lb < 3

            if u_dark and l_dark:
                text.append(" ")
            elif u_dark:
                text.append("▄", style=f"rgb({lr},{lg},{lb})")
            elif l_dark:
                text.append("▀", style=f"rgb({ur},{ug},{ub})")
            else:
                text.append(
                    "▀",
                    style=f"rgb({ur},{ug},{ub}) on rgb({lr},{lg},{lb})",
                )

        if row < term_rows - 1:
            text.append("\n")

    return text


# ─── Zoom Targets ─────────────────────────────────────────────────────────────

TARGETS = {
    "seahorse":   (-0.7269, 0.1889, 5e-5, "Seahorse Valley — spiraling tentacles of infinite depth"),
    "elephant":   ( 0.2929, -0.0000, 6e-5, "Elephant Valley — majestic fractal tusks"),
    "lightning":  (-0.5252, -0.5235, 4e-5, "Lightning Spiral — a storm of recursive spirals"),
    "bulb":       (-1.2548, 0.0000, 5e-4, "Largest Bulb — the gateway to chaos"),
    "overview":   (-0.5,    0.0000, 1.8,  "Full Mandelbrot — the whole infinite coastline"),
}


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def exp_lerp(a: float, b: float, t: float) -> float:
    """Exponential interpolation — smooth zoom feel."""
    if a <= 0 or b <= 0:
        return lerp(a, b, t)
    return a * (b / a) ** t


# ─── Animation ────────────────────────────────────────────────────────────────

def run_zoom_animation(
    scheme: str,
    target_name: str,
    fps: int,
    max_iter: int,
    julia_mode: bool,
    julia_c: Tuple[float, float],
) -> None:
    """Main animation loop."""
    cmap = COLORMAPS.get(scheme, COLORMAPS["psychedelic"])
    console = Console()

    # Reserve 2 rows for panel borders + 1 for subtitle
    term_w = console.width - 4
    term_h = console.height - 5
    pixel_w = term_w
    pixel_h = term_h * 2      # 2× vertical resolution via half-blocks

    if julia_mode:
        _run_julia_animation(console, cmap, pixel_w, pixel_h, term_w, term_h,
                             fps, max_iter, julia_c, scheme)
        return

    tx, ty, t_scale, t_desc = TARGETS.get(target_name, TARGETS["seahorse"])

    start_x, start_y = -0.5, 0.0
    start_scale = 1.8
    end_scale = t_scale

    zoom_frames = 80
    hold_frames = 30
    total_frames = zoom_frames + hold_frames

    def frame_bounds(frame_idx: int):
        if frame_idx < zoom_frames:
            t = frame_idx / zoom_frames
            # ease in-out cubic
            t = t * t * (3 - 2 * t)
            scale = exp_lerp(start_scale, end_scale, t)
            cx = lerp(start_x, tx, t)
            cy = lerp(start_y, ty, t)
        else:
            scale = end_scale
            cx, cy = tx, ty

        # Adjust for terminal character aspect (chars ~2× taller than wide)
        aspect = pixel_w / pixel_h
        x_half = scale * aspect
        y_half = scale
        return cx - x_half, cx + x_half, cy - y_half, cy + y_half

    def dynamic_max_iter(frame_idx: int) -> int:
        if frame_idx < zoom_frames:
            t = frame_idx / zoom_frames
            return int(max_iter * (0.4 + 0.6 * t))
        return max_iter

    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        try:
            for frame in range(total_frames):
                t0 = time.monotonic()

                x_min, x_max, y_min, y_max = frame_bounds(frame)
                n_iter = dynamic_max_iter(frame)

                values = compute_mandelbrot(pixel_w, pixel_h, x_min, x_max,
                                            y_min, y_max, n_iter)
                rgb = apply_colormap(values, cmap)
                canvas = rgb_to_rich_text(rgb)

                t = min(frame / max(zoom_frames - 1, 1), 1.0)
                zoom_factor = start_scale / (x_max - x_min) * 2

                panel = Panel(
                    canvas,
                    title=(
                        f"[bold cyan]✦ MandelCLI[/]  "
                        f"[magenta]{scheme}[/]  "
                        f"[yellow]{target_name}[/]"
                    ),
                    subtitle=(
                        f"[dim]zoom ×{zoom_factor:.0f}  "
                        f"iter {n_iter}  "
                        f"({(x_min+x_max)/2:.6f}, {(y_min+y_max)/2:.6f})  "
                        f"frame {frame+1}/{total_frames}  Ctrl+C to quit[/]"
                    ),
                    border_style="bright_blue dim",
                )
                live.update(panel)

                elapsed = time.monotonic() - t0
                sleep = max(0.0, 1.0 / fps - elapsed)
                time.sleep(sleep)

        except KeyboardInterrupt:
            pass

    console.print(
        "\n[bold cyan]✦ MandelCLI[/] — thanks for exploring infinite complexity!\n"
    )


def _run_julia_animation(
    console, cmap, pixel_w, pixel_h, term_w, term_h,
    fps, max_iter, julia_c, scheme
):
    """Animate a fixed Julia set parameter."""
    c_re, c_im = julia_c
    x_scale = 1.8
    aspect = pixel_w / pixel_h
    x_min, x_max = -x_scale * aspect, x_scale * aspect
    y_min, y_max = -x_scale, x_scale

    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        try:
            frame = 0
            while True:
                t0 = time.monotonic()
                values = compute_julia(pixel_w, pixel_h, x_min, x_max,
                                       y_min, y_max, c_re, c_im, max_iter)
                rgb = apply_colormap(values, cmap)
                canvas = rgb_to_rich_text(rgb)

                panel = Panel(
                    canvas,
                    title=(
                        f"[bold cyan]✦ MandelCLI — Julia Set[/]  "
                        f"[magenta]{scheme}[/]"
                    ),
                    subtitle=(
                        f"[dim]c = {c_re:+.6f} {c_im:+.6f}i  "
                        f"iter {max_iter}  Ctrl+C to quit[/]"
                    ),
                    border_style="bright_magenta dim",
                )
                live.update(panel)

                frame += 1
                elapsed = time.monotonic() - t0
                time.sleep(max(0.0, 1.0 / fps - elapsed))

        except KeyboardInterrupt:
            pass


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="MandelCLI — Terminal Fractal Explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fractal_explorer.py                        # default: seahorse zoom, psychedelic
  python3 fractal_explorer.py --target elephant      # zoom into elephant valley
  python3 fractal_explorer.py --scheme fire          # fire color scheme
  python3 fractal_explorer.py --julia -0.7269 0.1889 # Julia set
  python3 fractal_explorer.py --list-targets         # show all zoom targets
        """,
    )
    parser.add_argument(
        "--scheme",
        choices=list(COLORMAPS.keys()),
        default="psychedelic",
        help="Color scheme (default: psychedelic)",
    )
    parser.add_argument(
        "--target",
        choices=list(TARGETS.keys()),
        default="seahorse",
        help="Zoom destination (default: seahorse)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=8,
        metavar="N",
        help="Target frames per second (default: 8)",
    )
    parser.add_argument(
        "--iter",
        type=int,
        default=256,
        metavar="N",
        help="Maximum iteration depth (default: 256)",
    )
    parser.add_argument(
        "--julia",
        nargs=2,
        type=float,
        metavar=("RE", "IM"),
        help="Show Julia set for constant c = RE + IM*i",
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="List available zoom targets and exit",
    )

    args = parser.parse_args()

    if args.list_targets:
        print("\nAvailable zoom targets:\n")
        for name, (x, y, scale, desc) in TARGETS.items():
            print(f"  {name:12}  {desc}")
            print(f"              center ({x}, {y}), final scale {scale:.1e}\n")
        return

    julia_mode = args.julia is not None
    julia_c = tuple(args.julia) if julia_mode else (-0.7, 0.27)

    run_zoom_animation(
        scheme=args.scheme,
        target_name=args.target,
        fps=args.fps,
        max_iter=args.iter,
        julia_mode=julia_mode,
        julia_c=julia_c,
    )


if __name__ == "__main__":
    main()
