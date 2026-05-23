"""Interactive terminal exploration mode using curses."""
import curses
import time
from typing import Tuple
from .maze import Maze, Wall, DELTA, ALGORITHMS
from .renderer import THEMES


def _init_colors(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)     # walls
    curses.init_pair(2, curses.COLOR_CYAN, -1)      # player
    curses.init_pair(3, curses.COLOR_GREEN, -1)     # start
    curses.init_pair(4, curses.COLOR_RED, -1)       # end
    curses.init_pair(5, curses.COLOR_YELLOW, -1)    # path breadcrumbs
    curses.init_pair(6, curses.COLOR_BLUE, -1)      # visited
    curses.init_pair(7, curses.COLOR_MAGENTA, -1)   # UI


def run_interactive(maze: Maze, fog: bool = True, reveal_radius: int = 4):
    """Launch an interactive exploration session."""

    def _game(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        _init_colors(stdscr)

        player = list(maze.start)
        visited = {tuple(player)}
        steps = 0
        won = False
        show_solution = False
        solution_path = set()

        key_map = {
            curses.KEY_UP:    Wall.NORTH,
            curses.KEY_DOWN:  Wall.SOUTH,
            curses.KEY_RIGHT: Wall.EAST,
            curses.KEY_LEFT:  Wall.WEST,
            ord('w'): Wall.NORTH,
            ord('s'): Wall.SOUTH,
            ord('d'): Wall.EAST,
            ord('a'): Wall.WEST,
        }

        def draw():
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            pr, pc = player

            # Revealed cells for fog of war
            revealed = set()
            if fog:
                for dr in range(-reveal_radius, reveal_radius + 1):
                    for dc in range(-reveal_radius, reveal_radius + 1):
                        if dr*dr + dc*dc <= reveal_radius*reveal_radius:
                            revealed.add((pr + dr, pc + dc))

            # Center viewport on player
            vp_rows = (h - 4) // 2
            vp_cols = (w - 2) // 2
            offset_r = pr - vp_rows
            offset_c = pc - vp_cols

            for gr in range(h - 4):
                for gc in range(w - 2):
                    maze_gr = gr + offset_r * 2 - 1
                    maze_gc = gc + offset_c * 2 - 1

                    cell_r = (maze_gr - 1) // 2 if maze_gr % 2 == 1 else maze_gr // 2
                    cell_c = (maze_gc - 1) // 2 if maze_gc % 2 == 1 else maze_gc // 2
                    is_cell = maze_gr % 2 == 1 and maze_gc % 2 == 1

                    # Bounds check
                    max_gr = 2 * maze.rows
                    max_gc = 2 * maze.cols
                    if maze_gr < 0 or maze_gr > max_gr or maze_gc < 0 or maze_gc > max_gc:
                        try:
                            stdscr.addch(gr, gc, ' ')
                        except curses.error:
                            pass
                        continue

                    if fog and is_cell and (cell_r, cell_c) not in revealed:
                        try:
                            stdscr.addch(gr, gc, '▓', curses.color_pair(1) | curses.A_DIM)
                        except (curses.error, UnicodeEncodeError):
                            try:
                                stdscr.addch(gr, gc, '#', curses.color_pair(1) | curses.A_DIM)
                            except curses.error:
                                pass
                        continue

                    if is_cell:
                        cell = (cell_r, cell_c)
                        if cell == tuple(player):
                            ch, attr = '@', curses.color_pair(2) | curses.A_BOLD
                        elif cell == maze.start:
                            ch, attr = 'S', curses.color_pair(3) | curses.A_BOLD
                        elif cell == maze.end:
                            ch, attr = 'E', curses.color_pair(4) | curses.A_BOLD
                        elif show_solution and cell in solution_path:
                            ch, attr = '*', curses.color_pair(5)
                        elif cell in visited:
                            ch, attr = '.', curses.color_pair(6)
                        else:
                            ch, attr = ' ', curses.color_pair(1)
                    else:
                        # Wall or passage between cells
                        adj_r = maze_gr // 2
                        adj_c = maze_gc // 2
                        # Determine if this is a wall
                        is_wall = True
                        if maze_gr % 2 == 1:  # Horizontal run — east/west passage
                            r1, c1 = (maze_gr - 1) // 2, adj_c - 1
                            r2, c2 = r1, adj_c
                            if (0 <= r1 < maze.rows and 0 <= c1 < maze.cols and
                                    0 <= c2 < maze.cols and
                                    not maze.has_wall(r1, c1, Wall.EAST)):
                                is_wall = False
                        elif maze_gc % 2 == 1:  # Vertical run — north/south passage
                            r1, c1 = adj_r - 1, (maze_gc - 1) // 2
                            r2, c2 = adj_r, c1
                            if (0 <= c1 < maze.cols and 0 <= r1 < maze.rows and
                                    0 <= r2 < maze.rows and
                                    not maze.has_wall(r1, c1, Wall.SOUTH)):
                                is_wall = False

                        if is_wall:
                            ch, attr = '#', curses.color_pair(1)
                        else:
                            ch, attr = ' ', curses.color_pair(1)

                    try:
                        stdscr.addch(gr, gc, ch, attr)
                    except (curses.error, UnicodeEncodeError):
                        try:
                            if ch not in (' ', '.', '*', '@', 'S', 'E', '#'):
                                stdscr.addch(gr, gc, '?', attr)
                        except curses.error:
                            pass

            # Status bar
            status = (f" Steps: {steps} | Explored: {len(visited)}/{maze.rows*maze.cols} "
                      f"| [WASD/Arrows] Move  [H] Hint  [Q] Quit")
            if won:
                status = f" ★ YOU WIN! Steps: {steps} | Press Q to quit ★"
            try:
                stdscr.addstr(h - 4, 0, "─" * (w - 1), curses.color_pair(7))
                stdscr.addstr(h - 3, 0, status[:w-1], curses.color_pair(7) | curses.A_BOLD)
                stdscr.addstr(h - 2, 0, "─" * (w - 1), curses.color_pair(7))
                title = " LABYRINTHINE — Maze Explorer "
                stdscr.addstr(h - 1, 0, title[:w-1], curses.color_pair(2) | curses.A_BOLD)
            except curses.error:
                pass

            stdscr.refresh()

        draw()

        while True:
            key = stdscr.getch()

            if key in (ord('q'), ord('Q')):
                break

            if key in (ord('h'), ord('H')):
                # Toggle solution hint
                show_solution = not show_solution
                if show_solution and not solution_path:
                    from .solver import AStarSolver
                    result = AStarSolver.solve(maze)
                    solution_path = set(result.path)

            elif key in key_map:
                direction = key_map[key]
                r, c = player
                if not maze.has_wall(r, c, direction):
                    dr, dc = DELTA[direction]
                    player = [r + dr, c + dc]
                    visited.add(tuple(player))
                    steps += 1

                    if tuple(player) == maze.end:
                        won = True

            draw()

    curses.wrapper(_game)
