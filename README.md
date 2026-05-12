# 🌿 Terrarium

> *A living ecosystem in your terminal — where predators hunt, prey graze, and plants reclaim the world.*

Terrarium is a terminal-based ecosystem simulator. Plants spread across an ANSI-colored grid, herbivores graze and reproduce, carnivores hunt in packs, and the whole system self-organizes into the classic **Lotka-Volterra predator-prey oscillations** — entirely from local rules, no global coordination.

---

## Preview

```
╔══════════════════════════════════════════════════════════════════════╗
║  TERRARIUM — Living Ecosystem Simulator                              ║
╠══════════════════════════════════════════════════════════════════════╣
║·♣♣♣·♣♣·♣·♣♣♣♣♣·♣♣♣·♣·♣·♣♣♣·♣♣·♣·♣♣♣♣♣·♣♣♣·◉·♣♣·♣·♣♣♣♣·♣·♣♣♣·♣♣♣♣║
║♣♣·♣♣♣♣·♣♣·♣♣♣·♣·♣·♣♣♣·♣·♣♣♣♣·♣·♣♣♣·◉·♣♣·♣♣♣♣·♣♣·♣·♣·♣♣♣·♣♣♣·♣·♣♣║
║♣·♣♣♣·♣♣♣♣♣·♣·♣♣♣·♣·♣♣♣·♣♣♣·◉·♣♣·♣♣·♣·♣·♣♣♣♣·♣♣·♣♣♣·♣·♣♣·♣·♣·♣♣♣║
║·♣♣♣·♣·♣♣·♣♣♣♣·♣♣·♣♣·♣·♣♣♣·♣♣♣·♣♣·◉♣♣·♣·♣♣♣♣♣·♣♣·♣·♣·♣♣♣·♣♣♣·♣·♣║
║♣♣·♣♣♣♣·♣♣·♣·♣♣♣·◉·♣·♣♣·♣♣·◆·♣♣♣·♣♣♣♣·♣·♣♣·♣·♣♣♣·♣♣♣·♣·♣♣♣·♣·♣♣·║
║♣·♣·♣♣·♣♣♣♣·♣·♣♣♣·♣♣♣·♣·◉♣♣♣·♣♣·♣♣·♣·♣·♣♣♣·◉·♣♣·♣♣♣♣·♣·♣·♣·♣♣♣♣║
║♣♣·♣·♣·♣♣♣♣·♣♣·♣·♣♣♣·♣·♣♣·♣♣·♣♣♣·♣·♣♣♣·♣·♣♣♣♣♣·♣·♣♣·◉♣♣·♣♣·♣·♣·♣║
╠══════════════════════════════════════════════════════════════════════╣
║  Tick     347    19.8 fps                                            ║
║  ♣ Plants      893  ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ║
║  ◉ Herbivores   31  ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ║
║  ◆ Carnivores   11  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ║
║  Population history:                                                 ║
║  ♣ ▃▄▅▇▇▆▄▂▁▁▁▂▃▄▆▇▇▆▅▄▃▂▁▁▂▃▄▅▆▇▇▆▅▄▃▂▁▂▃▄▅▇▇▆▄▃▂▁▁▂▃▄▅▆▇▇▆▄▃▂  ║
║  ◉ ▁▁▂▃▅▇▇▆▄▂▁▁▂▃▅▇▇▆▄▂▁▁▂▃▅▇▇▆▄▂▁▁▂▃▄▅▇▇▆▄▂▁▁▂▃▅▇▇▆▄▃▁▁▂▃▄▅▇▇▆▄  ║
║  ◆ ▁▁▁▂▃▄▅▇▇▆▃▂▁▁▁▂▃▄▅▇▇▆▃▂▁▁▁▂▃▄▅▇▇▆▃▂▁▁▁▂▃▄▅▇▇▆▃▂▁▁▁▂▃▄▅▇▇▆▃▂▁  ║
║  [Ctrl+C] exit  [--biome forest|savanna|sparse|archipelago]          ║
╚══════════════════════════════════════════════════════════════════════╝
```

*(Live terminal output uses full ANSI 256-color — green plants, yellow herbivores, red carnivores)*

