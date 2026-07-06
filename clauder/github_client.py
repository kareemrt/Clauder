"""GitHub REST API client for fetching repository data."""

import os
import time
from dataclasses import dataclass, field
from typing import Optional
import requests


@dataclass
class Contributor:
    login: str
    contributions: int
    avatar_url: str
    html_url: str


@dataclass
class CommitInfo:
    sha: str
    message: str
    author: str
    date: str
    url: str


@dataclass
class RepoStats:
    full_name: str
    description: Optional[str]
    stars: int
    forks: int
    watchers: int
    open_issues: int
    language: Optional[str]
    topics: list[str]
    created_at: str
    updated_at: str
    homepage: Optional[str]
    license: Optional[str]
    size_kb: int


@dataclass
class RepoData:
    stats: RepoStats
    contributors: list[Contributor]
    commits: list[CommitInfo]
    languages: dict[str, int]
    recent_issues: list[dict]
    recent_prs: list[dict]


class GitHubClient:
    BASE = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Clauder/0.1.0",
        })
        if self.token:
            self.session.headers["Authorization"] = f"token {self.token}"

    def _get(self, path: str, params: dict = None) -> dict | list:
        url = f"{self.BASE}{path}"
        resp = self.session.get(url, params=params or {})
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(0, reset - time.time()) + 1
            time.sleep(min(wait, 10))
            resp = self.session.get(url, params=params or {})
        resp.raise_for_status()
        return resp.json()

    def _get_paginated(self, path: str, params: dict = None, max_items: int = 100) -> list:
        items = []
        page = 1
        while len(items) < max_items:
            p = {**(params or {}), "per_page": min(100, max_items - len(items)), "page": page}
            batch = self._get(path, p)
            if not batch:
                break
            items.extend(batch)
            if len(batch) < p["per_page"]:
                break
            page += 1
        return items[:max_items]

    def fetch_repo_data(self, owner: str, repo: str) -> RepoData:
        repo_path = f"/repos/{owner}/{repo}"

        raw = self._get(repo_path)
        stats = RepoStats(
            full_name=raw["full_name"],
            description=raw.get("description"),
            stars=raw["stargazers_count"],
            forks=raw["forks_count"],
            watchers=raw["watchers_count"],
            open_issues=raw["open_issues_count"],
            language=raw.get("language"),
            topics=raw.get("topics", []),
            created_at=raw["created_at"],
            updated_at=raw["updated_at"],
            homepage=raw.get("homepage"),
            license=raw.get("license", {}).get("name") if raw.get("license") else None,
            size_kb=raw.get("size", 0),
        )

        raw_contributors = self._get_paginated(f"{repo_path}/contributors", max_items=20)
        contributors = [
            Contributor(
                login=c["login"],
                contributions=c["contributions"],
                avatar_url=c["avatar_url"],
                html_url=c["html_url"],
            )
            for c in raw_contributors
            if c.get("type") != "Bot"
        ]

        raw_commits = self._get_paginated(f"{repo_path}/commits", max_items=50)
        commits = []
        for c in raw_commits:
            commit = c.get("commit", {})
            author = commit.get("author", {})
            commits.append(CommitInfo(
                sha=c["sha"][:7],
                message=commit.get("message", "").split("\n")[0][:120],
                author=author.get("name", "Unknown"),
                date=author.get("date", ""),
                url=c.get("html_url", ""),
            ))

        try:
            languages = self._get(f"{repo_path}/languages")
        except Exception:
            languages = {}

        try:
            raw_issues = self._get_paginated(
                f"{repo_path}/issues",
                {"state": "all", "sort": "updated"},
                max_items=10,
            )
            issues = [
                {"title": i["title"], "state": i["state"], "url": i["html_url"],
                 "labels": [l["name"] for l in i.get("labels", [])]}
                for i in raw_issues
                if "pull_request" not in i
            ][:10]
        except Exception:
            issues = []

        try:
            raw_prs = self._get_paginated(
                f"{repo_path}/pulls",
                {"state": "all", "sort": "updated"},
                max_items=10,
            )
            prs = [
                {"title": p["title"], "state": p["state"], "url": p["html_url"],
                 "merged": p.get("merged_at") is not None}
                for p in raw_prs
            ][:10]
        except Exception:
            prs = []

        return RepoData(
            stats=stats,
            contributors=contributors,
            commits=commits,
            languages=languages,
            recent_issues=issues,
            recent_prs=prs,
        )
