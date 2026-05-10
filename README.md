# FractalScape

```
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗      ███████╗ ██████╗ █████╗ ██████╗ ███████╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║      ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║      ███████╗██║     ███████║██████╔╝█████╗
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║      ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗ ███████║╚██████╗██║  ██║██║     ███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝
```

> **Explore the Infinite in Your Terminal** — render Mandelbrot sets, Julia sets, and
> Burning Ship fractals with 256-color ANSI output, named zoom locations, 8 palettes,
> and multiple character sets. Zero dependencies beyond numpy, click, and rich.

---

## What It Looks Like

```
                              Mandelbrot Set — full view
....
                                               ....``....
                                             ......`'^`....
                                          .......`)   :;`.....
                                      .........```,    '``.......
                                . ........'~ ^z           (,`l^;`..
                           .............`^^n                  -`...
                       ....``...``.....`^!                     '''..
                    .......``"l^^ ^{l``^                        `...
                  ......```'?         ^                         '...
            ....`.....``'; ?                                   `....
            ....`.....``'; ?                                   `....
                  ......```'?         ^                         '...
                    .......``"l^^ ^{l``^                        `...
                       ....``...``.....`^!                     '''..
                           .............`^^n                  -`...
                                . ........'~ ^z           (,`l^;`..
                                      .........```,    '``.......
                                          .......`)   :;`.....
                                             ......`'^`....
                                               ....``....
```

```
                           Julia Set — spiral (c = -0.7 + 0.27015j)
