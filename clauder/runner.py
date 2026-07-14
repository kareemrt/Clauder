"""Test runner abstraction — captures output and parses failures."""

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestFailure:
    test_id: str
    file_path: str
    line_number: int | None
    error_type: str
    error_message: str
    traceback: str
    source_file: str | None = None  # the actual .py file that needs fixing


@dataclass
class RunResult:
    passed: bool
    stdout: str
    stderr: str
    failures: list[TestFailure] = field(default_factory=list)
    total: int = 0
    failed_count: int = 0
    duration: float = 0.0


def run_tests(command: str, cwd: Path) -> RunResult:
    """Run a test command and return structured results."""
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        stdout = proc.stdout
        stderr = proc.stderr
        passed = proc.returncode == 0
    except subprocess.TimeoutExpired:
        return RunResult(passed=False, stdout="", stderr="Test command timed out after 120s.")
    except Exception as exc:
        return RunResult(passed=False, stdout="", stderr=str(exc))

    failures = _parse_pytest_failures(stdout + stderr)
    total, failed_count = _parse_counts(stdout + stderr)

    return RunResult(
        passed=passed,
        stdout=stdout,
        stderr=stderr,
        failures=failures,
        total=total,
        failed_count=failed_count,
    )


def _parse_pytest_failures(output: str) -> list[TestFailure]:
    failures: list[TestFailure] = []

    # Split on pytest failure sections (===== FAILURES =====)
    failure_blocks = re.split(r"_{5,}\s+(\S+)\s+_{5,}", output)

    # failure_blocks: [pre, test_id, block, test_id, block, ...]
    i = 1
    while i < len(failure_blocks) - 1:
        test_id = failure_blocks[i].strip()
        block = failure_blocks[i + 1]
        i += 2

        file_path, line_number = _extract_location(block)
        error_type, error_message = _extract_error(block)
        source_file = _infer_source_file(block, file_path)

        failures.append(TestFailure(
            test_id=test_id,
            file_path=file_path or "",
            line_number=line_number,
            error_type=error_type,
            error_message=error_message,
            traceback=block.strip(),
            source_file=source_file,
        ))

    return failures


def _extract_location(block: str) -> tuple[str | None, int | None]:
    # Match lines like:   tests/test_foo.py:42: AssertionError
    m = re.search(r"([\w/\\.\-]+\.py):(\d+):", block)
    if m:
        return m.group(1), int(m.group(2))
    return None, None


def _extract_error(block: str) -> tuple[str, str]:
    # Last "E  ..." lines contain the actual error
    e_lines = re.findall(r"^E\s+(.+)$", block, re.MULTILINE)
    if not e_lines:
        return "UnknownError", block[-500:].strip()

    error_line = e_lines[-1].strip()
    m = re.match(r"(\w+(?:\.\w+)*(?:Error|Exception|Warning|Fault)):\s*(.*)", error_line)
    if m:
        return m.group(1), m.group(2)
    return "AssertionError", error_line


def _infer_source_file(block: str, test_file: str | None) -> str | None:
    """Find the non-test source file referenced in the traceback."""
    candidates = re.findall(r"([\w/\\.\-]+\.py):\d+:", block)
    for c in candidates:
        if c and "test_" not in Path(c).name and c != test_file:
            return c
    return test_file  # fallback to test file itself


def _parse_counts(output: str) -> tuple[int, int]:
    # "5 failed, 3 passed in 1.23s"
    m = re.search(r"(\d+) failed", output)
    failed = int(m.group(1)) if m else 0
    m2 = re.search(r"(\d+) passed", output)
    passed = int(m2.group(1)) if m2 else 0
    return failed + passed, failed
