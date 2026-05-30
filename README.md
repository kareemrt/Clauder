# FractalDive 🌀

> **Explore infinite mathematical beauty — right inside your terminal.**

FractalDive is an interactive fractal explorer that renders the **Mandelbrot set** and **Julia sets** in full truecolor using Unicode half-block characters (`▄`). Zoom through infinite complexity, switch color themes on the fly, and export ASCII snapshots — all without leaving your shell.

---

## Table of Contents

- [Why Fractals?](#why-fractals)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive Explorer](#interactive-explorer)
  - [Static Render](#static-render)
  - [Theme Showcase](#theme-showcase)
- [Controls](#controls)
- [Color Themes](#color-themes)
- [Julia Set Presets](#julia-set-presets)
- [Project Structure](#project-structure)
- [The Math](#the-math)
- [Performance Notes](#performance-notes)

---

## Why Fractals?

The Mandelbrot set is defined by a devastatingly simple rule:

```
z₀ = 0
zₙ₊₁ = zₙ² + c
```

Yet this tiny recurrence generates **infinite, self-similar complexity** — zoom in anywhere on the boundary and new structures emerge forever. No matter how deep you go, you never reach a "bottom." This is one of the most astonishing facts in all of mathematics.

```
                        ████████
                    ████████████████
                  ████████████████████
                ████████████████████████
        ██    ██████████████████████████ ██
       █████████████████████████████████████
      ████████████████████████████████████████
    █████████████████████████████████████████████
   ████████████████████████████████████████████████
  ██ ██████████████████████████████████████████████
  █████████████████████████████████████████████████
 ████████████████████████████████████████████████
 █████████████████████████████████████████████████
  ██████████████████████████████████████████████
  ████████████████████████████████████████████████
   ███████████████████████████████████████████████
    █████████████████████████████████████████████
      █████████████████████████████████████████
       ████████████████████████████████████████
        ████████████████████████████████████
                ████████████████████████████ ██
                ████████████████████████
                  ████████████████████
                    ████████████████
                        ████████
```
*The classic Mandelbrot set shape (ASCII approximation)*

---

## Features

| Feature | Description |
|---|---|
| **Truecolor rendering** | 24-bit RGB via ANSI escape codes — 16 million possible colors |
| **Half-block trick** | Each terminal row renders **2 pixel rows** using `▄`, doubling vertical resolution |
| **Smooth coloring** | Escape-time algorithm with logarithmic normalization — no ugly color bands |
| **Interactive explorer** | Real-time pan, zoom, and mode switching via keyboard |
| **Julia sets** | 6 named presets; switch instantly from any Mandelbrot coordinate |
| **6 color themes** | Fire, Ocean, Electric, Midnight, Gold, Psychedelic |
| **ASCII snapshot export** | Save any view as a portable `.txt` file |
| **Zero external deps** | Only requires `numpy` — no GUI libraries |

---

## How It Works

### The Half-Block Rendering Trick

Standard terminals have character cells that are roughly twice as tall as they are wide. FractalDive exploits the Unicode half-block character `▄` to pack **two pixel rows into one terminal row**:

```
Terminal row N  →  pixel rows 2N  and  2N+1
                   ┌──────────────┐
                   │  top pixel   │  ← foreground color
                   │──────────────│
                   │ bottom pixel │  ← background color
                   └──────────────┘
                         ▄
```

This doubles vertical resolution with no additional screen space.

### Smooth Coloring

Raw escape-time coloring produces harsh color bands. FractalDive uses the **normalized iteration count**:

```
smooth = iteration - log₂(log₂(|z|))
```

This maps integer escape counts to smooth floats, which are then passed through a color gradient to produce continuous, band-free color transitions.

### Computation Pipeline

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│  Viewport   │───▶│  numpy grid  │───▶│  Iteration  │───▶│   Smooth     │
│  (cx,cy,z)  │    │  of complex  │    │  loop       │    │   coloring   │
│             │    │  numbers     │    │  z = z²+c   │    │  (float[])   │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                                                                  │
                                                                  ▼
                                                        ┌──────────────────┐
                                                        │  Palette lookup  │
                                                        │  ANSI truecolor  │
                                                        │  half-block ▄    │
                                                        └──────────────────┘
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install the only dependency
pip install numpy

# Run it
python main.py
```

**Requirements:**
- Python 3.11+
- numpy >= 1.24
- A terminal with truecolor support (iTerm2, kitty, Windows Terminal, most modern terminals)

---

## Usage

### Interactive Explorer

```bash
# Launch with Mandelbrot set (default)
python main.py

# Launch directly in Julia mode
python main.py explore --julia
```

The explorer fills your terminal window and responds to keyboard input in real time.

### Static Render

Print a single frame directly to your terminal — useful for screenshots or piping:

```bash
# Mandelbrot, fire theme, 120x40
python main.py render

# Julia galaxy preset, ocean theme
python main.py render --julia --preset galaxy --theme ocean

# Custom size and iteration depth
python main.py render --width 160 --height 50 --max-iter 512 --theme electric
```

### Theme Showcase

Print all 6 themes back-to-back:

```bash
python main.py demo
```

---

## Controls

```
┌─────────────────────────────────────┐
│         Interactive Controls        │
├──────────────┬──────────────────────┤
│  <- -> Up Dn │  Pan                 │
│  +  /  -     │  Zoom in / out       │
│  T           │  Cycle color theme   │
│  J           │  Toggle Julia mode   │
│  N           │  Next Julia preset   │
│  M           │  Cycle max iters     │
│  R           │  Reset view          │
│  S           │  Save snapshot       │
│  H           │  Toggle help         │
│  Q / Esc     │  Quit                │
└──────────────┴──────────────────────┘
```

**Zoom levels:** Each `+` press multiplies zoom by ~1.67x. After 20 presses you're looking at a region 160,000x smaller than the starting view — and still finding new detail.

---

## Color Themes

Six handcrafted gradient themes, each mapped to `[0, 1]` smooth escape values:

```
fire        [##########] black → deep red → orange → yellow → white
ocean       [~~~~~~~~~~] deep navy → cobalt → teal → cyan → white
electric    [**********] black → purple → blue → cyan-green → chartreuse
midnight    [::::::::::] near-black → indigo → violet → lavender → white
gold        [$$$$$$$$$$] near-black → dark amber → gold → pale yellow
psychedelic [@@@@@@@@@@] full HSV rainbow cycling (smooth, no banding)
```

Interior points (confirmed non-escaping) are rendered in a deep midnight blue — distinct from all theme colors — so the fractal boundary is always crisp.

---

## Julia Set Presets

Julia sets use the same iteration rule (`z = z² + c`) but with a **fixed** complex constant `c` and **variable** starting point `z`. Each value of `c` produces a completely different shape:

| Preset | c value | Character |
|---|---|---|
| `classic` | -0.7 + 0.27015i | Dendrite spirals |
| `spiral` | -0.4 + 0.6i | Double spirals |
| `galaxy` | 0.285 + 0.01i | Branching galaxies |
| `dragon` | -0.70176 - 0.3842i | Dragon curves |
| `lightning` | -0.835 - 0.2321i | Lightning bolt trees |
| `star` | 0.45 + 0.1428i | Star clusters |

```bash
python main.py render --julia --preset lightning --theme midnight
```

---

## Project Structure

```
fractal_dive/
│
├── __init__.py          Package metadata
│
├── core.py              Fractal computation engine
│   ├── mandelbrot()     Vectorized Mandelbrot via numpy
│   ├── julia()          Julia set for any complex c
│   └── _smooth_iter()   Normalized escape-time coloring
│
├── themes.py            Color palettes
│   ├── _gradient()      Linear interpolation between color stops
│   ├── FIRE / OCEAN     Pre-built theme palettes
│   ├── ELECTRIC / etc.  ...
│   └── psychedelic()    HSV-cycling rainbow function
│
├── renderer.py          Terminal output
│   ├── render_frame()   Array -> ANSI half-block string
│   └── render_static()  Print one frame to stdout
│
└── explorer.py          Interactive curses UI
    ├── Explorer          State machine: viewport, mode, theme
    ├── _compute()        Calls core.py with current viewport
    ├── _draw()           Renders frame via renderer.py
    └── launch()          curses.wrapper entry point

main.py                  CLI entry point (argparse)
requirements.txt         numpy>=1.24
```

---

## The Math

### Mandelbrot Set Membership

A point `c` in the complex plane is in the Mandelbrot set if the sequence:

```
z_0 = 0
z_{n+1} = z_n^2 + c
```

remains **bounded** (i.e., `|z_n| <= 2` for all n). Points that escape to infinity get colored by *how fast* they escape — that's what creates the colorful boundary.

### The Escape Radius

Once `|z| > 2`, the sequence is guaranteed to diverge. This is the escape radius — a beautiful result that means we only need to check `|z| <= 2`.

*Proof sketch:* If `|z| > 2` and `|z| > |c|`, then `|z²+c| >= |z|² - |c| > |z|(|z|-1) > |z|`. Each iteration strictly increases the magnitude — divergence is certain.

### Smooth Coloring Formula

The raw iteration count `n` creates discrete color bands. The smooth version:

```
mu = n - log2(log2(|z_n|))
```

As `|z_n|` grows exponentially after escape, `log2(log2(|z_n|))` grows slowly and smoothly, giving fractional iteration counts that interpolate between integer bands.

### Julia Sets

For any fixed `c`, the map `f_c(z) = z² + c` has a **Julia set** — the boundary between initial values `z_0` that escape and those that don't. When `c` is inside the Mandelbrot set, the Julia set is connected; when `c` is outside, the Julia set is a Cantor dust. This is the **fundamental theorem connecting the two sets**.

---

## Performance Notes

- Rendering uses fully vectorized numpy operations — no Python loops over individual pixels
- A 120x80 frame (9,600 pixels, 256 iterations) renders in ~0.5-1s on modern hardware
- Increase `--max-iter` for sharper detail in deep zooms; decrease for faster exploration
- The half-block trick means the actual pixel array is `width x (2 x terminal_rows)` — tall framebuffers are expected

---

*Built with numpy and one mathematical rabbit hole.*
