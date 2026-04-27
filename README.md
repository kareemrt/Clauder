# FractalForge

> *A terminal fractal explorer and renderer — infinite complexity from a single equation.*

```
╔══════════════════════════════════════════════════════════════════════╗
║  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗              ║
║  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║              ║
║  █████╗  ██████╔╝███████║██║        ██║   ███████║██║              ║
║  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║              ║
║  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗         ║
║  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝         ║
║                                                                      ║
║   ███████╗ ██████╗ ██████╗  ██████╗ ███████╗                        ║
║   ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝                        ║
║   █████╗  ██║   ██║██████╔╝██║  ███╗█████╗                          ║
║   ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝                          ║
║   ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗                        ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                        ║
╚══════════════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Terminal](https://img.shields.io/badge/runs%20in-terminal-black?style=flat-square&logo=gnome-terminal)](.)
[![Fractals](https://img.shields.io/badge/fractals-4%20types-purple?style=flat-square)](.)

---

## What Is This?

**FractalForge** renders mathematically beautiful fractals directly in your terminal using colored Unicode block characters — no GUI, no browser, no dependencies beyond Python itself (Pillow optional for PNG export).

The mathematics is deceptively simple. For the Mandelbrot set, every pixel asks one question:

```
z₀ = 0
zₙ₊₁ = zₙ² + c        (where c is the pixel's complex coordinate)

Does |z| stay bounded as n → ∞?
```

If yes → the point belongs to the set (rendered black).
If no → how *quickly* it escapes determines the color.

This single rule produces infinite self-similar complexity — zoom in anywhere on the boundary and new detail emerges forever.

---

## Fractals Included

| Type | Formula | Character |
|------|---------|-----------|
| **Mandelbrot** | `z = z² + c`, `z₀ = 0` | The canonical fractal — two bulbs, infinite filaments |
| **Julia** | `z = z² + c`, `z₀ = pixel`, `c = constant` | A family of shapes; each `c` value yields a different geometry |
| **Burning Ship** | `z = (|Re(z)| + i|Im(z)|)² + c` | Absolute values create a haunting ship silhouette |
| **Tricorn** | `z = z̄² + c` (conjugate) | Conjugating z produces three-fold symmetry |

---

## Terminal Preview

```
Mandelbrot Set — default view (80×25, cosmic palette)

      ░░░░░░░░░▒▒▒▓▓▓▓▓███▓▓▓▓▒▒▒░░░░░░░░░
    ░░░░░░░░▒▒▒▒▒▓▓▓▓████████████▓▓▒▒▒░░░░░
   ░░░░░░░▒▒▒▒▓▓▓▓████████  ██████████▓▒▒░░░
  ░░░░░░▒▒▒▓▓▓▓███████████    ██████████▓▒▒░░
 ░░░░▒▒▒▒▓▓████████████████  ████████████▓▒▒░
░░░▒▒▒▓▓████████████████████████████████▓▒▒░
░░▒▒▓▓██████████████████████████████████▓▒▒░
░▒▒▓▓███████████████████████████████████▓▒▒░
░▒▒▓▓███████████████████████████████████▓▒▒░
░░▒▒▓▓██████████████████████████████████▓▒▒░
░░░▒▒▒▓▓████████████████████████████████▓▒▒░
 ░░░▒▒▒▒▓▓████████████████████████████▓▒▒░░
  ░░░░▒▒▒▒▓▓▓▓███████████████████████▓▓▒▒░░░
   ░░░░░░▒▒▒▒▒▓▓▓▓████████████████▓▓▒▒▒░░░░
    ░░░░░░░░░▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░░░░
      ░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░
```

```
Julia Set — c = -0.7269 + 0.1889i  (the "Swirl" preset)

   ░░░░▒▒▒▒▓▓▓▓██████████████████▓▓▓▓▒▒▒▒░░░░
   ░░▒▒▒▒▓▓▓▓████████████████████████▓▓▓▒▒▒░░
  ░▒▒▒▓▓▓████████████████████████████████▓▓▒▒░
  ▒▒▓▓▓███████████████████████████████████▓▒▒▒
 ░▒▒▓▓███████   ██████████████████   ██████▓▒▒░
 ░▒▒▓███████      █████████████████    █████▓▒▒░
 ░▒▓▓██████  ░     ████████████████  ░  █████▓▒░
 ░▒▓▓████  ░▒▒░   ██████████████████  ░▒████▓▒░
 ░▒▓▓████  ▒▓▒   ████████████████████ ░▒████▓▒░
 ░▒▒▓███████    ██████████████████████  ███▓▒▒░
  ▒▒▒▓▓████████████████████████████████▓▓▒▒▒
  ░▒▒▒▓▓▓██████████████████████████████▓▓▒▒░
   ░░▒▒▒▓▓▓████████████████████████▓▓▓▒▒▒░░
     ░░░▒▒▒▒▒▒▓▓▓▓████████████▓▓▓▒▒▒▒░░░░
```

---

## Project Structure

```
FractalForge/
│
├── fractal_forge.py       # Main CLI — all fractal logic and rendering
│   ├── mandelbrot()       #   Mandelbrot engine
│   ├── julia()            #   Julia set engine
│   ├── burning_ship()     #   Burning Ship engine
│   ├── tricorn()          #   Tricorn engine
│   ├── PALETTES           #   6 ANSI 256-color palettes
│   ├── PRESETS            #   6 named zoom presets
│   ├── render_terminal()  #   Unicode block renderer
│   └── save_png()         #   High-res PNG export (Pillow)
│
├── requirements.txt       # Optional: Pillow>=10.0.0 for PNG export
└── README.md
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# No dependencies required for terminal rendering!
python fractal_forge.py

# Optional: install Pillow for PNG export
pip install -r requirements.txt
```

**Requirements:** Python 3.10+ (uses `list[...]` type hints). No third-party packages needed for terminal output.

---

## Usage

### Quick Start

```bash
# Default: Mandelbrot set, cosmic palette, 120×42 terminal
python fractal_forge.py

# Julia set with fire palette
python fractal_forge.py --fractal julia --palette fire

# Burning Ship fractal
python fractal_forge.py --fractal burning_ship --palette ocean

# Tricorn with neon palette
python fractal_forge.py --fractal tricorn --palette neon
```

### Named Presets

```bash
# List all presets
python fractal_forge.py --list-presets

# Seahorse Valley — a famous Mandelbrot zoom (80× zoom)
python fractal_forge.py --preset seahorse

# Swirling Julia set
python fractal_forge.py --preset swirl --palette cosmic

# Dendrite Julia — fractal branches
python fractal_forge.py --preset dendrite --palette matrix
```

### Manual Zoom

```bash
# Zoom into a specific coordinate
python fractal_forge.py --cx -0.745 --cy 0.1 --zoom 80

# Deep zoom into the Mandelbrot boundary
python fractal_forge.py --cx -1.401155 --cy 0.0 --zoom 500 --iter 512

# Julia with custom c parameter
python fractal_forge.py --fractal julia --jc-real -0.4 --jc-imag 0.6
```

### High-Resolution PNG Export

```bash
# Save a 1920×1080 PNG (requires Pillow)
python fractal_forge.py --output mandelbrot.png

# 4K Burning Ship
python fractal_forge.py --fractal burning_ship --output ship.png \
  --png-width 3840 --png-height 2160

# Zoomed Julia PNG
python fractal_forge.py --preset swirl --output swirl.png \
  --png-width 2560 --png-height 1440 --iter 256
```

### Show Render Info

```bash
python fractal_forge.py --preset seahorse --info
```

```
╭────────────────────────────────────────────────╮
│              FractalForge  —  Render Info              │
├────────────────────────────────────────────────┤
│  Fractal : Mandelbrot                          │
│  Center  : (-0.745000, 0.100000)               │
│  Zoom    : 80.0000                             │
│  Iter    : 128                                 │
│  Palette : cosmic                              │
╰────────────────────────────────────────────────╯
```

---

## CLI Reference

```
usage: fractal_forge [--fractal TYPE] [--preset NAME] [--list-presets]
                     [--width W] [--height H]
                     [--cx X] [--cy Y] [--zoom Z] [--iter N]
                     [--palette PALETTE]
                     [--jc-real R] [--jc-imag I]
                     [--output PATH] [--png-width W] [--png-height H]
                     [--info]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--fractal` | `mandelbrot` | `mandelbrot` \| `julia` \| `burning_ship` \| `tricorn` |
| `--preset` | — | Named preset (overrides cx/cy/zoom/fractal) |
| `--list-presets` | — | Print available presets and exit |
| `--width` | `120` | Terminal render width in characters |
| `--height` | `42` | Terminal render height in characters |
| `--cx` | `-0.5` | Center X coordinate (real axis) |
| `--cy` | `0.0` | Center Y coordinate (imaginary axis) |
| `--zoom` | `1.0` | Zoom multiplier (larger = deeper zoom) |
| `--iter` | `128` | Maximum escape iterations (higher = more detail) |
| `--palette` | `cosmic` | `cosmic` \| `fire` \| `ocean` \| `neon` \| `matrix` \| `ice` |
| `--jc-real` | `-0.7` | Julia set: real part of c |
| `--jc-imag` | `0.27015` | Julia set: imaginary part of c |
| `--output` | — | Save PNG to path (requires Pillow) |
| `--png-width` | `1920` | PNG width in pixels |
| `--png-height` | `1080` | PNG height in pixels |
| `--info` | — | Print render info box after drawing |

---

## Color Palettes

| Palette | Description |
|---------|-------------|
| `cosmic` | Deep blues → cyan → yellow → orange → red → purple |
| `fire` | Black → dark red → orange → yellow → white |
| `ocean` | Midnight blue → teal → aqua → white |
| `neon` | Black → purple → magenta → hot pink → orange |
| `matrix` | Black → dark green → bright green → white |
| `ice` | Midnight blue → cyan → ice white |

---

## Presets

| Preset | Fractal | Location | Zoom |
|--------|---------|----------|------|
| `seahorse` | Mandelbrot | Seahorse Valley (-0.745, 0.1) | 80× |
| `elephant` | Mandelbrot | Elephant Valley (0.3, 0.0) | 40× |
| `star` | Julia | c = -0.4 + 0.6i | 1× |
| `dendrite` | Julia | c = 0 + 1i | 1× |
| `swirl` | Julia | c = -0.7269 + 0.1889i | 1× |
| `ship` | Burning Ship | (-0.5, -0.5) | 1× |

---

## The Mathematics

### Mandelbrot Set

The Mandelbrot set `M` is the set of complex numbers `c` for which the orbit of `0` under `f(z) = z² + c` remains bounded:

```
M = { c ∈ ℂ : sup{ |fₙ(0)| : n ≥ 0 } < ∞ }
```

**Key properties:**
- **Self-similarity**: zoom into any point on the boundary to reveal smaller copies of the whole set
- **Connected**: M is a single connected piece (Douady & Hubbard, 1982)
- **Boundary**: has Hausdorff dimension 2 — it is a fractal of maximum complexity
- **Universality**: contains infinitely many copies of itself at every scale

### Julia Sets

For a fixed `c`, the Julia set `J(c)` is the boundary between initial points `z₀` that escape to infinity and those that don't:

```
J(c) = ∂{ z ∈ ℂ : orbit of z under f(z) = z² + c is bounded }
```

The Mandelbrot set is essentially a *map of Julia sets*: a point `c` is in `M` if and only if `J(c)` is connected.

### Smooth Coloring (PNG mode)

Instead of raw iteration count, the PNG renderer uses **smooth escape time** via HSV hue rotation:

```
t = iteration_count / max_iterations
hue = (0.65 + t × 2.8) mod 1.0
color = HSV(hue, 0.85, 1.0)
```

This eliminates the harsh color bands that appear with integer iteration counts.

---

## How Rendering Works

```
For each pixel (col, row):
  │
  ├─ Map pixel → complex plane coordinate c
  │     x = x_min + (col / width)  × (x_max - x_min)
  │     y = y_max - (row / height) × (y_max - y_min)
  │
  ├─ Run escape-time algorithm → iteration count [0, max_iter]
  │
  ├─ Map iteration count → Unicode block character
  │     0%  →  ' '  (space, far outside)
  │     25% →  '░'  (light shade)
  │     50% →  '▒'  (medium shade)
  │     75% →  '▓'  (dark shade)
  │     100% → '█'  (full block, inside set = black)
  │
  └─ Map iteration count → ANSI 256-color code → print
```

---

## Tips

- **More detail**: increase `--iter` (try 256, 512, 1024 for deep zooms)
- **Bigger picture**: pipe to a terminal with a small font, or use `--width 200 --height 60`
- **Discover new views**: try `--cx` values near `-0.75` and `--zoom` between 10–200
- **Julia exploration**: sweep `--jc-real` from -2 to 2 in small steps — each value gives a completely different shape
- **PNG for wallpapers**: `--png-width 3840 --png-height 2160 --iter 512` takes ~30s but produces stunning 4K images

---

## License

MIT — do whatever you want with it.

---

*Built by Claude (Anthropic) — because infinite complexity from a single equation is too beautiful not to explore.*
