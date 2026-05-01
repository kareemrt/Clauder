"""Famous fractal zoom locations and preset configurations."""

from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass
class Preset:
    name: str
    description: str
    fractal: str
    center: Tuple[float, float]
    zoom: float
    max_iter: int
    palette: str
    julia_c: Optional[complex] = None

    def display(self) -> str:
        return f"  {self.name:<22} {self.description}"


PRESETS = [
    Preset(
        name="mandelbrot-overview",
        description="Classic Mandelbrot set overview",
        fractal="mandelbrot",
        center=(-0.5, 0.0),
        zoom=1.0,
        max_iter=200,
        palette="electric",
    ),
    Preset(
        name="seahorse-valley",
        description="The famous Seahorse Valley",
        fractal="mandelbrot",
        center=(-0.75, 0.1),
        zoom=15.0,
        max_iter=512,
        palette="ocean",
    ),
    Preset(
        name="elephant-valley",
        description="Elephant Valley — intricate filaments",
        fractal="mandelbrot",
        center=(0.3, 0.0),
        zoom=12.0,
        max_iter=512,
        palette="gold",
    ),
    Preset(
        name="spiral-galaxy",
        description="Double spiral near the period-2 bulb",
        fractal="mandelbrot",
        center=(-1.2, 0.15),
        zoom=40.0,
        max_iter=800,
        palette="psychedelic",
    ),
    Preset(
        name="mini-brot",
        description="Deep zoom mini Mandelbrot",
        fractal="mandelbrot",
        center=(-1.768778833, -0.001738996),
        zoom=5000.0,
        max_iter=2000,
        palette="fire",
    ),
    Preset(
        name="julia-classic",
        description="Classic Julia set (c = -0.7269 + 0.1889i)",
        fractal="julia",
        center=(0.0, 0.0),
        zoom=1.0,
        max_iter=300,
        palette="electric",
        julia_c=complex(-0.7269, 0.1889),
    ),
    Preset(
        name="julia-rabbit",
        description="Douady's rabbit Julia set",
        fractal="julia",
        center=(0.0, 0.0),
        zoom=1.0,
        max_iter=300,
        palette="psychedelic",
        julia_c=complex(-0.123, 0.745),
    ),
    Preset(
        name="julia-dragon",
        description="Dragon Julia set (c = -0.8 + 0.156i)",
        fractal="julia",
        center=(0.0, 0.0),
        zoom=1.0,
        max_iter=400,
        palette="fire",
        julia_c=complex(-0.8, 0.156),
    ),
    Preset(
        name="julia-snowflake",
        description="Snowflake Julia (c = -0.4 + 0.6i)",
        fractal="julia",
        center=(0.0, 0.0),
        zoom=1.0,
        max_iter=300,
        palette="ice",
        julia_c=complex(-0.4, 0.6),
    ),
    Preset(
        name="burning-ship",
        description="Classic Burning Ship overview",
        fractal="burning_ship",
        center=(-0.5, -0.5),
        zoom=0.9,
        max_iter=256,
        palette="fire",
    ),
    Preset(
        name="burning-deck",
        description="The Burning Ship's prow",
        fractal="burning_ship",
        center=(-1.755, -0.028),
        zoom=60.0,
        max_iter=600,
        palette="gold",
    ),
    Preset(
        name="tricorn",
        description="The Tricorn (Mandelbar) set",
        fractal="tricorn",
        center=(0.0, 0.0),
        zoom=1.0,
        max_iter=256,
        palette="ice",
    ),
]

PRESET_MAP = {p.name: p for p in PRESETS}
