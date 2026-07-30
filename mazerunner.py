#!/usr/bin/env python3
"""
Mazerunner — Terminal maze generator and solver with animated visualization.

Generate mazes with DFS, Prim's, or Recursive Division algorithms,
then watch BFS, DFS, or A* pathfinding solve them in real time.
"""

import sys
import time
import random
import argparse
from collections import deque
import heapq

# ─────────────────────────────────────────────────────────────────────────────
#  ANSI Colors
# ─────────────────────────────────────────────────────────────────────────────

class C:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    BRED    = '\033[91m'
    BGREEN  = '\033[92m'
    BYELLOW = '\033[93m'
    BBLUE   = '\033[94m'
    BMAGENTA= '\033[95m'
    BCYAN   = '\033[96m'
    BWHITE  = '\033[97m'

USE_COLOR = True

def col(color, text):
    return (color + text + C.RESET) if USE_COLOR else text

# ─────────────────────────────────────────────────────────────────────────────
#  Maze Data Structure
# ─────────────────────────────────────────────────────────────────────────────

DIRS = {
    'N': (-1,  0, 'S'),
    'S': ( 1,  0, 'N'),
    'E': ( 0,  1, 'W'),
    'W': ( 0, -1, 'E'),
}

class Maze:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.walls  = [[set('NSEW') for _ in range(width)] for _ in range(height)]
        self.start  = (0, 0)
        self.end    = (height - 1, width - 1)

    def has_wall(self, r, c, d):
        return d in self.walls[r][c]

    def carve(self, r1, c1, r2, c2):
        """Remove the wall between two adjacent cells."""
        dr, dc = r2 - r1, c2 - c1
        d1 = {(-1,0):'N',(1,0):'S',(0,1):'E',(0,-1):'W'}[(dr, dc)]
        d2 = DIRS[d1][2]
        self.walls[r1][c1].discard(d1)
        self.walls[r2][c2].discard(d2)

    def valid(self, r, c):
        return 0 <= r < self.height and 0 <= c < self.width

    def unvisited_neighbors(self, r, c, visited):
        result = []
        for d, (dr, dc, _) in DIRS.items():
            nr, nc = r + dr, c + dc
            if self.valid(nr, nc) and (nr, nc) not in visited:
                result.append((d, nr, nc))
        return result

    def open_neighbors(self, r, c):
        """Neighbors reachable through open walls."""
        result = []
        for d, (dr, dc, _) in DIRS.items():
            if d not in self.walls[r][c]:
                nr, nc = r + dr, c + dc
                if self.valid(nr, nc):
                    result.append((nr, nc))
        return result

# ─────────────────────────────────────────────────────────────────────────────
#  Generation Algorithms
# ─────────────────────────────────────────────────────────────────────────────

def gen_dfs(maze):
    """Recursive backtracker — long winding corridors, high dead-end density."""
    visited = {(0, 0)}
    stack   = [(0, 0)]
    while stack:
        r, c  = stack[-1]
        nbrs  = maze.unvisited_neighbors(r, c, visited)
        if nbrs:
            _, nr, nc = random.choice(nbrs)
            maze.carve(r, c, nr, nc)
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()

def gen_prims(maze):
    """Randomized Prim's — highly branched, textured appearance."""
    visited  = {(0, 0)}
    frontier = set(maze.unvisited_neighbors(0, 0, visited))

    while frontier:
        _, nr, nc = random.choice(list(frontier))
        frontier.discard((_, nr, nc))
        if (nr, nc) in visited:
            continue
        visited.add((nr, nc))
        in_maze = [
            (pr, pc) for d, (dr, dc, _) in DIRS.items()
            for pr, pc in [(nr + dr, nc + dc)]
            if maze.valid(pr, pc) and (pr, pc) in visited
        ]
        if in_maze:
            pr, pc = random.choice(in_maze)
            maze.carve(nr, nc, pr, pc)
        for item in maze.unvisited_neighbors(nr, nc, visited):
            frontier.add(item)

