"""Claude-powered narrative generation for repository stories."""

import os
import json
from typing import Optional
import anthropic

from .github_client import RepoData


STORY_PROMPT = """You are a gifted technology journalist and historian. Analyze this GitHub repository's data and write a captivating "documentary" story about it.

Repository Data:
{data}

Write a structured story with these exact sections (use these exact headings):

## The Origin
A compelling 2-3 paragraph introduction about what this project is, why it exists, and the problem it solves. Make it feel like the opening of a documentary.

## The Architects
Introduce the key contributors as characters in this story. Highlight their contributions and what they brought to the project. Be specific and human.

## The Journey
A narrative timeline of the project's evolution based on the commit history. Identify distinct "chapters" or phases. Reference specific commits when relevant.

## The Technology
An engaging analysis of the technical choices — languages, architecture patterns visible in the codebase, and what they reveal about the team's values.

## The Current State
Where the project stands today — its strengths, open questions, community health. Reference issues/PRs if available.

## The Future
A thoughtful 1-2 paragraph speculation about where this project might go, based on its trajectory and current state.

## One-Line Story
End with a single, poetic sentence that captures the essence of this project's story.

Guidelines:
- Write in an engaging, documentary-style narrative voice
- Be specific — reference actual commit messages, contributor names, dates
- Find the human story behind the code
- Keep each section substantive but focused (150-250 words each)
- Make it genuinely interesting to read
"""


class Storyteller:
    def __init__(self, api_key: Optional[str] = None):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )

    def _serialize_repo_data(self, data: RepoData) -> str:
        s = data.stats
        summary = {
            "repository": {
                "name": s.full_name,
                "description": s.description,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
                "stars": s.stars,
                "forks": s.forks,
                "open_issues": s.open_issues,
                "primary_language": s.language,
                "topics": s.topics,
                "license": s.license,
                "size_kb": s.size_kb,
            },
            "languages": data.languages,
            "top_contributors": [
                {"login": c.login, "contributions": c.contributions}
                for c in data.contributors[:10]
            ],
            "recent_commits": [
                {"sha": c.sha, "message": c.message, "author": c.author, "date": c.date}
                for c in data.commits[:30]
            ],
            "recent_issues": data.recent_issues[:8],
            "recent_prs": data.recent_prs[:8],
        }
        return json.dumps(summary, indent=2, default=str)

    def generate_story(self, data: RepoData) -> str:
        serialized = self._serialize_repo_data(data)
        prompt = STORY_PROMPT.format(data=serialized)

        message = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def generate_tagline(self, data: RepoData) -> str:
        name = data.stats.full_name
        desc = data.stats.description or "a software project"
        lang = data.stats.language or "code"

        message = self.client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": (
                    f"Write a single compelling tagline (under 15 words) for a GitHub repository called '{name}'. "
                    f"Description: {desc}. Primary language: {lang}. "
                    "Make it punchy and memorable. Return only the tagline, no quotes."
                )
            }],
        )
        return message.content[0].text.strip()
