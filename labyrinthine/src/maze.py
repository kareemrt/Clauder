"""Maze data structure and generation algorithms."""
import random
from enum import IntFlag
from typing import List, Tuple, Optional


class Wall(IntFlag):
    NORTH = 1
    SOUTH = 2
    EAST  = 4
    WEST  = 8
    ALL   = 15


OPPOSITE = {Wall.NORTH: Wall.SOUTH, Wall.SOUTH: Wall.NORTH,
            Wall.EAST: Wall.WEST,   Wall.WEST: Wall.EAST}

DELTA = {Wall.NORTH: (-1, 0), Wall.SOUTH: (1, 0),
         Wall.EAST:  (0, 1),  Wall.WEST:  (0, -1)}


class Maze:
    """Grid-based maze: cells store which walls are present."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # Each cell starts with all 4 walls
        self._cells: List[List[int]] = [[Wall.ALL for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)

    def has_wall(self, r: int, c: int, direction: Wall) -> bool:
        return bool(self._cells[r][c] & direction)

    def remove_wall(self, r: int, c: int, direction: Wall) -> None:
        self._cells[r][c] &= ~direction
        dr, dc = DELTA[direction]
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.rows and 0 <= nc < self.cols:
            self._cells[nr][nc] &= ~OPPOSITE[direction]

    def neighbors(self, r: int, c: int):
        for d in (Wall.NORTH, Wall.SOUTH, Wall.EAST, Wall.WEST):
            dr, dc = DELTA[d]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield nr, nc, d

    def connected_neighbors(self, r: int, c: int):
        for d in (Wall.NORTH, Wall.SOUTH, Wall.EAST, Wall.WEST):
            if not self.has_wall(r, c, d):
                dr, dc = DELTA[d]
                yield r + dr, c + dc

    def is_fully_connected(self) -> bool:
        """BFS to verify all cells are reachable from start."""
        visited = set()
        queue = [self.start]
        visited.add(self.start)
        while queue:
            r, c = queue.pop()
            for nr, nc in self.connected_neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return len(visited) == self.rows * self.cols


# ──────────────────────────────────────────────────────────────────────────────
# Generation Algorithms
# ──────────────────────────────────────────────────────────────────────────────

class RecursiveBacktracker:
    """Depth-first search with backtracking — creates long, winding passages."""
    name = "Recursive Backtracker"
    description = "Creates mazes with long winding corridors and few dead-ends"

    @staticmethod
    def generate(maze: Maze, seed: Optional[int] = None) -> List[Tuple[int, int]]:
        rng = random.Random(seed)
        visited = [[False] * maze.cols for _ in range(maze.rows)]
        order = []

        def dfs(r, c):
            visited[r][c] = True
            order.append((r, c))
            directions = list(DELTA.keys())
            rng.shuffle(directions)
            for d in directions:
                dr, dc = DELTA[d]
                nr, nc = r + dr, c + dc
                if 0 <= nr < maze.rows and 0 <= nc < maze.cols and not visited[nr][nc]:
                    maze.remove_wall(r, c, d)
                    dfs(nr, nc)

        # Use Python's sys.setrecursionlimit to handle large mazes
        import sys
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(old_limit, maze.rows * maze.cols * 2 + 100))
        dfs(*maze.start)
        sys.setrecursionlimit(old_limit)
        return order


class PrimsAlgorithm:
    """Randomized Prim's — creates mazes with many short branches."""
    name = "Prim's Algorithm"
    description = "Creates mazes with many short branches and a more uniform texture"

    @staticmethod
    def generate(maze: Maze, seed: Optional[int] = None) -> List[Tuple[int, int]]:
        rng = random.Random(seed)
        in_maze = set()
        order = []
        frontier = []

        def add_frontiers(r, c):
            for nr, nc, d in maze.neighbors(r, c):
                if (nr, nc) not in in_maze:
                    frontier.append((nr, nc))

        sr, sc = maze.start
        in_maze.add((sr, sc))
        order.append((sr, sc))
        add_frontiers(sr, sc)

        while frontier:
            idx = rng.randint(0, len(frontier) - 1)
            r, c = frontier.pop(idx)
            if (r, c) in in_maze:
                continue
            # Find a neighbor already in the maze to connect through
            neighbors_in = [(nr, nc, d) for nr, nc, d in maze.neighbors(r, c)
                            if (nr, nc) in in_maze]
            nr, nc, d = rng.choice(neighbors_in)
            maze.remove_wall(nr, nc, OPPOSITE[d])
            in_maze.add((r, c))
            order.append((r, c))
            add_frontiers(r, c)

        return order


