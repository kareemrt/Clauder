# FractalForge

> **Render breathtaking fractal art directly in your terminal — no GPU, no GUI, no dependencies.**

```
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Dependencies](https://img.shields.io/badge/Dependencies-zero-brightgreen?style=flat-square)
![Terminal](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square)

---

## What Is It?

FractalForge renders mathematically precise fractal art inside any modern terminal.
It uses **Unicode half-block characters** (`▀`) with **24-bit ANSI true-color** to
produce near-square pixels at twice the vertical resolution of the character grid —
turning your shell into an art gallery.

Four fractal families, seven color themes, nine ready-to-use presets, and an ASCII
fallback mode for environments without color support.

---

## Feature Highlights

| Capability | Details |
|---|---|
| **4 fractal types** | Mandelbrot, Julia sets, Burning Ship, Newton z³−1 |
| **7 color themes** | fire, ocean, neon, plasma, matrix, ice, mono |
| **9 presets** | Curated deep-zoom coordinates with one flag |
| **Smooth coloring** | Log-log escape time normalization eliminates harsh banding |
| **2× vertical resolution** | Half-block rendering doubles pixel density |
| **ASCII fallback** | `--ascii` mode works on any terminal, SSH, tmux |
| **Save to file** | `--save output.txt` writes a plain-text copy |
| **Zero dependencies** | Pure Python standard library (+ optional `colorama` on Windows) |
| **Fully customizable** | Zoom, pan, custom Julia constants, iteration depth |

---

## Gallery

### Mandelbrot Set — full view (`--preset mandelbrot`)
```
                           ...................`--'`...........
                        ....................``-',-`............
                     .....................```~    \'.............
                  ...................```````-n    ;```............
               .....................`~=^--         C; -`-`_`.......
           ........................``-~                o  -`........
         .......................```,=;                   ,-`........
       ..............`_````;``````,\                      j;:........
       ..............``->+_' '!_--'                        <`........
      .............```':        I_                         -`.........
      ..........```-__'                                   ,`..........
                                                        ,-``..........
      ..........```-__'                                   ,`..........
      .............```':        I_                         -`.........
       ..............``->+_' '!_--'                        <`........
       ..............`_````;``````,\                      j;:........
         .......................```,=;                   ,-`........
           ........................``-~                o  -`........
               .....................`~=^--         C; -`-`_`.......
                  ...................```````-n    ;```............
                     .....................```~    \'.............
                        ....................``-',-`............
