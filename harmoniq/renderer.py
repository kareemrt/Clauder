"""
Rendering engine — produces terminal art, piano rolls, and ASCII staff notation.
All output is pure Python, no dependencies required.
"""

from typing import List
from .composer import Composition, Note
from .theory import CHROMATIC

# ANSI colour codes
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_DIM    = "\033[2m"
_RED    = "\033[31m"
_GREEN  = "\033[32m"
_YELLOW = "\033[33m"
_BLUE   = "\033[34m"
_MAGENTA= "\033[35m"
_CYAN   = "\033[36m"
_WHITE  = "\033[37m"
_BG_DARK= "\033[48;5;235m"

NOTE_COLOURS = {
    "C":  _CYAN,
    "C#": _BLUE,
    "D":  _GREEN,
    "D#": _MAGENTA,
    "E":  _YELLOW,
    "F":  _RED,
    "F#": _RED,
    "G":  _CYAN,
    "G#": _BLUE,
    "A":  _GREEN,
    "A#": _MAGENTA,
    "B":  _YELLOW,
}

BLOCK_CHARS = {
    "sixteenth": "▪",
    "eighth":    "▬",
    "quarter":   "█",
    "half":      "██",
    "whole":     "████",
}

OCTAVE_ROWS = list(range(3, 7))  # octaves 3–6, bottom to top


def _coloured(text: str, colour: str) -> str:
    return f"{colour}{text}{_RESET}"


def render_piano_roll(comp: Composition, width: int = 72) -> str:
    """
    Renders a coloured horizontal piano-roll where:
      - each row = one octave (3 at bottom, 6 at top)
      - each column = one note event (not time-accurate, event-based)
      - block size reflects duration
    """
    notes = comp.all_notes()
    if not notes:
        return "(empty composition)"

    rows: dict[int, List[str]] = {oct_: [] for oct_ in reversed(OCTAVE_ROWS)}

    for note in notes:
        block = BLOCK_CHARS.get(note.duration_name, "█")
        colour = NOTE_COLOURS.get(note.name, _WHITE)
        cell = _coloured(block, colour + _BOLD)
        oct_key = max(OCTAVE_ROWS[0], min(OCTAVE_ROWS[-1], note.octave))
        rows[oct_key].append(cell)
        # fill other rows with dim dots to keep columns aligned
        for other_oct in OCTAVE_ROWS:
            if other_oct != oct_key:
                rows[other_oct].append(_coloured("·", _DIM))

    lines = []
    lines.append(_coloured(f"  ♩  Piano Roll — {comp.title}", _BOLD + _WHITE))
    lines.append(_coloured("  " + "─" * min(width, len(notes) * 1 + 4), _DIM))

    for oct_ in reversed(OCTAVE_ROWS):
        row_str = "".join(rows[oct_])
        label = _coloured(f"Oct {oct_} │", _DIM)
        lines.append(f"  {label} {row_str}")

    lines.append(_coloured("  " + "─" * min(width, len(notes) * 1 + 4), _DIM))
    return "\n".join(lines)


