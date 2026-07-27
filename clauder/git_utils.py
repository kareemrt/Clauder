"""Helpers for fetching diffs from local git repos and GitHub."""

import subprocess
from pathlib import Path


def diff_staged(repo_path: str = ".") -> str:
    """Return the staged diff (git diff --cached)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--unified=5"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return result.stdout


def diff_branch(base: str, head: str = "HEAD", repo_path: str = ".") -> str:
    """Return the diff between base and head branches."""
    result = subprocess.run(
        ["git", "diff", f"{base}...{head}", "--unified=5"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return result.stdout


def diff_commit(commit: str, repo_path: str = ".") -> str:
    """Return the diff for a specific commit."""
    result = subprocess.run(
        ["git", "show", commit, "--unified=5"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return result.stdout


def diff_last_n(n: int = 1, repo_path: str = ".") -> str:
    """Return the combined diff for the last N commits."""
    result = subprocess.run(
        ["git", "diff", f"HEAD~{n}", "HEAD", "--unified=5"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return result.stdout


def get_pr_diff_from_github(
    repo: str, pr_number: int, github_token: str | None = None
) -> str:
    """Fetch a PR diff from the GitHub API."""
    import urllib.request

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3.diff")
    req.add_header("User-Agent", "Clauder/0.1")
    if github_token:
        req.add_header("Authorization", f"token {github_token}")

    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")
