import pytest

from mazecraft.algorithms import ALGORITHMS, astar, bfs, dfs, dijkstra
from mazecraft.maze import generate_maze


@pytest.fixture(params=list(ALGORITHMS.values()), ids=list(ALGORITHMS.keys()))
def solver(request):
    return request.param


def test_solver_finds_a_path(solver):
    maze = generate_maze(15, 15, seed=5)
    result = solver(maze)
    assert result.path
    assert result.path[0] == maze.start
    assert result.path[-1] == maze.end


def test_path_steps_are_adjacent_open_passages(solver):
    maze = generate_maze(15, 15, seed=5)
    result = solver(maze)
    for a, b in zip(result.path, result.path[1:]):
        assert b in set(maze.neighbors(a))


def test_optimal_solvers_agree_on_shortest_path_length():
    # On a perfect maze there is a single unique path, so every algorithm
    # that finds *a* path must find one of the same length.
    maze = generate_maze(20, 20, seed=11)
    lengths = {name: ALGORITHMS[name](maze).path_length for name in ("bfs", "dijkstra", "astar")}
    assert len(set(lengths.values())) == 1


def test_visited_order_starts_at_start_cell(solver):
    maze = generate_maze(10, 10, seed=2)
    result = solver(maze)
    assert result.visited_order[0] == maze.start


def test_nodes_explored_never_exceeds_total_cells(solver):
    maze = generate_maze(12, 12, seed=8)
    result = solver(maze)
    assert result.nodes_explored <= maze.rows * maze.cols
