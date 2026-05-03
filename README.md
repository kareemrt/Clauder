# FractalForge 🌀

**Terminal Fractal Art Generator** — render stunning mathematical fractals directly in your terminal with ANSI colors, multiple palettes, zoom controls, and file export.

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
  Terminal Fractal Art Generator  v1.0.0
```

---

## Table of Contents

- [Features](#features)
- [Fractals](#fractals)
- [Gallery](#gallery)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Color Palettes](#color-palettes)

---

## Features

| Feature | Description |
|---|---|
| **5 Fractal Types** | Mandelbrot, Julia, Burning Ship, Tricorn, Newton |
| **6 Color Palettes** | fire, ocean, neon, grayscale, rainbow, matrix |
| **Zoom Control** | Specify center and radius to explore any region |
| **Animation** | Watch iteration depth build up frame-by-frame |
| **File Export** | Save plain-text ASCII art to any file |
| **Gallery Mode** | Render all fractals back-to-back in a showcase |
| **Pure Python** | Only dependency is `colorama` — no NumPy, no C extensions |

---

## Fractals

### Mandelbrot Set
The **Mandelbrot set** is the set of complex numbers `c` for which the iteration `z → z² + c` does not diverge. It is the most studied fractal in mathematics, exhibiting infinite self-similar complexity at every scale.

### Julia Sets
**Julia sets** are defined by the same iteration as Mandelbrot, but the parameter `c` is fixed and the starting point `z` varies. Each value of `c` produces a completely different shape — from connected dendrites to disconnected "Fatou dust."

### Burning Ship
The **Burning Ship fractal** uses `z → (|Re(z)| + i|Im(z)|)² + c`. Taking the absolute values of the real and imaginary parts before squaring distorts the symmetry and creates forms that resemble a burning ship rising from the sea.

### Tricorn (Mandelbar)
The **Tricorn** replaces `z` with its complex conjugate: `z → z̄² + c`. This creates a three-fold symmetric shape (hence "tricorn") that looks like a three-pronged pitchfork of the Mandelbrot set.

### Newton Fractal
The **Newton fractal** visualizes the basins of attraction of Newton's root-finding method applied to `f(z) = z³ − 1`. Each color region converges to a different root of the cubic, with beautiful fractal boundaries between the basins.

---

## Gallery

### Mandelbrot Set — `fire` palette
```
                                                                                
                                                                                
                                                     ..                         
                                                      ...                       
                                                   .:=  ::.                     
                                                  ..=    ..                     
                                           .:-=..            ......             
                                           ..:                   :              
                            .            .:                       .             
                             .:...-.:....:                        #.            
                            ...*      =..                          :            
                         ....           -                         -             
                                                               =..              
                         ....           -                         -             
                            ...*      =..                          :            
                             .:...-.:....:                        #.            
                            .            .:                       .             
                                           ..:                   :              
                                           .:-=..            ......             
                                                  ..=    ..                     
                                                   .:=  ::.                     
                                                      ...                       
                                                     ..                         
```

### Julia Set (c = −0.7 + 0.27i) — `neon` palette
```
                                                                                
                                      :                                         
                                       -                                        
                           -   .  .       -.  .                                 
            .   .        ... *=- . * *     =  .                                 
            .  -:.....:  ++#   #   +   * :.....                                 
    .+..:     %      =#            #%  -  .........-...    .                    
  .               *+                  =-=% #  :    =   +  -  +   *.             
        .  . .... *  #           %%% #     # %%%           #  * .... .  .       
              .*   +  -  +   =    :  # %=-=                  +*               . 
                     .    ...-.........  -  %#            #=      %     :..+.   
                                  .....: *   +   #   #++  :.....:-  .           
                                  .  =     * * . -=* ...        .   .           
                                  .  .-       .  .   -                          
                                         -                                      
                                          :                                     
```

### Burning Ship — `ocean` palette
```
                                                      ..                        
                                                  ..:                           
                                               ..:                              
                                          ....-                                 
                            ....:   :...:-                                      
              . ....                                    .                       
                    .                                   ..                      
                     :                                  ..                      
                      *                                 :.                      
                        .                                ..                     
                                                          ..                    
                            :- . +                         ..                   
                             ..:=%.    *                    :.                  
                             .:.-.--= % %                    -.                 
                              :.:#..#*=    = .                 ..               
                                  :: :=- .   .::*  #             .              
                                   :                ...   : +   =-+.....        
                                                             -.:.--=.           
```

### Mandelbrot Zoom — center (−0.5, 0) radius 0.4 — `rainbow` palette
```
                 ........:+ *                                                   
               ....:#= ::                                                       
.        ..........::=                                                          
..................:::-                                                          
:.: :.............:+=                                                           
++=+%:=-........:-#                                                             
       ==:......:-                                                              
           :::::                                                                
             :::                                                                
              --                                                                
               +                                                                
               +                                                                
              --                                                                
             :::                                                                
           :::::                                                                
       ==:......:-                                                              
++=+%:=-........:-#                                                             
:.: :.............:+=                                                           
..................:::-                                                          
.        ..........::=                                                          
               ....:#= ::                                                       
```

> **Note:** The terminal renders these with full ANSI color. The above are plain-text representations — run the tool yourself for the full experience!

---

## Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install the single dependency
pip install -r requirements.txt
```

**Requirements:** Python 3.11+ · colorama ≥ 0.4.6

---

## Usage

```bash
python main.py [OPTIONS]
```

### Quick Start

