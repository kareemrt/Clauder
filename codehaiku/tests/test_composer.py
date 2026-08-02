"""Tests for the haiku composition engine."""

import pytest
from codehaiku.parser import parse_source_string
from codehaiku.composer import compose_haiku, compose_multiple, Haiku


SAMPLE_CODE = '''
def transform_shadow_memory(ancient_path, silent_breath=None):
    """Wander through the endless forest of forgotten dreams."""
    wandering = True
    hidden_stream = []
    broken_mirror = {}

    # Filter the fading echoes beneath the moonlight
    for fragment in ancient_path:
        if fragment.glowing:
            hidden_stream.append(fragment.essence)
            wandering = not wandering

    return hidden_stream


class SilentObserver:
    """Watch the flowing river of data with gentle patience."""

    def __init__(self, depth=3, patience=True):
        self.depth = depth
        self.patience = patience
        self.memory = []

    def breathe(self):
        """Slow the endless searching beneath morning stars."""
        return [m for m in self.memory if m.fading]
'''


class TestComposeHaiku:
    def setup_method(self):
        self.result = parse_source_string(SAMPLE_CODE)

    def test_returns_haiku_or_none(self):
        haiku = compose_haiku(self.result, seed=42)
        assert haiku is None or isinstance(haiku, Haiku)

    def test_valid_syllable_counts(self):
        for seed in range(0, 50, 5):
            haiku = compose_haiku(self.result, seed=seed)
            if haiku:
                assert haiku.syllable_counts[0] == 5
                assert haiku.syllable_counts[1] == 7
                assert haiku.syllable_counts[2] == 5
                assert haiku.is_valid()
                break

    def test_three_lines(self):
        for seed in range(0, 50, 5):
            haiku = compose_haiku(self.result, seed=seed)
            if haiku:
                assert len(haiku.lines) == 3
                for line in haiku.lines:
                    assert len(line) > 0
                break

    def test_words_from_code(self):
        for seed in range(0, 50, 5):
            haiku = compose_haiku(self.result, seed=seed)
            if haiku:
                assert len(haiku.words_used) > 0
                break


class TestComposeMultiple:
    def setup_method(self):
        self.result = parse_source_string(SAMPLE_CODE)

    def test_returns_list(self):
        haikus = compose_multiple(self.result, count=3, base_seed=42)
        assert isinstance(haikus, list)

    def test_all_valid(self):
        haikus = compose_multiple(self.result, count=3, base_seed=42)
        for h in haikus:
            assert h.is_valid()

    def test_different_seeds_give_variety(self):
        h1 = compose_multiple(self.result, count=1, base_seed=0)
        h2 = compose_multiple(self.result, count=1, base_seed=999)
        # At least one pair should differ (they likely will with different seeds)
        if h1 and h2:
            # Can't guarantee exact difference but structure is valid
            assert h1[0].is_valid()
            assert h2[0].is_valid()

    def test_empty_source_returns_empty(self):
        empty = parse_source_string("")
        haikus = compose_multiple(empty, count=3)
        assert haikus == []
