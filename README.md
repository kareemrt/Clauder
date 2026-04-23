```
  ███████╗██╗   ██╗ ██████╗     ██╗     ██╗███████╗███████╗
  ██╔════╝██║   ██║██╔═══██╗    ██║     ██║██╔════╝██╔════╝
  █████╗  ██║   ██║██║   ██║    ██║     ██║█████╗  █████╗
  ██╔══╝  ╚██╗ ██╔╝██║   ██║    ██║     ██║██╔══╝  ██╔══╝
  ███████╗ ╚████╔╝ ╚██████╔╝    ███████╗██║██║     ███████╗
  ╚══════╝  ╚═══╝   ╚═════╝     ╚══════╝╚═╝╚═╝     ╚══════╝
```
> **Conway's Game of Life × Genetic Evolution Simulator**
> *"Life finds a way."*

---

## What Is EvoLife?

**EvoLife** is a terminal-native simulation engine that fuses two of the most fascinating ideas in computer science:

1. **Conway's Game of Life** — The legendary cellular automaton where four simple rules generate infinite complexity.
2. **Genetic Algorithms** — Darwinian selection applied to the *initial seed patterns*, evolving them toward emergent goals.

Every generation of the genetic algorithm is a competition: dozens of initial patterns are simulated in parallel Game of Life universes. The ones that survive longest, grow largest, or oscillate most stably are selected to reproduce. Their "DNA" (the initial cell arrangement) undergoes crossover and mutation. After enough generations, *something beautiful emerges*.

---

## Features

```
┌─────────────────────────────────────────────────────────────┐
│                     EVOLIFE FEATURES                        │
├─────────────────────────────────────────────────────────────┤
│  🧬  Genetic Algorithm        Tournament selection +        │
│      Evolution Engine         uniform crossover + bit-flip  │
│                               mutation                      │
├─────────────────────────────────────────────────────────────┤
│  🔬  Conway's Game of Life    Wrap-around infinite grid,    │
│      Simulator                efficient NumPy convolution   │
├─────────────────────────────────────────────────────────────┤
│  🎯  4 Fitness Goals          lifespan / population /       │
│                               balanced / oscillator         │
├─────────────────────────────────────────────────────────────┤
│  🎨  5 Color Themes           matrix / ocean / fire /       │
│                               mono / plasma                 │
├─────────────────────────────────────────────────────────────┤
│  📚  Pattern Library          10 classic GoL patterns       │
│                               (glider, pulsar, acorn, ...)  │
├─────────────────────────────────────────────────────────────┤
│  📊  Live ASCII Charts        Real-time evolution progress  │
│                               bar charts in terminal        │
├─────────────────────────────────────────────────────────────┤
│  🐍  Pure Python              Only NumPy + SciPy required   │
└─────────────────────────────────────────────────────────────┘
```

---

## How It Looks

### Game of Life Simulation (Matrix Theme)
```
╔────────────────────────────────────────────────────────────╗
║  ██        ██  ██          ██  ██  ██          ██          ║
║        ██          ██  ██  ██      ██  ██  ██          ██  ║
║  ██  ██  ██    ██          ██  ██          ██  ██  ██      ║
║      ██  ██  ██  ██  ██          ██  ██  ██  ██            ║
║  ██      ██      ██          ██  ██      ██  ██  ██  ██    ║
║      ██          ██  ██  ██      ██          ██  ██        ║
╚────────────────────────────────────────────────────────────╝
  Gen:   47  Pop:   134  Born: +23    Died: -18   Fitness:  89.0
```

### Evolution Progress Chart
```
Best Fitness over Generations
  200.0 │▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  175.0 │          ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  150.0 │    ▄▄▄▄▄▄
  125.0 │  ▄▄
  100.0 │▄▄
   75.0 │
   50.0 │
   25.0 │
         └──────────────────────────────────────────────────
         Gen 1                                        Gen 20
```

### Best Evolved Genome
```
  Best Genome (Gen 15)
  █·█·██·█
  ████····
  ··█·█·██
  ██···███
  ███·█···
  █·███·██
  ···█··██
  ·█████·█
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt
```

