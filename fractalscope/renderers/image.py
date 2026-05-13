"""PNG image renderer using Pillow."""

from pathlib import Path
import numpy as np

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False


def render_image(rgb: np.ndarray, path: str | Path, scale: int = 1) -> Path:
    """
    Save a fractal RGB array as a PNG file.

    Parameters
    ----------
    rgb   : (H, W, 3) uint8 array
    path  : output file path
    scale : integer upscale factor (e.g. 2 → double resolution)
    """
    if not _PIL_AVAILABLE:
        raise RuntimeError(
            "Pillow is required for PNG export. Install it with:\n"
            "    pip install Pillow"
        )

    img = Image.fromarray(rgb, mode="RGB")
    if scale > 1:
        img = img.resize(
            (rgb.shape[1] * scale, rgb.shape[0] * scale),
            resample=Image.NEAREST,
        )

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)
    return path


def is_available() -> bool:
    return _PIL_AVAILABLE
