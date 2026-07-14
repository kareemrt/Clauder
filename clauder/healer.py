"""Core healing logic — uses Claude to fix failing tests autonomously."""

import os
import re
from pathlib import Path

import anthropic

from .runner import RunResult, TestFailure, run_tests
from .ui import console, error, info, success, thinking, warn, show_diff


class HealerConfig:
    def __init__(
        self,
        test_command: str = "pytest -v",
        max_iterations: int = 5,
        dry_run: bool = False,
        model: str = "claude-sonnet-5",
        auto_apply: bool = True,
    ):
        self.test_command = test_command
        self.max_iterations = max_iterations
        self.dry_run = dry_run
        self.model = model
        self.auto_apply = auto_apply


class Healer:
    def __init__(self, config: HealerConfig, cwd: Path):
        self.config = config
        self.cwd = cwd
        self._client: anthropic.Anthropic | None = None
        self.fix_history: list[dict] = []

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY environment variable is not set.\n"
                    "Export it with: export ANTHROPIC_API_KEY=your_key_here"
                )
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def heal(self) -> tuple[bool, int, int]:
        """
        Run the healing loop. Returns (success, iterations_used, fixes_applied).
        """
        fixes_applied = 0
        result = None

        for iteration in range(1, self.config.max_iterations + 1):
            info(f"[bold]Iteration {iteration}/{self.config.max_iterations}[/] — running tests…")
            result = run_tests(self.config.test_command, self.cwd)

            if result.passed:
                success(f"All tests pass! (after {iteration - 1} fix{'es' if fixes_applied != 1 else ''})")
                return True, iteration - 1, fixes_applied

            warn(f"{result.failed_count} test(s) failing.")

            if not result.failures:
                error("Tests failed but no structured failures could be parsed. Check test output manually.")
                console.print(result.stdout[-2000:])
                break

            for failure in result.failures:
                fixed = self._heal_failure(failure)
                if fixed:
                    fixes_applied += 1

        # Final run
        final = run_tests(self.config.test_command, self.cwd)
        return final.passed, self.config.max_iterations, fixes_applied

    def _heal_failure(self, failure: TestFailure) -> bool:
        """Ask Claude to fix a single test failure. Returns True if a fix was applied."""
        thinking(f"Analyzing failure: [cyan]{failure.test_id}[/]")

        target_file = failure.source_file or failure.file_path
        if not target_file:
            warn(f"Cannot locate source file for {failure.test_id}")
            return False

        file_path = self.cwd / target_file
        if not file_path.exists():
            # Try relative path from cwd
            candidates = list(self.cwd.rglob(Path(target_file).name))
            if candidates:
                file_path = candidates[0]
            else:
                warn(f"Source file not found: {target_file}")
                return False

        original_code = file_path.read_text()

        prompt = _build_fix_prompt(failure, original_code, str(file_path.relative_to(self.cwd)))

        thinking("Asking Claude for a fix…")
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.APIError as exc:
            error(f"Claude API error: {exc}")
            return False

        raw = response.content[0].text
        fixed_code = _extract_code_block(raw)

        if not fixed_code or fixed_code.strip() == original_code.strip():
            warn("Claude did not return a usable code fix.")
            console.print(f"[dim]{raw[:500]}[/dim]")
            return False

        show_diff(original_code, fixed_code, file_path.name)

        if self.config.dry_run:
            warn("Dry-run mode: fix NOT applied.")
            return False

        if not self.config.auto_apply:
            apply = console.input("[bold yellow]Apply this fix? [y/N] [/]")
            if apply.strip().lower() != "y":
                warn("Fix skipped.")
                return False

        file_path.write_text(fixed_code)
        success(f"Fix applied to [cyan]{file_path.relative_to(self.cwd)}[/]")

        self.fix_history.append({
            "test_id": failure.test_id,
            "file": str(file_path.relative_to(self.cwd)),
            "error_type": failure.error_type,
            "error_message": failure.error_message,
        })
        return True


def _build_fix_prompt(failure: TestFailure, code: str, filename: str) -> str:
    return f"""You are an expert Python debugging assistant. A test is failing and you must fix the source code.

## Failing Test
Test ID: `{failure.test_id}`
File: `{failure.file_path}` (line {failure.line_number})

## Error
```
{failure.error_type}: {failure.error_message}
```

## Full Traceback
```
{failure.traceback}
```

## Source File: `{filename}`
```python
{code}
```

## Instructions
1. Identify the root cause of the failure in the source file above.
2. Fix ONLY the minimal change necessary to make the test pass.
3. Do NOT change function signatures, add new functions, or alter logic beyond what is required.
4. Return the COMPLETE fixed file wrapped in a ```python code block.
5. After the code block, write a one-sentence explanation of the fix.

Fix the code now:"""


def _extract_code_block(text: str) -> str | None:
    """Extract the first ```python ... ``` block from Claude's response."""
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1)
    # Fallback: bare ``` block
    m2 = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
    if m2:
        return m2.group(1)
    return None
