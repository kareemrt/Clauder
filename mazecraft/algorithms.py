"""Pathfinding algorithms that all share the same interface, so they can be
raced against each other on an identical maze: BFS, DFS, Dijkstra, and A*."""

from __future__ import annotations

import heapq
import time
from collections import deque
from dataclasses import dataclass

from mazecraft.maze import Maze


@dataclass
class SolveResult:
    name: str
    visited_order: list  # cells in the order the algorithm expanded them
    path: list  # cells from start to end, empty if no path exists
    elapsed_seconds: float

    @property
    def nodes_explored(self) -> int:
        return len(self.visited_order)

    @property
    def path_length(self) -> int:
        return max(len(self.path) - 1, 0)


def _manhattan(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _reconstruct(came_from: dict, start: tuple, end: tuple) -> list:
    if end not in came_from and end != start:
        return []
    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def bfs(maze: Maze) -> SolveResult:
    started = time.perf_counter()
    start, end = maze.start, maze.end
    frontier = deque([start])
    came_from = {}
    visited_order = []
    seen = {start}

    while frontier:
        cell = frontier.popleft()
        visited_order.append(cell)
        if cell == end:
            break
        for nxt in maze.neighbors(cell):
            if nxt not in seen:
                seen.add(nxt)
                came_from[nxt] = cell
                frontier.append(nxt)

    path = _reconstruct(came_from, start, end)
    return SolveResult("BFS", visited_order, path, time.perf_counter() - started)


def dfs(maze: Maze) -> SolveResult:
    started = time.perf_counter()
    start, end = maze.start, maze.end
    stack = [start]
    came_from = {}
    visited_order = []
    seen = {start}

    while stack:
        cell = stack.pop()
        visited_order.append(cell)
        if cell == end:
            break
        for nxt in maze.neighbors(cell):
            if nxt not in seen:
                seen.add(nxt)
                came_from[nxt] = cell
                stack.append(nxt)

    path = _reconstruct(came_from, start, end)
    return SolveResult("DFS", visited_order, path, time.perf_counter() - started)


def dijkstra(maze: Maze) -> SolveResult:
    started = time.perf_counter()
    start, end = maze.start, maze.end
    dist = {start: 0}
    came_from = {}
    visited_order = []
    finalized = set()
    heap = [(0, start)]

    while heap:
        d, cell = heapq.heappop(heap)
        if cell in finalized:
            continue
        finalized.add(cell)
        visited_order.append(cell)
        if cell == end:
            break
        for nxt in maze.neighbors(cell):
            nd = d + 1
            if nxt not in dist or nd < dist[nxt]:
                dist[nxt] = nd
                came_from[nxt] = cell
                heapq.heappush(heap, (nd, nxt))

    path = _reconstruct(came_from, start, end)
    return SolveResult("Dijkstra", visited_order, path, time.perf_counter() - started)


def astar(maze: Maze) -> SolveResult:
    started = time.perf_counter()
    start, end = maze.start, maze.end
    g_score = {start: 0}
    came_from = {}
    visited_order = []
    finalized = set()
    heap = [(_manhattan(start, end), start)]

    while heap:
        _, cell = heapq.heappop(heap)
        if cell in finalized:
            continue
        finalized.add(cell)
        visited_order.append(cell)
        if cell == end:
            break
        for nxt in maze.neighbors(cell):
            tentative = g_score[cell] + 1
            if nxt not in g_score or tentative < g_score[nxt]:
                g_score[nxt] = tentative
                came_from[nxt] = cell
                f = tentative + _manhattan(nxt, end)
                heapq.heappush(heap, (f, nxt))

    path = _reconstruct(came_from, start, end)
    return SolveResult("A*", visited_order, path, time.perf_counter() - started)


ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "dijkstra": dijkstra,
    "astar": astar,
}
