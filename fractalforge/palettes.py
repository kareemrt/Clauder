"""Color palettes for mapping normalized fractal values to RGB colors."""

import numpy as np

# Each palette is a list of (position, (r, g, b)) stops, position in [0, 1].
PALETTES = {
    "fire": [
        (0.00, (0, 0, 4)),
        (0.20, (40, 11, 84)),
        (0.40, (101, 21, 110)),
        (0.60, (159, 42, 99)),
        (0.80, (212, 72, 66)),
        (0.90, (245, 125, 21)),
        (1.00, (252, 255, 164)),
    ],
    "ocean": [
        (0.00, (0, 7, 30)),
        (0.25, (0, 38, 77)),
        (0.50, (0, 91, 130)),
        (0.75, (60, 170, 200)),
        (1.00, (220, 250, 255)),
    ],
    "twilight": [
        (0.00, (10, 5, 30)),
        (0.30, (60, 20, 110)),
        (0.55, (160, 60, 160)),
        (0.80, (250, 130, 120)),
        (1.00, (255, 240, 200)),
    ],
    "forest": [
        (0.00, (5, 15, 5)),
        (0.30, (20, 70, 30)),
        (0.55, (70, 130, 50)),
        (0.80, (190, 210, 90)),
        (1.00, (255, 255, 230)),
    ],
    "electric": [
        (0.00, (0, 0, 0)),
        (0.25, (30, 0, 90)),
        (0.50, (0, 100, 220)),
        (0.75, (0, 230, 230)),
        (1.00, (255, 255, 255)),
    ],
    "grayscale": [
        (0.00, (0, 0, 0)),
        (1.00, (255, 255, 255)),
    ],
}


def available_palettes():
    """Return the list of palette names available."""
    return sorted(PALETTES.keys())


def apply_palette(values, name="fire"):
    """Map an array of normalized values (0..1) to an (H, W, 3) uint8 RGB image."""
    if name not in PALETTES:
        raise ValueError(
            f"Unknown palette '{name}'. Available: {', '.join(available_palettes())}"
        )

    stops = PALETTES[name]
    positions = np.array([s[0] for s in stops])
    colors = np.array([s[1] for s in stops], dtype=np.float64)

    clipped = np.clip(values, 0.0, 1.0)
    out = np.empty(clipped.shape + (3,), dtype=np.float64)
    for channel in range(3):
        out[..., channel] = np.interp(clipped, positions, colors[:, channel])

    return out.astype(np.uint8)