@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@                                  @@@@@@@@@@
@@@@@@@@                                              @@@@
@@@@                                                     @
@
                           .. c ..
                       ..,  L[  ^'uU .......(`
              . `........``'8 | /Q /a1 _X''ku L<...
           ..f Iq|{o -v/) ! q i1kf      X<Z {q z `U.
      .U` z q{ Z<X      fk1i q ! )/v- o{|qI f..
       ...<L uk''X_ 1a/ Q/ | 8'``........` .
            `(....... Uu'^  [L  ,..
                        .. c ..
                                                         @
@                                                     @@@@
@@@@                                              @@@@@@@@
@@@@@@@@@@                                  @@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@
```

```
                              Mandelbrot — Seahorse Valley zoom
;o    B
;;;b _  1
;_qw p}
::;I~ L j 0
::;(l!i>  t
::;;ptt L
,:::;}<<><
,:/&t f?-mY
,,::; ]p](0
,,,,:;[>>iiJ
,,:?>0n+h~ a  J
,,:[;B jn1
",,,,IL-h >Mq(_-
",,,,,:;c~il!! [{
",,1ic1ruOX _{
"",<f:~Uuh}}
```

> In a real terminal these render in full 24-bit color — fire reds fading to gold,
> icy blues, electric purples. The ASCII above is a monochrome preview.

---

## Features

| Feature | Details |
|---|---|
| **3 Fractals** | Mandelbrot, Julia (any `c`), Burning Ship |
| **8 Palettes** | `fire` `ice` `electric` `forest` `ocean` `classic` `sunset` `monochrome` |
| **4 Char sets** | `dense` `simple` `blocks` `dots` |
| **8 Julia presets** | `dendrite` `spiral` `galaxy` `lightning` `siegel_disk` … |
| **6 Zoom locations** | `full` `seahorse` `elephant` `triple_spiral` `mini_mandelbrot` `lightning_bolt` |
| **Smooth coloring** | Fractional escape counts eliminate color banding |
| **Tour mode** | Auto-cycles through every location or Julia preset |
| **Save output** | Dump plain ASCII to any file with `--save` |
| **Rich stats panel** | Interior %, mean iteration, render time |

---

## Project Structure

```
Clauder/
├── fractalscape/               ← Python package
│   ├── __init__.py
│   ├── compute.py              ← Pure-math escape-time engines
│   │   ├── mandelbrot()        ← vectorised numpy Mandelbrot
│   │   ├── julia()             ← Julia set with any c ∈ ℂ
│   │   └── burning_ship()      ← |Re(z)| + i|Im(z)| variant
│   ├── palette.py              ← Color interpolation & ANSI rendering
│   │   ├── PALETTES{}          ← 8 RGB gradient definitions
│   │   ├── iterations_to_ansi()← 24-bit ANSI color string builder
│   │   └── iterations_to_plain_ascii()
│   ├── renderer.py             ← Orchestration layer
│   │   ├── RenderConfig        ← Dataclass: all render parameters
│   │   ├── RenderResult        ← Dataclass: output + stats
│   │   └── render()            ← Main entry point
│   └── cli.py                  ← Click CLI with three commands
│       ├── fractalscape render  ← One-shot render
│       ├── fractalscape tour    ← Animated tour
│       └── fractalscape list    ← Show all options
├── main.py                     ← python main.py entry point
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt

# Run immediately
python main.py --help
```

---

## Usage

### Render a fractal

```bash
# Default: Mandelbrot, fire palette, 120x40
python main.py render

# Julia set — spiral preset
python main.py render --fractal julia --julia-preset spiral --palette electric

# Mandelbrot zoomed into the seahorse valley
python main.py render --fractal mandelbrot --zoom seahorse --palette ice --width 160 --height 50

# Burning Ship with block characters
python main.py render --fractal burning_ship --palette sunset --chars blocks

# Custom Julia parameter
python main.py render --fractal julia --julia-c "-0.8+0.156j" --palette ocean

# Save to file
python main.py render --fractal mandelbrot --save mandelbrot.txt
```

### Tour mode — auto-cycle all locations

```bash
# Mandelbrot tour (all 6 zoom locations, fire palette)
python main.py tour --fractal mandelbrot --palette fire

# Julia tour (all 8 presets, electric palette)
python main.py tour --fractal julia --palette electric --width 100 --height 32
```

### List everything available

```bash
python main.py list
```

---

## How It Works

### The Escape-Time Algorithm

Every point `c` in the complex plane is tested: starting at `z = 0`, repeatedly
compute `z <- z^2 + c`. If `|z|` exceeds 2 before `max_iter` iterations, the point
**escapes** and is colored by *how quickly* it escaped. If it never escapes, it
belongs to the set and is drawn black.

```
for i in range(max_iter):
    z = z^2 + c
    if |z| > 2:
        color = smooth_escape_count(i, z)   <- fractional for smooth gradients
        break
```

### Vectorisation with NumPy

The entire `width x height` grid is computed as a single NumPy operation — no
Python loops over pixels. A boolean mask tracks which points haven't escaped yet,
so escaped points stop being updated:

```python
Z[mask] = Z[mask] ** 2 + C[mask]   # update only active points
escaped = mask & (np.abs(Z) > 2.0)
iterations[escaped] = i + 1 - log2(log2(|Z[escaped]|))  # smooth coloring
mask[escaped] = False
```

### Smooth Coloring

Naive integer iteration counts produce harsh color bands. The fractional escape
count formula `i + 1 - log2(log2(|z|))` maps escaping points to a continuous
real value, resulting in smooth gradient transitions even at low iteration counts.

### ANSI 24-bit Color

Each character cell emits `\033[38;2;R;G;Bm` — the 24-bit "true color" ANSI
escape that modern terminals support. Colors are produced by linearly interpolating
between the palette's RGB stops and indexing by the smooth escape count.

---

## Fractal Gallery

### Burning Ship

The **Burning Ship** fractal replaces `z^2 + c` with `(|Re(z)| + i|Im(z)|)^2 + c` —
taking absolute values before squaring. This breaks the symmetry and produces
the jagged, ship-like silhouette:

```
                                                           
                                  -
                              .  *.-
               .           +*     %.
               . -.== +
            ...%--
          - .
          .#
      %*-.
```

### Julia Set — Dendrite (c = 0 + 1.0j)

```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%          %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%                                 %%%%%%%%%%%
%%%%%%%%%                                             %%%%%%
%%%%%                                                     %%
%%
                              % *
                           -. -.  # :% +    =.=
               ::             -+#   == *:+ :  - -.
                . :+-  #-.:=+  . #:    *  # + .+ .*
         *. +. + #  *    :# .  +=:.-#  -+: .
          .- -  : +:* ==   #+-             ::
             =.=    + %: #  .- .-
                           * %

%%                                                     %%%%%
%%%%%%                                             %%%%%%%%%
%%%%%%%%%%%                                 %%%%%%%%%%%%%%%%
```

---

## Color Palettes

| Palette | Gradient |
|---|---|
| `fire` | Black → dark red → orange → yellow → white |
| `ice` | Black → navy → cyan → pale blue → white |
| `electric` | Black → deep purple → magenta → white |
| `forest` | Black → dark green → lime → white |
| `ocean` | Black → deep blue → teal → white |
| `classic` | Black → red → teal → sky blue → white |
| `sunset` | Midnight blue → crimson → orange → gold |
| `monochrome` | Black → dark grey → light grey → white |

---

## CLI Reference

```
Usage: python main.py [OPTIONS] COMMAND [ARGS]...

Commands:
  render   Render a fractal to the terminal
  tour     Auto-tour all zoom locations or Julia presets
  list     List palettes, presets, and zoom locations

render options:
  -f, --fractal [mandelbrot|julia|burning_ship]
  -W, --width INTEGER          Output width in characters
  -H, --height INTEGER         Output height in characters
  -m, --max-iter INTEGER       Maximum iterations (more = finer detail)
  -p, --palette PALETTE        Color palette name
  -c, --chars [dense|simple|blocks|dots]
  --invert                     Invert color mapping
  --julia-c TEXT               Julia c as 'real+imagj'
  --julia-preset PRESET        Named Julia preset
  --zoom LOCATION              Named Mandelbrot zoom (mandelbrot only)
  --x-min / --x-max FLOAT      Custom viewport bounds
  --y-min / --y-max FLOAT      Custom viewport bounds
  --save FILE                  Save plain ASCII output to file
  --stats / --no-stats         Show render statistics panel
```

---

## Requirements

- Python 3.9+
- `numpy >= 1.24` — vectorised fractal computation
- `click >= 8.1` — CLI parsing
- `rich >= 13.0` — stats panels and tour output

---

## Acknowledgements

- **Benoit Mandelbrot** (1924-2010) — for discovering that infinity hides inside simple equations
- **Gaston Julia** (1893-1978) — for the family of sets bearing his name
- The **smooth coloring** technique is attributed to Linas Vepstas (2004)

---

*Made with curiosity and numpy.*
