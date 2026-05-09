"""Generate narrative stories from git history using Claude."""

from __future__ import annotations

from typing import Iterator

import anthropic

from .git_analyzer import RepoStats, build_story_context

_SYSTEM_PROMPT = """\
You are a gifted technical author and storyteller. You receive raw statistics \
and commit logs from a software project and you transform them into a vivid, \
engaging narrative — a "developer diary" written in the voice of the project \
itself, as if the code is looking back on its own creation.

Your story should:
- Open with a dramatic, evocative introduction
- Weave in real data points (dates, commit messages, authors, line counts)
- Identify pivotal moments (first commit, major refactors, busiest periods)
- Celebrate the contributors by name with personality
- Have a clear narrative arc: birth → struggle → growth → current state
- Use vivid metaphors but remain technically grounded
- Be structured with clear sections, each with a poetic heading
- Close with a reflection on what the project means and where it might go

Keep the tone: curious, warm, slightly dramatic, technically honest.
Length: ~600–900 words. Use markdown headings and emphasis freely.\
"""


def stream_story(stats: RepoStats, client: anthropic.Anthropic) -> Iterator[str]:
    """Stream a narrative story about the repo, yielding text chunks."""
    context = build_story_context(stats)
    prompt = (
        f"Here is the full profile of the repository I want you to narrate:\n\n"
        f"{context}\n\n"
        f"Now write the developer diary / narrative story."
    )

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def generate_commit_haiku(stats: RepoStats, client: anthropic.Anthropic) -> str:
    """Generate a haiku that captures the soul of the project."""
    context = build_story_context(stats)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Based on this project:\n{context}\n\n"
                    "Write a single haiku (3 lines, 5-7-5 syllables) that captures "
                    "the soul of this codebase. Reply with only the haiku, no explanation."
                ),
            }
        ],
    )
    return response.content[0].text.strip()


def generate_one_line_tagline(stats: RepoStats, client: anthropic.Anthropic) -> str:
    """Generate a punchy one-line tagline for the project."""
    context = build_story_context(stats)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=60,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Based on this project:\n{context}\n\n"
                    "Write a single punchy tagline (under 12 words) for this project. "
                    "Think startup pitch meets poetry. Reply with only the tagline."
                ),
            }
        ],
    )
    return response.content[0].text.strip().strip('"')
