"""Parse unified git diffs into structured data."""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class HunkLine:
    content: str
    kind: str  # "added" | "removed" | "context"
    new_lineno: int | None = None
    old_lineno: int | None = None


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[HunkLine] = field(default_factory=list)

    @property
    def added_lines(self) -> list[str]:
        return [l.content for l in self.lines if l.kind == "added"]

    @property
    def removed_lines(self) -> list[str]:
        return [l.content for l in self.lines if l.kind == "removed"]


@dataclass
class FileDiff:
    path: str
    old_path: str | None
    hunks: list[Hunk] = field(default_factory=list)
    is_new: bool = False
    is_deleted: bool = False
    is_binary: bool = False

    @property
    def extension(self) -> str:
        return Path(self.path).suffix.lstrip(".")

    @property
    def added_count(self) -> int:
        return sum(len(h.added_lines) for h in self.hunks)

    @property
    def removed_count(self) -> int:
        return sum(len(h.removed_lines) for h in self.hunks)

    def to_review_text(self) -> str:
        """Render this file diff as a readable text block for the LLM."""
        lines = [f"### {self.path}"]
        if self.is_new:
            lines.append("(new file)")
        if self.is_deleted:
            lines.append("(deleted file)")
        for hunk in self.hunks:
            lines.append(
                f"@@ -{hunk.old_start},{hunk.old_count} "
                f"+{hunk.new_start},{hunk.new_count} @@"
            )
            for line in hunk.lines:
                prefix = {"added": "+", "removed": "-", "context": " "}[line.kind]
                lines.append(f"{prefix}{line.content}")
        return "\n".join(lines)


@dataclass
class ParsedDiff:
    files: list[FileDiff] = field(default_factory=list)

    @property
    def total_added(self) -> int:
        return sum(f.added_count for f in self.files)

    @property
    def total_removed(self) -> int:
        return sum(f.removed_count for f in self.files)

    @property
    def changed_files(self) -> list[str]:
        return [f.path for f in self.files]


_HUNK_HEADER = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"
)
_DIFF_HEADER = re.compile(r"^diff --git a/(.+) b/(.+)$")
_NEW_FILE = re.compile(r"^new file mode")
_DELETED_FILE = re.compile(r"^deleted file mode")
_BINARY = re.compile(r"^Binary files")
_OLD_PATH = re.compile(r"^--- a/(.+)$")
_NEW_PATH = re.compile(r"^\+\+\+ b/(.+)$")


def parse_diff(raw: str) -> ParsedDiff:
    """Parse a unified diff string into structured objects."""
    result = ParsedDiff()
    current_file: FileDiff | None = None
    current_hunk: Hunk | None = None
    old_lineno = 0
    new_lineno = 0

    for line in raw.splitlines():
        m = _DIFF_HEADER.match(line)
        if m:
            if current_file is not None:
                result.files.append(current_file)
            current_file = FileDiff(path=m.group(2), old_path=m.group(1))
            current_hunk = None
            continue

        if current_file is None:
            continue

        if _NEW_FILE.match(line):
            current_file.is_new = True
            continue
        if _DELETED_FILE.match(line):
            current_file.is_deleted = True
            continue
        if _BINARY.match(line):
            current_file.is_binary = True
            continue

        m = _HUNK_HEADER.match(line)
        if m:
            current_hunk = Hunk(
                old_start=int(m.group(1)),
                old_count=int(m.group(2) or 1),
                new_start=int(m.group(3)),
                new_count=int(m.group(4) or 1),
            )
            old_lineno = current_hunk.old_start
            new_lineno = current_hunk.new_start
            current_file.hunks.append(current_hunk)
            continue

        if current_hunk is None:
            continue

        if line.startswith("+") and not line.startswith("+++"):
            current_hunk.lines.append(
                HunkLine(content=line[1:], kind="added", new_lineno=new_lineno)
            )
            new_lineno += 1
        elif line.startswith("-") and not line.startswith("---"):
            current_hunk.lines.append(
                HunkLine(content=line[1:], kind="removed", old_lineno=old_lineno)
            )
            old_lineno += 1
        elif line.startswith(" "):
            current_hunk.lines.append(
                HunkLine(
                    content=line[1:],
                    kind="context",
                    old_lineno=old_lineno,
                    new_lineno=new_lineno,
                )
            )
            old_lineno += 1
            new_lineno += 1

    if current_file is not None:
        result.files.append(current_file)

    return result
