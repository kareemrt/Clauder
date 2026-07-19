# Game of Life — Evolutionary Pattern Discovery

> Conway's Game of Life, turbocharged with a **genetic algorithm** that breeds
> initial configurations for maximum "interestingness": long lifespan, rich
> state diversity, and sustained populations.

```
  ██████╗ █████╗ ███╗   ███╗███████╗     ██████╗ ███████╗    ██╗     ██╗███████╗███████╗
 ██╔════╝██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██╔════╝    ██║     ██║██╔════╝██╔════╝
 ██║     ███████║██╔████╔██║█████╗      ██║   ██║█████╗      ██║     ██║█████╗  █████╗
 ██║     ██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██╔══╝      ██║     ██║██╔══╝  ██╔══╝
 ╚██████╗██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝██║         ███████╗██║██║     ███████╗
  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝         ╚══════╝╚═╝╚═╝     ╚══════╝
```

---

## What is this?

**Conway's Game of Life** is a zero-player cellular automaton devised by mathematician
John Conway in 1970.  A grid of cells lives, dies, or is born each tick according to
four simple rules:

| Rule | Condition | Result |
|------|-----------|--------|
| Underpopulation | Live cell with < 2 live neighbours | Dies |
| Survival | Live cell with 2–3 live neighbours | Lives |
| Overpopulation | Live cell with > 3 live neighbours | Dies |
| Reproduction | Dead cell with exactly 3 live neighbours | Born |

Despite their simplicity, these rules produce astonishing complexity — spaceships,
oscillators, infinite-growth patterns, and even Turing-complete constructions.

**This project adds a genetic algorithm** on top: it breeds populations of random
starting grids, selects the ones that produce the most interesting simulations, and
crosses & mutates survivors to discover new emergent behaviour automatically.

---

## Project Structure

```
Clauder/
├── life/
│   ├── __init__.py        — package root
│   ├── __main__.py        — python -m life entry point
│   ├── board.py           — Game of Life engine (NumPy-accelerated)
│   ├── patterns.py        — 11 classic patterns with metadata
│   ├── evolution.py       — (μ+λ) genetic algorithm
│   ├── renderer.py        — Rich terminal renderer with age-gradient colouring
│   └── main.py            — CLI commands (demo / evolve / random / pattern / list)
├── requirements.txt
└── README.md
```

---

## Installation

```bash
pip install rich numpy
python -m life --help
```

---

## Usage

### List all built-in patterns
```
python -m life list
```
```
╭────────────────┬──────────────────────────────────────────────────────────╮
│ Name           │ Description                                              │
├────────────────┼──────────────────────────────────────────────────────────┤
│ glider         │ Period-4 spaceship — travels diagonally across the board │
│ blinker        │ Period-2 oscillator — simplest possible oscillator       │
│ pulsar         │ Period-3 oscillator — one of the most common large       │
│ glider_gun     │ Period-30 gun — Gosper's famous infinite-glider factory  │
│ pentadecathlon │ Period-15 oscillator — ten cells in a row with tweaks    │
│ …              │ …                                                        │
╰────────────────┴──────────────────────────────────────────────────────────╯
```

### Watch a curated pattern showcase
```
python -m life demo
```

### Run a specific pattern
```
python -m life pattern glider_gun
python -m life pattern pulsar --gens 200
python -m life pattern lwss --delay 0.1
```

### Run a random soup
```
python -m life random
python -m life random --density 0.45 --seed 42
```

### Run the evolutionary algorithm
```
python -m life evolve
python -m life evolve --pop 40 --evo-gens 25 --eval-gens 300
```

---

## Pattern Gallery

### Glider — the quintessential spaceship
```
 ·█·
 ··█
 ███

     ↓  4 generations later  ↓

 ·█·
 ··█
 ███   (shifted diagonally)
```

### Pulsar — period-3 oscillator
```
   ███   ███
 █    █ █    █
 █    █ █    █
 █    █ █    █
   ███   ███

   ███   ███
 █    █ █    █
 █    █ █    █
 █    █ █    █
   ███   ███
```

### Gosper Glider Gun — infinite glider factory
```
                        █
          ██    ████  █  █            ██
          ██   █    █ █ █             ██
  ██       ·  █      ██    ██ ██
  ██       ·  █      ██    ██ ██  ····
             █    █  ·          ·  ████
             ████   ·
```

### Lightweight Spaceship (LWSS)
```
 ·█··█
 █····
 █···█
 ████·
       →  travels right at c/2
```

---

## The Evolutionary Algorithm

```
┌─────────────────────────────────────────────────────────────┐
│  GENERATION 0                                               │
│  Initialise population of N random grids                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  EVALUATE FITNESS                                           │
│                                                             │
│  For each individual, simulate up to eval_gens steps:       │
│                                                             │
│    fitness = 0.35 × longevity_score                         │
│            + 0.40 × state_diversity_score                   │
│            + 0.25 × population_density_score                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  SELECTION  (μ+λ strategy)                                  │
│  Keep top elite_frac of population as survivors             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  CROSSOVER + MUTATION                                       │
│  Random two-parent bitwise crossover                        │
│  Bit-flip mutation at rate 1.5%                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                 repeat evo_gens times
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  CHAMPION REPLAY                                            │
│  Animate the all-time best individual live in terminal      │
└─────────────────────────────────────────────────────────────┘
```

### Fitness Function

| Component | Weight | What it rewards |
|-----------|--------|-----------------|
| **Longevity** | 35% | Grids that stay alive for many generations |
| **State diversity** | 40% | Unique board states (avoids loops & stagnation) |
| **Density balance** | 25% | Average ~20% cell density (not too sparse, not overcrowded) |

---

## Terminal Rendering

Cells are rendered with `Rich` using a **5-level age gradient**:

| Age (generations alive) | Colour |
|--------------------------|--------|
| 0–4 | `bright_cyan` |
| 5–9 | `bright_green` |
| 10–14 | `bright_yellow` |
| 15–19 | `bright_magenta` |
| 20+ | `bright_blue` |

Long-lived structures like still lifes and oscillators glow with deep colours;
newly born cells flicker bright cyan — giving an immediate visual sense of the
grid's history at a glance.

---

## Why Conway's Game of Life?

| Property | Significance |
|----------|-------------|
| **Turing completeness** | Any computable function can be implemented in Life |
| **Emergence** | Global complexity from purely local rules |
| **Zero parameters** | No tuning — the rules are fixed, yet infinite variety emerges |
| **Visual beauty** | Organic, fractal-like structures arise spontaneously |

The evolutionary layer makes it a **computational creativity** experiment: we
are literally evolving interesting programs, where each genome is an initial
condition for a cellular automaton.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `numpy ≥ 1.24` | Vectorised board stepping (rolling-window neighbour count) |
| `rich ≥ 13.0` | Colour terminal rendering, live updates, tables |

Python 3.11+ required.

---

## Ideas for Extension

- **GIF export** — capture frames with `Pillow` and write animated GIFs
- **Interactive mode** — click cells with mouse support via `textual`
- **Parallel evolution** — multi-process fitness evaluation with `multiprocessing`
- **Pattern database** — auto-detect and classify oscillators by period
- **Hyperparameter sweep** — vary board size, density, and mutation rate to map the fitness landscape
- **Web UI** — port the renderer to a browser canvas via Pyodide

---

*Built by Claude — an experiment in computational creativity.*
