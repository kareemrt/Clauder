"""Scene composer: assembles stars, nebulae, and planets into a final image."""
import numpy as np
from PIL import Image

from .stars import render_star_field, add_star_glow
from .nebula import render_nebula, PALETTES
from .planets import render_planet, PLANET_THEMES


def _alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Porter-Duff 'over' blend for float RGBA arrays."""
    a_o = overlay[:, :, 3:4]
    a_b = base[:, :, 3:4]
    a_out = a_o + a_b * (1 - a_o)
    rgb_out = np.where(
        a_out > 0,
        (overlay[:, :, :3] * a_o + base[:, :, :3] * a_b * (1 - a_o)) / (a_out + 1e-9),
        0,
    )
    return np.concatenate([rgb_out, a_out], axis=2).astype(np.float32)


def _paste_layer(canvas: np.ndarray, layer: np.ndarray, cx: int, cy: int) -> np.ndarray:
    """Paste a smaller RGBA layer onto the canvas centered at (cx, cy)."""
    H, W = canvas.shape[:2]
    h, w = layer.shape[:2]
    x0 = cx - w // 2
    y0 = cy - h // 2
    x1, y1 = x0 + w, y0 + h

    # Clamp to canvas bounds
    sx0 = max(-x0, 0)
    sy0 = max(-y0, 0)
    sx1 = w - max(x1 - W, 0)
    sy1 = h - max(y1 - H, 0)
    dx0 = max(x0, 0)
    dy0 = max(y0, 0)
    dx1 = dx0 + (sx1 - sx0)
    dy1 = dy0 + (sy1 - sy0)

    if dx0 >= W or dy0 >= H or dx1 <= 0 or dy1 <= 0:
        return canvas

    region = canvas[dy0:dy1, dx0:dx1]
    patch = layer[sy0:sy1, sx0:sx1]
    canvas[dy0:dy1, dx0:dx1] = _alpha_composite(region, patch)
    return canvas


def generate_scene(
    width: int = 1920,
    height: int = 1080,
    seed: int = 42,
    nebula_palette: str | None = None,
    planet_theme: str | None = None,
    star_count: int = 2200,
    n_planets: int = 2,
) -> Image.Image:
    """
    Compose a full cosmic scene and return a PIL Image (RGB).

    Args:
        width, height: Output resolution.
        seed: Random seed for full reproducibility.
        nebula_palette: One of the named palettes, or None to choose randomly.
        planet_theme: One of the named themes, or None to choose randomly.
        star_count: Number of stars to scatter.
        n_planets: How many planets to include (0–3).
    """
    rng = np.random.default_rng(seed)

    palette_name = nebula_palette or rng.choice(list(PALETTES.keys()))
    theme_name = planet_theme or rng.choice(list(PLANET_THEMES.keys()))

    # ── Background: deep space black ──────────────────────────────────────────
    canvas = np.zeros((height, width, 4), dtype=np.float32)
    canvas[:, :, 3] = 1.0  # fully opaque black

    # ── Layer 1: distant background star haze ─────────────────────────────────
    bg_stars = np.zeros((height, width, 4), dtype=np.float32)
    bg_stars = render_star_field(bg_stars, count=int(star_count * 0.6), rng=rng)
    # Dim the background haze
    bg_stars[:, :, :3] *= 0.5
    canvas = _alpha_composite(canvas, bg_stars)

    # ── Layer 2: nebula ────────────────────────────────────────────────────────
    nebula_rgba = render_nebula(width, height, palette_name, rng, density=0.55)
    canvas = _alpha_composite(canvas, nebula_rgba)

    # ── Layer 3: foreground stars ──────────────────────────────────────────────
    fg_stars = np.zeros((height, width, 4), dtype=np.float32)
    fg_stars = render_star_field(fg_stars, count=int(star_count * 0.4), rng=rng)
    canvas = _alpha_composite(canvas, fg_stars)

    # ── Layer 4: planets ───────────────────────────────────────────────────────
    available_themes = list(PLANET_THEMES.keys())
    chosen_themes = rng.choice(available_themes, size=min(n_planets, len(available_themes)),
                                replace=False)
    for i in range(n_planets):
        t_name = chosen_themes[i] if i < len(chosen_themes) else theme_name
        # Planet size: 8–15% of the shorter dimension
        pct = rng.uniform(0.08, 0.16)
        p_size = int(min(width, height) * pct)
        # Light comes roughly from upper-right
        angle = rng.uniform(-0.6, 0.6)
        light = np.array([np.sin(angle) * 0.6 + 0.3, -0.3, 0.8])
        planet_rgba = render_planet(p_size, t_name, rng, light_dir=light)

        # Position: avoid center cluster, favor edges with some inset
        margin = int(p_size * 0.6)
        cx = int(rng.integers(margin, width - margin))
        cy = int(rng.integers(margin, height - margin))
        canvas = _paste_layer(canvas, planet_rgba, cx, cy)

    # ── Finalize ───────────────────────────────────────────────────────────────
    # Tone-map: soft exposure + gamma
    rgb = canvas[:, :, :3]
    rgb = 1.0 - np.exp(-rgb * 1.6)   # exposure
    rgb = np.power(np.clip(rgb, 0, 1), 1 / 2.2)  # gamma

    img = Image.fromarray((rgb * 255).astype(np.uint8), mode="RGB")
    img = add_star_glow(img.convert("RGBA"), intensity=0.6).convert("RGB")
    return img
