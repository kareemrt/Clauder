"""Beautiful terminal display for CodeHaiku."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.padding import Padding

from .composer import Haiku

console = Console()

BANNER = r"""
  ██████╗ ██████╗ ██████╗ ███████╗
 ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║     ██║   ██║██║  ██║█████╗
 ██║     ██║   ██║██║  ██║██╔══╝
 ╚██████╗╚██████╔╝██████╔╝███████╗
  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
 ██╗  ██╗ █████╗ ██╗██╗  ██╗██╗   ██╗
 ██║  ██║██╔══██╗██║██║ ██╔╝██║   ██║
 ███████║███████║██║█████╔╝ ██║   ██║
 ██╔══██║██╔══██║██║██╔═██╗ ██║   ██║
 ██║  ██║██║  ██║██║██║  ██╗╚██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝
"""

SOURCE_COLORS = {
    'identifier': 'cyan',
    'comment': 'green',
    'string': 'yellow',
    'docstring': 'magenta',
    'connector': 'dim white',
}


def print_banner():
    """Print the CodeHaiku ASCII art banner."""
    text = Text(BANNER, style="bold blue", justify="center")
    console.print(text)
    console.print(
        Align.center(
            Text("✦ Poetry distilled from code ✦", style="italic dim cyan")
        )
    )
    console.print()


def _build_haiku_text(haiku: Haiku, show_syllables: bool = False) -> Text:
    """Build a styled Rich Text object for a haiku."""
    text = Text()

    for i, (line, syl_count, words_in_line) in enumerate(
        zip(haiku.lines, haiku.syllable_counts, _split_lines(haiku))
    ):
        if show_syllables:
            text.append(f"({syl_count}) ", style="dim")

        # Color words by their source type
        word_sources = dict(zip(haiku.words_used, haiku.source_types))
        words = line.split()
        for j, word in enumerate(words):
            w_lower = word.lower()
            src = word_sources.get(w_lower, 'identifier')
            color = SOURCE_COLORS.get(src, 'white')
            text.append(word, style=f"bold {color}")
            if j < len(words) - 1:
                text.append(" ")

        if i < 2:
            text.append("\n")

    return text


def _split_lines(haiku: Haiku) -> list[list[str]]:
    """Split haiku words back into per-line groups."""
    line_words = [[], [], []]
    word_counts = [len(line.split()) for line in haiku.lines]

    idx = 0
    for line_i, count in enumerate(word_counts):
        line_words[line_i] = haiku.words_used[idx:idx + count]
        idx += count

    return line_words


def print_haiku(haiku: Haiku,
                title: str = "",
                show_syllables: bool = False,
                number: int | None = None):
    """Print a single haiku in a beautiful panel."""
    title_str = title or "~ code haiku ~"
    if number is not None:
        title_str = f"[dim]#{number}[/dim]  {title_str}"

    haiku_text = _build_haiku_text(haiku, show_syllables)

    panel = Panel(
        Align.center(haiku_text),
        title=f"[bold magenta]{title_str}[/bold magenta]",
        border_style="blue",
        box=box.DOUBLE_EDGE,
        padding=(1, 4),
    )
    console.print(panel)


def print_haiku_gallery(haikus: list[Haiku],
                        file_path: str = "",
                        show_syllables: bool = False):
    """Print multiple haikus in a gallery layout."""
    if not haikus:
        console.print("[dim]No haikus could be composed from this source.[/dim]")
        return

    console.print()
    if file_path:
        console.print(Rule(f"[bold cyan]{file_path}[/bold cyan]", style="dim blue"))
    else:
        console.print(Rule("[bold cyan]Code Poetry[/bold cyan]", style="dim blue"))
    console.print()

    for i, haiku in enumerate(haikus, 1):
        print_haiku(haiku, show_syllables=show_syllables, number=i)
        console.print()


def print_word_cloud(haiku: Haiku):
    """Print an analysis of words used in the haiku."""
    table = Table(
        title="Word Origins",
        box=box.SIMPLE_HEAD,
        border_style="dim",
        show_header=True,
    )
    table.add_column("Word", style="bold white")
    table.add_column("Syllables", justify="center", style="dim")
    table.add_column("Source", justify="center")

    from .syllables import count_syllables

    word_src = dict(zip(haiku.words_used, haiku.source_types))
    for word in haiku.words_used:
        src = word_src.get(word, 'identifier')
        syl = count_syllables(word)
        color = SOURCE_COLORS.get(src, 'white')
        table.add_row(
            word,
            str(syl),
            f"[{color}]{src}[/{color}]",
        )

    console.print(table)


def print_stats(file_path: str, line_count: int, haiku_count: int,
                identifier_count: int, comment_count: int):
    """Print file statistics."""
    table = Table(box=box.MINIMAL, show_header=False, border_style="dim")
    table.add_column("Metric", style="dim cyan")
    table.add_column("Value", style="bold white")

    table.add_row("File", file_path)
    table.add_row("Lines", str(line_count))
    table.add_row("Identifiers extracted", str(identifier_count))
    table.add_row("Comment words", str(comment_count))
    table.add_row("Haikus composed", str(haiku_count))

    console.print(Padding(table, (0, 2)))


def print_error(msg: str):
    console.print(f"[bold red]✗[/bold red] {msg}")


def print_success(msg: str):
    console.print(f"[bold green]✓[/bold green] {msg}")


def print_info(msg: str):
    console.print(f"[dim cyan]→[/dim cyan] {msg}")
