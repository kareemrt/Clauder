"""Render a rotating 3D GIF of an attractor's trajectory."""

from __future__ import annotations

import io

import numpy as np
from PIL import Image

from .render import render_attractor_3d, plt
from .systems import AttractorSystem


def make_rotation_gif(
    trajectory: np.ndarray,
    system: AttractorSystem,
    path: str,
    n_frames: int = 60,
    elev: float = 22,
    duration_ms: int = 60,
    cmap: str = "plasma",
    figsize: tuple[float, float] = (5, 5),
    dpi: int = 90,
):
    frames = []
    azimuths = np.linspace(0, 360, n_frames, endpoint=False)
    for azim in azimuths:
        fig, _ = render_attractor_3d(
            trajectory, system, elev=elev, azim=azim, cmap=cmap, figsize=figsize, dpi=dpi
        )
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor="black")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).convert("P", palette=Image.ADAPTIVE))

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    return path
