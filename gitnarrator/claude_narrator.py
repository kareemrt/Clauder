"""Uses Claude API with streaming to generate narrative stories from git history."""

from __future__ import annotations

import os
from typing import Iterator

import anthropic

from .git_analyzer import RepoStats

_CLIENT: anthropic.Anthropic | None = None


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    return _CLIENT


def _chapter_context(chapter: dict) -> str:
    authors = ", ".join(f"{a} ({n} commits)" for a, n in chapter["authors"].items())
    files = ", ".join(f[0] for f in chapter["hottest_files"][:3])
    msgs = "\n  - ".join(chapter["sample_messages"][:6])
    return (
        f"Duration: {chapter['duration_days']} days | "
        f"Commits: {chapter['commit_count']} | "
        f"Authors: {authors} | "
        f"Hot files: {files} | "
        f"+{chapter['insertions']}/-{chapter['deletions']} lines\n"
        f"Sample commits:\n  - {msgs}"
    )


def stream_full_story(stats: RepoStats) -> Iterator[str]:
    """Stream the full narrative story of the repository."""
    chapters_text = "\n\n".join(
        f"=== Chapter {ch['number']} ({ch['start_date'].strftime('%b %Y')} – "
        f"{ch['end_date'].strftime('%b %Y')}) ===\n{_chapter_context(ch)}"
        for ch in stats.chapters
    )

    top_authors = sorted(stats.authors.items(), key=lambda x: x[1], reverse=True)[:5]
    authors_text = ", ".join(f"{a} ({n})" for a, n in top_authors)

    top_files = sorted(stats.file_heatmap.items(), key=lambda x: x[1], reverse=True)[:8]
    files_text = ", ".join(f"{f} ({n}x)" for f, n in top_files)

    prompt = f"""You are GitNarrator, an AI that reads git repository history and tells the story of how a project came to life.
Write a vivid, engaging narrative about the evolution of "{stats.name}" — as if narrating a documentary about its creation.

REPOSITORY FACTS:
- Project: {stats.name}
- Total commits: {stats.total_commits}
- Active period: {stats.first_commit.strftime('%B %d, %Y')} → {stats.last_commit.strftime('%B %d, %Y')}
- Contributors: {authors_text}
- Most-changed files: {files_text}

CHAPTER DATA:
{chapters_text}

INSTRUCTIONS:
1. Write a compelling TITLE for this project's story (one line, dramatic)
2. Write an INTRODUCTION paragraph setting the scene (2-3 sentences)
3. For each chapter, write a short evocative title and 2-3 sentences describing what was happening in the codebase — what was being built, what challenges were faced, how the team evolved
4. Write a CONCLUSION paragraph reflecting on the project's journey
5. Add an EPITAPH — one memorable sentence that captures the project's essence

Be vivid, specific, and engaging. Use metaphors. Make it feel human.
Format with clear headings: TITLE, INTRODUCTION, CHAPTER N: [Title], CONCLUSION, EPITAPH"""

    with _client().messages.stream(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def generate_chapter_title(chapter: dict, repo_name: str) -> str:
    """Generate a punchy title for a single chapter (non-streaming, cached)."""
    ctx = _chapter_context(chapter)
    msg = _client().messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=60,
        messages=[{
            "role": "user",
            "content": (
                f"Give a short, evocative 4-7 word chapter title for this phase of "
                f"the '{repo_name}' project's git history. Return ONLY the title, no quotes.\n\n{ctx}"
            ),
        }],
    )
    return msg.content[0].text.strip()


def generate_one_liner(stats: RepoStats) -> str:
    """Generate a single tagline for the whole project."""
    top = sorted(stats.authors.items(), key=lambda x: x[1], reverse=True)
    prompt = (
        f"Write one punchy tagline (max 12 words) for a software project called '{stats.name}' "
        f"with {stats.total_commits} commits, {len(stats.authors)} contributors, "
        f"spanning {(stats.last_commit - stats.first_commit).days} days. "
        f"Return ONLY the tagline."
    )
    msg = _client().messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=40,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()
