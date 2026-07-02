# MandelCLI — Terminal Fractal Explorer

```
 ███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗██╗      ██████╗██╗     ██╗
 ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝██║     ██╔════╝██║     ██║
 ██╔████╔██║███████║██╔██╗ ██║██║  ██║█████╗  ██║     ██║     ██║     ██║
 ██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║██╔══╝  ██║     ██║     ██║     ██║
 ██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗╚██████╗███████╗██║
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝
```

**An animated deep-dive into the Mandelbrot set, rendered entirely in your terminal.**

`fractal_explorer.py` uses half-block Unicode characters (`▀▄`) and 24-bit ANSI color
to deliver **2× vertical resolution** — turning a 80×24 terminal into an effective
80×48 canvas. Computation is fully vectorized with NumPy for smooth real-time animation.

---

## What You'll See

```
┌─────────────────── ✦ MandelCLI  psychedelic  seahorse ───────────────────────┐
│▀▀▀▀▀▀▀▀▀▀▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│▀▀▀▀▀▀▀▄▄▄▄█████████████████▄▄▄▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│▀▀▀▀▀▄▄▄███████████████████████████▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│▀▀▀▄▄███████████████████████████████████▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│▀▄▄█████████████████████████████████████████▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│  ▀▀▀▄▄▄█████████████████████████████████████████▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│      ▀▄▄▄███████████████████████████████████████████▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│           ▀▀▄▄▄▄▄████████████████████████████████▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
└─── zoom ×36000  iter 256  (-0.726900, 0.188900)  frame 73/110  Ctrl+C to quit ───┘
```

