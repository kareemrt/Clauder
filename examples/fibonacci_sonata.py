"""
Fibonacci Sonata — example script.
Composes a piece from Fibonacci numbers and saves ABC notation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from harmoniq import Composition
from harmoniq.renderer import render_piano_roll, render_waveform, render_summary_box

comp = Composition.from_fibonacci(length=32, scale="major", root="C")

print(render_summary_box(comp))
print(render_waveform(comp))
print(render_piano_roll(comp))

abc = comp.to_abc()
with open("fibonacci_sonata.abc", "w") as f:
    f.write(abc)

print("\nSaved: fibonacci_sonata.abc")
print("Open at https://abc.rectanglered.com/ to play it!")