def gen_division(maze):
    """Recursive division — room-and-corridor structure."""
    for r in range(maze.height):
        for c in range(maze.width):
            keep = set()
            if r == 0:              keep.add('N')
            if r == maze.height-1:  keep.add('S')
            if c == 0:              keep.add('W')
            if c == maze.width-1:   keep.add('E')
            maze.walls[r][c] = keep

    def divide(r1, c1, r2, c2):
        h, w = r2 - r1 + 1, c2 - c1 + 1
        if h <= 1 or w <= 1:
            return
        if w >= h:
            wc = random.randint(c1, c2 - 1)
            pr = random.randint(r1, r2)
            for r in range(r1, r2 + 1):
                if r != pr:
                    maze.walls[r][wc].add('E')
                    maze.walls[r][wc + 1].add('W')
            divide(r1, c1, r2, wc)
            divide(r1, wc + 1, r2, c2)
        else:
            wr = random.randint(r1, r2 - 1)
            pc = random.randint(c1, c2)
            for c in range(c1, c2 + 1):
                if c != pc:
                    maze.walls[wr][c].add('S')
                    maze.walls[wr + 1][c].add('N')
            divide(r1, c1, wr, c2)
            divide(wr + 1, c1, r2, c2)

    divide(0, 0, maze.height - 1, maze.width - 1)

GENERATORS = {'dfs': gen_dfs, 'prims': gen_prims, 'division': gen_division}

# ─────────────────────────────────────────────────────────────────────────────
#  Solving Algorithms
# ─────────────────────────────────────────────────────────────────────────────

def _reconstruct(parent, end):
    path, node = [], end
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return path

