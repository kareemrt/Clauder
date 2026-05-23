"""Maze solving algorithms."""
import heapq
from typing import List, Tuple, Dict, Optional, Set
from .maze import Maze, DELTA, Wall


class SolveResult:
    def __init__(self, path: List[Tuple[int, int]], visited: List[Tuple[int, int]],
                 algorithm: str, steps: int):
        self.path = path
        self.visited = visited
        self.algorithm = algorithm
        self.steps = steps
        self.path_length = len(path)

    def __repr__(self):
        return (f"SolveResult(algorithm={self.algorithm!r}, "
                f"path_length={self.path_length}, steps={self.steps})")


def _reconstruct(came_from: Dict, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


class AStarSolver:
    """A* with Manhattan distance heuristic — optimal path."""
    name = "A* Search"
    description = "Finds the optimal shortest path using a heuristic"

    @staticmethod
    def solve(maze: Maze) -> SolveResult:
        start, end = maze.start, maze.end

        def h(r, c):
            return abs(r - end[0]) + abs(c - end[1])

        g_score = {start: 0}
        f_score = {start: h(*start)}
        came_from = {start: None}
        open_heap = [(f_score[start], start)]
        visited_order = []
        steps = 0

        while open_heap:
            _, current = heapq.heappop(open_heap)
            r, c = current
            visited_order.append(current)
            steps += 1

            if current == end:
                return SolveResult(_reconstruct(came_from, current),
                                   visited_order, AStarSolver.name, steps)

            for nr, nc in maze.connected_neighbors(r, c):
                tentative = g_score[current] + 1
                if (nr, nc) not in g_score or tentative < g_score[(nr, nc)]:
                    came_from[(nr, nc)] = current
                    g_score[(nr, nc)] = tentative
                    f_score[(nr, nc)] = tentative + h(nr, nc)
                    heapq.heappush(open_heap, (f_score[(nr, nc)], (nr, nc)))

        return SolveResult([], visited_order, AStarSolver.name, steps)


class BFSSolver:
    """Breadth-first search — also finds the shortest path."""
    name = "BFS"
    description = "Explores all cells level by level, guaranteed shortest path"

    @staticmethod
    def solve(maze: Maze) -> SolveResult:
        start, end = maze.start, maze.end
        came_from = {start: None}
        queue = [start]
        visited_order = []
        steps = 0

        while queue:
            current = queue.pop(0)
            r, c = current
            visited_order.append(current)
            steps += 1

            if current == end:
                return SolveResult(_reconstruct(came_from, current),
                                   visited_order, BFSSolver.name, steps)

            for nr, nc in maze.connected_neighbors(r, c):
                if (nr, nc) not in came_from:
                    came_from[(nr, nc)] = current
                    queue.append((nr, nc))

        return SolveResult([], visited_order, BFSSolver.name, steps)


class DFSSolver:
    """Depth-first search — finds a path, not necessarily shortest."""
    name = "DFS"
    description = "Explores deeply before backtracking — produces winding paths"

    @staticmethod
    def solve(maze: Maze) -> SolveResult:
        start, end = maze.start, maze.end
        came_from = {start: None}
        stack = [start]
        visited = set()
        visited_order = []
        steps = 0

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            r, c = current
            visited_order.append(current)
            steps += 1

            if current == end:
                return SolveResult(_reconstruct(came_from, current),
                                   visited_order, DFSSolver.name, steps)

            for nr, nc in maze.connected_neighbors(r, c):
                if (nr, nc) not in visited:
                    came_from[(nr, nc)] = current
                    stack.append((nr, nc))

        return SolveResult([], visited_order, DFSSolver.name, steps)


class RightHandRuleSolver:
    """Right-hand rule wall follower — works only on simply-connected mazes."""
    name = "Right-Hand Rule"
    description = "Follows the right wall — works on simply-connected mazes"

    @staticmethod
    def solve(maze: Maze) -> SolveResult:
        # Direction order: NORTH, EAST, SOUTH, WEST (clockwise)
        dirs = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        start, end = maze.start, maze.end

        pos = start
        facing = 1  # Start facing EAST
        path = [pos]
        visited_order = [pos]
        steps = 0
        max_steps = maze.rows * maze.cols * 8

        while pos != end and steps < max_steps:
            steps += 1
            # Try to turn right, go straight, turn left, turn back
            right = (facing + 1) % 4
            d_right = dirs[right]
            d_fwd = dirs[facing]

            if not maze.has_wall(*pos, d_right):
                # Turn right and move
                facing = right
                dr, dc = DELTA[dirs[facing]]
                pos = (pos[0] + dr, pos[1] + dc)
            elif not maze.has_wall(*pos, d_fwd):
                # Go straight
                dr, dc = DELTA[d_fwd]
                pos = (pos[0] + dr, pos[1] + dc)
            else:
                # Turn left
                facing = (facing - 1) % 4
                dr, dc = DELTA[dirs[facing]]
                if not maze.has_wall(*pos, dirs[facing]):
                    pos = (pos[0] + dr, pos[1] + dc)
                else:
                    facing = (facing - 1) % 4  # Turn around

            path.append(pos)
            visited_order.append(pos)

        if pos == end:
            return SolveResult(path, visited_order, RightHandRuleSolver.name, steps)
        # Fallback to BFS if right-hand rule fails
        return BFSSolver.solve(maze)


SOLVERS = {
    "astar":      AStarSolver,
    "bfs":        BFSSolver,
    "dfs":        DFSSolver,
    "righthand":  RightHandRuleSolver,
}
