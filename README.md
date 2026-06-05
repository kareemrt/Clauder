# FractalScope 🔭

> **Infinite complexity from simple rules** — a terminal fractal renderer built in pure Python.

FractalScope renders stunning **Mandelbrot sets**, **Julia sets**, **Burning Ship fractals**, and **Sierpinski triangles** directly in your terminal using ASCII art and true-color ANSI gradients. No dependencies, no GPU — just math and your shell.

---

## Gallery

### Mandelbrot Set

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%   %%@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=    %@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%@%+##       %#@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:                *  @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#%%                   %@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                      =%@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@%*%% %-%@@                        #@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%        .%                         @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@-%%=                                  *@@@@@@@@@@@@@@@@@@
@@@@@@                                                 %@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@-%%=                                  *@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%        .%                         @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@%*%% %-%@@                        #@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                      =%@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#%%                   %@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:                *  @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%@%+##       %#@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=    %@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%   %%@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```
*`--fractal mandelbrot --charset classic --palette plasma`*

---

### Julia Set  `c = -0.7 + 0.27015i`

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@? @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@   S##S    *   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@  % S@@@@ ,#   +%S  *     *:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@ ;# ;S###@#  ?+     **   ;####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@ *@#      S +S  .        +  ? +###@@@@@@@; #@@S #@@@@@@@@@@@@@@@@@@
@@@@@@@;  *       *, ,;:          .   SS   #  # %S  ?# ,  #@@@@@@@@@@@@@@@@@
@@@@@@@@@@#  ,. + ; ?  .            ?    :  ? .    ; ?  % S @@@@@@@@@@@@@@@@
@@@@@@@@@@@ @###@###            ,:   ...   :,            ###@###@ @@@@@@@@@@
@@@@@@@@@@@@@@@@@ S %  ? ;    . ?  :    ?            .  ? ; + .,  #@@@@@@@@@
@@@@@@@@@@@@@@@@@@#  , #?  S% #  #   SS   .          :;, ,*       *  ;@@@@@@
@@@@@@@@@@@@@@@@@@@# S@@# ;@@@@@@@###+ ?  +        .  S+ S      #@* @@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@####;   **     +?  #@###S; #; @@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:*     *  S%+   #, @@@@S %  @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   *    S##S   @@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```
*`--fractal julia --cx -0.7 --cy 0.27015 --charset dense`*

---

### Burning Ship Fractal

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#              :%%@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@%@@%@@%%%%@%-*                   *%@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@%@@@@@@@%%%#      *#-*                       @@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@##@@@@%                                      %@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@%:%#@@                                       %@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@#%@@@@@                                       %@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@ %                                      #%@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@                                         %@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@                                          @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@:%                                           @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@%                                           @@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@*                                         @@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@  .                                    @@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@  - =                              @@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@#  -                       +@  %@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@                    =#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@                  :##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@              %-# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```
*`--fractal burning --charset classic --palette fire`*

---

### Sierpinski Triangle  `depth = 4`

```
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
*`--fractal sierpinski --depth 4`*

---

## Features

| Feature | Details |
|---|---|
| **Fractals** | Mandelbrot, Julia set, Burning Ship, Sierpinski triangle |
| **Color palettes** | `plasma` `fire` `ocean` `matrix` `gold` `neon` |
| **Charsets** | `dense` `blocks` `dots` `classic` `simple` |
| **True color** | 24-bit ANSI gradients with smooth iteration mapping |
| **Configurable** | Center, zoom, C-parameter, iterations, width, height |
| **Export** | Save plain-text renders to file |
| **Zero deps** | Pure Python 3.8+ standard library only |

---

## Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Run directly
python main.py

# Or install as CLI tool
pip install -e .
fractalscope
```

---

## Usage

```
usage: fractalscope [-h] [--fractal {mandelbrot,julia,burning,sierpinski}]
                    [--palette {fire,ocean,matrix,plasma,gold,neon}]
                    [--charset {dense,blocks,dots,classic,simple}]
                    [--width W] [--height H] [--iters N] [--zoom Z]
                    [--cx CX] [--cy CY] [--depth D]
                    [--no-color] [--save FILE] [--list]
```

### Examples

