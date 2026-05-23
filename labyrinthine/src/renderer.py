"""Terminal rendering with ANSI color support."""
from typing import Optional, Set, Tuple, List
from .maze import Maze, Wall


# ANSI color codes
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    BRIGHT_RED     = "\033[91m"
    BRIGHT_GREEN   = "\033[92m"
    BRIGHT_YELLOW  = "\033[93m"
    BRIGHT_BLUE    = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN    = "\033[96m"
    BRIGHT_WHITE   = "\033[97m"

    BG_BLACK   = "\033[40m"
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"
    BG_WHITE   = "\033[47m"

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"


THEMES = {
    "classic": {
        "wall":    Color.WHITE,
        "passage": Color.BLACK,
        "path":    Color.BRIGHT_YELLOW,
        "visited": Color.BLUE,
        "start":   Color.BRIGHT_GREEN,
        "end":     Color.BRIGHT_RED,
        "player":  Color.BRIGHT_CYAN,
        "wall_char":    "█",
        "passage_char": " ",
        "path_char":    "·",
        "visited_char": "░",
        "start_char":   "S",
        "end_char":     "E",
        "player_char":  "@",
    },
    "neon": {
        "wall":    Color.rgb(0, 255, 150),
        "passage": Color.rgb(5, 10, 20),
        "path":    Color.rgb(255, 220, 0),
        "visited": Color.rgb(50, 50, 180),
        "start":   Color.rgb(0, 255, 80),
        "end":     Color.rgb(255, 50, 50),
        "player":  Color.rgb(255, 100, 255),
        "wall_char":    "▓",
        "passage_char": " ",
        "path_char":    "·",
        "visited_char": "░",
        "start_char":   "S",
        "end_char":     "E",
        "player_char":  "☺",
    },
    "dungeon": {
        "wall":    Color.rgb(80, 60, 40),
        "passage": Color.rgb(20, 15, 10),
        "path":    Color.rgb(255, 180, 60),
        "visited": Color.rgb(40, 35, 50),
        "start":   Color.rgb(100, 220, 100),
        "end":     Color.rgb(220, 80, 80),
        "player":  Color.rgb(200, 180, 100),
        "wall_char":    "▓",
        "passage_char": "·",
        "path_char":    "•",
        "visited_char": "∙",
        "start_char":   "▶",
        "end_char":     "★",
        "player_char":  "♟",
    },
    "ocean": {
        "wall":    Color.rgb(0, 80, 160),
        "passage": Color.rgb(0, 170, 220),
        "path":    Color.rgb(255, 255, 100),
        "visited": Color.rgb(0, 120, 180),
        "start":   Color.rgb(100, 255, 200),
        "end":     Color.rgb(255, 150, 50),
        "player":  Color.rgb(255, 255, 255),
        "wall_char":    "▒",
        "passage_char": "~",
        "path_char":    "≈",
        "visited_char": "·",
        "start_char":   "⚓",
        "end_char":     "🏝",
        "player_char":  "⛵",
    },
    "matrix": {
        "wall":    Color.rgb(0, 40, 0),
        "passage": Color.rgb(0, 60, 0),
        "path":    Color.rgb(0, 255, 70),
        "visited": Color.rgb(0, 100, 0),
        "start":   Color.rgb(100, 255, 100),
        "end":     Color.rgb(255, 100, 100),
        "player":  Color.rgb(200, 255, 200),
        "wall_char":    "▓",
        "passage_char": "0",
        "path_char":    "1",
        "visited_char": "░",
        "start_char":   "[",
        "end_char":     "]",
        "player_char":  "¥",
    },
}


