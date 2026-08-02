"""Source code parser that extracts meaningful words from code files."""

import re
import ast
from pathlib import Path
from dataclasses import dataclass, field

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "up", "about", "into", "through",
    "it", "its", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "shall", "this", "that",
    "these", "those", "i", "we", "you", "he", "she", "they", "who",
    "which", "what", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such",
    "no", "not", "only", "same", "so", "than", "too", "very", "just",
    "s", "t", "re", "ll", "ve", "d", "m", "o",
    "get", "set", "add", "run", "new", "old", "if", "else", "def",
    "class", "return", "import", "from", "as", "pass", "none",
    "true", "false", "null", "var", "let", "const", "fn", "pub",
    "self", "cls", "args", "kwargs", "tmp", "temp", "buf", "idx",
    "num", "str", "int", "bool", "list", "dict", "tuple", "type",
}

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 20


@dataclass
class WordEntry:
    word: str
    source: str  # 'identifier', 'comment', 'string', 'docstring'
    frequency: int = 1
    syllables: int = 0


@dataclass
class ParseResult:
    words: list[WordEntry] = field(default_factory=list)
    file_path: str = ""
    language: str = ""
    line_count: int = 0
    identifier_count: int = 0
    comment_count: int = 0


LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.jsx': 'javascript',
    '.rs': 'rust',
    '.go': 'go',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.rb': 'ruby',
    '.sh': 'shell',
    '.cs': 'csharp',
    '.kt': 'kotlin',
    '.swift': 'swift',
    '.php': 'php',
    '.lua': 'lua',
    '.r': 'r',
}


def _extract_words_from_text(text: str) -> list[str]:
    """Extract meaningful words from arbitrary text."""
    # Split on whitespace and common delimiters
    tokens = re.findall(r'[a-zA-Z][a-zA-Z_\-]{2,}', text)
    words = []

    for token in tokens:
        # Split camelCase
        split = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', token)
        split = re.sub(r'([a-z\d])([A-Z])', r'\1 \2', split)
        parts = re.split(r'[_\-\s]+', split)
        for part in parts:
            w = part.lower().strip()
            if (MIN_WORD_LENGTH <= len(w) <= MAX_WORD_LENGTH
                    and w not in STOP_WORDS
                    and not w.isdigit()
                    and re.match(r'^[a-z]+$', w)):
                words.append(w)

    return words


def _parse_python(source: str) -> tuple[list[tuple[str, str]], int]:
    """Parse Python source and return (word, source_type) pairs."""
    results = []
    line_count = source.count('\n') + 1

    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                words = _extract_words_from_text(node.name)
                results.extend((w, 'identifier') for w in words)
                for arg in node.args.args:
                    words = _extract_words_from_text(arg.arg)
                    results.extend((w, 'identifier') for w in words)
            elif isinstance(node, ast.ClassDef):
                words = _extract_words_from_text(node.name)
                results.extend((w, 'identifier') for w in words)
            elif isinstance(node, (ast.Name, ast.Attribute)):
                name = node.id if isinstance(node, ast.Name) else node.attr
                words = _extract_words_from_text(name)
                results.extend((w, 'identifier') for w in words)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                if len(node.value) > 10:
                    words = _extract_words_from_text(node.value)
                    results.extend((w, 'string') for w in words)
    except SyntaxError:
        pass

    # Extract comments
    for line in source.splitlines():
        if '#' in line:
            comment = line[line.index('#') + 1:]
            words = _extract_words_from_text(comment)
            results.extend((w, 'comment') for w in words)

    return results, line_count


def _parse_generic(source: str, comment_chars: list[str]) -> tuple[list[tuple[str, str]], int]:
    """Generic parser for other languages."""
    results = []
    line_count = source.count('\n') + 1

    for line in source.splitlines():
        stripped = line.strip()

        # Detect comments
        is_comment = any(stripped.startswith(c) for c in comment_chars)
        if is_comment:
            words = _extract_words_from_text(stripped[2:] if len(stripped) > 2 else '')
            results.extend((w, 'comment') for w in words)
        else:
            words = _extract_words_from_text(stripped)
            results.extend((w, 'identifier') for w in words)

    return results, line_count


def parse_file(file_path: str) -> ParseResult:
    """Parse a source code file and extract meaningful words."""
    path = Path(file_path)
    ext = path.suffix.lower()
    language = LANGUAGE_MAP.get(ext, 'unknown')

    result = ParseResult(file_path=str(path), language=language)

    try:
        source = path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return result

    result.line_count = source.count('\n') + 1

    comment_chars = {
        'python': ['#'],
        'javascript': ['//', '/*'],
        'typescript': ['//', '/*'],
        'rust': ['//', '/*'],
        'go': ['//', '/*'],
        'java': ['//', '/*'],
        'cpp': ['//', '/*'],
        'c': ['//', '/*'],
        'ruby': ['#'],
        'shell': ['#'],
        'csharp': ['//', '/*'],
    }

    if language == 'python':
        word_pairs, _ = _parse_python(source)
    else:
        chars = comment_chars.get(language, ['#', '//'])
        word_pairs, _ = _parse_generic(source, chars)

    # Aggregate words by type
    word_map: dict[tuple[str, str], int] = {}
    for word, source_type in word_pairs:
        key = (word, source_type)
        word_map[key] = word_map.get(key, 0) + 1

    result.words = [
        WordEntry(word=w, source=s, frequency=f)
        for (w, s), f in word_map.items()
    ]

    result.identifier_count = sum(1 for e in result.words if e.source == 'identifier')
    result.comment_count = sum(1 for e in result.words if e.source == 'comment')

    return result


def parse_source_string(source: str, language: str = 'python') -> ParseResult:
    """Parse source code from a string directly."""
    result = ParseResult(language=language)

    if language == 'python':
        word_pairs, line_count = _parse_python(source)
    else:
        chars = ['#', '//']
        word_pairs, line_count = _parse_generic(source, chars)

    result.line_count = line_count

    word_map: dict[tuple[str, str], int] = {}
    for word, source_type in word_pairs:
        key = (word, source_type)
        word_map[key] = word_map.get(key, 0) + 1

    result.words = [
        WordEntry(word=w, source=s, frequency=f)
        for (w, s), f in word_map.items()
    ]

    return result
