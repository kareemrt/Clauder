# Clauder

A collection of projects built by Claude.

## Projects

### [Labyrinthine](./labyrinthine/) 🌀
A Procedural Maze Universe Explorer — generate, solve, and explore mazes using 4 generation algorithms (Recursive Backtracker, Prim's, Wilson's, Kruskal's), 4 solvers (A\*, BFS, DFS, Right-Hand Rule), 5 color themes, animated rendering, SVG export, and interactive fog-of-war exploration. Zero external dependencies.

```bash
cd labyrinthine
python main.py generate -r 20 -c 40 --solve --animate --theme neon
python main.py compare -r 25 -c 25 --seed 42
python main.py explore -r 20 -c 40
```
