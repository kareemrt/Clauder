# Harmoniq 🎵

> **Mathematical Music Composer** — transform the hidden patterns of mathematics into real, playable music.

```
  ██╗  ██╗ █████╗ ██████╗ ███╗   ███╗ ██████╗ ███╗   ██╗██╗ ██████╗
  ██║  ██║██╔══██╗██╔══██╗████╗ ████║██╔═══██╗████╗  ██║██║██╔═══██╗
  ███████║███████║██████╔╝██╔████╔██║██║   ██║██╔██╗ ██║██║██║   ██║
  ██╔══██║██╔══██║██╔══██╗██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║▄▄ ██║
  ██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║╚██████╔╝
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚══▀▀╝

  Mathematical Music Composer  ·  v1.0.0
```

---

## What Is Harmoniq?

Mathematics and music share a deep structural kinship — both deal in ratios, patterns, and ordered relationships. Harmoniq makes this connection tangible. It takes well-known mathematical sequences and **maps them directly to music theory**, producing compositions you can actually hear and play.

- Feed it **Fibonacci numbers** → get a naturally harmonious melody (because φ ≈ 1.618 is built into Western scales)
- Feed it **prime numbers** → get rhythmically irregular, jazz-like phrases
- Feed it **Mandelbrot iteration depths** → get an eerie boundary-haunting nocturne
- Feed it **Collatz sequences** → get chaotic ascent and sudden collapse, mirroring the 3n+1 mystery

Output is **ABC notation** — a plain-text music format playable in any browser or importable into MuseScore, GarageBand, or LilyPond.

---

## Architecture

```
harmoniq/
│
├── sequences.py     ← Mathematical sequence generators
│     fibonacci()    ·  1, 1, 2, 3, 5, 8, 13, 21 ...
│     primes()       ·  2, 3, 5, 7, 11, 13 ...
│     collatz()      ·  3n+1 until convergence
│     mandelbrot_sequence()  ·  iteration depths along a boundary path
│     golden_ratio() ·  powers of φ scaled to integers
│     look_and_say() ·  Conway's sequence by term length
│
├── theory.py        ← Music theory translation layer
│     number_to_note()      ·  integer → (note_name, octave)
│     number_to_duration()  ·  integer → (name, beat_value)
│     number_to_dynamic()   ·  integer → pp / p / mp / mf / f / ff
│     SCALES{}              ·  9 modes: major, minor, dorian, phrygian ...
│
├── composer.py      ← Composition engine
│     Composition    ·  core data model: measures, notes, metadata
│     .from_fibonacci()     ·  factory method
│     .from_primes()        ·  factory method
│     .from_collatz()       ·  factory method
│     .from_mandelbrot()    ·  factory method
│     .from_golden_ratio()  ·  factory method
│     .from_look_and_say()  ·  factory method
│     .to_abc()             ·  export to ABC notation string
│
├── renderer.py      ← Terminal visualisation engine
│     render_piano_roll()   ·  coloured horizontal event grid
│     render_ascii_staff()  ·  5-line treble staff with note heads
│     render_waveform()     ·  Unicode block-chart of source values
│     render_summary_box()  ·  formatted composition metadata box
│
└── cli.py           ← Command-line interface
      harmoniq compose <source> [options]
      harmoniq demo
      harmoniq info <source>
```

---

## The Pipeline

```
  Mathematical       Music Theory          Composition          Output
   Sequence           Mapping               Engine
  ─────────────     ───────────────       ───────────────     ───────────
                    ┌─────────────┐       ┌─────────────┐
  fibonacci(32) ──► │ n mod 7     │──────►│ Note(       │
                    │ → scale     │       │  name="G",  │
   [1,1,2,3,5,  ──► │   step      │       │  octave=4,  │──────► ABC
    8,13,21 ...]    │ n mod 5     │       │  dur="qtr", │       notation
                    │ → duration  │       │  dyn="mf"   │
                    │ n mod 6     │       │ )           │──────► Piano
                    │ → dynamic   │       └─────────────┘        Roll
                    └─────────────┘
                                          Measures               Staff
                                         ┌──────┬──────┐        View
                                         │4/4   │4/4   │
                                         │♩♩♩♩ │♩♩♩  │──────► Summary
                                         └──────┴──────┘        Box
```

---

## Sequences Explained

### Fibonacci — Natural Harmony

