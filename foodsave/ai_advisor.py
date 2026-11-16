"""Claude-powered recipe suggestions and waste-reduction advice."""

import os
from typing import List, Optional

try:
    import anthropic
    _HAS_ANTHROPIC = True
except ImportError:
    _HAS_ANTHROPIC = False

from .models import FoodItem


SYSTEM_PROMPT = """You are FoodSave AI — a friendly, knowledgeable assistant that helps people \
reduce food waste. You suggest practical recipes using ingredients people already have, \
explain smart food storage tips, and offer personalised meal-planning advice.

Keep responses concise and actionable. Format recipe suggestions with:
- A short title
- Key ingredients used
- Estimated prep time
- 3-5 simple steps

Always highlight how using an ingredient prevents waste and saves money."""


def _get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Export it to unlock AI-powered suggestions."
        )
    if not _HAS_ANTHROPIC:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")
    return anthropic.Anthropic(api_key=api_key)


def suggest_recipes(items: List[FoodItem], preferences: Optional[str] = None) -> str:
    """Ask Claude to suggest recipes for the given food items."""
    if not items:
        return "No items provided. Add items to your inventory first!"

    expiring = [i for i in items if i.days_until_expiry() <= 5]
    focus = expiring if expiring else items[:5]

    ingredient_list = "\n".join(
        f"- {i.name} ({i.quantity} {i.unit}, expires in {i.days_until_expiry()} days)"
        for i in focus
    )
    pref_note = f"\nDietary preferences / restrictions: {preferences}" if preferences else ""

    prompt = f"""I need to use these ingredients before they go bad:
{ingredient_list}{pref_note}

Please suggest 2-3 practical recipes that use as many of these ingredients as possible. \
Prioritise items expiring soonest."""

    client = _get_client()
    message = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def get_storage_tips(item: FoodItem) -> str:
    """Get storage tips to extend the life of a specific food item."""
    prompt = (
        f"Give me 3 specific storage tips to extend the shelf life of "
        f"{item.name} ({item.category}). Be concise and practical."
    )
    client = _get_client()
    message = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def get_reduction_plan(waste_summary: str) -> str:
    """Generate a personalised waste-reduction plan based on waste history."""
    prompt = (
        f"Based on this food waste summary, give me a personalised 5-step action plan "
        f"to reduce my food waste next month:\n\n{waste_summary}\n\n"
        "Be specific, practical, and encouraging."
    )
    client = _get_client()
    message = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=768,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
