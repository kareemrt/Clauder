"""High score persistence via JSON."""

import json
from pathlib import Path
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import Player

SCORES_FILE = Path.home() / ".terminalquest_scores.json"


def load_scores() -> List[Dict[str, Any]]:
    try:
        if SCORES_FILE.exists():
            with open(SCORES_FILE) as f:
                data = json.load(f)
            return sorted(data, key=lambda x: x["score"], reverse=True)
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_score(player: "Player") -> None:
    scores = load_scores()
    scores.append(
        {
            "name": player.name,
            "class": player.char_class.value,
            "floor": player.dungeon_level,
            "kills": player.kills,
            "gold": player.gold,
            "score": player.score(),
        }
    )
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:20]
    try:
        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        pass
