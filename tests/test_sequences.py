"""Tests for mathematical sequence generators."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from harmoniq.sequences import (
    fibonacci, primes, collatz, golden_ratio, mandelbrot_sequence,
    triangular, look_and_say,
)
from harmoniq.theory import number_to_note, number_to_duration, SCALES
from harmoniq.composer import Composition


# ── sequences ─────────────────────────────────────────────────────────────────

def test_fibonacci_length():
    assert len(fibonacci(10)) == 10

def test_fibonacci_values():
    assert fibonacci(8) == [1, 1, 2, 3, 5, 8, 13, 21]

def test_fibonacci_growth():
    seq = fibonacci(20)
    for i in range(2, len(seq)):
        assert seq[i] == seq[i-1] + seq[i-2]

def test_primes_length():
    assert len(primes(10)) == 10

def test_primes_values():
    assert primes(6) == [2, 3, 5, 7, 11, 13]

def test_primes_are_prime():
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    for p in primes(50):
        assert is_prime(p), f"{p} is not prime"

def test_collatz_ends_at_one():
    seq = collatz(27)
    assert seq[-1] == 1
    assert seq[0] == 27

def test_collatz_rule():
    seq = collatz(10)
    for i in range(len(seq) - 1):
        n = seq[i]
        if n % 2 == 0:
            assert seq[i+1] == n // 2
        else:
            assert seq[i+1] == 3 * n + 1

def test_mandelbrot_length():
    seq = mandelbrot_sequence(steps=16)
    assert len(seq) == 16

def test_mandelbrot_range():
    seq = mandelbrot_sequence(steps=32, max_iter=100)
    assert all(1 <= v <= 100 for v in seq)

def test_triangular():
    assert triangular(5) == [1, 3, 6, 10, 15]

def test_look_and_say_length():
    assert len(look_and_say(8)) == 8

def test_look_and_say_grows():
    seq = look_and_say(10)
    # sequence lengths generally grow (Conway's constant)
    assert seq[-1] > seq[0]


# ── theory ────────────────────────────────────────────────────────────────────

def test_number_to_note_in_scale():
    from harmoniq.theory import SCALES, CHROMATIC
    note, octave = number_to_note(0, "major", "C")
    assert note == "C"
    assert octave == 3

def test_number_to_note_wraps_octave():
    _, o1 = number_to_note(0, "major", "C", (3, 5))
    _, o2 = number_to_note(7, "major", "C", (3, 5))
    _, o3 = number_to_note(14, "major", "C", (3, 5))
    assert o1 == 3
    assert o2 in (3, 4)
    assert o3 in (3, 4)

def test_all_scales_defined():
    for scale_name in SCALES:
        note, octave = number_to_note(5, scale_name, "C")
        assert note in ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

def test_number_to_duration_returns_valid():
    valid_names = {"whole", "half", "quarter", "eighth", "sixteenth"}
    for i in range(10):
        name, beats = number_to_duration(i)
        assert name in valid_names
        assert beats > 0


# ── composer ──────────────────────────────────────────────────────────────────

def test_composition_from_fibonacci():
    comp = Composition.from_fibonacci(16)
    assert len(comp.all_notes()) > 0
    assert comp.title != ""

def test_composition_from_primes():
    comp = Composition.from_primes(16)
    assert len(comp.measures) > 0

def test_composition_from_collatz():
    comp = Composition.from_collatz(27)
    notes = comp.all_notes()
    assert len(notes) > 0

def test_composition_from_mandelbrot():
    comp = Composition.from_mandelbrot(steps=16)
    assert comp.source_name == "Mandelbrot"

def test_composition_abc_output():
    comp = Composition.from_fibonacci(8)
    abc = comp.to_abc()
    assert "X:1" in abc
    assert "T:" in abc
    assert "|" in abc

def test_composition_summary_keys():
    comp = Composition.from_golden_ratio(12)
    s = comp.summary()
    for key in ("title", "source", "scale", "tempo", "measures", "total_notes"):
        assert key in s

def test_all_notes_non_empty_for_all_sources():
    compositions = [
        Composition.from_fibonacci(16),
        Composition.from_primes(16),
        Composition.from_collatz(12),
        Composition.from_mandelbrot(16),
        Composition.from_golden_ratio(12),
        Composition.from_look_and_say(8),
    ]
    for comp in compositions:
        assert len(comp.all_notes()) > 0, f"{comp.title} has no notes"


# ── renderer smoke tests ───────────────────────────────────────────────────────

def test_render_piano_roll_returns_string():
    from harmoniq.renderer import render_piano_roll
    comp = Composition.from_fibonacci(16)
    output = render_piano_roll(comp)
    assert isinstance(output, str)
    assert len(output) > 0

def test_render_waveform_returns_string():
    from harmoniq.renderer import render_waveform
    comp = Composition.from_primes(16)
    output = render_waveform(comp)
    assert isinstance(output, str)

def test_render_summary_box_returns_string():
    from harmoniq.renderer import render_summary_box
    comp = Composition.from_collatz(27)
    output = render_summary_box(comp)
    assert isinstance(output, str)
    assert comp.title in output or "Cascade" in output
