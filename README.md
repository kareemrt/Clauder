# Fractopia — Terminal Fractal Explorer

```
  ___               _              _
 | __| _ __ _  __  | |_  ___  _ __(_) __ _
 | _| | '_/ _|/ _| |  _|/ _ \| '_ \ |/ _` |
 |_|  |_| \__\__|   \__|\___/| .__/_|\__,_|
                              |_|

  Terminal Fractal Explorer  •  pure Python  •  zero dependencies
```

> **Render breathtaking mathematical fractals — directly in your terminal.**  
> Five fractal types. Infinite zoom. Six Julia presets. Full 256-color gradients.  
> No pip installs. No setup. Just Python ≥ 3.8 and a modern terminal.

---

## Table of Contents

1. [Features](#features)
2. [Quick Start](#quick-start)
3. [Fractal Gallery](#fractal-gallery)
   - [Mandelbrot Set](#mandelbrot-set)
   - [Julia Sets](#julia-sets)
   - [Sierpiński Triangle](#sierpiński-triangle)
   - [Dragon Curve](#dragon-curve)
   - [Burning Ship](#burning-ship)
4. [Usage & Options](#usage--options)
5. [The Math Behind the Magic](#the-math-behind-the-magic)
6. [Project Structure](#project-structure)
7. [Extending Fractopia](#extending-fractopia)

---

## Features

| Feature | Detail |
|---|---|
| **5 fractal types** | Mandelbrot, Julia, Sierpiński, Dragon Curve, Burning Ship |
| **6 Julia presets** | Classic spiral, Douady rabbit, Dendrite, Sea Horse Valley, Feather, Fat rabbit |
| **256-color gradients** | Smooth ANSI 256-color palette, gracefully degrades to no-color |
| **Infinite zoom** | `--zoom` + `--x-center` / `--y-center` for precise viewport control |
| **Gallery mode** | Render all fractals back-to-back with one command |
| **Zero dependencies** | Pure Python standard library — no pip, no venv, no fuss |
| **Scriptable** | Clean CLI with every parameter exposed; pipe output to files |

---

## Quick Start

```bash
# Clone and run — that's it
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Full gallery (all fractals)
python fractopia.py

# Single fractal
python fractopia.py mandelbrot

# No color (great for piping to files)
python fractopia.py mandelbrot --no-color > mandelbrot.txt
```

---

## Fractal Gallery

### Mandelbrot Set

The most famous fractal in mathematics. Each pixel represents a complex number `c`;
the color encodes how quickly the sequence `z → z² + c` escapes to infinity.

```
════════════════════════════════════════════════════════════════════════
                             Mandelbrot Set
════════════════════════════════════════════════════════════════════════

                                               .,..
                                               ....
                                             .··█:.·
                                             .·████.
                                        ·.....,███=...    .
                                      .█·:.:,███████▓o,...,.
                                      .,███████████████,██,.
                                     ..+█████████████████,.
                         .         ...████████████████████...
                         .....,......██████████████████████O.
                         ..·█:█:=·..+██████████████████████.
                        .,,███████+,███████████████████████.
                      ...,█████████#██████████████████████;.
               . .....,=██████████████████████████████████.
               . .....,=██████████████████████████████████.
                      ...,█████████#██████████████████████;.
                        .,,███████+,███████████████████████.
                         ..·█:█:=·..+██████████████████████.
                         .....,......██████████████████████O.
                         .         ...████████████████████...
                                     ..+█████████████████,.
                                      .,███████████████,██,.
                                      .█·:.:,███████▓o,...,.
                                        ·.....,███=...    .
```

```bash
# Zoom into the seahorse valley
python fractopia.py mandelbrot --zoom 50 --x-center -0.745 --y-center 0.125
```

---

### Julia Sets

Julia sets are the "cousins" of the Mandelbrot set — same iteration, but `z` is the
variable and `c` is a fixed parameter. Tiny changes to `c` produce wildly different shapes.

```
════════════════════════════════════════════════════════════════════════
                   Julia Set  c = -0.40000 +0.60000i
