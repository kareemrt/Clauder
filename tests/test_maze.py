from collections import deque

from mazecraft.maze import generate_maze


def reachable_cells(maze, start):
    seen = {start}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for nxt in maze.neighbors(cell):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def test_maze_has_correct_dimensions():
    maze = generate_maze(10, 12, seed=1)
    assert maze.rows == 10
    assert maze.cols == 12
    assert len(maze.passages) == 120


def test_maze_is_fully_connected():
    maze = generate_maze(20, 20, seed=42)
    assert reachable_cells(maze, maze.start) == set(maze.passages.keys())


def test_maze_is_a_perfect_maze_tree():
    # A perfect maze has exactly (cells - 1) passages, like a spanning tree.
    maze = generate_maze(8, 8, seed=3)
    open_edges = sum(len(dirs) for dirs in maze.passages.values()) // 2
    assert open_edges == maze.rows * maze.cols - 1


def test_same_seed_yields_same_maze():
    a = generate_maze(10, 10, seed=99)
    b = generate_maze(10, 10, seed=99)
    assert a.passages == b.passages


def test_different_seed_yields_different_maze():
    a = generate_maze(10, 10, seed=1)
    b = generate_maze(10, 10, seed=2)
    assert a.passages != b.passages
