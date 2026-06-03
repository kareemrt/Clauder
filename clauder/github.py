from __future__ import annotations

import base64
import os
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx

from clauder.models import FileInfo, RepoData

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2",
    ".ttf", ".eot", ".otf", ".mp4", ".mp3", ".zip", ".tar", ".gz",
    ".lock", ".bin", ".exe", ".dll", ".so", ".dylib", ".pdf",
}

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
    "build", ".next", ".nuxt", "coverage", ".nyc_output", "vendor",
}

MAX_FILE_BYTES = 50_000
LANGUAGE_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".jsx": "JavaScript", ".tsx": "TypeScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".rb": "Ruby", ".php": "PHP",
    ".cs": "C#", ".cpp": "C++", ".c": "C", ".h": "C/C++",
    ".swift": "Swift", ".kt": "Kotlin", ".scala": "Scala",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS",
    ".md": "Markdown", ".yaml": "YAML", ".yml": "YAML",
    ".json": "JSON", ".toml": "TOML", ".sh": "Shell",
    ".dockerfile": "Dockerfile", ".tf": "Terraform",
}


def _parse_repo_identifier(repo: str) -> tuple[str, str]:
    """Parse 'owner/name', full GitHub URL, or local path into (owner, name)."""
    if repo.startswith(("http://", "https://")):
        parts = urlparse(repo).path.strip("/").split("/")
        return parts[0], parts[1].removesuffix(".git")
    if "/" in repo and not repo.startswith(".") and not os.path.isdir(repo):
        parts = repo.split("/")
        return parts[0], parts[1]
    raise ValueError(f"Cannot parse repo identifier: {repo!r}")


def _detect_language(path: str) -> Optional[str]:
    suffix = Path(path).suffix.lower()
    if Path(path).name.lower() == "dockerfile":
        return "Dockerfile"
    return LANGUAGE_MAP.get(suffix)


class RepoFetcher:
    def __init__(self, github_token: Optional[str] = None):
        self.token = github_token or os.getenv("GITHUB_TOKEN")
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self._client = httpx.AsyncClient(
            base_url="https://api.github.com",
            headers=headers,
            timeout=30,
        )

    async def fetch(self, repo: str, max_files: int = 60) -> RepoData:
        owner, name = _parse_repo_identifier(repo)

        meta_resp = await self._client.get(f"/repos/{owner}/{name}")
        meta_resp.raise_for_status()
        meta = meta_resp.json()

        tree_resp = await self._client.get(
            f"/repos/{owner}/{name}/git/trees/{meta['default_branch']}",
            params={"recursive": "1"},
        )
        tree_resp.raise_for_status()
        tree = tree_resp.json()

        all_paths = [
            item["path"] for item in tree.get("tree", [])
            if item["type"] == "blob"
        ]
        filtered = _filter_paths(all_paths, max_files)

        files: list[FileInfo] = []
        for path in filtered:
            content = await self._fetch_file(owner, name, path, meta["default_branch"])
            if content is not None:
                files.append(FileInfo(
                    path=path,
                    content=content,
                    size=len(content),
                    language=_detect_language(path),
                ))

        return RepoData(
            owner=owner,
            name=name,
            description=meta.get("description"),
            url=meta["html_url"],
            default_branch=meta["default_branch"],
            stars=meta.get("stargazers_count", 0),
            language=meta.get("language"),
            files=files,
            file_tree=all_paths,
            topics=meta.get("topics", []),
        )

    async def _fetch_file(self, owner: str, name: str, path: str, branch: str) -> Optional[str]:
        try:
            resp = await self._client.get(f"/repos/{owner}/{name}/contents/{path}", params={"ref": branch})
            resp.raise_for_status()
            data = resp.json()
            if data.get("encoding") == "base64":
                raw = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
                return raw[:MAX_FILE_BYTES]
        except Exception:
            pass
        return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._client.aclose()


def _filter_paths(paths: list[str], max_files: int) -> list[str]:
    """Filter out noise and prioritize interesting files."""
    def is_skippable(p: str) -> bool:
        parts = p.split("/")
        if any(part in SKIP_DIRS for part in parts):
            return True
        suffix = Path(p).suffix.lower()
        if suffix in SKIP_EXTENSIONS:
            return True
        return False

    def priority(p: str) -> int:
        name = Path(p).name.lower()
        if name in {"readme.md", "readme.rst", "readme.txt"}:
            return 0
        if name in {"dockerfile", "docker-compose.yml", "pyproject.toml", "package.json", "go.mod", "cargo.toml"}:
            return 1
        suffix = Path(p).suffix.lower()
        if suffix in {".py", ".ts", ".js", ".go", ".rs", ".java", ".rb"}:
            return 2
        if suffix in {".yaml", ".yml", ".json", ".toml", ".sh"}:
            return 3
        return 4

    filtered = [p for p in paths if not is_skippable(p)]
    filtered.sort(key=priority)
    return filtered[:max_files]
