# Fractals — Terminal Fractal Explorer

> Explore infinite mathematical beauty directly in your terminal.
> Zero dependencies. Pure Python. Pure art.

```
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗     ███████╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║     ██╔════╝
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║     ███████╗
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║     ╚════██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗███████║
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
```

---

## What Is This?

**Fractals** is an interactive terminal application for exploring mathematical fractals — rendered entirely with ANSI escape codes and ASCII characters, with zero external dependencies.

Three fractal types, six color palettes, real-time zoom/pan, smooth coloring algorithms, and a demo mode that cycles through the most spectacular views automatically.

---

## Fractals Available

### 1. Mandelbrot Set

The most famous fractal in mathematics. The boundary of the Mandelbrot set has infinite complexity — no matter how much you zoom in, new structures appear forever.

```
                             ......,,,,,,,,,,......
                             ......,,,,,,,,,,......
                            ......,,,,,,,,,,,,......
                            .....,,,,,,,,,,,,,,.....
                           .....,,,,,:::::,,,,,,.....
                           .....,,,,,::::::,,,,,.....
                           .....,,,,::::::::,,,,.....
                           ....,,,,::::;;::::,,,,....
                           ....,,,,:::;;;;:::,,,,....
                           ....,,,,::;;++;;::,,,,....
                          .....,,,,::;;+=+;::,,,,.....
                          .....,,,,::;+x@+;::,,,,.....
                          .....,,,,::;=  +;::,,,,.....     <- the gap is
                          .....,,,,::;=  +;::,,,,.....        the Mandelbrot
                          .....,,,,::;+x@+;::,,,,.....        cardioid
                          .....,,,,::;;+=+;::,,,,.....
                           ....,,,,::;;++;;::,,,,....
                           ....,,,,:::;;;;:::,,,,....
                           ....,,,,::::;;::::,,,,....
                           .....,,,,::::::::,,,,.....
```

### 2. Julia Sets

Every point in the Mandelbrot set corresponds to a unique Julia set. This app ships **8 seed constants**, each producing a completely different shape:

| Seed | Constant | Character |
|------|----------|-----------|
| `dragon` | c = −0.7269 + 0.1889i | Fractal lightning bolt |
| `rabbit` | c = −0.123 + 0.745i | Douady rabbit ears |
| `galaxy` | c = −0.70176 − 0.3842i | Galaxy spirals |
| `dendrite` | c = 0 + 1i | Snowflake dendrites |
| `lightning` | c = −0.8 + 0.156i | Electric arcs |
| `snowflake` | c = −0.4 + 0.6i | Symmetric snowflake |
| `spiral` | c = 0.285 + 0.01i | Spiral tendrils |
| `douady_rabbit` | c = −0.12256 + 0.74486i | Classic Douady rabbit |

**Example — Douady Rabbit (zoom 3.5x):**

```
                         ....,,,,,,::,,,,,....
                         ...,,,,,::::::,,,,...
                        ....,,,,::::::::,,,...
                        ....,,,,:::;::::,,,....
                        ...,,,,:::;;;;:::,,,...
                       ....,,,,::;;++;;::,,,...
                       ....,,,:::;+X+++;:,,,...
                       ...,,,,::;;= xxx;::,,...
                       ...,,,:::;+= #  +::,,...
                       ...,,,::;;+x@  &=::,,...
                       ...,,,::;;X    =+::,,...
                       ...,,,::;+&  Xx+;::,,...
                       ...,,::;;+X  $=+;::,,...
                       ...,,::;+=$  X+;;::,,...
                       ...,,::;+xX  &+;::,,,...
                       ...,,::+=    X;;::,,,...
                       ...,,::=&  @x+;;::,,,...
```

### 3. Barnsley Fern (IFS Fractals)

Iterated Function Systems (IFS) build complex natural shapes from just 4 simple affine transformations applied randomly, millions of times. The result is a perfect botanical fern — built entirely from math.

Three IFS attractors included: `fern`, `tree`, `snowflake`.

```
                                              **************
                                         **************
                                    *****************
                                 *******************
                             **********************
                         *** *********************
                     **  *************************
                     *****************************
                ***  *****************************
                **********************************
           **** ***********************************
           ****************************************
      **   *****************************************
     ***********************************************
      *********************************************  *
***    ****************************************** ****
******* ******************* **************************
****************************************************   **
 ***************************** ******************** *****
  *********************** *******************************
    ***************************************************
       ***********************************************
          **********  *****   **********************
                          ***********************
```

---

## Color Palettes

Six distinct palettes, switchable live with `1`–`6`:

| Key | Name | Description |
|-----|------|-------------|
| `1` | **Cosmic** | Deep blues fading to bright cyan-white |
| `2` | **Fire** | Black → red → orange → yellow → white |
| `3` | **Matrix** | Pure green on black, like the movie |
| `4` | **Ocean** | Deep navy through teal to aqua |
| `5` | **Neon** | Electric purple → pink → white |
| `6` | **Gold** | Dark brown through gold to brilliant white |

---

## Installation & Running

**Requirements:** Python 3.10+ (stdlib only — no pip install needed)

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Run interactively (splash screen → full TUI)
python main.py

# Start directly in a specific mode
python main.py --fractal m          # Mandelbrot
python main.py --fractal j          # Julia set
python main.py --fractal f          # Barnsley Fern

