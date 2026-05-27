#!/usr/bin/env python3
"""Generate example images for the README."""
import time, sys
sys.path.insert(0, "/home/user/Clauder")

from fractalscape.core import compute_fractal
from fractalscape.export import export_png

EXAMPLES = [
    {
        "name": "examples/mandelbrot_classic.png",
        "fractal": "mandelbrot",
        "bounds": (-2.5, 1.0, -1.25, 1.25),
        "max_iter": 256,
        "theme": "electric",
        "size": (1200, 675),
    },
    {
        "name": "examples/julia_classic.png",
        "fractal": "julia",
        "julia_c": (-0.7, 0.27015),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 256,
        "theme": "ice",
        "size": (1200, 675),
    },
    {
        "name": "examples/burning_ship.png",
        "fractal": "burning_ship",
        "bounds": (-2.5, 1.5, -2.0, 0.5),
        "max_iter": 256,
        "theme": "inferno",
        "size": (1200, 675),
    },
    {
        "name": "examples/sea_horse_valley.png",
        "fractal": "mandelbrot",
        "bounds": (-0.760, -0.730, 0.100, 0.130),
        "max_iter": 512,
        "theme": "ocean",
        "size": (1200, 675),
    },
    {
        "name": "examples/julia_rabbit.png",
        "fractal": "julia",
        "julia_c": (-0.123, 0.745),
        "bounds": (-1.6, 1.6, -1.0, 1.0),
        "max_iter": 512,
        "theme": "neon",
        "size": (1200, 675),
    },
    {
        "name": "examples/tricorn.png",
        "fractal": "tricorn",
        "bounds": (-2.5, 1.0, -1.25, 1.25),
        "max_iter": 256,
        "theme": "twilight",
        "size": (1200, 675),
    },
]

for ex in EXAMPLES:
    w, h = ex["size"]
    b = ex["bounds"]
    julia_c = ex.get("julia_c", (-0.7, 0.27015))
    print(f"  Generating {ex['name']} ({w}×{h})...", end="", flush=True)
    t0 = time.time()
    data = compute_fractal(w, h, b[0], b[1], b[2], b[3],
                            fractal_type=ex["fractal"],
                            max_iter=ex["max_iter"],
                            julia_c=julia_c)
    ok = export_png(data, ex["max_iter"], ex["theme"], ex["name"],
                     cycle_period=64.0, sharpen=True)
    print(f" done ({time.time()-t0:.1f}s)" if ok else " FAILED")

print("\nAll examples generated.")
