# Mazerunner

```
  __  __               _____
 |  \/  |             |  __ \
 | \  / | __ _ _______| |__) |_   _ _ __  _ __   ___ _ __
 | |\/| |/ _` |_  / _ \  _  /| | | | '_ \| '_ \ / _ \ '__|
 | |  | | (_| |/ /  __/ | \ \| |_| | | | | | | |  __/ |
 |_|  |_|\__,_/___\___|_|  \_\\__,_|_| |_|_| |_|\___|_|
```

**A terminal maze generator and animated pathfinding visualizer — pure Python, zero dependencies.**

Watch mazes spring to life from three generation algorithms, then see BFS, DFS, and A* race to find the exit in real time.

---

## What It Does

Mazerunner gives you a complete playground for exploring maze generation and graph-search algorithms, all rendered in the terminal with Unicode box-drawing characters and ANSI colors.

```
┌───────────────┬───────────────────┬───┐
│ S   ·   ·   ░ │                   │   │
│   ╷   ╷   ╶───┘   ╷   ╷   ┌───┬───┤   │
│ ░ │ ░ │ ·   ·   · │   │   │   │   │   │
│   │   │   ╷   ╷   └───┤   ╵   ╵   │   │
│ ░ │ ░ │ ░ │ ░ │ ·   · │           │   │
├───┘   │   └───┤   ╷   └───────┐   ╵   │
│     ░ │ ░   ░ │ ░ │ ·   ·   · │       │
├───────┴───╴   └───┴───┐   ╷   └───────┤
│             ░   ░   ░ │ ░ │ ·   ·   · │
├───────╴   ╷   ╷   ╷   ├───┘   ╷   ╷   │
│           │ ░ │ ░ │ ░ │     ░ │ ░ │ E │
└───────────┴───┴───┴───┴───────┴───┴───┘

  Path length  : 15 steps
  Cells visited: 35
  Efficiency   : 42.9%
```

**Legend:** `S` = Start  `E` = Exit  `·` = Solution path  `░` = Cells explored

---

## Features

- **3 maze generation algorithms** — each produces a structurally distinct maze
- **3 pathfinding algorithms** — compare exploration patterns side-by-side
- **Animated visualization** — watch cells get explored and the solution traced
- **Proper Unicode rendering** — box-drawing characters with correct junction logic
- **ANSI color support** — green start, red exit, yellow path, blue explored
- **Statistics panel** — path length, cells visited, efficiency, elapsed time
- **Reproducible mazes** — `--seed` flag for exact repeats
- **Zero dependencies** — pure Python 3.6+ standard library

---

## Quick Start

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Default: 20×10 maze, DFS generation, BFS solving, animated
python mazerunner.py

# Jump straight to the result (no animation)
python mazerunner.py --no-animate

# Large Prim's maze solved with A*
python mazerunner.py -W 40 -H 20 -g prims -s astar

# Room-and-corridor maze, DFS solver
python mazerunner.py -g division -s dfs --delay 0.05

# Reproducible run
python mazerunner.py --seed 42
```

---

## Generation Algorithms

### DFS — Recursive Backtracker

The depth-first search carver digs as deep as possible before backtracking. This produces long, winding corridors with many dead ends — mazes that feel *labyrinthine*.

```
┌───────────────────────────┐
│ S   ·   ·   ·   ·   ·   · │
│   ╷   ╶───────┐   ┌───╴   │
│ · │           │   │       │
│   └───────╴   ╵   └───┐   │
│ ·   ·   · │           │   │
├───┐   ╶───┤   ╶───────┴───┤
│   │       │ ·   ·   ·   E │
└───┴───────┴───────────────┘
```

- Long straight corridors; high solution-to-explored ratio
- Uniform spanning tree — exactly one path between any two cells
- Time: O(W×H)

---

### Prim's — Randomized Prim's Algorithm

Starts from a seed cell and greedily grows a spanning tree by repeatedly adding a random frontier cell. The result is highly branched, with lots of short dead ends radiating outward.

```
┌───┬───┬───────────┬───┐
│ S │   │           │   │
│   ╵   ╵   ╶───┐   │   │
│       │       │   ╵   │
│   ╷   └───────┘       │
│   │           │   ╷   │
├───┘   ╷   ╷   └───┤   │
│       │   │     · │ E │
└───────┴───┴───────┴───┘
```

- Dense branching; visually textured appearance
- Tends to create mazes that look more like organic structures
- Time: O(W×H log(W×H))

---

### Division — Recursive Division

Starts with a fully open grid and adds walls recursively, leaving a single passage in each wall. Creates recognizable room-and-corridor patterns.

```
┌───────────┬───────────────┐
│           │               │
│   ╶───────┤   ╶───────┐   │
│           │           │   │
├───────┐   └───────────┤   │
│       │               │   │
│   ╷   └───╴   ╷   ╶───┤   │
│   │           │       │ E │
└───┴───────────┴───────┴───┘
```

- Clear room structure visible in the output
- Passage width is always 1 cell
- Time: O(W×H)

---

## Solving Algorithms

### BFS — Breadth-First Search

Explores cells layer by layer outward from the start. **Guarantees the shortest path** in an unweighted graph.

```
Flow diagram:
  Start
    │
    ├── neighbor A ── neighbor D ── …
    │
    └── neighbor B ── neighbor E ── … ← Exit reached at minimum depth
```

- **Path**: Always shortest
- **Explored**: Most cells (expands uniformly in all directions)
- **Best for**: When shortest path is required

---

### DFS — Depth-First Search

Dives deep along one branch before backtracking. Fast to implement, but the found path may be far from optimal.

```
Flow diagram:
  Start → A → B → C → D → (dead end, backtrack)
                ↓
                E → F → Exit
```

- **Path**: Not guaranteed shortest
- **Explored**: Varies; often fewer cells than BFS in practice
- **Best for**: When any path is acceptable and speed matters

---

### A* — A-Star Search

Uses a Manhattan-distance heuristic to guide exploration toward the exit. Finds the shortest path while exploring fewer cells than BFS.

```
Heuristic: h(r,c) = |r - end_row| + |c - end_col|
Priority:  f(n) = g(n) + h(n)
           where g(n) = cost from start to n
```

- **Path**: Always shortest (admissible heuristic)
- **Explored**: Fewest cells among the three solvers
- **Best for**: Large mazes where speed and optimality both matter

---

## Algorithm Comparison

| Algorithm | Path Optimal | Cells Explored | Time Complexity | Memory  |
|-----------|:---:|:-----------:|:-----------:|:-------:|
| BFS       | ✅  | Most         | O(V + E)    | O(V)    |
| DFS       | ❌  | Varies       | O(V + E)    | O(V)    |
| A\*       | ✅  | Fewest       | O(E log V)  | O(V)    |

*V = cells, E = open passages*

---

## CLI Reference

```
python mazerunner.py [options]

Maze dimensions:
  -W, --width     INT    Maze width in cells (default: 20)
  -H, --height    INT    Maze height in cells (default: 10)

Algorithms:
  -g, --generator STR    dfs | prims | division  (default: dfs)
  -s, --solver    STR    bfs | dfs | astar        (default: bfs)

Display:
  --no-animate           Skip animation, show final result
  --delay         FLOAT  Animation frame delay in seconds (default: 0.02)
  --no-color             Disable ANSI color output

Misc:
  --seed          INT    Random seed for reproducibility
  -h, --help             Show this help message
```

---

## Example Gallery

**Tiny maze for quick demo (`--seed 42 -W 8 -H 5`):**
```
┌───┬───────┬───────┬───┬───────┐
│ S │ ·   · │ ·   · │   │ ░   ░ │
│   │   ╷   │   ╷   │   ╵   ╷   │
│ · │ · │ · │ · │ · │       │ ░ │
│   ╵   │   ╵   │   │   ┌───┘   │
│ ·   · │ ·   · │ · │   │ ·   · │
├───────┴───┬───┘   │   │   ╷   │
│ ░   ░   ░ │ ·   · │   │ · │ · │
│   ╶───┐   ╵   ╶───┴───┘   │   │
│ ░   ░ │ ░   ·   ·   ·   · │ E │
└───────┴───────────────────┴───┘
```

**Division maze — rooms visible (`-g division -W 12 -H 6 --seed 99`):**
```
┌───────┬───┬───┬───────────┬───────────────────┐
│ S   ░ │   │   │           │                   │
│   ╷   │   ╵   ├───┬───┐   ├───────┐   ┌───────┤
│ · │ ░ │       │   │   │   │       │   │ ░   ░ │
│   └───┤   ┌───┘   ╵   ╵   │   ╷   ╵   ╵   ╷   │
│ ·   · │   │               │   │ ·   ·   ░ │ ░ │
├───╴   │   ╵   ╷   ┌───╴   └───┘   ╷   ┌───┴───┤
│ ░   · │       │   │ ░   ·   ·   · │ · │ ·   · │
│   ╷   └───┬───┼───┼───┐   ╷   ╶───┤   ╵   ╷   │
│ ░ │ ·   · │   │   │   │ · │       │ ·   · │ · │
│   └───┐   ╵   ╵   ╵   ╵   │   ╷   ├───────┘   │
│ ░   ░ │ ·   ·   ·   ·   · │   │   │         E │
└───────┴───────────────────┴───┴───┴───────────┘
```

---

## Architecture

```
mazerunner.py
├── Colors (C)          — ANSI escape code constants
├── Maze                — Grid of cells with wall sets
│   ├── carve()         — Remove wall between two adjacent cells
│   ├── open_neighbors()— Return cells reachable from a position
│   └── unvisited_neighbors() — Used by generators
├── Generators
│   ├── gen_dfs()       — Recursive backtracker
│   ├── gen_prims()     — Randomized Prim's
│   └── gen_division()  — Recursive division
├── Solvers
│   ├── solve_bfs()     — Breadth-first search
│   ├── solve_dfs()     — Depth-first search
│   └── solve_astar()   — A* with Manhattan heuristic
├── Renderer
│   ├── _junction_char()— Computes correct box-drawing junction
│   └── render_maze()   — Returns list of colored strings
└── main()              — CLI parsing, orchestration, animation loop
```

The junction character for each grid intersection is computed from four boolean flags (N, S, E, W — whether a wall segment extends in each direction), mapped to the correct Unicode box-drawing character from a 16-entry lookup table.

---

## License

MIT — do whatever you like with it.