════════════════════════════════════════════════════════════════════════

                                     ,+
                                    *=+=,█+
                                  .,:O▒;:O..   ;··.      .·$.
                                   ,▓,+··$░o·O:█·=....OO.▓·;█.
                                 ...;o:=+@██░█=█#;::▓,#:=o$▒@+█.*.+
                               .+█+·#=+*=██▓███O█@o:···++O=o=;+,:+:█
                     O.       ...o,,·█+==#▓@▓▒██o@=:+*.+█=,:,.
                    .$█*O....,.,..#*;;:oo==o*█=█$:O·o*·.  ..o
                   .░:oo·,,,*=::,,;····+=o:O+;:*·█o..
                   ..o█·*:;+O:o=+····;,,::=*,,,·oo:░.
           o..  .·*o·O:$█=█*o==oo:;;*#..,.,....O*█$.
          .,:,=█+.*+:=@o██▒▓@▓#==+█·,,o...       .O
    █:+:,+;=o=O++···:o@█O███▓██=*+=#·+█+.
     +.*.█+@▒$o=:#,▓::;#█=█░██@+=:o;...
```

**Available presets** (`--preset 0` through `--preset 5`):

| # | c value | Name |
|---|---------|------|
| 0 | −0.7 + 0.27015i | Classic spiral |
| 1 | −0.4 + 0.6i | Douady rabbit |
| 2 | 0.285 + 0.01i | Dendrite |
| 3 | −0.70176 − 0.3842i | Sea horse valley |
| 4 | 0.45 + 0.1428i | Feather |
| 5 | −0.835 − 0.2321i | Fat rabbit |

```bash
python fractopia.py julia --preset 1          # Douady rabbit
python fractopia.py julia --c-real 0.285 --c-imag 0.01   # Dendrite (manual)
```

---

### Sierpiński Triangle

A self-similar fractal built by recursively removing the central triangle from each
sub-triangle. At order N, the triangle has `3^N` filled cells.

```
════════════════════════════════════════════════════════════════
                    Sierpinski Triangle (order 4)
════════════════════════════════════════════════════════════════

               ▲
              ▲ ▲
             ▲   ▲
            ▲ ▲ ▲ ▲
           ▲       ▲
          ▲ ▲     ▲ ▲
         ▲   ▲   ▲   ▲
        ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
       ▲               ▲
      ▲ ▲             ▲ ▲
     ▲   ▲           ▲   ▲
    ▲ ▲ ▲ ▲         ▲ ▲ ▲ ▲
   ▲       ▲       ▲       ▲
  ▲ ▲     ▲ ▲     ▲ ▲     ▲ ▲
 ▲   ▲   ▲   ▲   ▲   ▲   ▲   ▲
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
```

```bash
python fractopia.py sierpinski --order 6   # Bigger triangle
```

---

### Dragon Curve

Fold a strip of paper in half repeatedly, always in the same direction, then unfold
it so every fold is 90°. The resulting path is the Dragon Curve — and it never
self-intersects, no matter how many folds.

```
════════════════════════════════════════════════════════════════════════════════
                         Dragon Curve  (10 iterations)
════════════════════════════════════════════════════════════════════════════════

          ████    ████
         █████   █████
         ███████ ███████
           █████   █████
      █████████████████
     █████████████████
     ██████ ███ ████████
       ████  ██ ████████
      ███       ███████   ████
     ████       ██████   █████
     ████  █    ███ ████ ███████
       █████     ██ ████   █████
       ████         ███████████
                  ████████████
                  ██████████████
                ████████████████
```

```bash
python fractopia.py dragon --iterations 15   # More folds → more detail
```

---

### Burning Ship

A variant of the Mandelbrot set where `z → (|Re(z)| + i|Im(z)|)² + c`.
The absolute-value trick introduces sharp angular features, giving the fractal
a distinctive "burning ship" silhouette.

```bash
python fractopia.py burning --width 120 --height 50
```

---

## Usage & Options

```
usage: fractopia [-h] [--width W] [--height H] [--max-iter N]
                 [--order N] [--iterations N]
                 [--c-real F] [--c-imag F]
                 [--zoom F] [--x-center F] [--y-center F]
                 [--preset {0..5}] [--no-color]
                 [{mandelbrot,julia,sierpinski,dragon,burning,gallery}]