class WilsonsAlgorithm:
    """Wilson's loop-erased random walk — uniform spanning tree."""
    name = "Wilson's Algorithm"
    description = "Produces a uniform spanning tree — statistically perfect randomness"

    @staticmethod
    def generate(maze: Maze, seed: Optional[int] = None) -> List[Tuple[int, int]]:
        rng = random.Random(seed)
        in_maze = set()
        order = []
        all_cells = [(r, c) for r in range(maze.rows) for c in range(maze.cols)]
        rng.shuffle(all_cells)

        # Seed the maze with one cell
        in_maze.add(all_cells[0])
        order.append(all_cells[0])

        for start_r, start_c in all_cells:
            if (start_r, start_c) in in_maze:
                continue
            # Loop-erased random walk
            path = [(start_r, start_c)]
            path_set = {(start_r, start_c): 0}

            while path[-1] not in in_maze:
                r, c = path[-1]
                neighbors = [(nr, nc, d) for nr, nc, d in maze.neighbors(r, c)]
                nr, nc, d = rng.choice(neighbors)
                if (nr, nc) in path_set:
                    # Erase the loop
                    loop_start = path_set[(nr, nc)]
                    for cell in path[loop_start + 1:]:
                        del path_set[cell]
                    path = path[:loop_start + 1]
                else:
                    path.append((nr, nc))
                    path_set[(nr, nc)] = len(path) - 1

            # Carve the path
            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]
                dr, dc = r2 - r1, c2 - c1
                for d, (ddr, ddc) in DELTA.items():
                    if ddr == dr and ddc == dc:
                        maze.remove_wall(r1, c1, d)
                        break
                in_maze.add((r1, c1))
                order.append((r1, c1))
            in_maze.add(path[-1])
            order.append(path[-1])

        return order


class KruskalsAlgorithm:
    """Randomized Kruskal's — union-find on random edges."""
    name = "Kruskal's Algorithm"
    description = "Builds a random spanning tree by merging disjoint sets"

    @staticmethod
    def generate(maze: Maze, seed: Optional[int] = None) -> List[Tuple[int, int]]:
        rng = random.Random(seed)
        parent = {(r, c): (r, c) for r in range(maze.rows) for c in range(maze.cols)}
        order = []

        def find(cell):
            while parent[cell] != cell:
                parent[cell] = parent[parent[cell]]
                cell = parent[cell]
            return cell

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
            return True

        # Collect all edges (walls between adjacent cells)
        edges = []
        for r in range(maze.rows):
            for c in range(maze.cols):
                if r + 1 < maze.rows:
                    edges.append((r, c, Wall.SOUTH))
                if c + 1 < maze.cols:
                    edges.append((r, c, Wall.EAST))
        rng.shuffle(edges)

        for r, c, d in edges:
            dr, dc = DELTA[d]
            nr, nc = r + dr, c + dc
            if union((r, c), (nr, nc)):
                maze.remove_wall(r, c, d)
                order.append((r, c))

        return order


ALGORITHMS = {
    "recursive": RecursiveBacktracker,
    "prims":     PrimsAlgorithm,
    "wilsons":   WilsonsAlgorithm,
    "kruskals":  KruskalsAlgorithm,
}