# Choose a starting palette
python main.py --palette fire

# Auto-cycle demo (great for screensavers)
python main.py --demo

# Export a frame to a text file (no ANSI, portable)
python main.py --export out.txt --fractal m --width 120 --height 40

# Override terminal dimensions
python main.py --width 160 --height 50
```

---

## Controls

| Key | Action |
|-----|--------|
| `W A S D` / Arrow keys | Pan the view |
| `+` / `-` | Zoom in / out |
| `i` / `o` | Increase / decrease max iterations |
| `1` – `6` | Switch color palette |
| `p` | Cycle to next palette |
| `m` | Switch to Mandelbrot mode |
| `j` | Switch to Julia set mode |
| `f` | Switch to Fern / IFS mode |
| `n` | Next Julia seed (in Julia mode) / Next IFS type (in Fern mode) |
| `r` | Reset view to default |
| `S` | Save current frame as text file |
| `q` | Quit |

---

## Project Structure

```
clauder/
│
├── main.py                  # CLI entry point, TUI event loop, key handling
│
├── fractals/
│   ├── __init__.py          # Public API exports
│   ├── mandelbrot.py        # Mandelbrot escape-time algorithm (smooth coloring)
│   ├── julia.py             # Julia set algorithm + 8 seed constants
│   ├── barnsley.py          # Barnsley Fern + IFS engine (fern / tree / snowflake)
│   ├── colormap.py          # 6 ANSI 256-color palettes + colorize()
│   └── renderer.py          # Terminal rendering, status bar, splash screen
│
└── README.md
```

### Module Overview

```
main.py
  └── FractalState           controls cx, cy, zoom, palette, mode
  └── interactive_mode()     raw-tty event loop, resize handling
  └── demo_mode()            auto-cycle showcase
  └── export_mode()          headless frame export

fractals/mandelbrot.py
  └── mandelbrot_escape()    per-point escape + smooth-t value
  └── compute_mandelbrot()   full grid computation

fractals/julia.py
  └── JULIA_SEEDS            8 named complex constants
  └── julia_escape()         per-point escape
  └── compute_julia()        full grid computation

fractals/barnsley.py
  └── IFS_SYSTEMS            fern / tree / snowflake affine matrices
  └── barnsley_fern()        stochastic IFS iteration → boolean grid

fractals/colormap.py
  └── PALETTES               6 named palettes (256-color stops + chars)
  └── colorize()             t ∈ [0,1] → ANSI escape + ASCII character

fractals/renderer.py
  └── _normalize_grid()      per-frame √ gamma normalization
  └── render_fractal()       escape-time grid → terminal output
  └── render_fern()          boolean grid → colored terminal output
  └── render_splash()        intro / welcome screen
```

---

## How It Works

### Escape-Time Algorithm

For each pixel `(col, row)` we map to a complex number `c = x + yi` in the fractal's coordinate space. We then iterate:

```
z₀ = 0
zₙ₊₁ = zₙ² + c      (Mandelbrot)
zₙ₊₁ = zₙ² + seed   (Julia)
```

If `|z|` exceeds an escape radius (256), the point is considered **outside** the set. Points that never escape within `max_iter` iterations are **inside** (rendered as the background).

### Smooth Coloring

Raw iteration counts produce harsh color bands. We use the **smooth / continuous coloring** formula:

```python
log_zn = log(|z|²) / 2
nu      = log(log_zn / log(2)) / log(2)
smooth  = (i + 1 - nu) / max_iter
```

This produces a floating-point value `t ∈ [0, 1]` that varies smoothly across pixel boundaries — no banding.

### Per-Frame Normalization

Because most escaped values cluster near 0 (points far from the set escape in just 1–2 iterations), we apply per-frame √-gamma normalization before rendering:

```python
t_normalized = sqrt((t - t_min) / (t_max - t_min))
```

This stretches the dynamic range to fill the full color palette regardless of zoom level.

### IFS (Barnsley Fern)

The Barnsley Fern uses four affine transformations:

| Transform | Matrix | Effect |
|-----------|--------|--------|
| **F₁** | `[0, 0; 0, 0.16]` + `(0,0)` | Draws the stem |
| **F₂** | `[0.85, 0.04; -0.04, 0.85]` + `(0, 1.6)` | Shrinks the whole fern → large fronds |
| **F₃** | `[0.20, -0.26; 0.23, 0.22]` + `(0, 1.6)` | Left-turning frond |
| **F₄** | `[-0.15, 0.28; 0.26, 0.24]` + `(0, 0.44)` | Right-turning frond |

One transformation is chosen at random (weighted by probability) and applied to the current point. After 200,000 iterations, the resulting point cloud converges to a perfect fern.

---

## Why Fractals?

Fractals appear everywhere in nature: coastlines, snowflakes, ferns, blood vessels, lightning bolts, mountain ranges. The Mandelbrot set, discovered by Benoît Mandelbrot in 1980, was the first fractal visualized on a computer. Its boundary has infinite length and complexity, yet emerges from a two-line equation.

> *"Clouds are not spheres, mountains are not cones, coastlines are not circles, and bark is not smooth, nor does lightning travel in a straight line."*
> — Benoît Mandelbrot

Running this in your terminal is a reminder that sometimes the most profound things in mathematics live just a few keystrokes away.

---

## License

MIT — do whatever you like with it.