```
1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 ...

Ratios approach φ = 1.618...

Frequency ratio 3:2 (perfect fifth)   ≈ 1.500
Frequency ratio 5:3 (major sixth)     ≈ 1.667
Fibonacci ratio 8:5                   = 1.600  ← near φ
Fibonacci ratio 13:8                  = 1.625  ← nearer
Fibonacci ratio 89:55                 = 1.6̄18̄  ← converging

Result: melodies with natural consonance — Fibonacci numbers
        naturally land on harmonically "correct" scale degrees.
```

### Primes — Rhythmic Irregularity

```
2, 3, 5, 7, 11, 13, 17, 19, 23, 29 ...

mod 5 → rhythm map:   0=quarter, 1=eighth, 2=half, 3=sixteenth, 4=quarter
mod 7 → scale step:   unpredictable, spread across full scale range

2 mod 5 = 2 → half note     │ 11 mod 5 = 1 → eighth
3 mod 5 = 3 → sixteenth      │ 13 mod 5 = 3 → sixteenth
5 mod 5 = 0 → quarter        │ 17 mod 5 = 2 → half
7 mod 5 = 2 → half           │ 19 mod 5 = 4 → quarter

Result: irregular, jazz-like phrases with no predictable pulse.
```

### Mandelbrot — Boundary Chaos

```
  Imaginary axis
  ▲
1.25┤          ░░░░░▓▓▓▓▒▒▒▒░░░░░░
  0┤      ████████████████░░░░░░░░░░
-1.25┤          ░░░░░▓▓▓▓▒▒▒▒░░░░░░
   └────────────────────────────────►
  -2.0                          0.5  Real axis

  Path sampled: ╲ diagonal cut from (-2.0,-1.25) to (0.5,1.25)

  In the black interior (████): iteration → max_iter   = sustained notes
  Near the boundary   (▒▒▒▒): iteration ≈ mid-range   = melodic motion
  Far outside         (░░░░): iteration → 1            = quick, light notes

Result: melodic contour that traces the fractal boundary —
        slow and sustained inside, frantic at the edge.
```

### Collatz — Chaos to Convergence

```
  Start: 27

  27 → 82 → 41 → 124 → 62 → 31 → 94 → 47 → 142 → 71
   ╲                                                /
    ╲     rapid ascent to maximum (9232)           /
     ╲                                            /
      ╲_________________________________________/
       → chaotic descent → ... → 4 → 2 → 1

  As music: dramatic crescendo and collapse.
            The 3n+1 mystery encoded in sound.
```

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -e .

# No external dependencies needed — pure Python 3.9+
```

### CLI Usage

```bash
# Compose from any sequence
harmoniq compose fibonacci --length 32 --scale pentatonic --root G
harmoniq compose primes    --length 24 --scale dorian     --root D
harmoniq compose mandelbrot                                           # uses full boundary path
harmoniq compose collatz   --start 27  --scale minor      --root A
harmoniq compose golden    --length 20 --scale lydian     --root F

# Save the ABC notation to a file
harmoniq compose mandelbrot --output nocturne.abc

# Run all sequences as a showcase
harmoniq demo

# Inspect a raw sequence
harmoniq info fibonacci
```

### Python API

```python
from harmoniq import Composition
from harmoniq.renderer import render_piano_roll, render_waveform

# Compose
comp = Composition.from_fibonacci(length=32, scale="major", root="C")

# Visualise
print(render_waveform(comp))
print(render_piano_roll(comp))

# Export to ABC notation
abc_text = comp.to_abc()
with open("my_piece.abc", "w") as f:
    f.write(abc_text)

# Inspect
print(comp.summary())
# {'title': 'Fibonacci Sonata in C', 'source': 'Fibonacci',
#  'scale': 'C pentatonic', 'tempo': 118, 'measures': 9, ...}
```

---

## Output Formats

### 1. Terminal Piano Roll

```
  ♩  Piano Roll — Fibonacci Sonata in G
  ──────────────────────────────────
Oct 6 │ · · · · · · · · · · · · · · ·
Oct 5 │ · · · · · · ▪ · · █ █ · · · █
Oct 4 │ · · · · █ ▪ · ▬ · · · █ ▪ · ·
Oct 3 │ ▬ ▬ ██ ▪ · · · · █ · · · · ██
  ──────────────────────────────────

  Block size = duration:  ▪=sixteenth  ▬=eighth  █=quarter  ██=half
  Colour     = note:      cyan=C/G  green=D/A  yellow=E/B  magenta=D#/A#