def render_maze(
    maze: Maze,
    theme_name: str = "classic",
    path: Optional[List[Tuple[int, int]]] = None,
    visited: Optional[List[Tuple[int, int]]] = None,
    player_pos: Optional[Tuple[int, int]] = None,
    fog_of_war: bool = False,
    reveal_radius: int = 3,
    color: bool = True,
) -> str:
    """Render maze as a colored ASCII string."""
    theme = THEMES.get(theme_name, THEMES["classic"])
    path_set: Set = set(path) if path else set()
    visited_set: Set = set(visited) if visited else set()
    revealed: Set = set()

    if fog_of_war and player_pos:
        pr, pc = player_pos
        for dr in range(-reveal_radius, reveal_radius + 1):
            for dc in range(-reveal_radius, reveal_radius + 1):
                if dr * dr + dc * dc <= reveal_radius * reveal_radius:
                    revealed.add((pr + dr, pc + dc))

    def c(color_str: str) -> str:
        return color_str if color else ""

    lines = []
    # Each cell is rendered as 2 rows × 2 cols of characters
    # Top-left pixel grid: (2*rows+1) × (2*cols+1)
    height = 2 * maze.rows + 1
    width  = 2 * maze.cols + 1

    grid = [[' '] * width for _ in range(height)]

    # Fill walls
    for gr in range(height):
        for gc in range(width):
            grid[gr][gc] = theme["wall_char"]

    # Carve passages
    for r in range(maze.rows):
        for c_idx in range(maze.cols):
            gr = 2 * r + 1
            gc = 2 * c_idx + 1
            grid[gr][gc] = theme["passage_char"]

            if not maze.has_wall(r, c_idx, Wall.SOUTH) and r + 1 < maze.rows:
                grid[gr + 1][gc] = theme["passage_char"]
            if not maze.has_wall(r, c_idx, Wall.EAST) and c_idx + 1 < maze.cols:
                grid[gr][gc + 1] = theme["passage_char"]

    def cell_color(r, c_idx):
        cell = (r, c_idx)
        if player_pos and cell == player_pos:
            return c(theme["player"])
        if cell == maze.start:
            return c(theme["start"])
        if cell == maze.end:
            return c(theme["end"])
        if cell in path_set:
            return c(theme["path"])
        if cell in visited_set:
            return c(theme["visited"])
        return c(theme["passage"])

    def cell_char(r, c_idx):
        cell = (r, c_idx)
        if player_pos and cell == player_pos:
            return theme["player_char"]
        if cell == maze.start:
            return theme["start_char"]
        if cell == maze.end:
            return theme["end_char"]
        if cell in path_set:
            return theme["path_char"]
        if cell in visited_set:
            return theme["visited_char"]
        return theme["passage_char"]

    # Build output
    output = []
    for gr in range(height):
        row_str = ""
        for gc in range(width):
            r = (gr - 1) // 2
            c_idx = (gc - 1) // 2
            is_cell = gr % 2 == 1 and gc % 2 == 1

            if fog_of_war and (r, c_idx) not in revealed and is_cell:
                row_str += c(theme["wall"]) + "▓" + c(Color.RESET)
                continue

            if is_cell:
                row_str += cell_color(r, c_idx) + cell_char(r, c_idx) + c(Color.RESET)
            else:
                ch = grid[gr][gc]
                if ch == theme["wall_char"]:
                    row_str += c(theme["wall"]) + ch + c(Color.RESET)
                else:
                    # This is a passage between cells — color based on adjacent cells
                    adj_r = gr // 2 if gr % 2 == 0 else (gr - 1) // 2
                    adj_c = gc // 2 if gc % 2 == 0 else (gc - 1) // 2
                    row_str += c(theme["passage"]) + ch + c(Color.RESET)
        output.append(row_str)

    return "\n".join(output)


def render_stats(maze: Maze, result=None, theme_name: str = "classic", color: bool = True) -> str:
    """Render statistics panel."""
    theme = THEMES.get(theme_name, THEMES["classic"])

    def c(color_str: str) -> str:
        return color_str if color else ""

    lines = [
        c(Color.BOLD) + c(Color.BRIGHT_CYAN) +
        "╔══════════════════════════════╗" + c(Color.RESET),
        c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
        c(Color.BOLD) + f"  {'LABYRINTHINE':^28}  " + c(Color.RESET) +
        c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
        c(Color.BRIGHT_CYAN) +
        "╠══════════════════════════════╣" + c(Color.RESET),
        c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
        f"  Size:    {maze.rows} × {maze.cols:<19}" +
        c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
        c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
        f"  Cells:   {maze.rows * maze.cols:<20}" +
        c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
    ]

    if result:
        lines += [
            c(Color.BRIGHT_CYAN) +
            "╠══════════════════════════════╣" + c(Color.RESET),
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
            c(Color.BOLD) + f"  {'SOLUTION':^28}  " + c(Color.RESET) +
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
            c(Color.BRIGHT_CYAN) +
            "╠══════════════════════════════╣" + c(Color.RESET),
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
            f"  Solver:  {result.algorithm[:20]:<20}" +
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
            f"  Path:    {result.path_length:<20}" +
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
            f"  Visited: {result.steps:<20}" +
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET) +
            f"  Eff:     {result.path_length/max(result.steps,1)*100:.1f}%{'':<17}" +
            c(Color.BRIGHT_CYAN) + "║" + c(Color.RESET),
        ]

    lines.append(c(Color.BRIGHT_CYAN) + "╚══════════════════════════════╝" + c(Color.RESET))
    return "\n".join(lines)