```

| Option | Default | Description |
|--------|---------|-------------|
| `fractal` | `gallery` | Which fractal to render |
| `--width` | 80 | Output width in characters |
| `--height` | 40 | Output height in characters |
| `--max-iter` | 128 | Iteration depth (higher = more detail, slower) |
| `--order` | 5 | Sierpiński recursion order (1–7) |
| `--iterations` | 13 | Dragon curve fold count |
| `--c-real` | −0.7 | Julia set `c` real part |
| `--c-imag` | 0.27015 | Julia set `c` imaginary part |
| `--zoom` | 1.0 | Viewport zoom factor |
| `--x-center` | −0.75 | Mandelbrot viewport X center |
| `--y-center` | 0.0 | Mandelbrot viewport Y center |
| `--preset` | — | Julia preset 0–5 (overrides `--c-real`/`--c-imag`) |
| `--no-color` | off | Disable ANSI colors |

### Recipes

```bash
# Thumbnail suitable for a narrow terminal
python fractopia.py mandelbrot --width 60 --height 25

# High-detail Mandelbrot (slow but beautiful)
python fractopia.py mandelbrot --max-iter 512 --width 120 --height 50

# Deep zoom into a spiral arm
python fractopia.py mandelbrot --zoom 200 --x-center -0.7435 --y-center 0.1315

# Save plain-text art to a file
python fractopia.py sierpinski --order 6 --no-color > sierpinski.txt

# Pipe into less for scrolling
python fractopia.py gallery --height 30 --no-color | less -R
```

---

## The Math Behind the Magic

### Escape-Time Algorithm

All escape-time fractals (Mandelbrot, Julia, Burning Ship) share the same core loop:

```
for each pixel (x, y):
    map (x, y) → complex number z₀ (or c for Mandelbrot)
    iterate:  zₙ₊₁ = f(zₙ)
    count iterations until |zₙ| > 2  (escape radius)
    color the pixel by escape count
```

The "escape radius" of 2 works because once `|z| > 2`, the sequence always diverges.

| Fractal | f(z) | Parameter |
|---------|------|-----------|
| Mandelbrot | z² + c | c = pixel position |
| Julia | z² + c | c = fixed constant |
| Burning Ship | (|Re z| + i|Im z|)² + c | c = pixel position |

### Sierpiński — Chaos Game

The triangle is built by pure recursion: split each triangle into four equal
sub-triangles and discard the middle one, forever.

```
order 0:    ▲
order 1:   ▲ ▲    (middle removed)
             ▲
order 2:  ▲ ▲ ▲  (each sub-triangle repeated)
```

### Dragon Curve — Paper Folding

The fold sequence `[1, 1, 0, 1, 1, 0, 0, …]` is generated by the rule:

```
new_sequence = old_sequence + [1] + reverse(complement(old_sequence))
```

Each `1` means "turn right" and `0` means "turn left", tracing out the curve
on a grid.

---

## Project Structure

```
clauder/
├── fractopia.py     # Everything — ~350 lines, zero dependencies
└── README.md        # This file
```

`fractopia.py` is organized into four layers:

```
fractopia.py
│
├── Math kernels          _mandelbrot(), _julia()
│   Pure complex-number iteration functions.
│
├── Renderers             render_mandelbrot(), render_julia(),
│   Map pixels → chars    render_sierpinski(), render_dragon(),
│   + ANSI color codes.   render_burning_ship()
│
├── UI helpers            _header(), print_banner(), gallery()
│   Terminal formatting.
│
└── CLI                   build_parser(), main()
    argparse front-end.
```

---

## Extending Fractopia

Adding a new fractal takes ~15 lines:

```python
def render_myfractal(width=80, height=40, color=True) -> str:
    rows = []
    for row in range(height):
        cols = []
        for col in range(width):
            # 1. map (col, row) → complex plane
            # 2. iterate your formula
            # 3. pick a char from GRADIENT
            # 4. optionally wrap in COLORS[…] + RESET
            cols.append(char)
        rows.append(''.join(cols))
    return '\n'.join(rows)
```

Then add it to `dispatch` and `title_map` in `main()`.

---

*Built with pure Python. No dependencies. Just math and imagination.*