def solve_bfs(maze):
    """BFS — always finds the shortest path."""
    start, end = maze.start, maze.end
    q        = deque([start])
    parent   = {start: None}
    explored = [start]
    while q:
        r, c = q.popleft()
        if (r, c) == end:
            break
        for nr, nc in maze.open_neighbors(r, c):
            if (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                q.append((nr, nc))
                explored.append((nr, nc))
    return _reconstruct(parent, end), explored

def solve_dfs(maze):
    """DFS — fast exploration, path length not guaranteed optimal."""
    start, end = maze.start, maze.end
    stack    = [start]
    parent   = {start: None}
    explored = []
    seen     = set()
    while stack:
        r, c = stack.pop()
        if (r, c) in seen:
            continue
        seen.add((r, c))
        explored.append((r, c))
        if (r, c) == end:
            break
        for nr, nc in maze.open_neighbors(r, c):
            if (nr, nc) not in seen:
                parent.setdefault((nr, nc), (r, c))
                stack.append((nr, nc))
    return _reconstruct(parent, end), explored

def solve_astar(maze):
    """A* — heuristic-guided; shortest path with fewer explored cells than BFS."""
    start, end = maze.start, maze.end
    def h(r, c): return abs(r - end[0]) + abs(c - end[1])
    heap     = [(h(*start), 0, start)]
    parent   = {start: None}
    g        = {start: 0}
    explored = []
    seen     = set()
    while heap:
        _, cost, (r, c) = heapq.heappop(heap)
        if (r, c) in seen:
            continue
        seen.add((r, c))
        explored.append((r, c))
        if (r, c) == end:
            break
        for nr, nc in maze.open_neighbors(r, c):
            ng = cost + 1
            if ng < g.get((nr, nc), float('inf')):
                g[(nr, nc)] = ng
                parent[(nr, nc)] = (r, c)
                heapq.heappush(heap, (ng + h(nr, nc), ng, (nr, nc)))
    return _reconstruct(parent, end), explored

SOLVERS = {'bfs': solve_bfs, 'dfs': solve_dfs, 'astar': solve_astar}

# ─────────────────────────────────────────────────────────────────────────────
#  Rendering
# ─────────────────────────────────────────────────────────────────────────────

# Unicode box-drawing junction lookup: (N, S, E, W) → character
# N/S = vertical arms (up/down), E/W = horizontal arms (right/left)
_JUNCTIONS = {
    (0,0,0,0): ' ',  (1,0,0,0): '╵',  (0,1,0,0): '╷',  (0,0,1,0): '╶',
    (0,0,0,1): '╴',  (1,1,0,0): '│',  (0,0,1,1): '─',  (1,0,1,0): '└',
    (1,0,0,1): '┘',  (0,1,1,0): '┌',  (0,1,0,1): '┐',  (1,1,1,0): '├',
    (1,1,0,1): '┤',  (0,1,1,1): '┬',  (1,0,1,1): '┴',  (1,1,1,1): '┼',
}

def _junction_char(wr, wc, H, W, maze):
    """
    Compute the junction character at wall-row wr ∈ [0,H], wall-col wc ∈ [0,W].
    N/S = vertical wall segments; E/W = horizontal wall segments.
    """
    # N: vertical segment going up — east wall of cell (wr-1, wc-1)
    if wr == 0:
        N = False
    elif wc == 0 or wc == W:
        N = True   # border
    else:
        N = maze.has_wall(wr - 1, wc - 1, 'E')

    # S: vertical segment going down — east wall of cell (wr, wc-1)
    if wr == H:
        S = False
    elif wc == 0 or wc == W:
        S = True
    else:
        S = maze.has_wall(wr, wc - 1, 'E')

    # W: horizontal segment going left — south wall of cell (wr-1, wc-1)
    if wc == 0:
        Wh = False
    elif wr == 0 or wr == H:
        Wh = True
    else:
        Wh = maze.has_wall(wr - 1, wc - 1, 'S')

    # E: horizontal segment going right — south wall of cell (wr-1, wc)
    if wc == W:
        Eh = False
    elif wr == 0 or wr == H:
        Eh = True
    else:
        Eh = maze.has_wall(wr - 1, wc, 'S')

    return _JUNCTIONS.get((int(N), int(S), int(Eh), int(Wh)), '+')

def render_maze(maze, path=None, explored=None):
    """Render the maze and return a list of strings (one per line)."""
    path_set     = set(path)     if path     else set()
    explored_set = set(explored) if explored else set()
    H, W         = maze.height, maze.width

    def cell_char(r, c):
        pos = (r, c)
        if pos == maze.start:    return col(C.BGREEN,   'S')
        if pos == maze.end:      return col(C.BRED,     'E')
        if pos in path_set:      return col(C.BYELLOW,  '·')
        if pos in explored_set:  return col(C.BBLUE,    '░')
        return ' '

    def h_seg(r, c):
        """Horizontal wall segment (3 chars) below cell (r, c)."""
        if r >= H - 1 or maze.has_wall(r, c, 'S'):
            return col(C.CYAN, '───')
        return '   '

    def v_seg(r, c):
        """Vertical wall character to the east of cell (r, c)."""
        if c >= W - 1 or maze.has_wall(r, c, 'E'):
            return col(C.CYAN, '│')
        return ' '

    lines = []

    # Top border (wall-row 0)
    line = col(C.CYAN, _junction_char(0, 0, H, W, maze))
    for c in range(W):
        line += col(C.CYAN, '───')   # top always walled
        line += col(C.CYAN, _junction_char(0, c + 1, H, W, maze))
    lines.append(line)

    for r in range(H):
        # Cell content row
        line = col(C.CYAN, '│')
        for c in range(W):
            line += ' ' + cell_char(r, c) + ' '
            line += v_seg(r, c)
        lines.append(line)

        # Wall row below row r (wall-row r+1)
        line = col(C.CYAN, _junction_char(r + 1, 0, H, W, maze))
        for c in range(W):
            line += h_seg(r, c)
            line += col(C.CYAN, _junction_char(r + 1, c + 1, H, W, maze))
        lines.append(line)

    return lines

# ─────────────────────────────────────────────────────────────────────────────
#  Display Helpers
# ─────────────────────────────────────────────────────────────────────────────

HEADER = r"""
  __  __               _____
 |  \/  |             |  __ \
 | \  / | __ _ _______| |__) |_   _ _ __  _ __   ___ _ __
 | |\/| |/ _` |_  / _ \  _  /| | | | '_ \| '_ \ / _ \ '__|
 | |  | | (_| |/ /  __/ | \ \| |_| | | | | | | |  __/ |
 |_|  |_|\__,_/___\___|_|  \_\\__,_|_| |_|_| |_|\___|_|
"""

def print_header():
    print(col(C.BCYAN, HEADER))
    print(col(C.DIM, '  Terminal Maze Generator & Solver\n'))

def progress_bar(value, total, width=32, label=''):
    filled = int(width * value / total) if total else 0
    bar    = '█' * filled + '░' * (width - filled)
    pct    = f'{100*value//total:3d}%' if total else '---'
    return f'{col(C.CYAN, "[")}{col(C.BYELLOW, bar)}{col(C.CYAN, "]")} {col(C.WHITE, pct)} {label}'

def clear_lines(n):
    """Move cursor up n lines and clear them."""
    sys.stdout.write(f'\033[{n}A\033[J')
    sys.stdout.flush()

def print_maze_frame(lines, status=''):
    for line in lines:
        print(line)
    if status:
        print(status)

def print_stats(maze, path, explored, gen_name, solve_name, elapsed):
    total   = maze.width * maze.height
    eff     = 100 * len(path) / len(explored) if explored else 0
    divider = col(C.DIM, '─' * 48)
    print(f'\n{divider}')
    print(f'  {col(C.BWHITE, "RESULTS")}')
    print(divider)
    print(f'  Maze         : {col(C.CYAN, f"{maze.width}×{maze.height}")} '
          f'{col(C.DIM, f"({total} cells)")}')
    print(f'  Generator    : {col(C.YELLOW, gen_name.upper())}')
    print(f'  Solver       : {col(C.YELLOW, solve_name.upper())}')
    print(f'  Path length  : {col(C.BGREEN,  str(len(path)))} steps')
    print(f'  Cells visited: {col(C.BBLUE,   str(len(explored)))}')
    print(f'  Efficiency   : {col(C.BYELLOW, f"{eff:.1f}%")}')
    print(f'  Time         : {col(C.WHITE,   f"{elapsed:.2f}s")}')
    print(divider)

# ─────────────────────────────────────────────────────────────────────────────
#  Animation
# ─────────────────────────────────────────────────────────────────────────────

def animate(maze, solver_name, delay):
    """Run animated solving visualization."""
    solver_fn           = SOLVERS[solver_name]
    path, explored_full = solver_fn(maze)

    # Phase 1 — exploration
    current_explored = []
    frame_lines_count = maze.height * 2 + 1 + 2  # maze lines + status + blank

    for i, pos in enumerate(explored_full):
        current_explored.append(pos)
        lines  = render_maze(maze, explored=current_explored)
        status = progress_bar(i + 1, len(explored_full), label=f'Exploring…')
        if i == 0:
            print_maze_frame(lines, status)
        else:
            clear_lines(frame_lines_count)
            print_maze_frame(lines, status)
        time.sleep(delay)

    # Phase 2 — path reveal
    current_path = []
    for i, pos in enumerate(path):
        current_path.append(pos)
        lines  = render_maze(maze, path=current_path, explored=current_explored)
        status = progress_bar(i + 1, len(path), label=f'Tracing path…')
        clear_lines(frame_lines_count)
        print_maze_frame(lines, status)
        time.sleep(delay * 3)

    clear_lines(frame_lines_count)
    lines = render_maze(maze, path=path, explored=current_explored)
    print_maze_frame(lines)

    return path, explored_full

# ─────────────────────────────────────────────────────────────────────────────
#  CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description='Mazerunner — terminal maze generator and animated solver',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
algorithms:
  generators : dfs (default), prims, division
  solvers    : bfs (default), dfs, astar

examples:
  python mazerunner.py                         # 20×10, DFS gen, BFS solve
  python mazerunner.py -W 40 -H 20 -g prims   # wide Prim's maze
  python mazerunner.py -g division -s astar    # rooms solved with A*
  python mazerunner.py --no-animate -W 60      # instant result, wide maze
  python mazerunner.py --seed 42               # reproducible maze
        """,
    )
    p.add_argument('-W', '--width',     type=int, default=20,
                   help='Maze width in cells (default: 20)')
    p.add_argument('-H', '--height',    type=int, default=10,
                   help='Maze height in cells (default: 10)')
    p.add_argument('-g', '--generator', choices=list(GENERATORS), default='dfs',
                   help='Generation algorithm (default: dfs)')
    p.add_argument('-s', '--solver',    choices=list(SOLVERS), default='bfs',
                   help='Solving algorithm (default: bfs)')
    p.add_argument('--no-animate',      action='store_true',
                   help='Skip animation, show final result immediately')
    p.add_argument('--delay',           type=float, default=0.02,
                   help='Animation delay per frame in seconds (default: 0.02)')
    p.add_argument('--no-color',        action='store_true',
                   help='Disable ANSI colors')
    p.add_argument('--seed',            type=int,
                   help='Random seed for reproducibility')
    return p.parse_args()

def main():
    global USE_COLOR
    args      = parse_args()
    USE_COLOR = not args.no_color and sys.stdout.isatty()

    if args.seed is not None:
        random.seed(args.seed)

    if USE_COLOR:
        print_header()

    # ── Generate ──────────────────────────────────────────────────
    t0   = time.time()
    maze = Maze(args.width, args.height)
    GENERATORS[args.generator](maze)
    gen_time = time.time() - t0

    if USE_COLOR:
        print(col(C.DIM,
            f'  Generated {args.width}×{args.height} maze '
            f'({args.generator}) in {gen_time*1000:.1f} ms\n'))

    # ── Solve ─────────────────────────────────────────────────────
    t1 = time.time()

    if args.no_animate:
        path, explored = SOLVERS[args.solver](maze)
        for line in render_maze(maze, path=path, explored=explored):
            print(line)
    else:
        path, explored = animate(maze, args.solver, delay=args.delay)

    elapsed = time.time() - t1
    print_stats(maze, path, explored, args.generator, args.solver, elapsed)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{col(C.YELLOW, "  Interrupted. Goodbye!")}')
        sys.exit(0)
