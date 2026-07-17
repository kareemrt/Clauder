"""Git operations for extracting diffs and file contents."""

import subprocess
from pathlib import Path


class GitError(Exception):
    pass


def _run(args: list[str], cwd: str | None = None) -> str:
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=cwd or str(Path.cwd()),
    )
    if result.returncode != 0:
        raise GitError(result.stderr.strip() or f"git command failed: {' '.join(args)}")
    return result.stdout


def get_staged_diff(cwd: str | None = None) -> str:
    return _run(["git", "diff", "--cached"], cwd=cwd)


def get_unstaged_diff(cwd: str | None = None) -> str:
    return _run(["git", "diff"], cwd=cwd)


def get_all_diff(cwd: str | None = None) -> str:
    staged = get_staged_diff(cwd)
    unstaged = get_unstaged_diff(cwd)
    return "\n".join(filter(None, [staged, unstaged]))


def get_commit_diff(commit: str, cwd: str | None = None) -> str:
    return _run(["git", "diff", f"{commit}^", commit], cwd=cwd)


def get_branch_diff(base: str = "main", cwd: str | None = None) -> str:
    try:
        return _run(["git", "diff", f"{base}...HEAD"], cwd=cwd)
    except GitError:
        return _run(["git", "diff", f"origin/{base}...HEAD"], cwd=cwd)


def get_file_content(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        raise GitError(f"Cannot read file: {e}") from e


def get_repo_root(cwd: str | None = None) -> str:
    return _run(["git", "rev-parse", "--show-toplevel"], cwd=cwd).strip()


def get_current_branch(cwd: str | None = None) -> str:
    try:
        return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd).strip()
    except GitError:
        return "unknown"


def get_recent_commits(n: int = 5, cwd: str | None = None) -> list[dict]:
    fmt = "%H|%an|%ar|%s"
    output = _run(["git", "log", f"-{n}", f"--pretty=format:{fmt}"], cwd=cwd)
    commits = []
    for line in output.strip().splitlines():
        if "|" in line:
            sha, author, when, msg = line.split("|", 3)
            commits.append({"sha": sha[:8], "author": author, "when": when, "message": msg})
    return commits
