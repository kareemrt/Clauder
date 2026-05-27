"""
Curated collection of breathtaking fractal locations.
Each preset captures a unique feature of its fractal type.
"""
from typing import Dict, Any

Preset = Dict[str, Any]

PRESETS: Dict[str, Preset] = {
    # ── Mandelbrot ────────────────────────────────────────────────────────
    "classic": {
        "description": "The full Mandelbrot set — the iconic overview",
        "fractal": "mandelbrot",
        "bounds": (-2.5, 1.0, -1.25, 1.25),
        "max_iter": 256,
        "theme": "electric",
        "cycle": 64,
    },
    "elephant-valley": {
        "description": "Elephant Valley — baby Mandelbrot elephants parading in rows",
        "fractal": "mandelbrot",
        "bounds": (0.175, 0.185, -0.006, 0.006),
        "max_iter": 1024,
        "theme": "gold",
        "cycle": 48,
    },
    "sea-horse-valley": {
        "description": "Seahorse Valley — swirling spiral arms and filaments",
        "fractal": "mandelbrot",
        "bounds": (-0.760, -0.730, 0.100, 0.130),
        "max_iter": 512,
        "theme": "ocean",
        "cycle": 32,
    },
    "deep-spiral": {
        "description": "A deep zoom spiral — infinite recursive complexity",
        "fractal": "mandelbrot",
        "bounds": (-0.16280, -0.16200, 1.03800, 1.03870),
        "max_iter": 2048,
        "theme": "fire",
        "cycle": 96,
    },
    "mini-brot": {
        "description": "A tiny satellite Mandelbrot — self-similarity in action",
        "fractal": "mandelbrot",
        "bounds": (-1.630, -1.570, -0.030, 0.030),
        "max_iter": 512,
        "theme": "neon",
        "cycle": 40,
    },
    "lightning": {
        "description": "Lightning filaments branching at the edge of chaos",
        "fractal": "mandelbrot",
        "bounds": (-0.2050, -0.1980, -1.1020, -1.0960),
        "max_iter": 1024,
        "theme": "electric",
        "cycle": 28,
    },
    "spiral-galaxy": {
        "description": "A spiral galaxy — swirling arms of infinite detail",
        "fractal": "mandelbrot",
        "bounds": (-0.748766713922161, -0.748766707771757, 0.123640844894813, 0.123640851045217),
        "max_iter": 4096,
        "theme": "inferno",
        "cycle": 128,
    },
    # ── Julia Sets ────────────────────────────────────────────────────────
    "julia-classic": {
        "description": "Classic Julia — c = -0.7 + 0.27015i (dragon-wing curves)",
        "fractal": "julia",
        "julia_c": (-0.7, 0.27015),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 256,
        "theme": "ice",
        "cycle": 48,
    },
    "julia-rabbit": {
        "description": "Douady Rabbit — c = -0.123 + 0.745i (three-petal symmetry)",
        "fractal": "julia",
        "julia_c": (-0.123, 0.745),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 512,
        "theme": "neon",
        "cycle": 36,
    },
    "julia-dragon": {
        "description": "Dragon Julia — c = 0.355 + 0.355i (tangled filaments)",
        "fractal": "julia",
        "julia_c": (0.355, 0.355),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 256,
        "theme": "fire",
        "cycle": 48,
    },
    "julia-dendrite": {
        "description": "Dendrite Julia — c = 0 + 1i (fractal snowflake branches)",
        "fractal": "julia",
        "julia_c": (0.0, 1.0),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 256,
        "theme": "electric",
        "cycle": 32,
    },
    "julia-san-marco": {
        "description": "San Marco Dragon — c = -0.75 + 0i (connected bubbles)",
        "fractal": "julia",
        "julia_c": (-0.75, 0.0),
        "bounds": (-1.8, 1.8, -1.1, 1.1),
        "max_iter": 256,
        "theme": "viridis",
        "cycle": 48,
    },
    "julia-siegel": {
        "description": "Siegel Disk Julia — c = -0.391 - 0.587i (rotation-symmetric)",
        "fractal": "julia",
        "julia_c": (-0.391, -0.587),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 512,
        "theme": "plasma",
        "cycle": 64,
    },
    # ── Burning Ship ──────────────────────────────────────────────────────
    "burning-ship": {
        "description": "Burning Ship — the full fractal with its fiery hull",
        "fractal": "burning_ship",
        "bounds": (-2.5, 1.5, -2.0, 0.5),
        "max_iter": 256,
        "theme": "inferno",
        "cycle": 48,
    },
    "burning-ship-zoom": {
        "description": "Burning Ship Hull — the 'burning ship' itself up close",
        "fractal": "burning_ship",
        "bounds": (-1.870, -1.640, -0.090, 0.040),
        "max_iter": 512,
        "theme": "fire",
        "cycle": 40,
    },
    # ── Tricorn ───────────────────────────────────────────────────────────
    "tricorn": {
        "description": "The Tricorn (Mandelbar) — three-fold anti-holomorphic symmetry",
        "fractal": "tricorn",
        "bounds": (-2.5, 1.0, -1.25, 1.25),
        "max_iter": 256,
        "theme": "twilight",
        "cycle": 48,
    },
    # ── Newton ────────────────────────────────────────────────────────────
    "newton": {
        "description": "Newton Fractal — basins of attraction for z³ = 1",
        "fractal": "newton",
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "max_iter": 128,
        "theme": "tropical",
        "cycle": 48,
    },
}


FEATURED_PRESETS = [
    "classic", "julia-classic", "burning-ship",
    "sea-horse-valley", "julia-rabbit", "tricorn",
]


def list_presets(verbose: bool = False) -> str:
    """Format preset list as a printable string."""
    lines = ["\033[1;97m  Available Presets\033[0m", ""]
    for name, p in PRESETS.items():
        fractal = p["fractal"].replace("_", " ").title()
        if verbose:
            bounds = p["bounds"]
            lines.append(
                f"  \033[96m{name:<22}\033[0m  \033[90m[{fractal}]\033[0m  {p['description']}"
            )
            lines.append(
                f"  {'':22}  bounds: x=[{bounds[0]:.4f},{bounds[1]:.4f}] "
                f"y=[{bounds[2]:.4f},{bounds[3]:.4f}]"
            )
            lines.append("")
        else:
            lines.append(
                f"  \033[96m{name:<22}\033[0m  \033[90m{fractal:<16}\033[0m  {p['description']}"
            )
    return "\n".join(lines)
