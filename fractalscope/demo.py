"""Quick demo: renders all three fractals to the terminal."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fractalscope.fractals import FRACTALS
from fractalscope.palettes import apply_palette
from fractalscope.renderers.terminal import print_fractal

DEMOS = [
    ("mandelbrot",   "fire",    dict(x_min=-2.5, x_max=1.0,  y_min=-1.25, y_max=1.25)),
    ("julia",        "neon",    dict(x_min=-1.8, x_max=1.8,  y_min=-1.8,  y_max=1.8,
                                     c_real=-0.7269, c_imag=0.1889)),
    ("burning_ship", "sunset",  dict(x_min=-2.5, x_max=1.5,  y_min=-2.0,  y_max=0.5)),
]

W, H = 120, 60

for fractal_name, palette, kwargs in DEMOS:
    fn = FRACTALS[fractal_name]
    data = fn(width=W, height=H, max_iter=200, **kwargs)
    rgb = apply_palette(data, palette)
    title = f"{fractal_name.replace('_', ' ').title()}  [{palette}]"
    print_fractal(rgb, title=title)
    print()
