# LifeSim

```
  _     _  __      _____ _
 | |   (_)/ _|    / ____(_)
 | |    _| |_ ___| (___  _ _ __ ___
 | |   | |  _/ _ \\___ \| | '_ ` _ \
 | |___| | ||  __/____) | | | | | | |
 |_____|_|_| \___|_____/|_|_| |_| |_|

 Interactive Cellular Automata Simulator
```

**LifeSim** is a zero-dependency terminal cellular automata simulator featuring
three distinct simulation engines, 21 built-in patterns, real-time statistics,
and a fully keyboard-driven curses UI — all in pure Python.

---

## Features

| Feature | Details |
|---|---|
| **3 simulation engines** | Conway's Game of Life · Brian's Brain · Langton's Ant |
| **21 built-in patterns** | Still lifes · Oscillators · Spaceships · Guns · Methuselahs |
| **Interactive UI** | Curses-based with live stats, pan, speed control, and step mode |
| **Zero dependencies** | Pure Python stdlib — `curses`, `argparse`, `random`, `time` |
| **Non-interactive demo** | ASCII animation mode for testing or scripted use |
| **Python 3.8+** | No external packages needed |

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder
cd clauder

# Launch interactive Game of Life (random seed)
python main.py

# Load the Gosper Glider Gun pattern
python main.py --pattern gosper_glider_gun

# Try Brian's Brain
python main.py --mode brain

# Watch Langton's Ant build its highway
python main.py --mode ant

# Run a quick non-interactive demo
python main.py --demo

# List all built-in patterns
python main.py --list-patterns
```

---

## Interactive UI

```
╔══════════════════════════ LifeSim ◆ Conway's Game of Life ══════════════════╗
║                                                                              ║
║  ██  ██        ██                        ██  ██                              ║
║    ██  ██  ██  ██  ██                ████                                    ║
║  ██  ██        ██                                                            ║
║              ████████████                                                    ║
║                        ██                                              ██   ║
║                      ████                                           ██ ██   ║
║                                                                     ██ ██   ║
║                                                                        ██   ║
║                                                                              ║
║  ▶ RUN    Gen:     1,247  Pop:     4,182  B:    312  D:    298  Speed: 10fps ║
║  [SPC] Pause  [R] Random  [C] Clear  [S] Step  [+/-] Speed  [←→↑↓] Pan  [Q]║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `R` | Randomize grid |
| `C` | Clear grid |
| `S` | Single step (when paused) |
| `+` / `-` | Speed up / slow down |
| `← → ↑ ↓` | Pan the viewport |
| `Q` / `Esc` | Quit |

---

## Simulation Modes

### 1. Conway's Game of Life (`--mode life`)

The original 1970 cellular automaton by John Conway. Four simple rules produce
staggering complexity — stable structures, oscillators, infinite growth, and
Turing-complete computation.

```
Rules (B3/S23):
  • A live cell with 2 or 3 live neighbors survives
  • A dead cell with exactly 3 live neighbors is born
  • All other cells die or stay dead
```

**Sample evolution — Gosper Glider Gun:**
```
Generation 0             Generation 15            Generation 30
+--------------------+   +--------------------+   +--------------------+
|            ██      |   |            ██      |   |            ██      |
|          ████      |   |          ████      |   |          ████      |
| ██       ████  ██  |   | ██       ████  ██  |   | ██       ████  ██  |
| ██       ████  ██  |   | ██       ████  ██  |   | ██       ████  ██  |
|          ████      |   |          ████      |   |          ████      |
|            ██      |   |            ██      |   |            ██      |
|                    |   |  ██                |   |        ██          |
|                    |   | ██ ██              |   |       ██ ██        |
|                    |   |  ████              |   |        ████        |
+--------------------+   +--------------------+   +--------------------+
Pop: 36                  Pop: 38                  Pop: 41
```

### 2. Brian's Brain (`--mode brain`)

A 3-state automaton by Brian Silverman. Each cell cycles through FIRING →
REFRACTORY → DEAD, creating rolling waves of activity that never settle —
it can be proven that Brian's Brain never reaches a fixed point.

```
States:
  ██  Firing      (bright green) — the "on" state
  ░░  Refractory  (dim yellow)   — the dying state
      Dead        (blank)        — the "off" state