```bash
# Default: Mandelbrot set with fire palette
python main.py

# Julia set with neon colors
python main.py -f julia -p neon

# Burning Ship with ocean palette, wide view
python main.py -f burning_ship -p ocean -W 140 -H 45

# Zoom into the Mandelbrot seahorse valley
python main.py -f mandelbrot --zoom -0.75 0.1 0.05 -p rainbow -i 200

# Animated Julia set building up iteration depth
python main.py -f julia -a --frames 30 -p fire

# Show all fractals in a gallery
python main.py --gallery

# Export to a text file
python main.py -f newton -o my_newton.txt

# List all fractals and palettes
python main.py --list
```

---

## Options

```
  -f, --fractal    {mandelbrot,julia,burning_ship,tricorn,newton}
                   Fractal type  (default: mandelbrot)

  -p, --palette    {fire,ocean,neon,grayscale,rainbow,matrix}
                   Color palette  (default: fire)

  -W, --width      Terminal width in characters  (default: 120)
  -H, --height     Terminal height in lines      (default: 40)
  -i, --max-iters  Maximum iteration depth       (default: 80)

  --zoom CX CY R   Zoom to center (CX, CY) with radius R
                   e.g. --zoom -0.5 0.6 0.2

  -c RE IM         Julia parameter c = RE + IM·i  (default: -0.7+0.27i)
                   e.g. -c -0.4 0.6   (produces a swirling dendrite)
                        -c 0.285 0.01  (produces a spiral galaxy)

  -a, --animate    Animate iteration depth build-up
  --frames N       Number of animation frames    (default: 20)

  -o, --output F   Save plain-text output to file F
  --gallery        Render all fractals as a gallery showcase
  --list           List available fractals and palettes
  -h, --help       Show this help message
```

---

## Examples

### Exploring Famous Coordinates

```bash
# Seahorse Valley (Mandelbrot)
python main.py -f mandelbrot --zoom -0.75 0.1 0.05 -p ocean -i 200

# Elephant Valley (Mandelbrot)
python main.py -f mandelbrot --zoom 0.3 0 0.1 -p fire -i 150

# Julia — "Douady's rabbit"
python main.py -f julia -c -0.123 0.745 -p rainbow -i 100

# Julia — "Basilica"
python main.py -f julia -c -1 0 -p neon -i 80

# Julia — spiral galaxy
python main.py -f julia -c 0.285 0.01 -p fire -i 100

# Newton fractal (root basin boundaries)
python main.py -f newton -p matrix -i 60 -W 100 -H 35
```

### Pipeline Usage

```bash
# Save a high-detail Mandelbrot
python main.py -f mandelbrot -i 300 -W 200 -H 60 -o mandelbrot_hd.txt

# View it later
cat mandelbrot_hd.txt
```

---

## Project Structure

```
clauder/
├── main.py                          # Entry point
├── requirements.txt                 # colorama
│
└── fractalforge/
    ├── __init__.py                  # Package metadata
    ├── fractals.py                  # Core escape-time algorithms
    │   ├── mandelbrot()             #   z → z² + c
    │   ├── julia()                  #   z → z² + c  (z varies, c fixed)
    │   ├── burning_ship()           #   z → (|Re|+i|Im|)² + c
    │   ├── tricorn()                #   z → z̄² + c
    │   ├── newton()                 #   Newton's method on z³−1
    │   └── render_frame()           #   Compute iteration grid
    │
    ├── palettes.py                  # ANSI color mapping
    │   ├── PALETTES dict            #   fire, ocean, neon, ...
    │   └── color_for_iters()        #   Map count → (color, char)
    │
    ├── renderer.py                  # Output layer
    │   ├── render_terminal()        #   ANSI colored terminal output
    │   ├── render_to_file()         #   Plain-text file export
    │   └── demo_gallery()           #   All-fractals showcase
    │
    ├── cli.py                       # argparse CLI + ASCII banner
    │
    └── examples/
        ├── mandelbrot_fire.txt
        ├── julia_neon.txt
        ├── burning_ship_ocean.txt
        └── mandelbrot_zoom.txt
```

---

## How It Works

FractalForge uses the **escape-time algorithm**: for each pixel `(x, y)` mapped to a complex number, we iterate a function and count how many steps it takes to "escape" beyond a threshold (usually radius 2). Points that never escape belong to the fractal set itself; points that escape quickly are on the outer fringes.

```
For each pixel (col, row):
  c = x_min + col * x_step  +  i * (y_max - row * y_step)
  z = 0
  for i in 0 .. max_iters:
      if |z| > 2.0:  return i        ← escaped: color by how fast
      z = z² + c
  return max_iters                   ← inside the set: draw black
```

The iteration count is then mapped to a character and ANSI color through the selected palette, producing a colored ASCII representation in the terminal.

### Smooth Coloring
Character density increases with iteration ratio (`ratio = iters / max_iters`), giving a smooth gradient from sparse dots near the set boundary to dense characters in the outer regions.

---

## Color Palettes

| Palette | Description | Best For |
|---|---|---|
| `fire` | White → yellow → red → blue | Mandelbrot, Julia |
| `ocean` | White → cyan → blue → magenta | Burning Ship |
| `neon` | Green → cyan → blue → magenta → red | Julia sets |
| `grayscale` | White gradient | Print-friendly output |
| `rainbow` | Full spectrum rotation | Zoom explorations |
| `matrix` | Monochrome green | Newton, tricorn |

---

## Mathematics

The escape-time algorithm exploits a key theorem: if `|z|` ever exceeds 2, the iteration diverges to infinity. This gives us a finite bound to check, making the computation tractable.

The **boundary** of the Mandelbrot set is infinitely complex — no matter how far you zoom in, new structure appears. This is a consequence of the set being a **fractal**: a self-similar shape with non-integer Hausdorff dimension (~2 for Mandelbrot).

Julia sets and the Mandelbrot set are deeply connected: a point `c` is in the Mandelbrot set if and only if the corresponding Julia set `J_c` is **connected**.

---

*Built with Python 3.11 · colorama · pure math*