```

### 2. Sequence Waveform

```
  ∿  Sequence Waveform — Fibonacci
  max=46368  n=24
  │                       ▁ ▁ ▃ ▄ █
  │                       ▁ ▁ ▃ ▄ █
  │                       ▁ ▁ ▃ ▄ █
  │                       ▁ ▁ ▃ ▄ █
  └────────────────────────────────
```

### 3. ABC Notation (playable)

```abc
X:1
T:Fibonacci Sonata in G
M:4/4
L:1/4
Q:118
K:Gmaj

A,/2 A,/2 B,2 D,/4 |
G1 D/4 d/4 A/2 E,1 g1 |
e1 E1 D/4 |
B,2 g1 |
...
|]
```

> Paste into **https://abc.rectanglered.com** to hear it play instantly, or import the `.abc` file into MuseScore / LilyPond.

---

## Scales / Modes Available

| Mode         | Intervals (semitones)        | Character            |
|:-------------|:-----------------------------|:---------------------|
| `major`      | 0,2,4,5,7,9,11               | Bright, resolved     |
| `minor`      | 0,2,3,5,7,8,10               | Melancholic, tense   |
| `dorian`     | 0,2,3,5,7,9,10               | Jazz, modal          |
| `phrygian`   | 0,1,3,5,7,8,10               | Flamenco, dark       |
| `lydian`     | 0,2,4,6,7,9,11               | Dreamy, floating     |
| `mixolydian` | 0,2,4,5,7,9,10               | Rock, bluesy         |
| `locrian`    | 0,1,3,5,6,8,10               | Dissonant, unstable  |
| `pentatonic` | 0,2,4,7,9                    | Universally pleasing |
| `blues`      | 0,3,5,6,7,10                 | Soulful, expressive  |
| `whole_tone` | 0,2,4,6,8,10                 | Impressionist, eerie |

---

## Running Tests

```bash
pytest tests/ -v
```

```
tests/test_sequences.py::test_fibonacci_length        PASSED
tests/test_sequences.py::test_fibonacci_values        PASSED
tests/test_sequences.py::test_fibonacci_growth        PASSED
tests/test_sequences.py::test_primes_are_prime        PASSED
tests/test_sequences.py::test_collatz_ends_at_one     PASSED
tests/test_sequences.py::test_mandelbrot_range        PASSED
tests/test_sequences.py::test_all_scales_defined      PASSED
tests/test_sequences.py::test_all_notes_non_empty_for_all_sources  PASSED
... 27 passed in 0.05s
```

---

## Project Structure

```
clauder/
├── harmoniq/
│   ├── __init__.py       public API
│   ├── sequences.py      6 mathematical sequence generators
│   ├── theory.py         music theory mapping layer
│   ├── composer.py       Composition class + factory methods
│   ├── renderer.py       4 terminal visualisation renderers
│   └── cli.py            argparse CLI with coloured output
│
├── examples/
│   ├── fibonacci_sonata.py     saves fibonacci_sonata.abc
│   └── mandelbrot_nocturne.py  saves mandelbrot_nocturne.abc
│
├── tests/
│   └── test_sequences.py  27 unit tests across all modules
│
├── setup.py
├── requirements.txt       (pytest only; no runtime deps)
└── README.md
```

---

## Design Decisions

**Why ABC notation?** It's the simplest plain-text music format that is both human-readable and machine-playable. MIDI requires binary encoding; MusicXML is verbose XML; Lilypond has a steep syntax. ABC is one line per measure, and dozens of free players exist online.

**Why zero runtime dependencies?** The mathematical sequences, music theory mappings, and terminal renderers are all straightforward enough to implement in pure Python stdlib. Keeping the dependency list empty means `pip install -e .` works instantly, anywhere.

**Why detect scale from the sequence?** Rather than always defaulting to C major, `detect_musical_character()` derives a tempo and scale suggestion from the sequence's statistical properties (mean, variance, span). The user can always override this, but the automatic choice tends to be more interesting than the default.

---

## Examples Gallery

```bash
# Serene, floating — golden ratio in Lydian
harmoniq compose golden --scale lydian --root F

# Intense and chromatic — primes in Phrygian
harmoniq compose primes --scale phrygian --root E --length 48

# Mysterious decay — Collatz starting from 97 (longer journey to 1)
harmoniq compose collatz --start 97 --scale blues --root A

# Impressionistic — Mandelbrot boundary in whole-tone scale
harmoniq compose mandelbrot --scale whole_tone --root C --output impressions.abc
```

---

## License

MIT — do whatever you like with the music you generate.

---

*"Mathematics is the music of reason." — James Joseph Sylvester*
