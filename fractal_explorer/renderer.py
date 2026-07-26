"""Terminal rendering engine for fractals using rich."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich import box

# Character palettes ordered from dense (inside) to sparse (outside/escaped)
PALETTES = {
    "classic":   list(" .:-=+*#%@"),
    "blocks":    list(" ░▒▓█"),
    "dots":      list(" ·•●"),
    "minimal":   list(" .+#"),
    "matrix":    list(" .:;!|(){}[]"),
    "space":     list(" ·✦★"),
}

# Rich color schemes for iteration-count coloring
COLOR_SCHEMES = {
    "fire":     ["black", "dark_red", "red", "yellow", "bright_yellow", "white"],
    "ocean":    ["black", "navy_blue", "blue", "cyan", "bright_cyan", "white"],
    "forest":   ["black", "dark_green", "green", "yellow_green", "bright_green", "white"],
    "purple":   ["black", "dark_magenta", "magenta", "violet", "bright_magenta", "white"],
    "grayscale":["black", "grey11", "grey30", "grey50", "grey70", "white"],
    "rainbow":  ["red", "orange1", "yellow", "green", "cyan", "blue"],
}


def _iter_to_char(count: int, max_iter: int, palette: list[str]) -> str:
    """Map an iteration count to an ASCII character."""
    if count == 0:
        return palette[0]
    ratio = count / max_iter
    idx = int(ratio * (len(palette) - 1))
    return palette[min(idx, len(palette) - 1)]


def _iter_to_color(count: int, max_iter: int, scheme: list[str]) -> str:
    """Map an iteration count to a rich color name."""
    if count == 0:
        return scheme[0]
    ratio = count / max_iter
    idx = int(ratio * (len(scheme) - 1))
    return scheme[min(idx, len(scheme) - 1)]


def render_grid(
    grid: list[list[int]],
    max_iter: int,
    palette_name: str = "blocks",
    color_scheme: str = "fire",
    use_color: bool = True,
) -> Text:
    """Render an iteration-count grid as a rich Text object."""
    palette = PALETTES.get(palette_name, PALETTES["blocks"])
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["fire"])
    text = Text(no_wrap=True)

    for row in grid:
        for count in row:
            ch = _iter_to_char(count, max_iter, palette)
            if use_color:
                color = _iter_to_color(count, max_iter, colors)
                text.append(ch, style=color)
            else:
                text.append(ch)
        text.append("\n")
    return text


def render_sierpinski(rows: list[str], color: str = "green") -> Text:
    """Render a Sierpinski triangle row list as rich Text."""
    text = Text(no_wrap=True)
    for row in rows:
        for ch in row:
            if ch != " ":
                text.append(ch, style=color)
            else:
                text.append(" ")
        text.append("\n")
    return text


def render_dragon(grid: list[list[bool]], color: str = "cyan") -> Text:
    """Render a boolean dragon-curve grid as rich Text."""
    text = Text(no_wrap=True)
    for row in grid:
        for cell in row:
            text.append("█" if cell else " ", style=color if cell else "")
        text.append("\n")
    return text


def make_info_table(title: str, info: dict[str, str]) -> Table:
    """Build a small info table for fractal parameters."""
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 1))
    table.add_column("Key", style="bright_cyan", no_wrap=True)
    table.add_column("Value", style="white")
    for k, v in info.items():
        table.add_row(k, str(v))
    return table


def make_palette_row(palette_name: str, color_scheme: str, max_iter: int = 80) -> Text:
    """Render a color legend bar."""
    palette = PALETTES.get(palette_name, PALETTES["blocks"])
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["fire"])
    text = Text()
    text.append("Legend: ", style="bold")
    steps = max(len(palette), len(colors))
    for i in range(steps):
        pi = min(i, len(palette) - 1)
        ci = min(i, len(colors) - 1)
        text.append(palette[pi], style=colors[ci])
    text.append(f"  ({max_iter} max iterations)")
    return text