---

## Features

- **Real emergent dynamics** — Lotka-Volterra predator-prey oscillations arise spontaneously from simple per-entity rules; no global equations, no scripted behavior
- **Four biomes** — Forest, Savanna, Sparse, and Archipelago, each with distinct starting conditions and emergent behaviors
- **Live sparkline history** — Unicode block-character population graphs update in real time
- **Pure stdlib** — zero third-party dependencies; runs anywhere Python 3.9+ is installed
- **Configurable** — world size, tick speed, random seed, biome, plain-ASCII fallback

---

## Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
python main.py          # no pip install required
```

Python **3.9+** is the only requirement. No virtual environment needed.

---

## Usage

```bash
# Default: forest biome, 70×28 world
python main.py

# Savanna — open grassland with active predator-prey cycles
python main.py --biome savanna

# Sparse — minimal seed; watch life bootstrap from almost nothing
python main.py --biome sparse

# Archipelago — island chains; isolated evolving pockets
python main.py --biome archipelago

# Custom world
python main.py --biome forest --width 100 --height 40 --speed 0.02

# Reproducible run
python main.py --biome savanna --seed 42

# Non-interactive (stop after 500 ticks, plain ASCII for logging)
python main.py --ticks 500 --plain
```

### All Options

| Flag | Default | Description |
|------|---------|-------------|
| `--biome` | `forest` | Starting biome (`forest` / `savanna` / `sparse` / `archipelago`) |
| `--width` | `70` | World width in cells |
| `--height` | `28` | World height in cells |
| `--speed` | `0.05` | Seconds between ticks |
| `--seed` | random | Integer seed for reproducibility |
| `--plain` | off | Plain ASCII characters instead of Unicode |
| `--ticks` | ∞ | Stop automatically after N ticks |

---

## The Four Biomes

```
┌─────────────────────┬──────────────────────────────────────────────────┐
│ Biome               │ Description                                      │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 🌲 forest           │ Dense woodland. Abundant plants sustain cycling  │
│                     │ herbivore/carnivore populations indefinitely.    │
│                     │ Best for observing Lotka-Volterra oscillations.  │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 🌾 savanna          │ Open grassland. Sparse cover means prey must     │
│                     │ forage widely. Predator-prey cycles are faster   │
│                     │ and more violent before eventual collapse.       │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 🌱 sparse           │ A single central plant patch. A few herbivores   │
│                     │ bootstrap the food chain. Classic boom-bust:     │
│                     │ overshoot → crash → extinction.                  │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 🏝️ archipelago      │ Water channels divide the world into islands.    │
│                     │ Isolated sub-populations evolve independently,   │
│                     │ producing mosaic dynamics across the grid.       │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

## Entity Reference

### 🌿 Plants  `♣` (green)

Plants are the primary producers. They photosynthesize by spreading clonally to adjacent empty cells. Without constant grazing pressure they will fill the entire world.

| Parameter | Value | Effect |
|-----------|-------|--------|
| `SPREAD_CHANCE` | 12% / tick | Rate of clonal spread to neighbors |
| `DEATH_CHANCE` | 0.2% / tick | Natural senescence |
| `MAX_AGE` | 300 ticks | Maximum lifespan |

### 🐇 Herbivores  `◉` (yellow)

Herbivores eat plants, reproduce when well-fed, and die when energy depletes or old age arrives. They navigate toward visible plant clusters.

| Parameter | Value | Effect |
|-----------|-------|--------|
| `INITIAL_ENERGY` | 30 | Starting energy |
| `EAT_GAIN` | 12 / plant | Energy gained per plant eaten |
| `REPRODUCE_THRESHOLD` | 78 | Energy needed to reproduce (~4 plant-eats) |
| `REPRODUCE_COST` | 38 | Energy transferred to offspring |
| `IDLE_COST` | 0.18 / tick | Energy lost each tick while alive |
| `MAX_AGE` | 200 ticks | Maximum lifespan |
| `VISION` | 4 cells | BFS plant-search radius |

### 🦊 Carnivores  `◆` (red)

