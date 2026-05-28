"""
Claude API integration — generates poetic, scientific narration for fractal renders.
Uses prompt caching for efficiency when narrating multiple presets in a session.
"""

from __future__ import annotations

import os

try:
    import anthropic
    _HAS_ANTHROPIC = True
except ImportError:
    _HAS_ANTHROPIC = False


_SYSTEM_PROMPT = """You are a fractal mathematician and poet. When given information about a fractal
render — its type, location, iteration depth, and mathematical properties — you write a short,
vivid description (3-5 sentences) that blends rigorous mathematical insight with lyrical wonder.
You illuminate what the viewer is seeing: the underlying dynamical system, what the colors represent,
any famous mathematical significance, and why this particular location is beautiful or strange.
Write in present tense, second person ("you are looking at..."). Be precise but evocative."""


def narrate(
    fractal_type: str,
    name: str,
    description: str,
    viewport: tuple[float, float, float, float],
    max_iter: int,
    palette: str,
    julia_c: complex | None = None,
) -> str:
    """
    Generate an AI narration for a fractal render using the Claude API.
    Returns a plain-text description, or a fallback message if unavailable.
    """
    if not _HAS_ANTHROPIC:
        return (
            "Install the `anthropic` package and set ANTHROPIC_API_KEY "
            "to enable AI narration."
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Set ANTHROPIC_API_KEY environment variable to enable AI narration."

    client = anthropic.Anthropic(api_key=api_key)

    xmin, xmax, ymin, ymax = viewport
    width = xmax - xmin
    height = ymax - ymin
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2

    prompt_lines = [
        f"Fractal type: {fractal_type}",
        f"Location name: {name}",
        f"Curator's note: {description}",
        f"Viewport center: {center_x:+.8f} + {center_y:+.8f}i",
        f"Viewport width: {width:.2e}, height: {height:.2e}",
        f"Zoom level: ~{1.0 / max(width, height):.0e}x",
        f"Max iterations: {max_iter}",
        f"Color palette: {palette}",
    ]
    if julia_c is not None:
        prompt_lines.append(f"Julia parameter c: {julia_c.real:+.4f} + {julia_c.imag:+.4f}i")

    user_content = "\n".join(prompt_lines)

    try:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=256,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},  # cache system prompt
                }
            ],
            messages=[{"role": "user", "content": user_content}],
        )
        return response.content[0].text.strip()
    except anthropic.APIError as e:
        return f"[Narration unavailable: {e}]"
