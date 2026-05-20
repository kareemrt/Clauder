"""Pre-defined fractal scenes at visually interesting coordinates."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Scene:
    name: str
    fractal: str          # "mandelbrot" | "julia" | "burning_ship"
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    max_iter: int
    colormap: str
    julia_c: Optional[complex] = None
    description: str = ""


PRESETS: dict[str, Scene] = {
    "classic": Scene(
        name="Classic Mandelbrot",
        fractal="mandelbrot",
        x_min=-2.5, x_max=1.0,
        y_min=-1.25, y_max=1.25,
        max_iter=256,
        colormap="nebula",
        description="The full Mandelbrot set — the iconic view",
    ),
    "seahorse": Scene(
        name="Seahorse Valley",
        fractal="mandelbrot",
        x_min=-0.77, x_max=-0.70,
        y_min=0.07,  y_max=0.14,
        max_iter=512,
        colormap="ocean",
        description="Intricate spirals near the main bulge",
    ),
    "elephant": Scene(
        name="Elephant Valley",
        fractal="mandelbrot",
        x_min=0.25, x_max=0.40,
        y_min=-0.08, y_max=0.07,
        max_iter=512,
        colormap="fire",
        description="A chain of elephant-trunk spirals",
    ),
    "triple_spiral": Scene(
        name="Triple Spiral",
        fractal="mandelbrot",
        x_min=-0.188, x_max=-0.186,
        y_min=0.653,  y_max=0.655,
        max_iter=1024,
        colormap="psychedelic",
        description="Ultra-deep zoom revealing self-similar spirals",
    ),
    "julia_dragon": Scene(
        name="Julia Dragon",
        fractal="julia",
        x_min=-1.6, x_max=1.6,
        y_min=-0.9, y_max=0.9,
        max_iter=256,
        colormap="fire",
        julia_c=complex(-0.7269, 0.1889),
        description="Classic dragon-wing Julia set",
    ),
    "julia_dendrite": Scene(
        name="Julia Dendrite",
        fractal="julia",
        x_min=-1.5, x_max=1.5,
        y_min=-1.0, y_max=1.0,
        max_iter=256,
        colormap="ocean",
        julia_c=complex(0.0, 1.0),
        description="Snowflake-like dendritic Julia set",
    ),
    "julia_rabbit": Scene(
        name="Douady Rabbit",
        fractal="julia",
        x_min=-1.5, x_max=1.5,
        y_min=-1.1, y_max=1.1,
        max_iter=256,
        colormap="cosmic",
        julia_c=complex(-0.123, 0.745),
        description="The famous Douady rabbit Julia set",
    ),
    "burning_ship_full": Scene(
        name="Burning Ship",
        fractal="burning_ship",
        x_min=-2.5, x_max=1.5,
        y_min=-2.0, y_max=0.5,
        max_iter=256,
        colormap="fire",
        description="The full Burning Ship fractal — asymmetric and eerie",
    ),
    "burning_ship_zoom": Scene(
        name="Burning Ship Detail",
        fractal="burning_ship",
        x_min=-1.85, x_max=-1.65,
        y_min=-0.10, y_max=0.05,
        max_iter=512,
        colormap="cosmic",
        description="The iconic ship's mast detail",
    ),
    "minibrot": Scene(
        name="Mini Mandelbrot",
        fractal="mandelbrot",
        x_min=-1.768, x_max=-1.764,
        y_min=-0.002, y_max=0.002,
        max_iter=2048,
        colormap="nebula",
        description="A tiny embedded copy of the full set at extreme zoom",
    ),
}
