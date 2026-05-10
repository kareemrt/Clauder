"""High-level renderer: ties together computation and color output."""

import time
from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np

from .compute import mandelbrot, julia, burning_ship, JULIA_PRESETS, MANDELBROT_TOURS
from .palette import iterations_to_ansi, iterations_to_plain_ascii, PALETTES


@dataclass
class RenderConfig:
    fractal: str = "mandelbrot"           # mandelbrot | julia | burning_ship
    width: int = 120
    height: int = 40
    max_iter: int = 256
    palette: str = "fire"
    char_set: str = "dense"
    invert: bool = False

    # Viewport (auto-set by fractal defaults if None)
    x_min: Optional[float] = None
    x_max: Optional[float] = None
    y_min: Optional[float] = None
    y_max: Optional[float] = None

    # Julia-specific
    julia_c: complex = -0.7 + 0.27015j
    julia_preset: Optional[str] = None


@dataclass
class RenderResult:
    ansi: str
    plain: str
    iterations: np.ndarray
    elapsed_ms: float
    config: RenderConfig
    stats: dict = field(default_factory=dict)


def render(cfg: RenderConfig) -> RenderResult:
    """Compute and render a fractal according to the given config."""
    t0 = time.perf_counter()

    # Resolve Julia preset
    c = cfg.julia_c
    if cfg.julia_preset and cfg.julia_preset in JULIA_PRESETS:
        c = JULIA_PRESETS[cfg.julia_preset]

    # Resolve viewport
    bounds = _resolve_bounds(cfg)

    # Dispatch to compute engine
    if cfg.fractal == "mandelbrot":
        iters = mandelbrot(cfg.width, cfg.height, *bounds, cfg.max_iter)
    elif cfg.fractal == "julia":
        iters = julia(cfg.width, cfg.height, c, *bounds, cfg.max_iter)
    elif cfg.fractal == "burning_ship":
        iters = burning_ship(cfg.width, cfg.height, *bounds, cfg.max_iter)
    else:
        raise ValueError(f"Unknown fractal type: {cfg.fractal!r}")

    elapsed_ms = (time.perf_counter() - t0) * 1000

    ansi = iterations_to_ansi(iters, cfg.max_iter, cfg.palette, cfg.char_set, cfg.invert)
    plain = iterations_to_plain_ascii(iters, cfg.max_iter, cfg.char_set)

    interior = np.sum(iters == 0)
    exterior = np.sum(iters > 0)
    total = iters.size

    stats = {
        "interior_pct": 100 * interior / total,
        "exterior_pct": 100 * exterior / total,
        "mean_iter": float(np.mean(iters[iters > 0])) if exterior > 0 else 0.0,
        "total_pixels": total,
    }

    return RenderResult(
        ansi=ansi,
        plain=plain,
        iterations=iters,
        elapsed_ms=elapsed_ms,
        config=cfg,
        stats=stats,
    )


def _resolve_bounds(cfg: RenderConfig) -> Tuple[float, float, float, float]:
    """Return (x_min, x_max, y_min, y_max) using defaults when not specified."""
    defaults = {
        "mandelbrot":   (-2.5, 1.0, -1.25, 1.25),
        "julia":        (-1.8, 1.8, -1.8, 1.8),
        "burning_ship": (-2.5, 1.5, -2.0, 0.5),
    }
    x_min, x_max, y_min, y_max = defaults.get(cfg.fractal, (-2.0, 2.0, -2.0, 2.0))
    return (
        cfg.x_min if cfg.x_min is not None else x_min,
        cfg.x_max if cfg.x_max is not None else x_max,
        cfg.y_min if cfg.y_min is not None else y_min,
        cfg.y_max if cfg.y_max is not None else y_max,
    )
