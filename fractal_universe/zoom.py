"""
Zoom sequence generator.

Produces a series of (x_min, x_max, y_min, y_max) view windows that
smoothly zoom into a target point over N frames.
"""

from typing import Iterator, Tuple

Bounds = Tuple[float, float, float, float]


def zoom_sequence(
    start: Bounds,
    target_x: float,
    target_y: float,
    zoom_factor: float,
    frames: int,
) -> Iterator[Bounds]:
    """
    Yield `frames` progressively zoomed bounds converging on (target_x, target_y).

    zoom_factor is the total magnification (e.g. 100 = 100x zoom over all frames).
    """
    x_min, x_max, y_min, y_max = start
    per_frame = zoom_factor ** (1.0 / frames)

    for _ in range(frames):
        cx = (x_min + x_max) / 2
        cy = (y_min + y_max) / 2

        # Shift center toward target, then shrink
        cx = cx + (target_x - cx) * 0.15
        cy = cy + (target_y - cy) * 0.15

        half_w = (x_max - x_min) / 2 / per_frame
        half_h = (y_max - y_min) / 2 / per_frame

        x_min, x_max = cx - half_w, cx + half_w
        y_min, y_max = cy - half_h, cy + half_h

        yield x_min, x_max, y_min, y_max


# Famous zoom destinations
ZOOM_DESTINATIONS = {
    "seahorse_valley": {
        "fractal": "mandelbrot",
        "target": (-0.7436438851, 0.1318259043),
        "zoom_factor": 50000,
    },
    "elephant_valley": {
        "fractal": "mandelbrot",
        "target": (0.3073848, 0.0228926),
        "zoom_factor": 10000,
    },
    "triple_spiral": {
        "fractal": "mandelbrot",
        "target": (-0.1583468, 1.0325218),
        "zoom_factor": 20000,
    },
    "mini_brot": {
        "fractal": "mandelbrot",
        "target": (-1.7687243, 0.00423684),
        "zoom_factor": 100000,
    },
}
