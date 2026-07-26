# Fractal Explorer 🔭

> **Infinite mathematical beauty, rendered directly in your terminal.**

Fractal Explorer is a Python CLI that renders stunning ASCII/Unicode fractal art without any external dependencies beyond `rich`. Explore the Mandelbrot set, Julia sets, the Sierpiński triangle, and the dragon curve — all from your command line.

---

## ✨ Features

| Fractal | Description |
|---|---|
| **Mandelbrot Set** | The iconic set of complex numbers with 6 zoom presets, 6 palettes, and 6 color schemes |
| **Julia Sets** | 8 presets — dragons, dendrites, spirals, and more — each with unique character |
| **Sierpiński Triangle** | Generated via the elegant XOR bit trick: `(x & y) == 0` |
| **Dragon Curve** | Space-filling L-system curve folded up to 15 times |
| **Gallery Mode** | All four fractals side-by-side in a single glance |

**Rendering options:**
- 6 ASCII palettes: `classic`, `blocks`, `dots`, `minimal`, `matrix`, `space`
- 6 color schemes: `fire`, `ocean`, `forest`, `purple`, `grayscale`, `rainbow`
- Custom zoom regions via `--xmin/--xmax/--ymin/--ymax`
- Custom canvas size via `--width` / `--height`
- No-color mode for plain ASCII export

---

## 📦 Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements.txt
```

**Requirements:** Python 3.11+ · `rich >= 13.0`

---

## 🚀 Quick Start

```bash
# Show the help menu with banner
python main.py

# Full Mandelbrot set (fire colorscheme, blocks palette)
python main.py mandelbrot

# Julia "Dragon" preset
python main.py julia --preset 0

# Sierpiński triangle, size 64
python main.py sierpinski --size 64

# Dragon curve, 12 folds
python main.py dragon --iterations 12

# All four fractals side-by-side
python main.py gallery
```

---

## 📖 Commands

### `mandelbrot` (alias: `mb`)

Renders the Mandelbrot set — the most famous object in complex dynamics.

```
python main.py mandelbrot [OPTIONS]

Options:
  -W, --width     INT    Canvas width in characters   [default: 100]
  -H, --height    INT    Canvas height in characters  [default: 40]
  --xmin          FLOAT  Left x boundary              [default: -2.5]
  --xmax          FLOAT  Right x boundary             [default:  1.0]
  --ymin          FLOAT  Bottom y boundary            [default: -1.25]
  --ymax          FLOAT  Top y boundary               [default:  1.25]
  --iter          INT    Maximum iterations           [default: 80]
  --palette       STR    ASCII palette name           [default: blocks]
  --color         STR    Color scheme name            [default: fire]
  --preset        INT    Use a zoom preset (0–5)
  --no-color             Disable color output
  --list-presets         Show all zoom presets
```

**Zoom Presets:**

| # | Name | Description |
|---|---|---|
| 0 | Full View | The complete Mandelbrot set |
| 1 | Seahorse Valley | Delicate seahorse-like spirals |
| 2 | Elephant Valley | Rows of elephant-trunk spirals |
| 3 | Mini Mandelbrot | A tiny copy of the whole set |
| 4 | Deep Spiral | Infinite recursive spirals |
| 5 | Center Zoom | The central cardioid up close |

```
Example — Seahorse Valley:
python main.py mandelbrot --preset 1 --width 120 --height 50 --iter 150 --color ocean
```

---

### `julia` (alias: `jl`)

Renders a Julia set for the constant `c = cx + cy·i`.

```
python main.py julia [OPTIONS]

Options:
  -W, --width     INT    Canvas width                 [default: 100]
  -H, --height    INT    Canvas height                [default: 40]
  --cx            FLOAT  Real part of c               [default: -0.7]
  --cy            FLOAT  Imaginary part of c          [default: 0.27015]
  --iter          INT    Maximum iterations           [default: 80]
  --palette       STR    ASCII palette name           [default: blocks]
  --color         STR    Color scheme name            [default: ocean]
  --preset        INT    Use a Julia preset (0–7)
  --no-color             Disable color output
  --list-presets         Show all Julia presets
```

**Julia Presets:**

| # | Name | c value | Character |
|---|---|---|---|
| 0 | Dragon | -0.7 + 0.27015i | Classic spiraling dragon |
| 1 | Dendrite | -0.835 - 0.2321i | Tree-like branching |
| 2 | Rabbit | -0.8 + 0.156i | Douady's rabbit (3 lobes) |
| 3 | Symmetric | 0.285 + 0.01i | Symmetric filaments |
| 4 | Spiral Galaxy | -0.4 + 0.6i | Galactic spiral arms |
| 5 | Rings | 0.0 + 0.8i | Concentric ring structure |
| 6 | Feather | -0.7269 + 0.1889i | Delicate feather pattern |
| 7 | San Marco | -0.12 + 0.74i | San Marco fractal dragon |

```
Example — Spiral Galaxy:
python main.py julia --preset 4 --color rainbow --palette dots
```

---

### `sierpinski` (alias: `si`)

Renders the Sierpiński triangle using the XOR bit trick: a point `(x, y)` is filled when `(x & y) == 0`.

```
python main.py sierpinski [OPTIONS]

