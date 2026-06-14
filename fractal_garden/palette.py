"""Named colour palettes and hex-colour interpolation."""

from __future__ import annotations

# Each palette is a (base_color, accent_color) pair of "#rrggbb" strings.
# `base_color` sits near the trunk/start of a plant, `accent_color` near
# its tips/leaves (or at the end of a curve for curves without branches).
PALETTES: dict[str, tuple[str, str]] = {
    "spring": ("#6b4423", "#7cd66b"),
    "autumn": ("#5b3a29", "#e08a2c"),
    "twilight": ("#2b1d3a", "#c879ff"),
    "ocean": ("#1d3b53", "#4fd2c5"),
    "fire": ("#3a1a0a", "#ff5e3a"),
    "mono": ("#2b2b2b", "#bdbdbd"),
}

DEFAULT_PALETTE = "spring"


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def interpolate(color_a: str, color_b: str, t: float) -> str:
    """Linearly interpolate between two ``"#rrggbb"`` colours.

    ``t=0`` returns ``color_a``, ``t=1`` returns ``color_b``.
    """
    t = max(0.0, min(1.0, t))
    a = _hex_to_rgb(color_a)
    b = _hex_to_rgb(color_b)
    mixed = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    return _rgb_to_hex(mixed)


def resolve(name: str) -> tuple[str, str]:
    """Look up a palette by name, raising a friendly error if unknown."""
    try:
        return PALETTES[name]
    except KeyError as exc:
        choices = ", ".join(sorted(PALETTES))
        raise ValueError(f"unknown palette {name!r}; choose from: {choices}") from exc
