"""Core composition engine — builds musical structures from mathematical sequences."""

from dataclasses import dataclass, field
from typing import List, Optional
from .sequences import fibonacci, primes, collatz, mandelbrot_sequence, golden_ratio, look_and_say
from .theory import (
    number_to_note, number_to_duration, number_to_dynamic,
    to_abc_note, detect_musical_character, SCALES,
)


@dataclass
class Note:
    name: str
    octave: int
    duration_name: str
    beat_value: float
    dynamic: str
    source_value: int  # the original integer that produced this note

    def to_abc(self) -> str:
        return to_abc_note(self.name, self.octave, self.duration_name)

    def __repr__(self) -> str:
        return f"{self.name}{self.octave}({self.duration_name})"


@dataclass
class Measure:
    notes: List[Note] = field(default_factory=list)
    time_signature: tuple = (4, 4)

    def beats(self) -> float:
        return sum(n.beat_value for n in self.notes)

    def to_abc(self) -> str:
        return " ".join(n.to_abc() for n in self.notes) + " |"


class Composition:
    """
    A musical composition built from a mathematical sequence.
    Stores notes as structured data and can render to multiple formats.
    """

    def __init__(
        self,
        title: str,
        scale: str = "major",
        root: str = "C",
        octave_range: tuple = (3, 6),
        time_sig: tuple = (4, 4),
    ):
        self.title = title
        self.scale = scale
        self.root = root
        self.octave_range = octave_range
        self.time_sig = time_sig
        self.measures: List[Measure] = []
        self.tempo: int = 120
        self.source_name: str = "unknown"
        self.source_sequence: List[int] = []
        self.character: dict = {}

    def _build_from_sequence(self, sequence: List[int], source_name: str) -> "Composition":
        self.source_name = source_name
        self.source_sequence = sequence
        self.character = detect_musical_character(sequence)
        self.tempo = self.character["tempo"]

        # Override scale with the detected one if not explicitly set
        if self.scale == "major":
            self.scale = self.character["scale"]

        beats_per_measure = self.time_sig[0]
        current_measure = Measure(time_signature=self.time_sig)

        for val in sequence:
            note_name, octave = number_to_note(val, self.scale, self.root, self.octave_range)
            dur_name, beat_val = number_to_duration(val)
            dynamic = number_to_dynamic(val)

            note = Note(
                name=note_name,
                octave=octave,
                duration_name=dur_name,
                beat_value=beat_val,
                dynamic=dynamic,
                source_value=val,
            )

            # If adding this note overflows the measure, start a new one
            if current_measure.beats() + beat_val > beats_per_measure:
                if current_measure.notes:
                    self.measures.append(current_measure)
                current_measure = Measure(time_signature=self.time_sig)

            current_measure.notes.append(note)

        if current_measure.notes:
            self.measures.append(current_measure)

        return self

    @classmethod
    def from_fibonacci(
        cls, length: int = 32, scale: str = "major", root: str = "C"
    ) -> "Composition":
        comp = cls(f"Fibonacci Sonata in {root}", scale=scale, root=root)
        seq = fibonacci(length)
        return comp._build_from_sequence(seq, "Fibonacci")

    @classmethod
    def from_primes(
        cls, length: int = 32, scale: str = "major", root: str = "C"
    ) -> "Composition":
        comp = cls(f"Prime Étude in {root}", scale=scale, root=root)
        seq = primes(length)
        return comp._build_from_sequence(seq, "Primes")

    @classmethod
    def from_collatz(
        cls, start: int = 27, scale: str = "minor", root: str = "A"
    ) -> "Composition":
        comp = cls(f"Collatz Cascade from {start}", scale=scale, root=root)
        seq = collatz(start)
        return comp._build_from_sequence(seq, f"Collatz({start})")

    @classmethod
    def from_mandelbrot(
        cls,
        steps: int = 32,
        scale: str = "phrygian",
        root: str = "E",
        real_range: tuple = (-2.0, 0.5),
        imag_range: tuple = (-1.25, 1.25),
    ) -> "Composition":
        comp = cls(f"Mandelbrot Nocturne in {root}", scale=scale, root=root)
        seq = mandelbrot_sequence(real_range, imag_range, steps)
        return comp._build_from_sequence(seq, "Mandelbrot")

    @classmethod
    def from_golden_ratio(
        cls, length: int = 24, scale: str = "lydian", root: str = "F"
    ) -> "Composition":
        comp = cls(f"Golden Spiral Prelude in {root}", scale=scale, root=root)
        seq = golden_ratio(length)
        return comp._build_from_sequence(seq, "Golden Ratio (φ)")

    @classmethod
    def from_look_and_say(
        cls, length: int = 12, scale: str = "whole_tone", root: str = "C"
    ) -> "Composition":
        comp = cls("Look-and-Say Variations", scale=scale, root=root)
        seq = look_and_say(length)
        return comp._build_from_sequence(seq, "Look-and-Say (Conway)")

    # ------------------------------------------------------------------ output

    def to_abc(self) -> str:
        """Renders the composition as ABC notation (playable text format)."""
        lines = [
            f"X:1",
            f"T:{self.title}",
            f"M:{self.time_sig[0]}/{self.time_sig[1]}",
            f"L:1/4",
            f"Q:{self.tempo}",
            f"K:{self.root}{self._abc_mode()}",
            "",
        ]
        for i, measure in enumerate(self.measures):
            lines.append(measure.to_abc())
            if (i + 1) % 4 == 0:
                lines.append("")  # blank line every 4 bars for readability

        lines.append("|]")
        return "\n".join(lines)

    def _abc_mode(self) -> str:
        mode_map = {
            "major": "maj", "minor": "min", "dorian": "dor",
            "phrygian": "phr", "lydian": "lyd", "mixolydian": "mix",
            "locrian": "loc", "pentatonic": "maj", "blues": "min",
            "whole_tone": "maj",
        }
        return mode_map.get(self.scale, "maj")

    def all_notes(self) -> List[Note]:
        return [note for measure in self.measures for note in measure.notes]

    def summary(self) -> dict:
        notes = self.all_notes()
        return {
            "title": self.title,
            "source": self.source_name,
            "scale": f"{self.root} {self.scale}",
            "tempo": self.tempo,
            "measures": len(self.measures),
            "total_notes": len(notes),
            "note_range": f"{min(n.octave for n in notes)} – {max(n.octave for n in notes)} octaves",
            "density": self.character.get("density", "n/a"),
        }
