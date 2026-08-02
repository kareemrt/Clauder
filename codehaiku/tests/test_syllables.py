"""Tests for the syllable counting module."""

import pytest
from codehaiku.syllables import count_syllables, split_identifier


class TestSplitIdentifier:
    def test_snake_case(self):
        assert split_identifier("get_user_data") == ["get", "user", "data"]

    def test_camel_case(self):
        assert split_identifier("getUserData") == ["get", "user", "data"]

    def test_pascal_case(self):
        assert split_identifier("GetUserData") == ["get", "user", "data"]

    def test_simple_word(self):
        assert split_identifier("parse") == ["parse"]

    def test_empty(self):
        assert split_identifier("") == []

    def test_kebab_case(self):
        assert split_identifier("get-user-data") == ["get", "user", "data"]

    def test_mixed(self):
        result = split_identifier("parseHTTPResponse")
        assert "parse" in result
        assert "response" in result


class TestCountSyllables:
    def test_known_exceptions(self):
        assert count_syllables("false") == 1
        assert count_syllables("return") == 2
        assert count_syllables("continue") == 3
        assert count_syllables("function") == 3

    def test_single_syllable(self):
        assert count_syllables("flow") == 1
        assert count_syllables("light") == 1
        assert count_syllables("call") == 1

    def test_two_syllable(self):
        assert count_syllables("broken") == 2
        assert count_syllables("silent") == 2
        assert count_syllables("error") == 2

    def test_three_syllable(self):
        assert count_syllables("silently") == 3
        assert count_syllables("beautiful") in (3, 4)

    def test_code_identifiers(self):
        assert count_syllables("getUserData") > 3
        assert count_syllables("parse_file") >= 2

    def test_minimum_one(self):
        assert count_syllables("x") >= 1
        assert count_syllables("a") >= 1

    def test_empty(self):
        assert count_syllables("") == 0
        assert count_syllables("   ") == 0

    def test_numbers_stripped(self):
        assert count_syllables("var1") >= 1
        assert count_syllables("node42") >= 1