```
*In a color terminal, the interior is solid black and the escape bands cycle
through the active theme's full gradient.*

---

### Julia Set — classic symmetric (`--preset julia`)
```
                                    ............
                                 ......-uq`..........
                              ........`-rn -................
                          ........```,Bc   Y```-`L`..............
                     .............`vv[ c}#Z,_-_\  -`.........-;.....
                  ...............` ='   ~<{  ,  d ~ d````-  B r`......
               .................```---'bj   <tr/  &l >_-`--: w:,j`......
             ......`q) ``-uo``_````--- v= tl f[Y C jr\a? &:fu/uJ**--MQ...
           ......`( [cLo_^\X = '!v_^B/:: o    j W    Z I J >Y W  LluO   ..
         ........`]',<}Cjvt \  ra~mX   J|+8ptr      htCcI~O O~mj  C'``-...
       ...._[-u```-_q>Ll [U akju{|L1OY){)YO1L|{ujka U[ lL>q_-```u-[_....
     ...-``'C  jm~O O~IcCth      rtp8+|J   Xm~ar  \ tvjC}<,']`........
     ..   OulL  W Y> J I Z    W j    o ::/B^_v!' = X\^_oLc[ (`......
      ...QM--**Ju/uf:& ?a\rj C Y[f lt =v ---````_``ou-`` )q`......
       ......`j,:w :--`-_> l&  /rt<   jb'---```.................
         ......`r B  -````d ~ d  ,  {<~   '= `...............
           .....;-.........`-  \_-_,Z#}c [vv`.............
              ..............`L`-```Y   cB,```........
                   ................- nr-`........
                          ..........`qu-......
                               ............
```

---

### Julia Set — dragon-wing (`--preset julia-dragon`)
```
                          ..........``_:, `................
                    ............:_`irz:Q:--;;-` `..............
                ...............`-,:> =,::} k c:_-`.........`).....
             .................`_: \c1 !x h|  !\fYq-`````X:|,^`.......
           ......`'m```'```````^|f mC z{C==! l,,<=c ``-  fu+/C -.......
        .......-- ,'\M\I b>-```-McQW crO c,b:''::,;r(-_\hU /!:,^'`C(`...
      ........`>qo}J|I8?,;<  _--_MQ / p> |:''''<<+}= '':~?/^''0>&'=^~':..
     ...`j~\?Y--XjajX,:'::;;^%___':^ !#! ^:'___%^;;::':,XjajX--Y?\~j`...
    ..:'~^='&>0''^/?~:'' =}+<<'''':| >p / QM_--_  <;,?8I|J}oq>`........
     ...`(C`'^,:!/ Uh\_-(r;,::'':b,c Orc WQcM-```->b I\M\', --.......
      .......- C/+uf  -`` c=<,,l !==C{z Cm f|^```````'```m'`......
        .......`^,|:X`````-qYf\!  |h x! 1c\ :_`.................
           .....)`.........`-_:c k }::,= >:,-`...............
              ..............` `-;;--:Q:zri`_:............
```

---

### Newton Fractal z³−1 (`--preset newton`)
```
$$$$$$$$$$$$$$$$$####################$$$$$$$$$$%&$$$$$%%$&&%$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$####################$$$$$$$$$%%%$$$$$&%%%$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$##################$$$$$$$$$%%%&%%%%%%%$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$################$$$$$$$%&%%&&8B&%%$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$#############$$$$$$$&%$$%8%&&%%$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$#####$$$$$$$$$$%%%%$$$%%$%8$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%$$$#$$$$%%$$$$$$$$$$$$##$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$8%$$$$$$$&8%$$$$$$$$############$$$$$$$
%%%%%$$$%%%%%$$$$$$$$$$$$$$$$$$$$$$$$$%&%$$$$$%M&%$$$$$$$################$$$$$
&%8%%%%%B%$$%8%%%%%$$%%&$$%&$%%%8%%%%%%&%%%%%%&%$$$$$$$####################$$$
%%%%m&&&%%%8%$$$%%&%%%%%%&$$$$$$$%%&&&&B&&&&%%$$$$$$$$#####################$$$
$$%%%&8*8%%$$$$$$$%%&B8%%$$$#$$$$$%%%&8 8&%%%$$$$$$$$$#####################$$$
%%%%m&&&%%%8%$$$%%&%%%%%%&$$$$$$$%%&&&&B&&&&%%$$$$$$$$#####################$$$
&%8%%%%%B%$$%8%%%%%$$%%&$$%&$%%%8%%%%%%&%%%%%%&%$$$$$$$####################$$$
%%%%%$$$%%%%%$$$$$$$$$$$$$$$$$$$$$$$$$%&%$$$$$%M&%$$$$$$$################$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$8%$$$$$$$&8%$$$$$$$$############$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%$$$#$$$$%%$$$$$$$$$$$$##$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$#####$$$$$$$$$$%%%%$$$%%$%8$$$$$$$$$$$$$$$$$$$$$$$$$$
```
*Three root basins of attraction glow red, green, and blue in color mode.*

---

### Burning Ship (`--preset burning-ship`)
```
                                            ..................................
                                     .........................................
                               ...............................................
                          ....................................................
                        ......................................................
                       .......................................................
                      ........................................................
                     .........................................................
                     .................................................````````
                    .....................................`..````````````------
                    ........`...```````--````````-``````````_------:___'',^
                    .....```````````_   I?---~--,:-_-_---_/
                    .............````;_!'^``````ll-`````--_
                    .................``,'`````````````````<
                    .....................`..``....````````J
                    ................................```````-o
                     ..................................`````-U
                     ..................................`````C~x &-
```
*The "ship" silhouette appears in the lower-center of the full color render.*

---

## Quick Start

```bash
# Clone and run — no pip install required
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Default render: Mandelbrot, fire theme, auto terminal size
python main.py

# Use a preset
python main.py --preset seahorse

# Julia set with ocean theme
python main.py --fractal julia --theme ocean

# Newton fractal with neon theme
python main.py --fractal newton --theme neon

# ASCII mode (no color — works over any SSH session)
python main.py --ascii

# Deep custom zoom
python main.py --cx -0.7436 --cy 0.1318 --zoom 400 --theme plasma

# Save a plain-text copy
python main.py --preset julia --save my_render.txt
```

---

## Installation

FractalForge has **no required dependencies** beyond the Python standard library.

```bash
# Python 3.8+ required
python --version

# Optional: colorama for Windows ANSI support
pip install colorama
```

---

## All Options

```
usage: fractalforge [-h] [--version] [--list]
                    [--fractal {mandelbrot,julia,burning_ship,newton}]
                    [--preset PRESET] [--cx X] [--cy Y] [--zoom ZOOM]
                    [--max-iter N] [--julia-cr R] [--julia-ci I]
                    [--theme THEME] [--width W] [--height H]
                    [--ascii] [--no-progress] [--save FILE]
```

### Fractal options

| Flag | Default | Description |
|---|---|---|
| `--fractal` | `mandelbrot` | Fractal type |
| `--preset` | — | Named preset (overrides fractal/cx/cy/zoom) |
| `--cx` | preset / `-0.5` | Center real coordinate |
| `--cy` | preset / `0.0` | Center imaginary coordinate |
| `--zoom` | preset / `1.0` | Magnification (higher = more zoomed in) |
| `--max-iter` | `256` | Iteration depth (higher = more detail, slower) |
| `--julia-cr` | `-0.7` | Julia set `c` real part |
| `--julia-ci` | `0.27015` | Julia set `c` imaginary part |

### Display options

| Flag | Default | Description |
|---|---|---|
| `--theme` | `fire` | Color palette |
| `--width` | terminal width | Output columns |
| `--height` | terminal height | Output rows |
| `--ascii` | off | ASCII density mode (no ANSI color) |
| `--no-progress` | off | Suppress the progress indicator |

### Output options

| Flag | Description |
|---|---|
| `--save FILE` | Save a plain-text (no ANSI) copy to `FILE` |
| `--list` | Print all presets and themes, then exit |

---

## Presets

```
python main.py --list
```

| Preset | Fractal | Description |
|---|---|---|
| `mandelbrot` | Mandelbrot | Classic full view |
| `seahorse` | Mandelbrot | Seahorse Valley — deep spiral arms |
| `elephant` | Mandelbrot | Elephant Valley — bulging lobes |
| `triple-spiral` | Mandelbrot | Triple-spiral at zoom 200 |
| `julia` | Julia | Classic symmetric Julia set |
| `julia-dragon` | Julia | Dragon-wing Julia set |
| `julia-dendrite` | Julia | Dendrite (fractal tree) |
| `burning-ship` | Burning Ship | The iconic ship hull |
| `newton` | Newton | z³−1 root basin portrait |

---

## Color Themes

```
--theme fire     Inferno gradient: deep violet → flame orange → white
--theme ocean    Abyss dive: midnight black → cobalt → seafoam white
--theme neon     Synthwave: deep purple → hot pink → acid yellow → cyan
--theme plasma   Matplotlib Plasma: indigo → magenta → saffron → yellow
--theme matrix   Green phosphor on black — classic terminal aesthetic
--theme ice      Arctic palette: navy → steel blue → frosty white
--theme mono     Pure grayscale
```

All themes are defined as **gradient stop tables** — a list of `(position, RGB)`
pairs that are linearly interpolated, then cyclically applied to the smooth
escape-time value. The result is banded color without harsh jumps.

---

## Fractal Types

### Mandelbrot Set
The canonical fractal. For each point `c` in the complex plane, iterate
`z → z² + c` starting from `z = 0`. Points that stay bounded form the set;
the escape speed of other points determines their color.

```
center: (-0.5, 0)    x ∈ [-2.5, 1.0]    y ∈ [-1.25, 1.25]
```

### Julia Sets
Uses the same iteration `z → z² + c` but fixes `c` and varies the starting
point `z`. Different values of `c` produce wildly different shapes — from
symmetric dragons to delicate dendrite trees. Controlled via `--julia-cr`
and `--julia-ci`.

```
Classic:   c = -0.7 + 0.27015i   (symmetric swirls)
Dragon:    c = -0.8 + 0.156i     (wing shapes)
Dendrite:  c = 0 + 1i            (branching tree)
```

### Burning Ship
Modifies the Mandelbrot iteration by taking the absolute value of each
component before squaring: `z → (|Re(z)| + i|Im(z)|)² + c`. The result
resembles a flaming ship seen from below.

### Newton Fractal
Applies Newton's root-finding method to `f(z) = z³ − 1`. Each pixel is
colored by *which root* it converges to (red / green / blue) and *how fast*
(brightness). The boundary between basins of attraction is infinitely complex.

---

## Architecture

```
clauder/
├── main.py                    Entry point
├── requirements.txt           Optional dependencies
├── README.md
└── fractalforge/
    ├── __init__.py            Package metadata
    ├── fractals.py            Core math
    │   ├── mandelbrot()       Smooth escape time, log-log normalization
    │   ├── julia()            Parametric Julia sets
    │   ├── burning_ship()     Absolute-value variant
    │   └── newton()           Root-finding convergence + basin index
    ├── themes.py              Color system
    │   ├── THEMES             Gradient stop tables (7 palettes)
    │   ├── get_color()        Interpolate palette at t ∈ [0,1]
    │   └── ANSI helpers       fg(), bg(), RESET, HIDE_CURSOR …
    ├── renderer.py            Rendering engine
    │   ├── _build_viewport()  Map fractal coords → pixel grid
    │   ├── _pixel_color()     Fractal value → RGB dispatch
    │   └── render()           Main render loop → list of ANSI strings
    └── cli.py                 CLI
        ├── PRESETS            Named coordinate/zoom configurations
        ├── main()             argparse → render() → print
        └── _print_info()      --list output
```

### How the half-block trick works

```
Terminal row N:
  ┌──────────────────────────────────────────────┐
  │  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  │
  └──────────────────────────────────────────────┘
         ↑ each ▀ character encodes TWO pixels:
           • foreground color = pixel row 2N     (top half)
           • background color = pixel row 2N+1   (bottom half)

Result: a W × (2H) pixel grid in a W × H character terminal.
Since terminal characters are ~2× taller than wide, each pixel
ends up approximately square.
```

### Smooth coloring formula

Raw iteration counts produce sharp concentric bands.  FractalForge uses the
**normalized iteration count** (Hubbard–Douady potential):

```
smooth_i = i + 1 − log₂(log₂(|z|))
```

This converts the integer escape step into a continuous real value.
The result is divided by `max_iter`, multiplied by a cycle count (6),
taken `mod 1`, and used to look up the color in the theme's gradient table —
producing smooth, multi-banded color without any post-processing passes.

---

## Tips & Tricks

**Increase iteration depth for deep zooms** — at zoom 100× you'll need at
least `--max-iter 512` to see fine detail.

```bash
python main.py --preset seahorse --max-iter 512 --theme plasma
```

**Explore Julia parameter space** — change `c` slightly and re-render:

```bash
python main.py --fractal julia --julia-cr -0.5 --julia-ci 0.5 --theme neon
python main.py --fractal julia --julia-cr  0.28 --julia-ci 0.008 --theme fire
```

**Override terminal size for a larger render:**

```bash
python main.py --width 200 --height 60 --theme ice | less -R
```

**Create a gallery of all themes:**

```bash
for t in fire ocean neon plasma matrix ice mono; do
    echo "=== $t ===" && python main.py --theme $t --height 16 --no-progress
done
```

---

## Contributing

Pull requests are welcome. The cleanest areas to extend:

- **New fractal types** — add a function to `fractals.py` and a branch in
  `renderer._pixel_color()` and `cli.PRESETS`.
- **New themes** — add an entry to `themes.THEMES` (gradient stops + interior color).
- **Performance** — the inner loop in `renderer.py` is a natural candidate for
  `multiprocessing.Pool.starmap()` across rows.
- **Interactive mode** — WASD navigation and live re-render via `curses` or
  `blessed`.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built by Claude — powered by mathematics, rendered in pure Python.*
