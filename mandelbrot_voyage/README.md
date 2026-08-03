# 🌀 Mandelbrot Voyage

> *Explore the infinite complexity of fractal geometry — right in your terminal and browser.*

A zero-dependency Python tool and interactive HTML explorer for **Mandelbrot**, **Julia**, **Burning Ship**, **Tricorn**, and **Multibrot** fractals.

---

## ✨ Features

| Feature | Details |
|---|---|
| **5 fractal types** | Mandelbrot, Julia sets, Burning Ship, Tricorn, Multibrot³ |
| **Terminal renderer** | 24-bit ANSI true-color output, auto-sized to your terminal |
| **8 color palettes** | Classic, Fire, Electric, Ocean, Neon, Matrix, Sunset, Ice |
| **8 built-in landmarks** | Famous zoom destinations pre-loaded |
| **Interactive HTML explorer** | Pan, zoom, all fractals — runs offline in any browser |
| **Zero dependencies** | Pure Python 3.8+ stdlib only |
| **Save PNG** | Export any view directly from the browser |

---

## 🚀 Quick Start

```bash
# Clone and enter the project
cd mandelbrot_voyage

# Render the Mandelbrot set in your terminal
python voyage.py

# Try a different fractal and palette
python voyage.py render --fractal julia --palette fire

# Zoom into Seahorse Valley
python voyage.py render --landmark "Seahorse Valley"

# Generate the interactive HTML explorer
python voyage.py html

# Open mandelbrot_voyage.html in your browser — no server needed!
```

---

## 📸 Terminal Output (ASCII Art)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌀  Mandelbrot Voyage  ◆  Mandelbrot Set  —  Full View
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ░░░░░░░░░░▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓███████████████████████▓▓▓▓▒▒▒░░░░░░░░░
  ░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓███████████████████████████▓▓▒▒▒░░░░░░░
  ░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓████████████████████████████████████▓▒▒░░░░░
  ░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓████████████████████████████████████████▓▒▒░░░
  ▒▒▒▒▒▓▓▓▓▓▓████████████████████████████████████████████████▒▒▒
  ▒▒▓▓▓▓▓▓▓██████████████████████████████████████████████████▓▓▒
  ▒▒▓▓▓▓▓▓▓██████████████████████████████████████████████████▓▓▒
  ▒▒▒▒▒▓▓▓▓▓▓████████████████████████████████████████████████▒▒▒
  ░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓████████████████████████████████████████▓▒▒░░░
  ░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓████████████████████████████████████▓▒▒░░░░░
  ░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓███████████████████████████▓▓▒▒▒░░░░░░░

  Center: -0.500000 +0.000000i   Zoom: 0.75×   Max iter: 100   Palette: classic

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

*In a true-color terminal, each character block is filled with a precisely computed 24-bit RGB color.*

---

## 🗺️ Built-in Landmarks

Zoom into famous locations in the Mandelbrot set with a single flag:

```bash
python voyage.py landmarks   # list all available
python voyage.py render --landmark "Seahorse Valley"
python voyage.py render --landmark "Dragon Spiral"
python voyage.py render --landmark "Deep Zoom"
```

| Landmark | Coordinates | Zoom |
|---|---|---|
| **Full View** | −0.5 + 0i | 0.75× |
| **Seahorse Valley** | −0.74529 + 0.11307i | 320× |
| **Elephant Valley** | 0.3010 + 0i | 14× |
| **Dragon Spiral** | −0.72689 + 0.18857i | 800× |
| **Mini-Brot** | −1.7499 + 0i | 250× |
| **Triple Spiral** | −0.088 + 0.654i | 45× |
| **Antenna** | −1.25506 + 0.38050i | 100× |
| **Deep Zoom** | −0.77568 + 0.13647i | 50,000× |

---

## 🎨 Color Palettes

| Palette | Description |
|---|---|
| `classic` | Deep blues fading through teal to white and gold |
| `fire` | Black → dark red → orange → incandescent white |
| `electric` | Deep purple → vivid cyan → white |
| `ocean` | Ink black → deep sea blue → aquamarine |
| `neon` | Black → magenta → yellow → white |
| `matrix` | Black → terminal green → bright lime |
| `sunset` | Midnight blue → crimson → orange → golden |
| `ice` | Void black → glacial blue → pure white |

```bash
# Try all palettes
python voyage.py gallery

# Specific palette
python voyage.py render --palette neon
```

---

## 🔬 Fractal Types

### Mandelbrot Set

The classic: `z_{n+1} = z_n² + c`, starting at `z = 0`. The boundary between escaping and bounded orbits reveals infinite complexity.

```bash
python voyage.py render --fractal mandelbrot
```

### Julia Sets

A Julia set uses the same formula but fixes `c` and varies the starting point `z`. Each complex value of `c` produces a distinct connected (or Cantor dust) pattern.

