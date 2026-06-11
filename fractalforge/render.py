"""Helpers for turning fractal data into Pillow images."""

import numpy as np
from PIL import Image, ImageDraw

from .palettes import apply_palette


def render_escape_grid(grid, palette="fire", inside_color=(0, 0, 0), gamma=0.45):
    """Render a normalized escape-time grid (values in [0, 1]) to an RGB image.

    A ``gamma`` below 1 brightens the large area of quickly-escaping points
    so detail near the set boundary doesn't get crushed to black.
    """
    inside_mask = grid >= 1.0
    shaded = np.power(grid, gamma)
    rgb = apply_palette(shaded, palette)
    rgb[inside_mask] = inside_color
    return Image.fromarray(rgb, "RGB")


def render_point_cloud(points, width, height, palette="forest", padding=0.05):
    """Render a 2D point cloud as a density-colored image (for chaos-game fractals)."""
    x, y = points[:, 0], points[:, 1]
    x_range = x.max() - x.min() or 1.0
    y_range = y.max() - y.min() or 1.0
    pad_x = x_range * padding
    pad_y = y_range * padding

    hist, _, _ = np.histogram2d(
        y,
        x,
        bins=(height, width),
        range=[[y.min() - pad_y, y.max() + pad_y], [x.min() - pad_x, x.max() + pad_x]],
    )
    hist = np.flipud(hist)

    # Log-scale the density so sparse and dense regions are both visible.
    log_density = np.log1p(hist)
    max_val = log_density.max() or 1.0
    normalized = log_density / max_val

    rgb = apply_palette(normalized, palette)
    # Pixels with no points at all stay at the palette's darkest color (already
    # the case since normalized == 0 there), so nothing further to mask.
    return Image.fromarray(rgb, "RGB")


def render_polyline(points, width, height, line_color=(180, 220, 255), background=(8, 10, 24), padding=0.08):
    """Render a closed polyline (e.g. a Koch snowflake outline) to an image."""
    x, y = points[:, 0], points[:, 1]
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    span = max(x_max - x_min, y_max - y_min)
    span *= 1.0 + 2 * padding
    cx, cy = (x_min + x_max) / 2, (y_min + y_max) / 2

    img = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(img)

    scale = min(width, height) / span
    px = (x - cx) * scale + width / 2
    # Flip Y because image coordinates increase downward.
    py = height / 2 - (y - cy) * scale

    coords = list(zip(px.tolist(), py.tolist()))
    draw.line(coords, fill=line_color, width=max(1, width // 400), joint="curve")
    return img