def render_ascii_staff(comp: Composition) -> str:
    """
    Renders a simplified 5-line ASCII music staff showing note heads.
    Maps pitch to vertical position on the staff (treble clef range).
    """
    notes = comp.all_notes()
    if not notes:
        return "(empty)"

    # Staff lines correspond to E4, G4, B4, D5, F5 (treble clef lines)
    STAFF_PITCHES = ["E", "F", "G", "A", "B", "C", "D", "E", "F"]
    STAFF_OCTAVES = [4,   4,   4,   4,   4,   5,   5,   5,   5]
    HEIGHT = 9  # 9 rows (5 lines + 4 spaces)

    columns: List[List[str]] = []
    for note in notes[:60]:  # cap at 60 notes for display
        col = ["─"] * HEIGHT
        # find the best row for this note
        for row_idx, (sp, so) in enumerate(zip(STAFF_PITCHES, STAFF_OCTAVES)):
            if note.name.replace("#", "") == sp and note.octave == so:
                col[row_idx] = "♩"
                break
        else:
            # out of range — put it at top or bottom
            col[0 if note.octave > 4 else HEIGHT - 1] = "♩"
        columns.append(col)

    # Draw the grid
    lines = []
    clef_lines = ["─", "─", "─", "─", "─", "─", "─", "─", "─"]
    staff_rows = {0, 2, 4, 6, 8}  # staff line positions

    lines.append(_coloured(f"\n  ♬  Staff View — {comp.title}", _BOLD + _WHITE))
    for row in range(HEIGHT):
        is_staff_line = row in staff_rows
        row_chars = []
        for col in columns:
            ch = col[row]
            if ch == "♩":
                row_chars.append(_coloured("♩", _YELLOW + _BOLD))
            elif is_staff_line:
                row_chars.append(_coloured("─", _DIM))
            else:
                row_chars.append(" ")
        prefix = "  𝄞  " if row == 4 else "     "
        lines.append(prefix + "".join(row_chars))

    return "\n".join(lines)


def render_waveform(comp: Composition, width: int = 68) -> str:
    """
    Renders the sequence values as a Unicode block-chart waveform.
    Higher values = taller bar. Great for visualising sequence shape.
    """
    seq = comp.source_sequence
    if not seq:
        return "(no sequence data)"

    max_val = max(seq) or 1
    chart_height = 8
    bar_chars = " ▁▂▃▄▅▆▇█"

    # Downsample if longer than display width
    if len(seq) > width:
        step = len(seq) / width
        seq = [seq[int(i * step)] for i in range(width)]

    lines = []
    lines.append(_coloured(f"\n  ∿  Sequence Waveform — {comp.source_name}", _BOLD + _CYAN))
    lines.append(_coloured(f"  max={max(comp.source_sequence)}  n={len(comp.source_sequence)}", _DIM))

    for row in range(chart_height, 0, -1):
        threshold = (row / chart_height) * max_val
        bar_line = ""
        for val in seq:
            ratio = val / max_val
            bar_index = int(ratio * (len(bar_chars) - 1))
            ch = bar_chars[bar_index]
            frac = val / max_val
            if frac > 0.75:
                colour = _RED
            elif frac > 0.5:
                colour = _YELLOW
            elif frac > 0.25:
                colour = _GREEN
            else:
                colour = _CYAN
            bar_line += _coloured(ch, colour)
        lines.append("  │" + bar_line)

    lines.append("  └" + _coloured("─" * len(seq), _DIM))
    return "\n".join(lines)


def render_summary_box(comp: Composition) -> str:
    """Renders a pretty summary box for a composition."""
    s = comp.summary()
    width = 52
    border = _coloured("╔" + "═" * width + "╗", _CYAN)
    footer = _coloured("╚" + "═" * width + "╝", _CYAN)

    def row(label: str, value: str) -> str:
        content = f"  {_coloured(label + ':', _DIM + _WHITE):<22} {_coloured(str(value), _BOLD + _YELLOW)}"
        return _coloured("║", _CYAN) + content.ljust(width + 30) + _coloured("║", _CYAN)

    title_line = f"  ♫  {s['title']}"
    title_row = _coloured("║", _CYAN) + _coloured(title_line.center(width), _BOLD + _WHITE) + _coloured("║", _CYAN)
    divider = _coloured("╠" + "═" * width + "╣", _CYAN)

    lines = [
        border,
        title_row,
        divider,
        row("Source Sequence", s["source"]),
        row("Scale / Mode",    s["scale"]),
        row("Tempo",           f"{s['tempo']} BPM"),
        row("Measures",        s["measures"]),
        row("Total Notes",     s["total_notes"]),
        row("Octave Range",    s["note_range"]),
        row("Density",         s["density"]),
        footer,
    ]
    return "\n".join(lines)