**Requirements:**
- Python 3.9+
- NumPy ≥ 1.24
- SciPy ≥ 1.10

---

## Usage

### 1. Watch a Classic Pattern

```bash
python main.py simulate --pattern glider
python main.py simulate --pattern pulsar --theme ocean
python main.py simulate --pattern acorn  --steps 500 --delay 0.05
```

### 2. Run the Genetic Evolution

```bash
# Evolve patterns for maximum lifespan (default: 20 generations, 30 individuals)
python main.py evolve

# Evolve for maximum population with custom settings
python main.py evolve --goal population --generations 50 --population 40

# Replay the winning genome after evolution finishes
python main.py evolve --goal balanced --replay

# Evolve oscillating patterns
python main.py evolve --goal oscillator --genome-size 12
```

### 3. Quick Demo

```bash
python main.py demo
```

### 4. List Built-in Patterns

```bash
python main.py patterns
```

### 5. Programmatic API

```python
from evolife.evolution import GeneticEvolver, FitnessGoal

evolver = GeneticEvolver(
    population_size=30,
    genome_size=10,
    fitness_fn=FitnessGoal.maximize_lifespan,
    rng_seed=42,
)
evolver.initialize()
evolver.evolve(generations=20)

best = evolver.best()
print(f"Best lifespan: {best.lifespan} | Fitness: {best.fitness:.2f}")
```

---

## Architecture

```
evolife/
├── __init__.py           Version info
│
├── grid.py               Conway's Game of Life engine
│   ├── Grid              The simulation grid (NumPy-backed)
│   ├── Grid.seed()       Place a pattern on the grid
│   ├── Grid.step()       Advance one generation (SciPy convolution)
│   ├── Grid.is_extinct() Population == 0
│   └── Grid.is_stable()  Population unchanged for N generations
│
├── patterns.py           Built-in pattern library
│   ├── LIBRARY           Dict of classic GoL patterns (NumPy arrays)
│   ├── get_pattern()     Retrieve a named pattern
│   └── random_genome()   Generate a random NxN binary genome
│
├── evolution.py          Genetic algorithm engine
│   ├── Individual        Genome + fitness + lifespan + max_pop
│   ├── FitnessGoal       Static fitness functions (4 presets)
│   └── GeneticEvolver    Full GA: init → evaluate → select → reproduce
│       ├── initialize()  Create random initial population
│       ├── evolve()      Run N generations (with optional callback)
│       ├── best()        Return best individual ever evaluated
│       └── stats()       Generation statistics dict
│
├── renderer.py           ANSI terminal rendering
│   ├── Color             ANSI escape code constants
│   ├── THEMES            Color theme presets (5 themes)
│   └── Renderer          Renders grid, stats bar, fitness chart, logo
│
└── stats.py              Statistics tracking & reporting
    ├── SimulationRecord  Single simulation snapshot
    └── StatsTracker      Aggregate stats across simulations

main.py                   CLI entry point (argparse)
examples/demo.py          Programmatic usage examples
```

---

## The Genetic Algorithm — How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVOLUTIONARY CYCLE                           │
│                                                                 │
│   ┌──────────────┐                                              │
│   │   INITIALIZE │  ← N random 10×10 binary patterns           │
│   └──────┬───────┘                                              │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     Simulate each genome in GoL             │
│   │   EVALUATE   │  ← Measure lifespan, max population         │
│   └──────┬───────┘     Apply fitness function                   │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     Tournament selection (k=3)              │
│   │    SELECT    │  ← Better fitness = higher chance           │
│   └──────┬───────┘     of becoming a parent                    │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     Uniform crossover (per-cell mask)       │
│   │  CROSSOVER   │  ← Two parents → two children               │
│   └──────┬───────┘     Rate: 70%                               │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     Randomly flip individual bits           │
│   │    MUTATE    │  ← Rate: 5% per cell                        │
│   └──────┬───────┘     Prevents premature convergence          │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     Top 3 individuals survive               │
│   │    ELITISM   │  ← unchanged into next generation           │
│   └──────┬───────┘                                              │
│          │                                                      │
│          └──────────────────────────► REPEAT                   │
└─────────────────────────────────────────────────────────────────┘
```

### Fitness Goals

| Goal | Description | Fitness Formula |
|------|-------------|-----------------|
| `lifespan` | Survive as long as possible | `lifespan` (generations before extinction/stability) |
| `population` | Grow as large as possible | `max_population` (peak cell count) |
| `balanced` | Balance survival and growth | `0.5 * lifespan + 0.5 * max_pop` |
| `oscillator` | Find stable periodic patterns | `max_pop / (1 + \|lifespan - 50\|)` |

---

## Conway's Rules

The four immortal rules applied every generation:

```
   ┌─────────────────────────────────────────────────────┐
   │  GAME OF LIFE RULES                                 │
   │                                                     │
   │  For a LIVE cell:                                   │
   │    < 2 neighbors  →  dies  (underpopulation)        │
   │    2-3 neighbors  →  lives (survival)               │
   │    > 3 neighbors  →  dies  (overpopulation)         │
   │                                                     │
   │  For a DEAD cell:                                   │
   │    = 3 neighbors  →  born  (reproduction)           │
   │                                                     │
   │  All cells update simultaneously each generation.   │
   └─────────────────────────────────────────────────────┘
