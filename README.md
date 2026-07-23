```
╔══════════════════════════════════════════════════════════════════╗
║   ░▒▓  F R A C T A L   U N I V E R S E  ▓▒░                  ║
║         Infinite mathematical beauty in your terminal          ║
╚══════════════════════════════════════════════════════════════════╝
```

<div align="center">

**A pure-Python ASCII/ANSI fractal art generator — zero dependencies, endlessly beautiful.**

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](#)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

</div>

---

## What Is This?

**Fractal Universe** renders [escape-time fractals](https://en.wikipedia.org/wiki/Escape_time_algorithm) — infinitely complex mathematical structures — directly in your terminal using Unicode block characters and 24-bit ANSI colour. It supports four fractal types, eight colour palettes, named location presets, and can export lossless SVG files.

It requires **nothing beyond the Python standard library**.

---

## Features

| Feature | Details |
|---------|---------|
| **4 fractal types** | Mandelbrot set, Julia sets, Burning Ship, Tricorn/Mandelbar |
| **8 colour palettes** | fire, ocean, neon, gold, aurora, cosmos, crimson, ice |
| **17 named presets** | Seahorse Valley, Elephant Valley, deep spirals, and more |
| **Smooth colouring** | Continuous colouring via the complex potential function |
| **Daily fractal** | Unique fractal seeded by today's date — different every day |
| **SVG export** | High-resolution pixel-art SVG output |
| **Zero dependencies** | Pure Python stdlib (`math`, `colorsys`, `hashlib`, …) |
| **ANSI true colour** | 24-bit RGB terminal output — works in any modern terminal |

---

## Gallery

### Classic Mandelbrot Set

```
  Fractal : MANDELBROT       Palette : fire
  Center  : (-0.500000, 0.000000i)  Zoom    : 1.0x

                                                              
                                     .                        
                                    ..:.                      
                                   .:  -:                     
                              ......#   ...                   
                             .= :          -.::.              
                           .#:               -.               
                 ..........-                    .             
                 ..+    +:.#                   =.             
              .:..                             .              
                                             ..               
              .:..                             .              
                 ..+    +:.#                   =.             
                 ..........-                    .             
                           .#:               -.               
                             .= :          -.::.              
                              ......#   ...                   
                                   .:  -:                     
                                    ..:.                      
                                     .                        
```

*The iconic cardioid and bulb structure at zoom 1×. Add colour: `python fractal_universe.py`*

---

### Seahorse Valley — Mandelbrot zoom 60×

```
  Fractal : MANDELBROT       Palette : ocean
  Center  : (-0.745000, 0.100000i)  Zoom    : 60.0x

++-::::::::::::::::::::::::::--#+=+*#                         
 +*::::::::::::::::::::::::::-+++++                           
   --:::::::::::::::::::::::--+                               
#=   * :::::::::::::::::::-*+                                 
++++*--::::::::::::::::::::*   +                              
      -::::::::::::::::::::---*++                             
      ---::::::::::::::::::--*                                
    +    --:::::::::::::::-*#                                 
   *++* ----:::::::::::::---*#=+*                             
        *----::::::::::------ ***                             
        = * ----::::---------                                 
      ***#-----------------*                                  
           ------------------#**                              
          ###---------------                                  
        #*##---------------#                                  
             --------------- #*                               
             # -------------                                  
           ###-------------  *#                               
              =------------=                                  
            ## =----------                                    
               =-----------= #                                
```

*Zoom into the seahorse-shaped tendrils near the main cardioid's boundary.*

---

### Julia Set — Classic (`c = -0.7 + 0.27015i`)

```
  Fractal : JULIA            Palette : fire
  Julia c : -0.70000 + 0.27015i

                                                              
                                      .:                      
                                        .                     
                               . - ..    =: .                 
                     .   .   . :    +     -                   
                         ...:       *    :...                 
                : .     =               -::....  .  .*  .     
                =.        *            =  #=-     # = * =.    
                   . ....                               ....#.
                              * #   -    =#           +       
                        .  . # . =....::-               +     
                                   ....-    #       ....   -  
                                      -          : .    :     
                                      .     ..                
                                        . #:                  
```

*The "rabbit" shape of the classic Julia set — connected but infinitely intricate.*

---

### Julia Set — Spiral (`c = -0.7269 + 0.1889i`)

```
  Fractal : JULIA            Palette : aurora
  Julia c : -0.72690 + 0.18890i

                                     .* .                     
                                  ...    #                    
                      *         .    -   +                    
                      :      . #    # +   :::                 
                 :      - .:            - ....... : + -       
              .         ++            #  *  -*           =    
                 #  *:.. *            ++ +*             :..# =
                        =         ==  -  #            +       
                       :  .:    .......              ..      .
                                    :::   +#      #. .:#  .   
                                   .#  #      # -.       :.   
                                   . .     ..#                
```

*Delicate tendrils spiral outward from a barely-connected Julia set near the boundary.*

---

### Burning Ship Fractal

```
  Fractal : BURNING_SHIP     Palette : fire

                                         ......               
                                      ...-                    
                                 ....:=                       
                     ............:+            .              
                                             ..               
             .                               :.               
              .                              :..              
               .* -                          +..              
                    -                         :..             
                     =-                        +..            
                      .-.=                       ..           
                     :=:-=#+                      ..          
                      .:-  * =-  :                 :.         
                         .:....    .# :              -.       
```

*A Mandelbrot variant with `|Re(z)|` and `|Im(z)|` taken each iteration — creating ship-like forms.*

---

## Quick Start

```bash
# Clone and run — no install needed
git clone https://github.com/kareemrt/Clauder.git
cd Clauder
python fractal_universe.py
```

---

## Usage

```
python fractal_universe.py [OPTIONS]
```

### Options

```
  --fractal {mandelbrot,julia,burning_ship,tricorn}
                        Fractal type (default: mandelbrot)
  --preset NAME         Named location preset (see --list-presets)
  --palette PALETTE     Colour palette: fire ocean neon gold aurora cosmos crimson ice
  --zoom FLOAT          Zoom level (default: 1.0; try 50–800 for deep dives)
  --cx FLOAT            Centre X / real axis
  --cy FLOAT            Centre Y / imaginary axis
  --jcx FLOAT           Julia c — real part (default: -0.7)
  --jcy FLOAT           Julia c — imaginary part (default: 0.27015)
  --width INT           Width in characters (default: terminal width)
  --height INT          Height in characters (default: terminal height)
  --iterations INT      Max iterations (default: 80; higher = more detail)
  --no-color            Plain ASCII output, no ANSI sequences
  --daily               Render today's unique fractal (new one every day)
  --list-presets        Print all named presets and exit
  --save-svg FILE       Export as a scalable SVG file
```

### Examples

```bash
# Zoom into Seahorse Valley with ocean palette
python fractal_universe.py --preset seahorse

# Julia set — the "dragon" variant
python fractal_universe.py --fractal julia --preset dragon

# Burning Ship with crimson palette
python fractal_universe.py --fractal burning_ship --palette crimson

# Deep dive: spiral at zoom 250x
python fractal_universe.py --preset spiral --iterations 150

# Today's unique fractal (different every day)
python fractal_universe.py --daily

# Custom coordinates — near the galaxy nebula
python fractal_universe.py --cx -0.1592 --cy 1.0317 --zoom 80 --palette cosmos

# Export a 1200×800 SVG
python fractal_universe.py --preset lightning --palette neon --save-svg lightning.svg

# Plain ASCII (no colour) — great for screenshots & docs
python fractal_universe.py --no-color --width 60 --height 28
```

---

## Presets Reference

### Mandelbrot Set Presets

| Preset | Centre | Zoom | Default Palette | Description |
|--------|--------|------|-----------------|-------------|
| `classic` | (−0.5, 0) | 1× | fire | The full set |
| `seahorse` | (−0.745, 0.1) | 60× | ocean | Seahorse Valley tendrils |
| `elephant` | (0.275, 0) | 8× | gold | Elephant Valley |
| `spiral` | (−0.7616, −0.0848) | 250× | aurora | Deep spiral arms |
| `lightning` | (−0.3905, −0.5868) | 120× | neon | Lightning bolt filaments |
| `galaxy` | (−0.1592, 1.0317) | 80× | cosmos | Nebula-like region |
| `minibrot` | (−1.749, 0) | 800× | fire | Mini Mandelbrot deep zoom |
| `valley` | (−0.5257, 0.5243) | 40× | ocean | Quiet valley with fine detail |
| `dendrite` | (0, 1) | 4× | ice | Dendritic boundary |

### Julia Set Presets

| Preset | `c` parameter | Default Palette | Character |
|--------|--------------|-----------------|-----------|
| `classic` | −0.7 + 0.27015i | fire | Connected blobs |
| `dragon` | −0.8 + 0.156i | neon | Dragon-wing shape |
| `lightning` | −0.4 + 0.6i | gold | Forked lightning |
| `spiral` | −0.7269 + 0.1889i | aurora | Thin tendrils |
| `snowflake` | −0.38 + 0.659i | ice | Snowflake symmetry |
| `dendrite` | 0 + 1i | cosmos | Tree-branch pattern |
| `rabbit` | −0.1226 + 0.7449i | aurora | San Marco rabbit |
| `galaxy` | −0.6277 + 0.4219i | cosmos | Spiral galaxy shape |

---

## Palette Reference

| Name | Character | Feel |
|------|-----------|------|
| `fire` | 🔥 | Deep red → orange → white-hot |
| `ocean` | 🌊 | Midnight blue → teal → seafoam |
| `neon` | ⚡ | Full spectrum rainbow at full saturation |
| `gold` | ✨ | Rich amber → bright gold |
| `aurora` | 🌌 | Green → teal → violet (northern lights) |
| `cosmos` | 🌠 | Deep purple → indigo → electric blue |
| `crimson` | 🩸 | Deep crimson → pink |
| `ice` | ❄️ | Pale blue → white |

---

## How It Works

### The Escape-Time Algorithm

For each pixel at complex coordinate `c`, iterate the recurrence:

```
z₀ = 0
z_{n+1} = z_n² + c          (Mandelbrot)
z_{n+1} = z_n² + c          (Julia — z₀ = pixel coord, c is fixed)
z_{n+1} = (|Re(z)| + i|Im(z)|)² + c   (Burning Ship)
z_{n+1} = conj(z_n)² + c   (Tricorn)
```

If `|z_n| > 2` at iteration `n`, the point *escapes* and is coloured by how quickly it escaped. Points that never escape (within `max_iter` iterations) are coloured black — they are *inside the set*.

### Smooth Colouring

Naive integer iteration counts produce visible "bands". To eliminate them, the [continuous (smooth) colouring](https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set#Continuous_(smooth)_colouring) formula is used:

```python
# At escape: smooth escape count via the complex potential
smooth_n = n + 1.0 - log2(log2(|z_n|))
```

This yields a floating-point escape value, which maps smoothly onto the colour palette.

### Terminal Rendering

Each character cell is one "pixel". Terminal characters are approximately 2× taller than wide, so the viewport's aspect ratio is corrected by scaling the imaginary range accordingly. Unicode block characters (`░▒▓█`) provide four levels of "density" within each ANSI-coloured cell, effectively doubling visual resolution.

---

## Project Structure

```
Clauder/
├── fractal_universe.py   # Core generator — all logic in one file
└── README.md             # This file
```

The entire renderer, CLI, and SVG exporter live in a single self-contained file with no external dependencies.

---

## Requirements

- Python 3.7+
- A terminal with 24-bit ANSI colour support (iTerm2, Windows Terminal, most modern Linux terminals)
- No `pip install` needed

---

## License

MIT — do whatever you like with it. If you generate something beautiful, share it.

---

*Built by [Claude](https://claude.ai) — AI-generated code exploring infinite mathematical beauty.*
