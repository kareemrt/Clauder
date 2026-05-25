# Fractal Canvas

```
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

   ██████╗ █████╗ ███╗   ██╗██╗   ██╗ █████╗ ███████╗
  ██╔════╝██╔══██╗████╗  ██║██║   ██║██╔══██╗██╔════╝
  ██║     ███████║██╔██╗ ██║██║   ██║███████║███████╗
  ██║     ██╔══██║██║╚██╗██║╚██╗ ██╔╝██╔══██║╚════██║
  ╚██████╗██║  ██║██║ ╚████║ ╚████╔╝ ██║  ██║███████║
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
  ─────────────────────────────────────────────────────
   Terminal Fractal Art Generator  ·  Infinite Depth
```

> **Render stunning fractal art directly in your terminal — ANSI colors, multiple fractals, zoom animation, and zero dependencies.**

---

## Table of Contents

- [Features](#features)
- [Fractals](#fractals)
- [Gallery](#gallery)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [render](#render)
  - [gallery](#gallery-command)
  - [animate](#animate)
  - [list](#list)
- [Options Reference](#options-reference)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [License](#license)

---

## Features

- **5 distinct fractals** — Mandelbrot, Julia sets, Burning Ship, Newton basins, Tricorn
- **8 Julia presets** — rabbit, dragon, spiral, dendrite, galaxy, lightning, frost, coral
- **8 color palettes** — fire, ocean, forest, violet, ice, gold, neon, mono
- **6 character sets** — ultra, standard, blocks, braille, minimal, binary
- **Smooth coloring** — floating-point iteration escape-time formula for gradient depth
- **Zoom animation** — animated terminal zoom with configurable speed and frame count
- **Gallery mode** — cycles through a curated gallery of 8 stunning presets
- **Plain-text export** — save any frame as a portable ASCII-art text file
- **Zero dependencies** — pure Python 3.8+, nothing to install

---

## Fractals

| Name | Formula | Unique Property |
|------|---------|-----------------|
| **Mandelbrot** | z → z² + c, z₀ = 0 | The canonical fractal — infinite self-similar boundary |
| **Julia** | z → z² + c, c fixed | Each point in the Mandelbrot set corresponds to a Julia set |
| **Burning Ship** | z → (\|Re(z)\| + i\|Im(z)\|)² + c | Absolute-value variant; resembles a ship on fire |
| **Newton** | Newton's method on z³ − 1 | Three-color basins of attraction for each cube root of unity |
| **Tricorn** | z → conj(z)² + c | Complex-conjugate variant; exhibits tricorn-shaped cardioid |

---

## Gallery

### Mandelbrot Set  *(palette: fire)*

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#S###@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###S##@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##S+  %S#@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##%     %##@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@## ###SSSS   %S##S######@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##S  S             .#%*%#@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###*;                   S#@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@##@@@@@@@@@###%                       ##@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@#############                          S#@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@###% %    S###                         S#@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@####.         %S                         S#@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@###S*S           *                         #@@@@@@@@@@@@@
@@@@@@@@@@@@                                                   *###@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@###S*S           *                         #@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@####.         %S                         S#@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@###% %    S###                         S#@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@#############                          S#@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@##@@@@@@@@@###%                       ##@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###*;                   S#@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##S  S             .#%*%#@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@## ###SSSS   %S##S######@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##%     %##@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##S+  %S#@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###S##@@@@@@@@@@@@@@@@@@@@@@
```

---

### Julia Set — Dragon  *(palette: forest)*

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@% S   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#     ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@ :##  ##*        #%?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@#@@@@@@@@@@@@@#S   *%SS      ,    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@#. .   #@@@@#?  %   :?   +:,  *     *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@#% S   ;% S###  ;.         :     SS%%.*#@@@@@@@@@@@@@#,@@@@@@@@@@@@@@@
@@@@@@@@@      :+%SS## ?.            ;+*?%SSSSS###### ##.   ##  S#@@@@@@@@@@@@@@
@@@@%  SS          %                   ;   SSS### S ;% * , %S       @@@@@@@@@@@@
@#    ;         ; ;,                 ,,   *?? ;? :.             ?   #@@@@@@@@@@@
@@@##+ ;       ?*  .                  ;   ;+  .              .:?SSS####   S@@@@@
@@@@@@S   ####SSS?:.              .  +;   ;                  .  *?       ; +##@@
@@@@@@@@@@@@#   ?             .: ?; ??*   ,,                 ,; ;         ;    #
@@@@@@@@@@@@@       S% , * %; S ###SSS   ;                   %          SS  %@@@
@@@@@@@@@@@@@@@#S  ##   .## ######SSSSS%?*+;            .? ##SS%+:      @@@@@@@@
@@@@@@@@@@@@@@@@,#@@@@@@@@@@@@@#*.%%SS     :         .;  ###S %;   S %#@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*     *  ,:+   ?:   %  ?#@@@@#   . .#@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#    ,      SS%*   S#@@@@@@@@@@@@@#@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@?%#        *##  ##: @@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   S %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

---

### Burning Ship Fractal  *(palette: ocean)*

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@####:    #@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@####S         @@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@####S;           @@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@######S%               @@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@####S%    %SSSS%*                  @@@@@@@@@@@@@@@@@@@@@@@@
                                                    S##@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@##                                        S##@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@                                        %##@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@S:                                     ?##@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@#:                                     S##@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@;S@@                                 %##@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@?                                 S##@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@S#                                 %##@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@# *##S                             %##@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@S;#S#:,                             %##@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@S;%?;#*,S S                          ?##@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@#S ?# %+.*S*                         ##@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@#%%@;+ ;S%%+@S#;                      %#@@@@@@@@@#@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@%S##?%+@@@@@@@%.  @@                S@@@@@@@@@@@@@@@@
```

---

### Newton Basins  *(3 roots of z³ = 1)*

```
████████████████████████████████████████████████████████████████████▓███████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████▓▓▓█████████████████████
████████████████████████████████████████████████████████▓███████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█████████████████████████████████████████████████████████████████████████▓██████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████▓███████████████████████████████████████
██████████████████████████▓█████████████████████████████████████████████████████
███████████████████████▓█████████████████▓██████████████████████████████████████
███████████████████████▓█████████████████▓██████████████████████████████████████
██████████████████████████▓█████████████████████████████████████████████████████
```

---

## Installation

**No installation required** — just clone and run:

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
python main.py --help
```

Or use as a Python module:

```bash
python -m fractal_canvas --help
```

**Requirements:** Python 3.8+, a terminal that supports ANSI 256-color codes (most modern terminals do).

---

## Quick Start

```bash
# Render the classic Mandelbrot set
python main.py render mandelbrot

# Render a Julia set (dragon preset) in violet
python main.py render julia --preset dragon --palette violet

# Show the full gallery
python main.py gallery

# Animate a zoom into the Mandelbrot seahorse valley
python main.py animate mandelbrot --cx -0.7453 --cy 0.1127 --frames 40

# List everything available
python main.py list
```

---

## Usage

### `render`

Render a single fractal frame to the terminal.

```
python main.py render <fractal> [options]
```

**Fractals:** `mandelbrot`  `julia`  `burning_ship`  `newton`  `tricorn`

```bash
# Full-detail Mandelbrot with ultra char-set
python main.py render mandelbrot --chars ultra --palette fire --width 140 --height 50

# Julia — spiral preset, ice palette
python main.py render julia --preset spiral --palette ice

# Custom Julia parameter c = -0.4 + 0.6i
python main.py render julia --julia-c -0.4 0.6

# Zoom into a specific region of the Mandelbrot set
python main.py render mandelbrot --xmin -0.76 --xmax -0.74 --ymin 0.09 --ymax 0.12

# Save to a text file
python main.py render burning_ship --save ship.txt
```

---

### `gallery` (command)

Cycle through 8 curated presets with varying palettes and char sets.

```bash
python main.py gallery --width 100 --height 36
python main.py gallery --pause 2.0      # 2-second pause between items
```

---

### `animate`

Zoom smoothly into any fractal at any coordinate.

```bash
# Zoom into Mandelbrot seahorse valley
python main.py animate mandelbrot --cx -0.7453 --cy 0.1127

# Zoom into a spiral Julia set
python main.py animate julia --preset spiral --cx 0.0 --cy 0.0 --frames 50

# Fast zoom, neon palette
python main.py animate mandelbrot --zoom 0.75 --delay 0.05 --palette neon
```

---

### `list`

Print all available fractals, Julia presets, palettes, and char sets.

```bash
python main.py list
```

---

## Options Reference

| Option | Default | Description |
|--------|---------|-------------|
| `--width N` | 100 | Output width in columns |
| `--height N` | 40 | Output height in rows |
| `--max-iter N` | 100 | Max iterations (higher = more detail, slower) |
| `--palette NAME` | fire | Color palette: `fire ocean forest violet ice gold neon mono` |
| `--chars NAME` | standard | Char set: `ultra standard blocks braille minimal binary` |
| `--preset NAME` | rabbit | Julia preset: `rabbit dragon spiral dendrite galaxy lightning frost coral` |
| `--julia-c RE IM` | — | Custom Julia c parameter (overrides `--preset`) |
| `--xmin/xmax/ymin/ymax` | — | Custom viewport bounds |
| `--save FILE` | — | Write plain-text (no ANSI) copy to FILE |
| `--frames N` | 30 | Animation frame count |
| `--zoom F` | 0.85 | Per-frame zoom factor (smaller = faster zoom) |
| `--delay F` | 0.08 | Seconds between animation frames |

---

## Project Structure

```
fractal_canvas/
│
├── fractal_canvas/          # Core package
│   ├── __init__.py          # Public API surface
│   ├── __main__.py          # python -m fractal_canvas entry point
│   ├── fractals.py          # Mandelbrot, Julia, Burning Ship, Newton, Tricorn
│   ├── palettes.py          # ANSI color palettes + ASCII char sets
│   ├── renderer.py          # Frame rendering, print, save, animate
│   └── cli.py               # argparse CLI + gallery definitions
│
├── examples/                # Pre-rendered ASCII art reference files
│   ├── mandelbrot.txt
│   ├── julia_dragon.txt
│   ├── burning_ship.txt
│   └── newton.txt
│
├── main.py                  # Convenience entry point
├── setup.py                 # Package installation
├── requirements.txt         # (empty — no deps)
└── README.md
```

---

## How It Works

### Escape-Time Algorithm

For each pixel `(col, row)` the renderer maps screen coordinates to a complex number `c` in the fractal's domain.  It then iterates the fractal's recurrence relation until either the orbit escapes (|z| > 2) or `max_iter` is reached.

### Smooth Coloring

Raw iteration counts produce harsh color bands.  Fractal Canvas uses the **normalized iteration count** (Mandelbrot/Julia):

```
ν = i + 1 − log₂(log₂(|z|))
```

This fractional offset produces continuous, band-free gradients.

### Rendering Pipeline

```
complex plane bounds
       │
       ▼
  pixel → complex c         (screen-to-domain mapping)
       │
       ▼
  fractal fn(c, max_iter)   (escape-time computation)
       │
       ▼
  smooth float value
       │
       ├─► map_to_char()    (value → ASCII character)
       │
       └─► map_to_color()   (value → ANSI 256-color code)
              │
              ▼
         colored string      (one per row → printed/saved)
```

### Terminal Aspect Ratio

Terminal character cells are roughly 2× taller than wide.  When the y-span equals the x-span in complex coordinates, rendered images appear compressed vertically.  The renderer automatically halves the y-span relative to x-span so the output looks proportional.

---

## Julia Preset Reference

| Preset | c parameter | Character |
|--------|------------|-----------|
| `rabbit` | −0.123 + 0.745i | Douady's rabbit — tri-lobed cardioid |
| `dragon` | −0.727 + 0.189i | Dragon wings with fine filaments |
| `spiral` | −0.400 + 0.600i | Dense spiral arms |
| `dendrite` | 0 + 1i | Infinitely branching dendrite (critically finite) |
| `galaxy` | −0.800 + 0.156i | Galactic spiral arms |
| `lightning` | −0.700 + 0.270i | Explosive branching lightning bolts |
| `frost` | −0.425 + 0.163i | Frost crystal lattice |
| `coral` | 0.285 + 0.010i | Coral reef branching |

---

## License

MIT — do whatever you want, just don't blame me if you lose hours zooming into seahorse valleys.
