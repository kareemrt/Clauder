"""Tests for the test runner parser."""

from clauder.runner import (
    _extract_error,
    _extract_location,
    _infer_source_file,
    _parse_counts,
    _parse_pytest_failures,
)

SAMPLE_OUTPUT = """
============================= test session starts ==============================
platform linux -- Python 3.11.15
collected 3 items

tests/test_math.py::test_add PASSED
tests/test_math.py::test_subtract FAILED
tests/test_math.py::test_multiply FAILED

=================================== FAILURES ===================================
________________________________ test_subtract _________________________________

    def test_subtract():
>       assert subtract(10, 3) == 7
E       AssertionError: assert 4 == 7
E       where 4 = subtract(10, 3)

tests/test_math.py:12: AssertionError
________________________________ test_multiply _________________________________

    def test_multiply():
>       assert multiply(3, 4) == 12
E       TypeError: multiply() takes 1 positional argument but 2 were given

tests/test_math.py:17: TypeError
=========================== 2 failed, 1 passed in 0.05s ============================
"""


def test_parse_counts():
    total, failed = _parse_counts(SAMPLE_OUTPUT)
    assert failed == 2
    assert total == 3


def test_parse_failures_count():
    failures = _parse_pytest_failures(SAMPLE_OUTPUT)
    assert len(failures) == 2


def test_parse_failure_test_ids():
    failures = _parse_pytest_failures(SAMPLE_OUTPUT)
    ids = {f.test_id for f in failures}
    assert "test_subtract" in ids
    assert "test_multiply" in ids


def test_extract_location():
    block = "tests/test_math.py:12: AssertionError"
    path, line = _extract_location(block)
    assert path == "tests/test_math.py"
    assert line == 12


def test_extract_error_assertion():
    block = "E       AssertionError: assert 4 == 7\ntests/test_math.py:12: AssertionError"
    etype, emsg = _extract_error(block)
    assert etype == "AssertionError"
    assert "4" in emsg


def test_extract_error_type_error():
    block = "E       TypeError: multiply() takes 1 positional argument but 2 were given"
    etype, emsg = _extract_error(block)
    assert etype == "TypeError"
    assert "positional" in emsg


def test_extract_counts_no_failures():
    output = "====== 5 passed in 0.12s ======"
    total, failed = _parse_counts(output)
    assert failed == 0
    assert total == 5


def test_infer_source_file_prefers_non_test():
    block = "clauder/math.py:5:\ntests/test_math.py:12: AssertionError"
    result = _infer_source_file(block, "tests/test_math.py")
    assert result == "clauder/math.py"