```

---

## Built-in Pattern Library

| Pattern | Size | Lives | Description |
|---------|------|-------|-------------|
| `glider` | 3×3 | 5 | The iconic traveling spaceship |
| `lwss` | 4×5 | 9 | Lightweight spaceship |
| `pulsar` | 13×13 | 48 | Period-3 oscillator |
| `blinker` | 1×3 | 3 | Simplest oscillator |
| `toad` | 2×4 | 6 | Period-2 oscillator |
| `beacon` | 4×4 | 8 | Period-2 oscillator |
| `r_pentomino` | 3×3 | 5 | Long-lived chaotic growth |
| `acorn` | 3×7 | 7 | Evolves for 5206 generations! |
| `diehard` | 3×8 | 7 | Disappears after 130 generations |
| `random_5x5` | 5×5 | ~12 | Randomly generated each run |

---

## CLI Reference

```
python main.py simulate [OPTIONS]
  --pattern  PATTERN     Seed pattern name         [glider]
  --steps    INT         Max simulation steps       [300]
  --delay    FLOAT       Seconds between frames     [0.08]
  --width    INT         Grid width in cells        [50]
  --height   INT         Grid height in cells       [25]
  --theme    THEME       Color theme                [matrix]
  --glyph    GLYPH       Cell glyph style           [block]

python main.py evolve [OPTIONS]
  --generations  INT     Number of evo generations  [20]
  --population   INT     Individuals per generation [30]
  --genome-size  INT     Genome grid NxN            [10]
  --goal         GOAL    Fitness objective           [balanced]
  --sim-steps    INT     Max GoL steps per eval      [200]
  --mutation-rate FLOAT  Bit-flip probability        [0.05]
  --seed         INT     Random seed for repro.      [None]
  --replay               Replay best genome in GoL
  --theme        THEME   Color theme                 [matrix]

Themes:  matrix | ocean | fire | mono | plasma
Goals:   lifespan | population | balanced | oscillator
Glyphs:  block | dot | square | ascii
```

---

## Example Run

```bash
$ python main.py evolve --goal lifespan --generations 30 --population 50 --replay
```

Output (abbreviated):
```
  Evolving 50 genomes over 30 generations...
  Goal: lifespan | Genome size: 10x10

  Best Genome (Gen 1)
  ·█·█·██·█·
  ████···█··
  ··█·█·████
  ██···████·
  ███·█·····
  ...

  Gen:    0  Pop:   208  Born: +0     Died: -0    EvoGen:   1  Fitness:  150.0  Lifespan:  150

  Evolution Progress (Best Fitness)
  150.0 │▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  ...
```

---

## Project Philosophy

EvoLife explores one of the deepest questions in science: **can complexity arise from simplicity?**

Conway's Game of Life proves it can — four rules create gliders, spaceships, logic gates, and even Turing-complete computers. The genetic algorithm asks a harder question: *can we find the seeds of the most interesting complexity?*

The answer, every time, is yes.

---

## License

MIT — do whatever you want. Life finds a way.
