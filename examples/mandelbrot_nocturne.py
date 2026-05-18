"""
Mandelbrot Nocturne — samples the Mandelbrot set boundary and turns
iteration-escape depths into eerie, chaotic melody.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from harmoniq import Composition
from harmoniq.renderer import render_waveform, render_piano_roll, render_summary_box

# Sample a dramatic diagonal cut through the Mandelbrot set
comp = Composition.from_mandelbrot(
    steps=40,
    scale="phrygian",
    root="E",
    real_range=(-2.0, 0.5),
    imag_range=(-1.25, 1.25),
)

print(render_summary_box(comp))
print(render_waveform(comp))
print(render_piano_roll(comp))

abc = comp.to_abc()
with open("mandelbrot_nocturne.abc", "w") as f:
    f.write(abc)

print("\nSaved: mandelbrot_nocturne.abc")