```bash
# Default Mandelbrot with plasma palette
fractalscope

# Julia set with custom C-parameter
fractalscope --fractal julia --cx -0.4 --cy 0.6

# Mandelbrot zoomed into the seahorse valley
fractalscope --cx -0.75 --cy 0.1 --zoom 8 --iters 200

# Burning Ship with fire palette and block characters
fractalscope --fractal burning --palette fire --charset blocks

# Sierpinski at depth 5
fractalscope --fractal sierpinski --depth 5

# Wide render, save to file
fractalscope --width 160 --height 60 --save render.txt

# No color (great for piping / logging)
fractalscope --no-color --charset simple

# List all available options
fractalscope --list
```

---

## Project Structure

```
clauder/
├── fractalscope/
│   ├── __init__.py       — package metadata
│   ├── cli.py            — argument parsing & main entry point
│   ├── fractals.py       — iteration engines (Mandelbrot, Julia, Burning Ship, Sierpinski)
│   ├── colors.py         — palettes, ANSI color helpers, charset mapping
│   └── display.py        — terminal rendering, header, legend
├── main.py               — convenience runner  (python main.py)
├── setup.py              — pip-installable entry point
└── README.md
```

---

## How It Works

Every fractal is based on iterating a simple complex-number formula and counting how many steps it takes to "escape" a boundary radius:

```
Mandelbrot:    z_{n+1} = z_n²  + c        (z₀ = 0,      c = pixel coordinate)
Julia:         z_{n+1} = z_n²  + c        (z₀ = pixel,  c = fixed constant)
Burning Ship:  z_{n+1} = (|Re(z)| + i|Im(z)|)²  + c
```

The escape count is mapped to an ASCII character (by density) and an RGB color (via a smooth palette function), producing the rendered image:

```
iteration count  →  normalize (0–1)  →  smooth curve  →  palette RGB  →  ANSI cell
                                     →  charset index  →  ASCII char   ↗
```

**Smooth coloring** applies a sine-wave modulation to the normalized iteration count before palette lookup, eliminating the harsh banding that basic linear mapping produces.

---

## Color Palettes

| Palette | Character | Description |
|---|---|---|
| `plasma` | default | Purple → cyan → yellow sine-wave gradient |
| `fire`   | 🔥 | Black → red → orange → white |
| `ocean`  | 🌊 | Deep navy → teal → light blue |
| `matrix` | 💚 | Black → bright green (hacker aesthetic) |
| `gold`   | ✨ | Black → amber → bright gold |
| `neon`   | ⚡ | Electric multi-hued pulsing gradient |

---

## Character Sets

| Charset | Sample | Best for |
|---|---|---|
| `dense`   | `@#S%?*+;:,.` | High-detail renders |
| `blocks`  | `█▓▒░`        | Clean blocky look  |
| `dots`    | `●◉◎○`        | Minimal / artistic |
| `classic` | `@%#*+=-:.`   | Classic ASCII art  |
| `simple`  | `#.`          | Stark contrast     |

---

## Requirements

- Python **3.8+**
- A terminal with **true-color support** for full color experience (iTerm2, Windows Terminal, Alacritty, most modern terminals)
- Falls back gracefully to plain ASCII in non-color environments

---

## The Math

**Why are fractals infinitely detailed?**

The Mandelbrot set's boundary has Hausdorff dimension ≈ 2. No matter how deep you zoom, new structures emerge — self-similar spirals called "mini-brots" appear at every scale, connected by intricate filaments. This infinite complexity arises purely from `z → z² + c`.

**Julia sets** are the "slices" of the Mandelbrot set: each point `c` in the Mandelbrot plane corresponds to a unique Julia set. Points inside the Mandelbrot set produce connected Julia sets; points outside produce Cantor dust.

**The Burning Ship** applies absolute values before squaring, warping the symmetry and producing its distinctive hull shape at the bottom of the rendered region.

**Sierpinski's triangle** emerges from Pascal's triangle: shade every cell where `C(n, k) mod 2 == 1` and the self-similar triangle appears. Its fractal dimension is `log(3)/log(2) ≈ 1.585`.

---

*Built with [Clauder](https://github.com/kareemrt/clauder)*
