# FractalForge

**Terminal fractal art engine** — render Mandelbrot sets, Julia sets, Sierpiński fractals, and Barnsley ferns directly in your terminal using colored Unicode characters and 8 hand-crafted palettes.

```
════════════════════════════════════════════════════════════
             ✦ FractalForge — Mandelbrot Set ✦
          preset=classic  size=120×40  iters=256
════════════════════════════════════════════════════════════
```

---

## Features

| Feature | Details |
|---|---|
| **Fractals** | Mandelbrot set, Julia sets, Sierpiński triangle, Sierpiński carpet, Barnsley fern |
| **Color palettes** | `fire` `ocean` `plasma` `matrix` `neon` `grayscale` `rainbow` `void` |
| **Character sets** | `block` (░▒▓█) `ascii` (.:=-+*#@) `dots` (·•●◉) `sparse` |
| **Presets** | 5 Mandelbrot zoom presets, 8 Julia parameter presets |
| **Smooth coloring** | Renormalized iteration counts for gradient-smooth boundaries |
| **Zero dependencies** | Pure Python 3.11 standard library only |
| **CLI + API** | Both `fractalforge` command and importable Python API |

---

## Architecture

```
fractalforge/
├── fractalforge/
│   ├── __init__.py        ← package exports
│   ├── mandelbrot.py      ← Mandelbrot set computation + zoom presets
│   ├── julia.py           ← Julia set computation + parameter presets
│   ├── sierpinski.py      ← Sierpiński triangle/carpet, Barnsley fern (IFS)
│   ├── renderer.py        ← ANSI terminal rendering engine
│   ├── palettes.py        ← Color palettes & character sets
│   └── cli.py             ← argparse CLI (fractalforge / ff commands)
├── tests/
│   ├── test_mandelbrot.py ← 6 unit tests
│   └── test_julia.py      ← 5 unit tests
├── examples/
│   └── showcase.py        ← Self-contained demo script
└── pyproject.toml
```

### How the math works

**Mandelbrot set** — For each pixel coordinate `(cx, cy)`, iterate `z → z² + c` starting from `z = 0`. Points that remain bounded after `max_iter` iterations are *in the set* (rendered black). Escaped points are colored by their smooth escape time using renormalization:

```
smooth_t = (iter + 1 - log(log(|z|)) / log(2)) / max_iter
```

This eliminates the banding that occurs with raw integer iteration counts, producing smooth gradient transitions across the boundary.

**Julia sets** — Identical iteration, but `c` is a fixed complex constant and `z` starts at each pixel. Different values of `c` produce radically different fractal shapes.

**Barnsley Fern** — Uses an Iterated Function System (IFS) chaos game: randomly apply one of 4 affine transformations with given probabilities for 50 000+ iterations. The attractor traces the shape of a fern leaf.

**Sierpiński triangle** — Recursive subdivision: draw a solid triangle, then subtract the central inverted triangle, repeat recursively to the requested depth.

---

## Installation

```bash
git clone <repo>
cd fractalforge
pip install -e .
```

No external dependencies — runs on any Python 3.11+ environment.

---

## Quick Start

```bash
# Mandelbrot set — fire palette (default)
fractalforge mandelbrot

# Seahorse valley zoom — ocean palette
fractalforge mandelbrot --preset seahorse --palette ocean

# Julia set — dragon preset, plasma palette
fractalforge julia --preset dragon --palette plasma

# Julia set with custom c parameter
fractalforge julia --cx -0.4 --cy 0.6 --palette neon --chars dots

# Sierpiński triangle
fractalforge sierpinski --variant triangle --palette matrix

# Barnsley fern
fractalforge sierpinski --variant fern

# Full showcase tour
fractalforge showcase
```

---

## CLI Reference

### Global options

```
fractalforge [command] [options]

  --palette / -p    fire ocean plasma matrix neon grayscale rainbow void
  --chars   / -c    block ascii dots sparse
  --width   / -W    terminal columns (auto-detected by default)
  --height  / -H    terminal rows   (auto-detected by default)
  --iterations / -i max iteration count
```

### `mandelbrot` (alias: `mb`)

```
fractalforge mandelbrot [--preset PRESET] [--x-min X] [--x-max X] [--y-min Y] [--y-max Y]
```

| Preset | Region | Highlight |
|---|---|---|
| `classic` | Full overview (-2.5 to 1.0) | The iconic cardioid + bulbs |
| `seahorse` | Valley near (-0.75, 0.10) | Seahorse spirals |
| `elephant` | Deep zoom at (0.255, 0.0) | Elephant valley |
| `spiral` | (-0.747, 0.100) | Dense spiral arms |
| `lightning` | (-1.786, 0.0) | Lightning bolt filaments |

### `julia` (alias: `jl`)

```
fractalforge julia [--preset PRESET] [--cx FLOAT] [--cy FLOAT]
```

| Preset | c value | Shape |
|---|---|---|
| `snowflake` | -0.7 + 0.27i | Snowflake (default) |
| `dragon` | -0.7269 + 0.1889i | Dragon curves |
| `galaxy` | -0.4 + 0.6i | Swirling galaxy |
| `dendrite` | 0.0 + 1.0i | Dendritic tree |
| `lightning` | 0.285 + 0.01i | Electric tendrils |
| `spiral` | -0.835 - 0.2321i | Tight spiral |
| `rabbit` | -0.123 + 0.745i | Douady rabbit |
| `douady` | -0.1 + 0.651i | Douady rabbit variant |

### `sierpinski` (alias: `sk`)

```
fractalforge sierpinski --variant [triangle|carpet|fern] [--depth N]
```

### `showcase` (alias: `demo`)

Renders a curated tour of 6 fractals using varied palettes. Great for a first look.

---

## Python API

```python
from fractalforge import mandelbrot, julia, sierpinski, renderer

# Compute a 120×40 Mandelbrot grid
grid = mandelbrot.compute(
    width=120, height=40,
    x_min=-2.5, x_max=1.0,
    y_min=-1.2, y_max=1.2,
    max_iter=256,
)

# Render to an ANSI string
art = renderer.render_smooth(grid, palette="fire", char_set="block")
print(art)

# Julia set with custom c
grid = julia.compute(120, 40, cx=-0.7269, cy=0.1889, max_iter=256)
print(renderer.render_smooth(grid, palette="plasma"))

# Sierpiński triangle (boolean grid)
grid = sierpinski.triangle(width=80, height=30, depth=5)
print(renderer.render_bool(grid, on_color="matrix"))

# Barnsley fern via IFS chaos game
grid = sierpinski.barnsley_fern(width=80, height=40, iterations=80000)
print(renderer.render_bool(grid, on_color="matrix", char_set="dots"))
```

---

## Palettes

```
fire      ████ dark red → red → orange → yellow → white
ocean     ████ black → navy → blue → cyan → pale
plasma    ████ black → purple → magenta → pink → yellow
matrix    ████ black → dark green → bright green → white-green
neon      ████ black → purple → magenta → red → orange → green → cyan
grayscale ████ black → dark gray → mid gray → light gray → white
rainbow   ████ red → orange → yellow → green → cyan → blue → violet
void      ████ black → deep purple → bright purple → magenta
```

---

## Character Sets

```
block    ░ ▒ ▓ █   (Unicode box-drawing — densest visual)
ascii    . : - = + * # @   (pure ASCII — works everywhere)
dots     · • ● ◉ ⬤   (circular density gradient)
sparse     · : │ ╬ █   (architectural feel)
```

---

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

```
collected 11 items

tests/test_julia.py::test_compute_returns_correct_dimensions PASSED
tests/test_julia.py::test_smooth_values_in_range PASSED
tests/test_julia.py::test_all_presets_compute PASSED
tests/test_julia.py::test_dendrite_has_in_set_points PASSED
tests/test_julia.py::test_different_c_values_differ PASSED
tests/test_mandelbrot.py::test_compute_returns_correct_dimensions PASSED
tests/test_mandelbrot.py::test_in_set_returns_zero PASSED
tests/test_mandelbrot.py::test_outside_set_returns_positive PASSED
tests/test_mandelbrot.py::test_smooth_values_in_range PASSED
tests/test_mandelbrot.py::test_presets_exist PASSED
tests/test_mandelbrot.py::test_all_presets_compute PASSED

11 passed in 0.37s
```

---

## Design Decisions

**Smooth coloring** — Raw iteration counts produce ugly color banding. The renormalization formula uses the magnitude of `z` at escape to interpolate fractional iteration counts, giving smooth gradients across the fractal boundary. This is the difference between blocky concentric rings and silky smooth color flows.

**Pure Python, no numpy** — The fractal computation loops are plain Python. This keeps installation friction at zero (no compiled extension required) while remaining fast enough for terminal-sized grids (120×40 renders in under a second on modern hardware).

**Terminal auto-sizing** — The CLI queries `os.get_terminal_size()` so fractals fill your window automatically without needing `--width`/`--height` flags.

**IFS chaos game for the fern** — Rather than recursively subdividing space (expensive), the Barnsley fern is generated by the chaos game: randomly applying one of 4 affine transformations and plotting where each point lands. After ~50 000 iterations, the attractor emerges as a perfect fern shape.

---

## License

MIT
