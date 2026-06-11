"""Generate zoom animations into the Mandelbrot set."""

import math

from PIL import Image

from .escape_time import mandelbrot
from .render import render_escape_grid


def mandelbrot_zoom_frames(
    width,
    height,
    frames=40,
    max_iter=200,
    target=(-0.7436438870371587, 0.13182590420533),
    zoom_factor=1.3,
    palette="fire",
):
    """Render a sequence of frames zooming into ``target`` on the Mandelbrot set.

    The iteration count grows with the zoom level so that detail stays sharp
    as the view gets deeper.
    """
    images = []
    zoom = 1.0
    for _ in range(frames):
        depth_iter = max_iter + int(40 * math.log2(zoom + 1))
        grid = mandelbrot(width, height, max_iter=depth_iter, center=target, zoom=zoom)
        images.append(render_escape_grid(grid, palette))
        zoom *= zoom_factor
    return images


def save_gif(images, path, duration=80, loop=0):
    """Save a list of Pillow images as an animated GIF."""
    quantized = [img.convert("P", palette=Image.ADAPTIVE, colors=256) for img in images]
    quantized[0].save(
        path,
        save_all=True,
        append_images=quantized[1:],
        duration=duration,
        loop=loop,
        optimize=True,
    )
