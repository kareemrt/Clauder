"""Rendering Particle Life frames to images and animated GIFs."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .simulation import ParticleSystem

BACKGROUND = (12, 12, 20)


def render_frame(
    system: ParticleSystem,
    colors: tuple[tuple[int, int, int], ...],
    size: int = 360,
    radius: int = 2,
) -> Image.Image:
    """Render the current state of ``system`` to an RGB image."""
    image = Image.new("RGB", (size, size), BACKGROUND)
    draw = ImageDraw.Draw(image)

    coords = system.positions * size
    for (x, y), particle_type in zip(coords, system.types):
        color = colors[particle_type % len(colors)]
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    return image


def render_gif(
    system: ParticleSystem,
    colors: tuple[tuple[int, int, int], ...],
    output_path: str | Path,
    frames: int,
    steps_per_frame: int = 1,
    size: int = 360,
    radius: int = 2,
    duration_ms: int = 40,
) -> Path:
    """Simulate ``system`` forward and write an animated GIF to ``output_path``."""
    images: list[Image.Image] = []
    for _ in range(frames):
        for _ in range(steps_per_frame):
            system.step()
        images.append(render_frame(system, colors, size=size, radius=radius))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    return output_path