Rule:
  • Firing     → Refractory  (always)
  • Refractory → Dead        (always)
  • Dead       → Firing      if exactly 2 firing neighbors
```

**Sample frame:**
```
+------------------------------------------+
|  ██  ░░  ██░░    ██░░  ██                |
|░░  ██  ░░  ██  ░░  ██░░  ██░░            |
|  ░░  ██  ░░  ██  ░░  ██  ░░  ██          |
|██  ░░  ██░░    ██  ░░  ██░░    ██        |
|  ██  ░░  ██  ░░  ██  ░░  ██  ░░          |
+------------------------------------------+
 Perpetual rolling waves — never stabilises
```

### 3. Langton's Ant (`--mode ant`)

A Turing-complete 2-state, 2-color automaton (Langton 1986). A single ant
follows two rules as it traverses an initially blank grid. For the first
~10,000 steps behavior appears chaotic — then the ant spontaneously constructs
a periodic diagonal "highway" that it follows indefinitely.

```
Rules:
  • On a WHITE cell: turn RIGHT 90°, flip cell BLACK, move forward
  • On a BLACK cell: turn LEFT 90°,  flip cell WHITE, move forward

Ant states shown as directional arrows: ↑  →  ↓  ←
```

**Population growth curve:**
```
Cells flipped
  1000 |                                           ___________
   800 |                                      ____/
   600 |                              _______/
   400 |                   __________/
   200 |       ___________/
     0 |______/
       +----------------------------------------------------->
       0    2k   4k   6k   8k   10k  12k  14k  16k  18k  20k
                                              Generation
                  ^ "Highway" phase begins ~10,000 steps
```

---

## Pattern Library

### Still Lifes — stable configurations

```
Block        Beehive      Loaf         Boat         Tub
████         .██.         .██.         ██.          .█.
████         █..█         █..█         █.█          █.█
             .██.         .█.█         .█.          .█.
                          ..█.
```

### Oscillators — periodic patterns

```
Blinker (period 2)   Pulsar (period 3)    Pentadecathlon (period 15)

Gen 0:  ...          ..██.██..
        ███   -->    .█...█..             .████████.
        ...          █.....█.      -->    █........█
                     .█...█..             .████████.
Gen 1:  .█.          ..██.██..
        .█.
        .█.
```

### Spaceships — self-propelling patterns

```
Glider (c/4 diagonal)    LWSS (c/2 horizontal)

  .█.                    .█..█
  ..█    -->-->-->        █....  -->-->-->-->-->
  ███                    █....
                         ████.
Moves diagonally
every 4 generations      Moves right every 4 gens
```

### Guns — infinite pattern generators

```
Gosper Glider Gun — emits a glider every 30 generations

 ........................██............████
 .......................██.█...........████
 .██.........████...███............████
 .██.........█..█..███.............████
 ............████.██.█..............██
 .............██..█.................████
 ..................█....................
                                       --> gliders -->

 Period 30 | Unbounded population growth
```

### Methuselahs — small seeds with long lives

| Pattern | Start Pop | Stabilizes At | Notes |
|---------|-----------|---------------|-------|
| R-pentomino | 5 | Gen 1,103 | Produces 6 gliders |
| Acorn | 7 | Gen 5,206 | Classic long-lived pattern |
| Diehard | 7 | Gen 130 | Vanishes completely |
| Pi heptomino | 9 | Gen 173 | Symmetric evolution |

```
R-pentomino   Acorn         Diehard

.██           .█.           ......█.
██.           ...█          █.....
.█.           ██..          .█....███

