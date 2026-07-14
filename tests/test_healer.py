"""Tests for the healer module (no API key required)."""

import re
from pathlib import Path

from clauder.healer import _extract_code_block, _build_fix_prompt
from clauder.runner import TestFailure


def test_extract_code_block_with_python_fence():
    text = """Here is the fix:
```python
def add(a, b):
    return a + b
```
This fixes the off-by-one error."""
    result = _extract_code_block(text)
    assert result is not None
    assert "def add" in result
    assert "return a + b" in result


def test_extract_code_block_with_bare_fence():
    text = "```\ndef foo():\n    pass\n```"
    result = _extract_code_block(text)
    assert result is not None
    assert "def foo" in result


def test_extract_code_block_no_fence():
    text = "No code block here, just text."
    result = _extract_code_block(text)
    assert result is None


def test_build_fix_prompt_contains_key_info():
    failure = TestFailure(
        test_id="tests/test_math.py::test_add",
        file_path="tests/test_math.py",
        line_number=5,
        error_type="AssertionError",
        error_message="assert 3 == 4",
        traceback="E  AssertionError: assert 3 == 4",
        source_file="clauder/math.py",
    )
    code = "def add(a, b):\n    return a - b\n"
    prompt = _build_fix_prompt(failure, code, "clauder/math.py")

    assert "test_add" in prompt
    assert "AssertionError" in prompt
    assert "assert 3 == 4" in prompt
    assert "def add" in prompt
    assert "clauder/math.py" in prompt
    assert "```python" in prompt


def test_build_fix_prompt_is_string():
    failure = TestFailure(
        test_id="test_foo",
        file_path="tests/test_foo.py",
        line_number=1,
        error_type="ValueError",
        error_message="bad value",
        traceback="",
    )
    result = _build_fix_prompt(failure, "pass\n", "foo.py")
    assert isinstance(result, str)
    assert len(result) > 100