Options:
  -s, --size  INT    Triangle size (power of 2 recommended)  [default: 32]
  --color     STR    Rich color name                         [default: green]
```

```
Example:
python main.py sierpinski --size 64 --color bright_cyan
```

The XOR construction reveals a deep truth: the Sierpiński triangle is the Pascal's triangle modulo 2.

---

### `dragon` (alias: `dr`)

Renders the dragon curve — a self-similar space-filling curve generated by repeatedly folding a strip of paper and unfolding at 90°. Implemented via L-system rewriting rules:

```
X → X+YF+
Y → −FX−Y
```

```
python main.py dragon [OPTIONS]

Options:
  -i, --iterations  INT  Number of folding iterations (max ~15)  [default: 13]
  -W, --width       INT  Grid width                              [default: 70]
  -H, --height      INT  Grid height                             [default: 30]
  --color           STR  Rich color name                         [default: cyan]
```

```
Example:
python main.py dragon --iterations 15 --width 100 --height 40 --color magenta
```

---

### `gallery`

Displays all four fractals side-by-side — great for a quick overview.

```
python main.py gallery [OPTIONS]

Options:
  --palette   STR  Palette for gradient fractals   [default: blocks]
  --mb-color  STR  Color scheme for Mandelbrot     [default: fire]
  --jl-color  STR  Color scheme for Julia          [default: ocean]
```

---

### `list`

Displays all available palettes and color schemes with visual previews.

```
python main.py list
```

---

## 🎨 Palettes & Color Schemes

### Palettes (density mapping)

| Name | Characters | Best for |
|---|---|---|
| `classic` | ` .:-=+*#%@` | Classic Unix ASCII art style |
| `blocks` | ` ░▒▓█` | Rich Unicode block shading |
| `dots` | ` ·•●` | Minimal dotwork |
| `minimal` | ` .+#` | Clean, high-contrast |
| `matrix` | ` .:;!|(){}[]` | Terminal hacker aesthetic |
| `space` | ` ·✦★` | Cosmic / starfield effect |

### Color Schemes

| Name | Gradient | Character |
|---|---|---|
| `fire` | Black → red → yellow → white | Hot lava |
| `ocean` | Black → navy → cyan → white | Deep sea |
| `forest` | Black → dark green → lime → white | Forest canopy |
| `purple` | Black → magenta → violet → white | Cosmic nebula |
| `grayscale` | Black → grey → white | Classic b/w |
| `rainbow` | Red → orange → yellow → green → cyan → blue | Full spectrum |

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

All 20 tests cover the computation engines, boundary conditions, and rendering pipeline:

```
tests/test_fractals.py::TestMandelbrot::test_returns_correct_shape      PASSED
tests/test_fractals.py::TestMandelbrot::test_origin_inside_set          PASSED
tests/test_fractals.py::TestMandelbrot::test_far_point_escapes_quickly  PASSED
tests/test_fractals.py::TestMandelbrot::test_iteration_counts_in_range  PASSED
tests/test_fractals.py::TestMandelbrot::test_negative_two_inside_set    PASSED
tests/test_fractals.py::TestJulia::test_returns_correct_shape           PASSED
tests/test_fractals.py::TestJulia::test_c_zero_origin_inside            PASSED
tests/test_fractals.py::TestJulia::test_far_z_escapes                   PASSED
tests/test_fractals.py::TestJulia::test_all_values_bounded              PASSED
tests/test_fractals.py::TestSierpinski::test_size                       PASSED
tests/test_fractals.py::TestSierpinski::test_top_left_always_filled     PASSED
tests/test_fractals.py::TestSierpinski::test_contains_spaces            PASSED
tests/test_fractals.py::TestDragonCurve::test_produces_points           PASSED
tests/test_fractals.py::TestDragonCurve::test_point_count_grows_...     PASSED
tests/test_fractals.py::TestDragonCurve::test_grid_shape                PASSED
tests/test_fractals.py::TestDragonCurve::test_grid_has_true_values      PASSED
tests/test_fractals.py::TestRenderer::test_render_grid_returns_text     PASSED
tests/test_fractals.py::TestRenderer::test_all_palettes_work            PASSED
tests/test_fractals.py::TestRenderer::test_all_color_schemes_work       PASSED
tests/test_fractals.py::TestRenderer::test_sierpinski_render            PASSED
20 passed in 0.06s
```

