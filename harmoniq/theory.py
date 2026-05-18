"""Music theory mappings — translates raw numbers into musical elements."""

from typing import List, Tuple, Optional

# Chromatic scale semitone offsets for common modes
SCALES = {
    "major":       [0, 2, 4, 5, 7, 9, 11],
    "minor":       [0, 2, 3, 5, 7, 8, 10],
    "dorian":      [0, 2, 3, 5, 7, 9, 10],
    "phrygian":    [0, 1, 3, 5, 7, 8, 10],
    "lydian":      [0, 2, 4, 6, 7, 9, 11],
    "mixolydian":  [0, 2, 4, 5, 7, 9, 10],
    "locrian":     [0, 1, 3, 5, 6, 8, 10],
    "pentatonic":  [0, 2, 4, 7, 9],
    "blues":       [0, 3, 5, 6, 7, 10],
    "whole_tone":  [0, 2, 4, 6, 8, 10],
}

# Note names (chromatic, starting from C)
CHROMATIC = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# ABC notation duration values (relative to a quarter note = 1)
DURATIONS = {
    "whole":        (4, "4"),
    "half":         (2, "2"),
    "quarter":      (1, "1"),
    "eighth":       (0.5, "/2"),
    "sixteenth":    (0.25, "/4"),
}

# Rhythm patterns indexed by value mod 5
RHYTHM_MAP = [
    ("quarter",  1.0),    # 0 → steady quarter
    ("eighth",   0.5),    # 1 → quick eighth
    ("half",     2.0),    # 2 → held half
    ("sixteenth",0.25),   # 3 → rapid sixteenth
    ("quarter",  1.0),    # 4 → quarter again
]

# Dynamic markings mapped from sequence value ranges
DYNAMICS = ["pp", "p", "mp", "mf", "f", "ff"]


def number_to_note(
    n: int,
    scale: str = "major",
    root: str = "C",
    octave_range: Tuple[int, int] = (3, 6),
) -> Tuple[str, int]:
    """
    Maps an integer to a (note_name, octave) tuple.
    Uses the scale's step pattern and wraps octaves within the given range.
    """
    intervals = SCALES.get(scale, SCALES["major"])
    scale_len = len(intervals)
    num_octaves = octave_range[1] - octave_range[0]

    root_idx = CHROMATIC.index(root)
    step = n % scale_len
    octave_offset = (n // scale_len) % num_octaves
    octave = octave_range[0] + octave_offset

    semitone = (root_idx + intervals[step]) % 12
    note_name = CHROMATIC[semitone]
    return note_name, octave


def number_to_duration(n: int) -> Tuple[str, float]:
    """Maps an integer to a (duration_name, beat_value) via rhythm map."""
    name, beats = RHYTHM_MAP[n % len(RHYTHM_MAP)]
    return name, beats


def number_to_dynamic(n: int) -> str:
    """Maps an integer to a dynamic marking (pp to ff)."""
    return DYNAMICS[n % len(DYNAMICS)]


def to_abc_note(note: str, octave: int, duration_name: str) -> str:
    """
    Converts (note, octave, duration) to ABC notation string.
    ABC middle C is C4 → written as 'C' in octave 4; octave 5 is lowercase 'c'.
    """
    _, abc_dur = DURATIONS.get(duration_name, DURATIONS["quarter"])

    base_octave = 4
    diff = octave - base_octave

    if diff == 0:
        abc_note = note
    elif diff == 1:
        abc_note = note.lower()
    elif diff > 1:
        abc_note = note.lower() + "'" * (diff - 1)
    elif diff == -1:
        abc_note = note + ","
    else:
        abc_note = note + "," * abs(diff)

    return abc_note + abc_dur


def numbers_to_chord(nums: List[int], scale: str = "major", root: str = "C") -> List[Tuple[str, int]]:
    """Returns up to 3 harmonically-related notes from a list of numbers."""
    notes = [number_to_note(n, scale, root) for n in nums[:3]]
    return notes


def detect_musical_character(sequence: List[int]) -> dict:
    """
    Analyses a sequence and returns descriptive musical characteristics.
    Used for README-style output and composition metadata.
    """
    mean_val = sum(sequence) / len(sequence)
    variance = sum((x - mean_val) ** 2 for x in sequence) / len(sequence)
    max_val = max(sequence)
    min_val = min(sequence)
    span = max_val - min_val

    tempo = 60 + int(mean_val % 100)
    scale = list(SCALES.keys())[int(mean_val) % len(SCALES)]
    density = "sparse" if variance > span else "dense"

    return {
        "tempo": max(60, min(180, tempo)),
        "scale": scale,
        "density": density,
        "range": span,
        "avg": mean_val,
    }
