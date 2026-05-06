# CelluVerse

```
   ██████╗███████╗██╗     ██╗     ██╗   ██╗██╗   ██╗███████╗██████╗ ███████╗███████╗
  ██╔════╝██╔════╝██║     ██║     ██║   ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝
  ██║     █████╗  ██║     ██║     ██║   ██║██║   ██║█████╗  ██████╔╝███████╗█████╗
  ██║     ██╔══╝  ██║     ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝
  ╚██████╗███████╗███████╗███████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████║███████╗
   ╚═════╝╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
         M u l t i - R u l e   C e l l u l a r   A u t o m a t a   P l a y g r o u n d
```

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Rich](https://img.shields.io/badge/TUI-Rich-purple)
![NumPy](https://img.shields.io/badge/engine-NumPy-orange?logo=numpy)
![Pillow](https://img.shields.io/badge/export-Pillow-yellow)

> **How does breathtaking complexity arise from a handful of simple rules?**  
> CelluVerse lets you watch it happen — live, in colour, in your terminal.

---

## What Is a Cellular Automaton?

A **cellular automaton (CA)** is a grid of cells, each in one of a small number of states. At every time step, every cell looks at its neighbours and updates itself according to a fixed rule. That's it. No central controller, no global plan.

Yet from those trivial rules, CAs produce:
- **Self-organizing structures** — still lifes, oscillators, spaceships
- **Unbounded growth** — guns that fire infinite streams of gliders
- **Turing completeness** — programs that can compute anything a computer can
- **Universal constructors** — patterns that can build copies of themselves
- **Emergent "highways"** — Langton's Ant, given 10 000 steps, spontaneously paves a perfect diagonal road

CelluVerse brings seven distinct rule engines together in one terminal playground.

---

## Features

| Feature | Details |
|---|---|
| 7 Rule Engines | Life, HighLife, Seeds, Day & Night, Maze, Brian's Brain, Langton's Ant |
| 25+ Patterns | Still lifes, oscillators, spaceships, methuselahs, guns |
| Live Terminal UI | Full-colour animation via `rich`, auto-scaled to your terminal |
| 7 Colour Schemes | matrix · ocean · fire · ghost · aurora · gold · mono |
| Stats Panel | Live population, density, Δ pop, stable/oscillating detection |
| GIF Export | Save any simulation as an animated GIF |
| PNG Export | Snapshot any generation to a PNG image |
| Demo Mode | Self-running tour through all major rules |
| Pattern Viewer | Render any pattern as ASCII art directly in the terminal |

---

## Showcase

### Conway's Game of Life — Gosper Glider Gun

```
· · · · · · · · · · · · · · · · · · · · · · · · █ · · · · · · · · · · ·
· · · · · · · · · · · · · · · · · · · · · · █ · █ · · · · · · · · · · ·
· · · · · · · · · · · · █ █ · · · · · · █ █ · · · · · · · · · · · · █ █
· · · · · · · · · · · █ · · · █ · · · · █ █ · · · · · · · · · · · · █ █
█ █ · · · · · · · · █ · · · · · █ · · · █ █ · · · · · · · · · · · · · ·
█ █ · · · · · · · · █ · · · █ · █ █ · · · · █ · █ · · · · · · · · · · ·
· · · · · · · · · · █ · · · · · █ · · · · · · · █ · · · · · · · · · · ·
· · · · · · · · · · · █ · · · █ · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · · · █ █ · · · · · · · · · · · · · · · · · · · · · ·
```
*First ever pattern with unbounded growth — discovered by Bill Gosper in 1970.*

---

### Brian's Brain — Electron Signals

```
  ░░  ░░    ██  ░░    ██    ░░  ██    ░░  ██    ░░  ██
██    ██  ░░    ██  ░░    ██    ░░  ██    ░░  ██    ░░
  ░░  ░░    ██  ░░    ██    ░░  ██    ░░  ██    ░░  ██
██    ██  ░░    ██  ░░    ██    ░░  ██    ░░  ██    ░░
```
*Three states: firing (white) → refractory (cyan) → dead (dark). Produces glider-like electron pulses.*

---

### Langton's Ant — The Spontaneous Highway

```
Generation 200:              Generation 10 000:
  ▓ ▓ ░ ▓ ░ ░ ▓ ▓          · · · · · ▓ ▓ · · · ·
  ░ ▓ ▓ ░ ▓ ▓ ░ ▓          · · · ▓ ▓ ░ ░ ▓ · · ·
  ▓ ░ ▓ ▓ ░ ▓ ▓ ░   →→→   · · ▓ ░ ░ ░ ░ ░ ▓ · ·   →→→  perfect diagonal highway
  ▓ ▓ ░ ▓ ▓ ░ ░ ▓          · ▓ ░ ░ ░ ░ ░ ░ ░ ▓ ·
  ░ ░ ▓ ░ ░ ▓ ░ ░          ▓ ░ ░ ░ ░ ░ ░ ░ ░ ░ ▓
   [chaotic phase]           [pre-highway phase]     [highway phase]
```

---

### Maze Rule (B3/S12345)

```
█ █ █ █ █ █ █ █ █ █ █ · · · █ █ █ █ █ █ █ · · · █ █ █ █ █ █
█ · · · · · · · · · █ · · · █ · · · · · █ · · · █ · · · · █
█ · █ █ █ █ █ · █ · █ · · · █ · █ █ █ · █ · · · █ · █ █ · █
█ · █ · · · █ · █ · · · · · · · █ · █ · █ · · · · · █ · █ ·
█ · █ · █ · █ · █ · █ · · · █ · █ · █ · · · · · █ · · · █ ·
█ · · · · · · · · · █ · · · █ · · · · · █ · · · █ · · · · █
█ █ █ █ █ █ █ █ █ █ █ · · · █ █ █ █ █ █ █ · · · █ █ █ █ █ █
```
*B3/S12345 carves perfect maze-like corridors from random noise.*

---

## Patterns Included

### Still Lifes  *(stable forever)*
| Name | Shape | Cells |
|------|-------|-------|
| `block` | `██`<br>`██` | 4 |
| `beehive` | `·██·`<br>`█··█`<br>`·██·` | 6 |
| `loaf` | 4 cells tall, asymmetric | 7 |
| `boat` | 3×3 diagonal | 5 |
| `tub` | diamond | 4 |

### Oscillators  *(periodic)*
| Name | Period | Notable Feature |
|------|--------|-----------------|
| `blinker` | 2 | Simplest oscillator — just 3 cells |
| `toad` | 2 | Two rows of 3 |
| `beacon` | 2 | Two touching blocks |
| `pulsar` | 3 | Most common period-3 oscillator |
| `pentadecathlon` | 15 | Longest period among common oscillators |

### Spaceships  *(translate across the grid)*
| Name | Speed | Direction |
|------|-------|-----------|
| `glider` | c/4 | Diagonal |
| `lwss` | c/2 | Horizontal |
| `mwss` | c/2 | Horizontal |

### Methuselahs  *(small patterns with dramatic long lives)*
| Name | Lifespan | Notes |
|------|----------|-------|
| `r_pentomino` | 1 103 gens | Famous long-liver, produces gliders |
| `diehard` | 130 gens | Completely disappears |
| `acorn` | 5 206 gens | From 7 cells to thousands |
| `pi_heptomino` | ~173 gens | Pi-shaped starter |

### Guns  *(emit infinite glider streams)*
| Name | Period | Discovery |
|------|--------|-----------|
| `gosper_gun` | 30 | Bill Gosper, 1970 — first known infinite growth |

---

## Rules Reference

### Conway's Game of Life (B3/S23)
```
Born  if exactly 3 live neighbours
Survives if 2 or 3 live neighbours
```
The most studied CA ever created. Proven Turing-complete.

### HighLife (B36/S23)
```
Born  if 3 or 6 live neighbours
Survives if 2 or 3 live neighbours
```
One extra birth condition enables self-replicating patterns — gliders that copy themselves.

### Seeds (B2/S)
```
Born  if exactly 2 live neighbours
Never survives
```
Every cell dies on the next step. Explosive growth that eventually extinguishes.

### Day & Night (B3678/S34678)
```
Born  if 3, 6, 7, or 8 live neighbours
Survives if 3, 4, 6, 7, or 8 live neighbours
```
Dead and alive are perfectly symmetric — an inverted grid evolves identically.

### Maze (B3/S12345)
```
Born  if exactly 3 live neighbours
Survives if 1, 2, 3, 4, or 5 live neighbours
```
Living cells almost never die, carving twisting corridors through dead space.

### Brian's Brain  *(3-state)*
```
dead (0) → firing (1)  if exactly 2 firing neighbours
firing (1) → refractory (2)  always
refractory (2) → dead (0)  always
```
The refractory period prevents double-firing — producing persistent, glider-like electron signals.

### Langton's Ant
```
On a white cell: turn right, flip colour, step forward
On a black cell: turn left,  flip colour, step forward
```
Simple enough to describe in one sentence. Turing-complete. After ~10 000 steps, every ant spontaneously builds an infinite diagonal highway — with no instruction to do so.

---

## Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements.txt
```

**Requirements:** Python 3.11+, pip

---

## Quick Start

```bash
# Classic Conway's Life with a random board
python main.py run

# Watch the Gosper Glider Gun fire forever
python main.py run --rule life --pattern gosper_gun --width 80 --height 40

# Brian's Brain with the ocean colour scheme
python main.py run --rule brain --scheme ocean --density 0.45

# Three ants competing on the same grid
python main.py run --rule ant --ants 3 --width 80 --height 40

# Maze rule grows stunning labyrinths
python main.py run --rule maze --scheme gold --density 0.35

# Self-running demo cycling all rules
python main.py demo

# List every built-in rule
python main.py list-rules

# List every built-in pattern
python main.py list-patterns

# Preview a pattern in ASCII
python main.py show pulsar
python main.py show gosper_gun
```

---

## Exporting

```bash
# Save an animated GIF (80 frames at 12 fps)
python main.py run --rule life --pattern acorn \
    --width 100 --height 60 \
    --export acorn_evolution.gif \
    --export-frames 120

# Save the final state as a high-resolution PNG
python main.py run --rule maze --density 0.4 --generations 200 \
    --export-png maze_final.png

# Combine both
python main.py run --rule brain --density 0.4 \
    --export brain.gif --export-frames 60 \
    --export-png brain_snapshot.png
```

---

## CLI Reference

```
Usage: python main.py [COMMAND] [OPTIONS]

Commands:
  run             Run a live simulation
  demo            Automatic tour through all rules
  list-rules      Show all rule engines
  list-patterns   Show the pattern library
  show NAME       ASCII preview of a pattern

Run Options:
  -r, --rule        life|highlife|seeds|day_and_night|maze|brain|ant
  -p, --pattern     Pattern name or 'random'
  -W, --width       Grid width  [default: 70]
  -H, --height      Grid height [default: 35]
  -d, --density     Random cell density 0–1  [default: 0.30]
  -g, --generations Max generations (0 = unlimited)
  -s, --speed       Seconds between frames  [default: 0.07]
  -c, --scheme      matrix|ocean|fire|ghost|aurora|gold|mono
      --ants        Number of ants (ant rule only)  [default: 1]
      --seed        Random seed for reproducibility
  -e, --export      Save animated GIF to path
      --export-frames  GIF frame count  [default: 80]
      --export-png  Save final state as PNG
```

---

## Architecture

```
celluverse/
│
├── celluverse/              ← Core package
│   ├── __init__.py          ← Version info
│   ├── grid.py              ← Grid: state container, step engine, stability detection
│   ├── rules.py             ← Pure functions: cells(t) → cells(t+1)
│   ├── langton.py           ← LangtonsAnt: stateful ant simulation (same Grid interface)
│   ├── patterns.py          ← Pattern library: 25+ named numpy arrays with metadata
│   ├── renderer.py          ← Rich terminal rendering: grid text, stats panel, layout
│   └── exporter.py          ← Pillow GIF/PNG export
│
├── main.py                  ← Click CLI: run · demo · list-rules · list-patterns · show
└── requirements.txt
```

### Data Flow

```
                  ┌─────────────┐
  User Input ───► │  main.py    │
                  │  Click CLI  │
                  └──────┬──────┘
                         │  creates
              ┌──────────▼──────────┐
              │  Grid / LangtonsAnt │  ← state container
              │  (grid.py/langton.py│
              └──────────┬──────────┘
                         │  .step(rule_fn)
              ┌──────────▼──────────┐
              │    rules.py         │  ← pure NumPy functions
              │  cells(t) → cells(t+1)
              └──────────┬──────────┘
                    ┌────┴────┐
                    │         │
         ┌──────────▼──┐  ┌───▼──────────┐
         │ renderer.py │  │ exporter.py  │
         │ Rich TUI    │  │ GIF / PNG    │
         └─────────────┘  └──────────────┘
```

---

## Scientific Context

Cellular automata were invented by John von Neumann and Stanislaw Ulam in the 1940s to study self-replication. Conway's Life (1970) made them famous. Stephen Wolfram's *A New Kind of Science* (2002) argued CAs may underlie physical reality.

Key theorems proven using Life:
- **Turing completeness** (Berlekamp, Conway, Guy — 1982)  
- **Universal construction** (patterns that build arbitrary other patterns)
- **Undecidability** of whether a given pattern ever stabilises

Langton's Ant was shown to be Turing-complete in 2000 (Gajardo, Moreira, Goles).

---

## Colour Schemes

| Scheme | Dead | Alive | Best For |
|--------|------|-------|----------|
| `matrix` | black | bright green | Life, Maze |
| `ocean` | black | bright cyan | Brian's Brain |
| `fire` | black | red/orange | Seeds, Ant |
| `ghost` | black | white | Day & Night |
| `aurora` | black | magenta | HighLife |
| `gold` | black | yellow/gold | Maze, Ant |
| `mono` | black | white | High contrast |

---

## Interesting Experiments

```bash
# Watch chaos resolve into perfect order (acorn takes 5206 generations)
python main.py run --rule life --pattern acorn --width 120 --height 60 \
    --speed 0.01 --generations 6000

# Two ants interfere chaotically — rare to settle into a highway
python main.py run --rule ant --ants 2 --seed 17

# Seeds: explosive then total extinction — blink and miss it
python main.py run --rule seeds --density 0.1 --speed 0.02

# Day & Night: inverted start, identical evolution
python main.py run --rule day_and_night --density 0.5 --scheme ghost

# Same seed, different rules — observe how rules shape destiny
python main.py run --rule life --seed 42
python main.py run --rule maze --seed 42
python main.py run --rule highlife --seed 42
```

---

## License

MIT — do whatever you want with it.

---

*Built with Python 3.11 · NumPy · Rich · Pillow · Click*