5 cells -->   7 cells -->   7 cells -->
1,103 gens    5,206 gens    dies gen 130
```

---

## Project Structure

```
Clauder/
├── lifesim/                  # Core library
│   ├── __init__.py           # Package exports
│   ├── automata.py           # Simulation engines
│   │   ├── GameOfLife        #   Conway's Game of Life (B3/S23)
│   │   ├── BriansBrain       #   3-state firing/refractory/dead
│   │   └── LangtonsAnt       #   2-color Turing machine
│   ├── patterns.py           # 21 built-in Life patterns
│   │   ├── Still lifes       #   block, beehive, loaf, boat, tub
│   │   ├── Oscillators       #   blinker, pulsar, pentadecathlon ...
│   │   ├── Spaceships        #   glider, LWSS, MWSS, HWSS
│   │   ├── Guns              #   Gosper glider gun
│   │   └── Methuselahs       #   R-pentomino, acorn, diehard ...
│   ├── renderer.py           # Terminal rendering
│   │   ├── CursesRenderer    #   Interactive curses UI
│   │   └── SimpleRenderer    #   Non-interactive ASCII output
│   └── cli.py                # argparse CLI interface
├── main.py                   # Entry point
├── requirements.txt          # (empty — zero dependencies)
└── README.md                 # This file
```

---

## CLI Reference

```
usage: python main.py [--mode MODE] [--pattern NAME] [--width W] [--height H]
                      [--density D] [--speed S] [--style STYLE] [--no-wrap]
                      [--list-patterns] [--demo]

Options:
  --mode,-m     MODE    Simulation engine: life | brain | ant  (default: life)
  --width,-W    INT     Grid width in cells  (default: 200)
  --height,-H   INT     Grid height in cells  (default: 80)
  --density,-d  FLOAT   Random seed density 0.0-1.0  (default: 0.30)
  --speed,-s    INT     Initial speed in steps/sec  (default: 10)
  --pattern,-p  NAME    Load a named pattern (life mode only)
  --style       STYLE   Cell style: block | shade | dot | square | hash | cross
  --no-wrap             Disable toroidal boundary (cells die at edges)
  --list-patterns       Print the pattern library and exit
  --demo                Run a brief non-interactive demo and exit
```

---

## Using LifeSim as a Library

```python
from lifesim.automata import GameOfLife, BriansBrain, LangtonsAnt
from lifesim.patterns import place_pattern

# Conway's Game of Life
sim = GameOfLife(width=100, height=50)
place_pattern(sim, "gosper_glider_gun", cx=30, cy=25)

for _ in range(100):
    births, deaths = sim.step()

print(f"Gen {sim.generation}, pop {sim.population()}")
# --> Gen 100, pop 142

# Brian's Brain
brain = BriansBrain(80, 40)
brain.randomize(density=0.15)
brain.step()

# Langton's Ant — run to the "highway" phase
ant = LangtonsAnt(200, 200)
for _ in range(12_000):
    ant.step()
print(f"Black cells: {ant.population()}")  # --> ~750
```

---

## The Science Behind the Simulations

### Emergence

Each simulation applies identical simple rules to every cell simultaneously,
yet produces rich global behavior that cannot be predicted from the rules alone.
This is the hallmark of **emergence** — complex patterns arising from simple
local interactions.

### Computational Universality

Both **Conway's Game of Life** and **Langton's Ant** are Turing-complete,
meaning they can simulate any computation given sufficient space. The Gosper
Glider Gun, discovered in 1970, was the first proof that Life could generate
unbounded growth — a $50 prize offered by Conway.

### Phase Transitions

**Langton's Ant** demonstrates a remarkable phase transition: the first ~10,000
steps show no discernible pattern, then the system abruptly self-organizes into
a perfectly periodic diagonal highway. The mechanism behind this transition
remains an active area of mathematical research.

---

## Requirements

- Python 3.8 or newer
- A terminal with at least 80x24 characters (larger is better)
- `curses` module (standard library — pre-installed on Linux/macOS)

> **Windows users:** The `windows-curses` package adds curses support:
> `pip install windows-curses`

---

## License

MIT — do whatever you like with it.

---

*Built with pure Python and a lot of curiosity about what simple rules can become.*
