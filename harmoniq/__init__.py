"""
Harmoniq: Mathematical Music Composer
Transforms mathematical sequences into playable musical compositions.
"""

from .sequences import fibonacci, primes, collatz, mandelbrot_sequence, golden_ratio
from .theory import number_to_note, number_to_duration, SCALES
from .composer import Composition
from .renderer import render_piano_roll, render_ascii_staff, render_waveform

__version__ = "1.0.0"
__all__ = [
    "fibonacci", "primes", "collatz", "mandelbrot_sequence", "golden_ratio",
    "number_to_note", "number_to_duration", "SCALES",
    "Composition",
    "render_piano_roll", "render_ascii_staff", "render_waveform",
]