```bash
# Dragon wing Julia set
python voyage.py render --fractal julia --jre -0.7269 --jim 0.1889

# Douady rabbit
python voyage.py render --fractal julia --jre -0.123 --jim 0.745

# Siegel disk
python voyage.py render --fractal julia --jre -0.391 --jim -0.587
```

### Burning Ship

`z_{n+1} = (|Re(z)| + i|Im(z)|)² + c` — taking absolute values before squaring creates a discontinuity that produces flame-like tendrils and a ship silhouette.

```bash
python voyage.py render --fractal burning_ship --palette fire
```

### Tricorn (Mandelbar)

Uses complex conjugation: `z_{n+1} = conj(z)² + c`. The result has three-fold symmetry and a distinctly different character from the Mandelbrot set.

```bash
python voyage.py render --fractal tricorn --palette ice
```

### Multibrot³

Higher-power iteration: `z_{n+1} = z_n³ + c`. The degree-3 Multibrot exhibits three-fold rotational symmetry and contains three main bulbs.

```bash
python voyage.py render --fractal multibrot --palette electric
```

---

## 🌐 Interactive HTML Explorer

Generate a standalone HTML file that works completely offline:

```bash
python voyage.py html
# Opens mandelbrot_voyage.html in any modern browser
```

### Browser Controls

| Action | Effect |
|---|---|
| **Scroll wheel** | Zoom in / out at cursor |
| **Double-click** | Zoom in 2.5× at that point |
| **Click & drag** | Pan the view |
| **`R`** | Reset to full Mandelbrot view |
| **`H`** | Toggle keyboard shortcut help |
| **`P`** | Cycle through color palettes |
| **`F`** | Cycle through fractal types |
| **`↑` / `↓`** | Increase / decrease max iterations |
| **`+` / `−`** | Zoom in / out at center |
| **`S`** | Save current view as PNG |

### Explorer Features

- **Chunked rendering** — the canvas updates row-by-row so you see results immediately
- **Supersampling (1×–3×)** — anti-aliasing for higher quality exports
- **Julia parameter sliders** — drag Re(c) and Im(c) to morph the Julia set live
- **Landmark presets** — one-click jumps to all 8 famous locations
- **Coordinate display** — real and imaginary parts shown at the cursor in real time
- **PNG export** — saves at full canvas resolution

---

## 📐 The Math

### Smooth Coloring

Mandelbrot Voyage uses the **smooth escape-time algorithm** to eliminate banding artifacts. Instead of coloring by raw iteration count, it uses the fractional escape value:

```
ν = i + 1 - log(log(|z|) / log(2)) / log(2)
```

This works because at bailout, `|z| > R`, and the correction `ν` accounts for the "partial" last iteration. Colors are interpolated smoothly across palette stops using this continuous value.

### Bailout Radius

The tool uses `R = 16` (i.e., `|z|² > 256`) rather than the minimum `R = 2`. A larger bailout radius significantly improves smooth coloring accuracy, as the log correction works best when `z` has traveled far from the set boundary.

### Coordinate System

The complex plane is parameterized as:

```
Re(c) ∈ [cx − (2/zoom) × aspect, cx + (2/zoom) × aspect]
Im(c) ∈ [cy − (2/zoom), cy + (2/zoom)]
```

where `aspect = width / height` corrects for terminal character proportions.

---

## 🗂️ Project Structure

```
mandelbrot_voyage/
├── voyage.py                  # CLI entry point
├── mandelbrot_voyage.html     # Generated interactive explorer
├── requirements.txt           # (empty — no dependencies!)
└── src/
    ├── __init__.py
    ├── fractals.py            # Mathematical core: mandelbrot, julia, etc.
    ├── palettes.py            # Color palettes and ANSI color utilities
    ├── renderer.py            # Terminal ASCII/ANSI renderer
    └── html_export.py         # Self-contained HTML generator
```

---

## 💡 Why Fractals?

The Mandelbrot set is defined by a simple rule — **iterate `z → z² + c` and check if the sequence escapes** — yet produces infinite self-similar complexity at every scale. This is a striking demonstration that:

1. **Simple rules can generate boundless complexity** — relevant to everything from coastline lengths to stock markets.
2. **The boundary is infinitely detailed** — you can zoom forever and always find new structures.
3. **Self-similarity** — mini-Mandelbrots appear deep within the set, connected to the main body by filaments.
4. **Phase transitions** — the boundary between bounded and unbounded orbits is a set of measure zero but fractal dimension ≈ 2.

---

## ⚡ Performance Notes

- The Python terminal renderer computes each pixel sequentially — expect a few seconds for large terminals.
- The HTML explorer renders in chunks using `requestAnimationFrame`, so the UI stays responsive and you see partial results immediately.
- For very deep zooms (> 10⁸×), standard 64-bit floats lose precision. This is expected behavior called **glitching**.

---

## 📄 License

MIT — do whatever you want with it.

---

*Built with Python 3 and a love for beautiful mathematics.*
*No pip install required. Open source. Forever free.*
