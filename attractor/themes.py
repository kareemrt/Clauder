"""
Color themes — each theme maps a density value in [0, 1] to an RGBA color.
Built on matplotlib colormaps so we stay dependency-light.
"""

from typing import Dict, Tuple
import numpy as np

# (background_hex, matplotlib_colormap_name)
THEMES: Dict[str, Tuple[str, str]] = {
    "plasma":     ("#0d0221", "plasma"),
    "inferno":    ("#000000", "inferno"),
    "galaxy":     ("#010b1a", "cool"),
    "ember":      ("#0a0200", "hot"),
    "forest":     ("#010a01", "Greens"),
    "ocean":      ("#00060f", "Blues"),
    "aurora":     ("#020a08", "summer"),
    "gold":       ("#080400", "YlOrBr"),
    "neon":       ("#000000", "spring"),
    "twilight":   ("#08000f", "twilight"),
}


def list_themes() -> list:
    return list(THEMES.keys())


def get_theme(name: str) -> Tuple[str, str]:
    key = name.lower()
    if key not in THEMES:
        raise ValueError(f"Unknown theme '{name}'. Choose from: {', '.join(THEMES)}")
    return THEMES[key]
