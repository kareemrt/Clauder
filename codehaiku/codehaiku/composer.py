"""Haiku composition engine using extracted code words."""

import random
from dataclasses import dataclass

from .syllables import count_syllables
from .parser import ParseResult, WordEntry

# Poetic transforms: suffix replacements to make identifiers sound more poetic
POETIC_TRANSFORMS = {
    'ing': 'ing',
    'tion': 'tion',
    'ness': 'ness',
    'less': 'less',
    'ful': 'ful',
    'ment': 'ment',
    'er': 'er',
    'ed': 'ed',
    'ly': 'ly',
}

# Words that sound poetic and can be injected if needed
CONNECTOR_WORDS = {
    1: ['waits', 'flows', 'sleeps', 'seeks', 'falls', 'fades', 'breaks',
        'turns', 'calls', 'drifts', 'bends', 'holds', 'breathes', 'moves',
        'hides', 'glows', 'blooms', 'rests', 'burns', 'shines'],
    2: ['slowly', 'softly', 'gently', 'quietly', 'shadows', 'silence',
        'whispers', 'endless', 'hidden', 'broken', 'fading', 'waking',
        'flowing', 'beneath', 'between', 'through', 'ancient', 'beyond'],
    3: ['silently', 'wandering', 'endlessly', 'forgotten', 'awakening',
        'dissolving', 'returning', 'unfolding', 'vanishing', 'resonates'],
}


@dataclass
class Haiku:
    lines: tuple[str, str, str]
    syllable_counts: tuple[int, int, int]
    words_used: list[str]
    source_types: list[str]
    title: str = ""

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def is_valid(self) -> bool:
        return (self.syllable_counts[0] == 5
                and self.syllable_counts[1] == 7
                and self.syllable_counts[2] == 5)


def _score_word(entry: WordEntry) -> float:
    """Score a word by poetic quality."""
    w = entry.word
    score = 0.0

    # Prefer longer, more evocative words
    score += min(len(w) / 8, 1.5)

    # Prefer words from comments (more intentional)
    if entry.source == 'comment':
        score += 2.0
    elif entry.source == 'string':
        score += 1.0
    elif entry.source == 'docstring':
        score += 1.5

    # Prefer less frequent words (more specific/interesting)
    score += 1.0 / (entry.frequency + 1)

    # Bonus for evocative endings
    for suffix in ['ness', 'less', 'ment', 'tion', 'ing', 'ful']:
        if w.endswith(suffix):
            score += 0.5

    return score


def _build_word_bank(parse_result: ParseResult, seed: int = 0) -> list[tuple[str, int, str]]:
    """Build a sorted word bank of (word, syllables, source_type)."""
    seen = set()
    bank = []

    for entry in parse_result.words:
        w = entry.word.lower()
        if w in seen:
            continue
        seen.add(w)

        syl = count_syllables(w)
        if 1 <= syl <= 7:
            score = _score_word(entry)
            bank.append((w, syl, entry.source, score))

    # Sort by score descending
    bank.sort(key=lambda x: x[3], reverse=True)

    return [(w, s, src) for w, s, src, _ in bank]


def _find_line(word_bank: list[tuple[str, int, str]],
               target: int,
               used: set[str],
               rng: random.Random) -> tuple[list[str], list[str]] | None:
    """Find words that sum to exactly `target` syllables."""
    # Shuffle to get variety while still being deterministic
    shuffled = list(word_bank)
    rng.shuffle(shuffled)

    def search(remaining: int, idx: int, chosen: list, sources: list):
        if remaining == 0:
            return chosen, sources
        if remaining < 0 or idx >= len(shuffled):
            return None

        word, syl, src = shuffled[idx]

        # Try including this word
        if word not in used and syl <= remaining:
            used.add(word)
            result = search(remaining - syl, idx + 1, chosen + [word], sources + [src])
            if result:
                return result
            used.discard(word)

        # Try skipping this word
        return search(remaining, idx + 1, chosen, sources)

    return search(target, 0, [], [])


def _inject_connectors(word_bank: list[tuple[str, int, str]],
                       target: int,
                       used: set[str],
                       rng: random.Random,
                       connectors: dict) -> tuple[list[str], list[str]] | None:
    """Try building a line using connector words to fill gaps."""
    # Build augmented bank with connectors
    augmented = list(word_bank)
    for syl, words in connectors.items():
        for w in words:
            if w not in used:
                augmented.append((w, syl, 'connector'))

    rng.shuffle(augmented)

    def search(remaining: int, idx: int, chosen: list, sources: list):
        if remaining == 0:
            return chosen, sources
        if remaining < 0 or idx >= len(augmented):
            return None

        word, syl, src = augmented[idx]

        if word not in used and syl <= remaining:
            used.add(word)
            result = search(remaining - syl, idx + 1, chosen + [word], sources + [src])
            if result:
                return result
            used.discard(word)

        return search(remaining, idx + 1, chosen, sources)

    return search(target, 0, [], [])


def _format_line(words: list[str]) -> str:
    """Format a list of words into a haiku line."""
    if not words:
        return ""
    line = " ".join(words)
    return line[0].upper() + line[1:]


def compose_haiku(parse_result: ParseResult, seed: int = 42) -> Haiku | None:
    """Compose a single haiku from parsed code."""
    rng = random.Random(seed)
    word_bank = _build_word_bank(parse_result, seed)

    if len(word_bank) < 3:
        return None

    used_words: set[str] = set()

    line1_result = (_find_line(word_bank, 5, used_words, rng)
                    or _inject_connectors(word_bank, 5, used_words, rng, CONNECTOR_WORDS))
    if not line1_result:
        return None

    line1_words, line1_sources = line1_result
    used_words.update(line1_words)

    line2_result = (_find_line(word_bank, 7, used_words, rng)
                    or _inject_connectors(word_bank, 7, used_words, rng, CONNECTOR_WORDS))
    if not line2_result:
        return None

    line2_words, line2_sources = line2_result
    used_words.update(line2_words)

    line3_result = (_find_line(word_bank, 5, used_words, rng)
                    or _inject_connectors(word_bank, 5, used_words, rng, CONNECTOR_WORDS))
    if not line3_result:
        return None

    line3_words, line3_sources = line3_result
    used_words.update(line3_words)

    lines = (
        _format_line(line1_words),
        _format_line(line2_words),
        _format_line(line3_words),
    )

    syllable_counts = (
        sum(count_syllables(w) for w in line1_words),
        sum(count_syllables(w) for w in line2_words),
        sum(count_syllables(w) for w in line3_words),
    )

    all_words = line1_words + line2_words + line3_words
    all_sources = line1_sources + line2_sources + line3_sources

    return Haiku(
        lines=lines,
        syllable_counts=syllable_counts,
        words_used=all_words,
        source_types=all_sources,
    )


def compose_multiple(parse_result: ParseResult,
                     count: int = 3,
                     base_seed: int = 42) -> list[Haiku]:
    """Compose multiple haikus from the same parse result."""
    haikus = []
    attempts = 0
    max_attempts = count * 20

    while len(haikus) < count and attempts < max_attempts:
        seed = base_seed + attempts * 7
        haiku = compose_haiku(parse_result, seed=seed)
        if haiku and haiku.is_valid():
            haikus.append(haiku)
        attempts += 1

    return haikus
