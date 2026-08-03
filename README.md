# Clauder

Claude Bot — a collection of projects built by Claude.

## Projects

### 🌀 [Mandelbrot Voyage](./mandelbrot_voyage/)

A zero-dependency interactive fractal explorer with terminal and browser modes.

- 5 fractal types: Mandelbrot, Julia, Burning Ship, Tricorn, Multibrot³
- 8 color palettes with smooth 24-bit ANSI terminal output
- Self-contained HTML interactive explorer (pan, zoom, export PNG)
- 8 famous pre-loaded landmark locations
- Pure Python 3 stdlib — no pip install required

```bash
cd mandelbrot_voyage
python voyage.py                           # render in terminal
python voyage.py render --palette fire     # different palette
python voyage.py render --landmark "Seahorse Valley"
python voyage.py html                      # generate browser explorer
```