---

## 📐 How It Works

### Escape-Time Algorithm (Mandelbrot & Julia)

Both the Mandelbrot and Julia sets use the **escape-time algorithm**:

```
For each pixel (cx, cy) on the complex plane:
  z = 0               ← Mandelbrot starts here
  z = (cx, cy)        ← Julia starts here with a fixed c

  Iterate: z → z² + c

  Count iterations until |z| > 2 (escapes to infinity)
  → Map iteration count to a color/character
  → Pixels that never escape (count=0) form the set itself
```

The boundary of the set — where iteration counts transition rapidly — is where the fractal detail lives.

### Sierpiński Triangle (XOR Trick)

```python
filled = (x & y) == 0    # bitwise AND equals zero → paint this pixel
```

This works because Pascal's triangle mod 2 produces the Sierpiński pattern, and Pascal's triangle mod 2 at position `(row, col)` is 1 when `(row & col) == 0` (no carries in binary addition).

### Dragon Curve (L-System)

An L-system is a string rewriting system that models self-similar structures:

```
Axiom:   FX
Rules:   X → X+YF+
         Y → −FX−Y

After n iterations, interpret F=forward, +=turn right 90°, −=turn left 90°
```

Each iteration doubles the number of segments, producing the characteristic self-similar "folded paper" shape.

---

## 🗂️ Project Structure

```
clauder/
├── main.py                    ← Entry point
├── requirements.txt
├── README.md
├── fractal_explorer/
│   ├── __init__.py
│   ├── mandelbrot.py          ← Mandelbrot computation + zoom presets
│   ├── julia.py               ← Julia set computation + presets
│   ├── sierpinski.py          ← Sierpiński triangle + dragon curve
│   ├── renderer.py            ← Rich-based terminal rendering engine
│   └── cli.py                 ← argparse CLI + all command handlers
└── tests/
    ├── __init__.py
    └── test_fractals.py       ← 20 unit tests
```

---

## 🧬 The Mathematics

Fractals are objects with **self-similarity at all scales** and often **non-integer (fractal) dimensions**.

| Fractal | Hausdorff Dimension | Discovery |
|---|---|---|
| Mandelbrot Set boundary | ~2.0 (area = 0, perimeter = ∞) | Benoit Mandelbrot, 1979 |
| Julia Sets | 1 to 2 depending on c | Gaston Julia, 1918 |
| Sierpiński Triangle | log(3)/log(2) ≈ 1.585 | Wacław Sierpiński, 1915 |
| Dragon Curve | ~1.5236 | Heighway, Harter & Banks, 1966 |

The Mandelbrot set is the **connectedness locus** of the Julia family: pick any point c inside M, and the Julia set for that c is a connected shape. Pick c outside M, and the Julia set shatters into a Cantor dust.

---

## 📋 Sample Output

### Mandelbrot Set (classic palette)

```
                                                                                
                                                     .                          
                                                      ..:.                      
                                                     .-=.                       
                                                   .:-   ..                     
                                                   .:     .                     
                                            .=...+.-=     -+:.   ..             
                                            .                     .             
                                          ...                   :.              
                             .    .      ..*                     =...           
                             ..:...+......                        :.            
                             ..:      =..=                         -            
                          ....          :                         *             
                        ...  =                                   .              
                        ...  =                                   .              
                          ....          :                         *             
                             ..:      =..=                         -            
                             ..:...+......                        :.            
                             .    .      ..*                     =...           
                                          ...                   :.              
                                            .                     .             
                                            .=...+.-=     -+:.   ..             
                                                   .:     .                     
                                                   .:-   ..                     
                                                     .-=.                       
                                                      ..:.                      
                                                     .                          
```

### Sierpiński Triangle (size 16)

```
████████████████
█ █ █ █ █ █ █ █ 
██  ██  ██  ██  
█   █   █   █   
████    ████    
█ █     █ █     
██      ██      
█       █       
████████        
█ █ █ █         
██  ██          
█   █           
████            
█ █             
██              
█               
```

---

## 💡 Ideas for Exploration

- **Zoom in on the seahorse valley**: `--preset 1 --iter 200 --color ocean`
- **Compare Julia presets side-by-side**: run `julia --preset N` for N in 0–7
- **Export ASCII art**: pipe output to a file: `python main.py mandelbrot --no-color > mandelbrot.txt`
- **Tweak the iteration limit**: higher `--iter` reveals more boundary detail but takes longer
- **Combine unusual palettes + color schemes**: `--palette space --color rainbow`

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with Python 3.11 and [rich](https://github.com/Textualize/rich). No numerical libraries required — pure Python math.*
