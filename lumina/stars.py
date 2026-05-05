"""Star field generation with realistic brightness distribution."""
import numpy as np
from PIL import Image, ImageFilter


# Stellar color temperatures mapped to RGB (blackbody approximation)
STAR_COLORS = [
    (155, 176, 255),  # O-type: blue-white
    (170, 191, 255),  # B-type: blue-white
    (202, 215, 255),  # A-type: white
    (255, 244, 234),  # F-type: yellow-white
    (255, 229, 207),  # G-type: yellow (sun-like)
    (255, 210, 161),  # K-type: orange
    (255, 180, 100),  # M-type: red-orange
    (255, 140,  80),  # M-type dim: deep orange-red
]
STAR_COLOR_WEIGHTS = [0.01, 0.05, 0.10, 0.15, 0.25, 0.20, 0.15, 0.09]


def render_star_field(canvas: np.ndarray, count: int, rng: np.random.Generator) -> np.ndarray:
    """Paint stars onto an RGBA float canvas (H x W x 4, values 0-1)."""
    h, w = canvas.shape[:2]
    color_indices = rng.choice(len(STAR_COLORS), size=count, p=STAR_COLOR_WEIGHTS)
    xs = rng.integers(0, w, size=count)
    ys = rng.integers(0, h, size=count)

    # Pareto-distributed brightness (most stars dim, a few brilliant)
    brightness = rng.pareto(3.5, size=count)
    brightness = np.clip(brightness / brightness.max(), 0.05, 1.0)

    # Radius: most tiny, a few prominent
    radii = np.clip(rng.exponential(0.6, size=count), 0.3, 3.5)

    for i in range(count):
        x, y = int(xs[i]), int(ys[i])
        r = int(np.ceil(radii[i]))
        b = float(brightness[i])
        rgb = np.array(STAR_COLORS[color_indices[i]], dtype=float) / 255.0

        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    dist = np.sqrt(dx * dx + dy * dy)
                    # Gaussian falloff
                    alpha = b * np.exp(-dist * dist / (0.5 * radii[i] ** 2 + 0.1))
                    alpha = min(alpha, 1.0)
                    existing = canvas[ny, nx]
                    canvas[ny, nx, :3] = existing[:3] * (1 - alpha) + rgb * alpha
                    canvas[ny, nx, 3] = min(existing[3] + alpha, 1.0)

    return canvas


def add_star_glow(img: Image.Image, intensity: float = 0.3) -> Image.Image:
    """Bloom effect: soft glow around bright stars."""
    bright = img.point(lambda p: p if p > 180 else 0)
    glow = bright.filter(ImageFilter.GaussianBlur(radius=3))
    r, g, b, a = img.split()
    gr, gg, gb, _ = glow.split()
    from PIL import ImageChops, ImageEnhance
    glow_rgb = Image.merge("RGB", (gr, gg, gb))
    glow_rgb = ImageEnhance.Brightness(glow_rgb).enhance(intensity)
    base_rgb = Image.merge("RGB", (r, g, b))
    blended = ImageChops.add(base_rgb, glow_rgb)
    return Image.merge("RGBA", (*blended.split(), a))