Carnivores hunt herbivores by BFS pathfinding. They need multiple kills before they can reproduce and starve quickly when prey is scarce — the built-in brake on predator population booms.

| Parameter | Value | Effect |
|-----------|-------|--------|
| `INITIAL_ENERGY` | 45 | Starting energy |
| `EAT_GAIN` | 15 / herbivore | Energy gained per kill |
| `REPRODUCE_THRESHOLD` | 95 | Energy needed to reproduce (~4 kills) |
| `REPRODUCE_COST` | 52 | Energy transferred to offspring |
| `IDLE_COST` | 0.65 / tick | Fast energy drain when not hunting |
| `MAX_AGE` | 220 ticks | Maximum lifespan |
| `HUNT_RANGE` | 5 cells | BFS hunt-search radius |

---

## Architecture

```
terrarium/                   ← Python package
├── __init__.py
├── entities.py              ← Plant / Herbivore / Carnivore dataclasses
│                               + cell type constants (EMPTY=0 … ROCK=5)
├── world.py                 ← 2-D grid with O(1) type lookup
│                               neighbors8(), find_nearest() BFS, step_toward()
├── simulation.py            ← Per-tick logic for each entity type
│                               snapshot → shuffle → process → write-back
└── renderer.py              ← ANSI 256-color frame builder
                                sparkline history, population bars

biomes.py                    ← World factory functions (forest/savanna/sparse/archipelago)
main.py                      ← CLI entry point (argparse, game loop, terminal control)
requirements.txt             ← Empty — zero external dependencies
```

### How a tick works

```
┌──────────────────────────────────────────────────────┐
│  1. Snapshot: collect (y, x, type, entity) for all  │
│     live cells at the START of the tick              │
│  2. Shuffle: randomise processing order for fairness │
│  3. For each entity in shuffled list:                │
│     a. Skip if entity no longer at (y,x) — was eaten │
│     b. Increment age; pay idle energy cost           │
│     c. Dispatch to _tick_plant / _herb / _carnivore  │
│        • Die?  remove from grid                      │
│        • Eat?  remove food, gain energy, maybe move  │
│        • Reproduce?  place baby on empty neighbour   │
│        • Move?  step toward target or wander         │
└──────────────────────────────────────────────────────┘
```

The `world.grid[y][x] is not entity` identity check on step 3a is the key to correctness: it prevents a "ghost" entity (already eaten this tick) from acting twice.

---

## The Science: Lotka-Volterra Dynamics

The simulation reproduces the classic predator-prey equations discovered independently by Alfred Lotka (1925) and Vito Volterra (1926):

```
dH/dt = αH − βHC        (herbivore growth minus predation)
dC/dt = δHC − γC        (carnivore growth from predation minus starvation)
```

Where **H** = herbivore count, **C** = carnivore count, and α, β, δ, γ are rate constants encoded in the entity parameters above.

**What you see in the terminal:**

```
Population
    │
900 │  ♣♣♣♣♣♣♣♣         ♣♣♣♣♣♣♣♣         ♣♣♣♣♣♣♣♣
    │ ♣        ♣♣      ♣♣        ♣♣      ♣♣
    │♣            ♣♣♣♣              ♣♣♣♣
 80 │         ◉◉◉◉          ◉◉◉◉          ◉◉◉◉
    │      ◉◉◉    ◉◉◉    ◉◉◉    ◉◉◉    ◉◉◉    ◉◉
 20 │    ◆◆◆          ◆◆◆          ◆◆◆          ◆◆
    │  ◆◆              ◆◆◆          ◆◆◆
    └──────────────────────────────────────────────→ ticks
     0   100  200  300  400  500  600  700  800
```

1. **Plants peak** → abundant food for herbivores
2. **Herbivores peak** (lagged) → abundant food for carnivores
3. **Carnivores peak** (lagged further) → herbivores crash
4. **Plants recover** → cycle repeats

In the `forest` biome this cycle sustains for hundreds to thousands of ticks.

---

## Controls

| Key | Action |
|-----|--------|
| `Ctrl+C` | Exit simulation |

The simulation prints a final population census on exit.

---

## License

MIT — do whatever you like.
