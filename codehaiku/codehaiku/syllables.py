"""Syllable counting for English words and code identifiers."""

import re

EXCEPTIONS = {
    "def": 1, "class": 1, "return": 2, "import": 2, "from": 1,
    "true": 1, "false": 1, "none": 1, "null": 1, "async": 2,
    "await": 2, "lambda": 2, "yield": 1, "raise": 1, "pass": 1,
    "break": 1, "continue": 3, "while": 1, "for": 1, "if": 1,
    "else": 1, "elif": 2, "try": 1, "except": 2, "finally": 3,
    "with": 1, "as": 1, "in": 1, "not": 1, "and": 1, "or": 1,
    "is": 1, "global": 2, "nonlocal": 3, "del": 1, "assert": 2,
    "the": 1, "a": 1, "an": 1, "it": 1, "be": 1, "do": 1,
    "go": 1, "we": 1, "he": 1, "she": 1, "they": 1, "you": 1,
    "data": 2, "node": 1, "type": 1, "code": 1, "file": 1,
    "line": 1, "name": 1, "time": 1, "string": 1, "list": 1,
    "dict": 1, "set": 1, "map": 1, "key": 1, "value": 3,
    "index": 2, "count": 1, "size": 1, "length": 2, "width": 1,
    "height": 1, "depth": 1, "level": 2, "state": 1, "mode": 1,
    "error": 2, "result": 2, "output": 2, "input": 2, "item": 2,
    "object": 2, "function": 3, "method": 2, "module": 2, "variable": 4,
    "create": 2, "update": 2, "delete": 2, "insert": 2, "select": 2,
    "parse": 1, "load": 1, "save": 1, "read": 1, "write": 1,
    "close": 1, "open": 2, "find": 1, "check": 1, "make": 1,
    "run": 1, "start": 1, "stop": 1, "init": 2, "setup": 2,
    "process": 2, "handle": 2, "get": 1, "set": 1, "add": 1,
    "remove": 2, "clear": 1, "reset": 2, "sort": 1, "filter": 2,
    "reduce": 2, "split": 1, "join": 1, "merge": 1, "copy": 2,
    "move": 1, "push": 1, "pop": 1, "peek": 1, "next": 1,
    "prev": 1, "first": 1, "last": 1, "new": 1, "old": 1,
    "min": 1, "max": 1, "sum": 1, "avg": 1, "total": 2,
    "base": 1, "child": 1, "parent": 2, "root": 1, "tree": 1,
    "graph": 1, "path": 1, "link": 1, "edge": 1, "vertex": 2,
    "cache": 1, "queue": 1, "stack": 1, "heap": 1, "array": 2,
    "buffer": 2, "stream": 1, "batch": 1, "chunk": 1, "block": 1,
    "token": 2, "char": 1, "byte": 1, "bit": 1, "flag": 1,
    "mask": 1, "hash": 1, "id": 1, "uuid": 4, "url": 3,
    "api": 3, "ui": 2, "io": 2, "os": 2, "db": 2,
    "sql": 3, "json": 2, "xml": 3, "csv": 3, "pdf": 3,
    "html": 4, "css": 3, "js": 2, "py": 2, "ts": 2,
    "beautiful": 4, "silence": 2, "ancient": 2, "broken": 2,
    "empty": 2, "hidden": 2, "infinite": 3, "sacred": 2,
    "shadow": 2, "gentle": 2, "fragile": 2, "simple": 2,
    "quiet": 2, "peaceful": 2, "flowing": 2, "seeking": 2,
    "drifting": 2, "falling": 2, "rising": 2, "fading": 2,
    "breathing": 2, "sleeping": 2, "waking": 2, "dancing": 2,
}


def split_identifier(word: str) -> list[str]:
    """Split code identifiers into component words."""
    word = word.strip()
    if not word:
        return []

    # snake_case and kebab-case
    parts = re.split(r'[_\-\s]+', word)

    # camelCase and PascalCase
    result = []
    for part in parts:
        if not part:
            continue
        split = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', part)
        split = re.sub(r'([a-z\d])([A-Z])', r'\1 \2', split)
        result.extend(split.split())

    return [p.lower() for p in result if p]


def _count_single_word(word: str) -> int:
    """Count syllables in a single lowercase English word."""
    word = word.lower().strip()
    if not word:
        return 0

    if word in EXCEPTIONS:
        return EXCEPTIONS[word]

    if len(word) <= 2:
        return 1

    # Remove trailing silent 'e'
    if word.endswith('le') and len(word) > 3 and word[-3] not in 'aeiou':
        count = 1
        word = word[:-2]
    elif word.endswith('e') and not word.endswith('ee') and len(word) > 2:
        word = word[:-1]
        count = 0
    else:
        count = 0

    vowels = set('aeiouy')
    i = 0
    while i < len(word):
        if word[i] in vowels:
            count += 1
            while i < len(word) and word[i] in vowels:
                i += 1
        else:
            i += 1

    # Handle specific endings
    if word.endswith('ion'):
        count += 1
    if word.endswith('ious') or word.endswith('eous'):
        count += 1

    return max(1, count)


def count_syllables(word: str) -> int:
    """Count total syllables in a word or code identifier."""
    if not word or not word.strip():
        return 0

    # Remove non-alpha characters
    cleaned = re.sub(r'[^a-zA-Z_\-]', '', word)
    if not cleaned:
        return 0

    parts = split_identifier(cleaned)
    if not parts:
        return 1

    return sum(_count_single_word(p) for p in parts)