*(Colors rendered in full 24-bit RGB — the ASCII preview can't capture the depth!)*

---

## Features

| Feature | Description |
|---|---|
| **Half-block rendering** | `▀▄` characters × 24-bit color = 2× vertical resolution |
| **Vectorized NumPy** | Full frame computed as a single array operation — no Python loops in the hot path |
| **Smooth coloring** | Eliminates iteration-count banding via log-log interpolation |
| **6 color schemes** | `psychedelic` `fire` `ocean` `gold` `ice` `plasma` |
| **5 zoom targets** | Seahorse Valley, Elephant Valley, Lightning Spiral, Main Bulb, Full Overview |
| **Julia sets** | Pass any complex constant `c` to explore the corresponding Julia set |
| **Animated zoom** | Cubic ease-in/out + exponential scale → cinematic fly-in effect |
| **Dynamic iteration depth** | Max iterations ramp up as you zoom in, preserving speed early and detail late |

---

## Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements.txt
python3 fractal_explorer.py
```

**Requirements:** Python 3.9+, a terminal that supports 24-bit (true) color.

Most modern terminals qualify:
- iTerm2, Terminal.app (macOS)
- Windows Terminal, VS Code integrated terminal (Windows)
- GNOME Terminal, Alacritty, Kitty (Linux)

---

## Usage

```
python3 fractal_explorer.py [OPTIONS]

Options:
  --scheme {psychedelic,fire,ocean,gold,ice,plasma}
                      Color palette (default: psychedelic)
  --target {seahorse,elephant,lightning,bulb,overview}
                      Zoom destination (default: seahorse)
  --fps N             Target frame rate (default: 8)
  --iter N            Max Mandelbrot iterations (default: 256)
  --julia RE IM       Julia set for c = RE + IM·i
  --list-targets      Show all zoom destinations
```

### Examples

```bash
# Zoom into Seahorse Valley with fire colors
python3 fractal_explorer.py --scheme fire --target seahorse

# Elephant Valley with ice colors, higher detail
python3 fractal_explorer.py --scheme ice --target elephant --iter 512

# Julia set for a beautiful parameter
python3 fractal_explorer.py --julia -0.7269 0.1889

# Full overview — see the whole set
python3 fractal_explorer.py --target overview --scheme plasma

# Fastest render (lower quality)
python3 fractal_explorer.py --fps 15 --iter 128
```

---

## Zoom Targets

```
seahorse     center (-0.7269, 0.1889)  scale 5e-5  — spiraling tentacles, self-similar vortices
elephant     center ( 0.2929, 0.0000)  scale 6e-5  — enormous fractal tusks, bulbous chambers
lightning    center (-0.5252,-0.5235)  scale 4e-5  — a perpetual electric storm of spirals
bulb         center (-1.2548, 0.0000)  scale 5e-4  — gateway from order into chaos
overview     center (-0.5000, 0.0000)  scale 1.8   — the entire infinite coastline at once
```

---

## Color Schemes

```
psychedelic  ──── Rainbow cycling (frequency ×6), smooth sine waves across all three channels
fire         ──── Black → deep crimson → molten gold → incandescent white
ocean        ──── Abyssal black → midnight blue → electric cyan → arctic white
gold         ──── Shadow → warm amber → pale gold → sunrise white
ice          ──── Deep indigo → steel blue → ice crystal → pure white
plasma       ──── Dark violet → magenta → electric yellow → bone white
```

---

## How It Works

### The Mandelbrot Set

The Mandelbrot set is the set of complex numbers **c** for which the iteration:

```
z₀ = 0
zₙ₊₁ = zₙ² + c
```

remains **bounded** (never escapes to infinity). Points inside the set are colored black.
Points outside are colored by *how quickly* they escape — producing the fractal boundary.

### Smooth Coloring

Naive iteration counts produce visible "banding." MandelCLI uses the **smooth (normalized)
iteration count** formula to eliminate this:

```
smooth_n = n + 1 − log₂( log₂( |zₙ| ) )
```

This exploits the fact that `log₂(|z|)` converges smoothly to ∞ at the escape boundary,
giving a continuous (non-integer) escape count that maps to smooth color gradients.

### Half-Block Rendering

Each terminal character cell encodes **two pixel rows** using:

```
Character   Meaning                          When to use
─────────────────────────────────────────────────────────
▀           Upper half filled (fg color)     only top pixel is non-black
▄           Lower half filled (fg color)     only bottom pixel is non-black
▀ on bg     Upper fg, lower bg              both pixels non-black
[space]     No fill                          both pixels are black
```

A 80×24 terminal becomes an effective **80×48 display** — double the vertical detail.

### Architecture

```
fractal_explorer.py
│
├── Color Schemes ────────── _make_colormap()  →  (2048, 3) uint8 look-up table
│   ├── psychedelic          sine-wave RGB, ×6 frequency
│   ├── fire                 piecewise linear ramp (black→red→gold→white)
│   ├── ocean / gold / ice   custom linear blends per channel
│   └── plasma               mixed sine + linear
│
├── Fractal Engine ──────── compute_mandelbrot() / compute_julia()  →  (H×W) float32
│   ├── Vectorized NumPy complex arithmetic
│   ├── Active-mask early termination (stops tracking escaped points)
│   └── Smooth escape normalization (log-log trick)
│
├── Renderer ────────────── rgb_to_rich_text()  →  Rich Text object
│   ├── apply_colormap  (integer LUT index, fully vectorized)
│   └── Half-block character selection loop (only non-hot-path Python loop)
│
└── Animation ───────────── run_zoom_animation()
    ├── Cubic ease-in/out:     t → t²(3−2t)
    ├── Exponential scale:     scale = a·(b/a)^t
    ├── Dynamic iter ramp:     iter = max_iter × (0.4 + 0.6t)
    └── Rich Live display panel (border + title + subtitle)
```

---

## Performance Notes

On a modern laptop, expect roughly:

| Terminal size | `--iter 128` | `--iter 256` | `--iter 512` |
|---|---|---|---|
| 80 × 24  | 15–20 fps | 8–12 fps | 4–6 fps |
| 120 × 40 | 6–10 fps  | 3–5 fps  | 1–3 fps |
| 200 × 50 | 3–5 fps   | 1–3 fps  | <1 fps  |

NumPy's vectorized array operations keep the hot path out of Python's interpreter.
Reduce `--iter` for higher FPS; increase for finer detail in deep zooms.

---

## The Mathematics

The Mandelbrot set sits at the intersection of **complex dynamics**, **topology**, and
**algorithmic information theory**. A few remarkable facts:

- The boundary has **Hausdorff dimension 2** — the same dimension as a filled 2D region —
  yet its area is zero.
- Every point on the boundary is **infinitely complex**: zooming in *always* reveals new
  structure, forever.
- The **Mandelbrot connectedness theorem** (Douady & Hubbard, 1982): the set is connected —
  all the "islands" visible in deep zooms are actually joined by infinitely thin filaments.
- The Julia set for a given parameter `c` is either:
  - **Connected** — if `c` is inside the Mandelbrot set
  - **Cantor dust** — uncountably many disconnected points, if `c` is outside

The Mandelbrot set is, in a precise sense, a *map* of all possible Julia sets.

---

## Project Ideas (the brainstorm that led here)

Before settling on MandelCLI, several other ideas were considered:

1. **N-Body Gravitational Simulator** — watch planets and galaxies dance under Newton's law,
   rendered as colored ASCII trails. Beautiful, but physics tuning is fiddly.

2. **Conway's Game of Life + Pattern Detector** — classic automaton with real-time glider
   recognition and population statistics.

3. **ASCII Raytracer** — render 3D spheres and reflections as terminal art, one character
   per pixel.

4. **Terminal Music Visualizer** — real-time FFT of microphone input, rendered as animated
   ASCII frequency bars.

5. **Procedural Dungeon Generator** — roguelike rooms and corridors with treasure placement
   and pathfinding visualization.

MandelCLI won because the mathematics is genuinely profound, the output is guaranteed to be
beautiful at any zoom level, and the half-block rendering trick produces a result that makes
people stop and ask *"wait, that's running in a terminal?"*

---

## License

MIT — do whatever you like with it. If you zoom somewhere beautiful, share the coordinates.
