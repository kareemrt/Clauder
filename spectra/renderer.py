"""Rendering engines: ASCII terminal output and PNG image export."""

import numpy as np
from pathlib import Path
from PIL import Image

from .palettes import apply_palette, apply_newton_palette


ASCII_RAMP = " .:-=+*#%@"


def to_ascii(iteration_map: np.ndarray, max_iter: int,
             width: int = 80, height: int = 40) -> str:
    """Convert iteration map to ASCII art string."""
    h, w = iteration_map.shape
    # Downsample to terminal size
    from PIL import Image as _Image
    arr = (iteration_map / max_iter * 255).astype(np.uint8)
    img = _Image.fromarray(arr, mode="L")
    img = img.resize((width, height), _Image.LANCZOS)
    arr_small = np.array(img)

    ramp = ASCII_RAMP
    n = len(ramp) - 1
    lines = []
    for row in arr_small:
        chars = [ramp[int(v / 255 * n)] for v in row]
        lines.append("".join(chars))
    return "\n".join(lines)


def to_ascii_newton(root_map: np.ndarray, speed_map: np.ndarray,
                    width: int = 80, height: int = 40) -> str:
    """ASCII art for Newton fractal using root symbols."""
    ROOT_CHARS = ["①", "②", "③", "·"]
    h, w = root_map.shape

    # Simple nearest-neighbor downsample
    row_idx = np.linspace(0, h - 1, height, dtype=int)
    col_idx = np.linspace(0, w - 1, width, dtype=int)
    small = root_map[np.ix_(row_idx, col_idx)]

    lines = []
    for row in small:
        chars = []
        for v in row:
            if v == 0:
                chars.append(ROOT_CHARS[0])
            elif v == 1:
                chars.append(ROOT_CHARS[1])
            elif v == 2:
                chars.append(ROOT_CHARS[2])
            else:
                chars.append(" ")
        lines.append("".join(chars))
    return "\n".join(lines)


def save_image(iteration_map: np.ndarray, output_path: str,
               palette: str = "inferno", max_iter: int = 256,
               scale: int = 1) -> Path:
    """Save fractal as a PNG image."""
    rgb = apply_palette(iteration_map, palette_name=palette, max_iter=max_iter)
    img = Image.fromarray(rgb, mode="RGB")
    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    return path


def save_newton_image(root_map: np.ndarray, speed_map: np.ndarray,
                      output_path: str, scale: int = 1) -> Path:
    """Save Newton fractal as a PNG image."""
    rgb = apply_newton_palette(root_map, speed_map)
    img = Image.fromarray(rgb, mode="RGB")
    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    return path


def create_contact_sheet(images: list[tuple[str, np.ndarray | tuple]],
                         output_path: str, palette: str = "inferno",
                         max_iter: int = 256, cols: int = 3,
                         thumb_size: int = 256) -> Path:
    """Create a contact sheet of multiple fractal thumbnails."""
    rows = (len(images) + cols - 1) // cols
    sheet_w = cols * thumb_size
    sheet_h = rows * thumb_size
    sheet = Image.new("RGB", (sheet_w, sheet_h), (10, 10, 10))

    for i, (label, data) in enumerate(images):
        if isinstance(data, tuple):
            # Newton fractal
            rgb = apply_newton_palette(data[0], data[1])
        else:
            rgb = apply_palette(data, palette_name=palette, max_iter=max_iter)
        thumb = Image.fromarray(rgb, mode="RGB").resize(
            (thumb_size, thumb_size), Image.LANCZOS
        )
        r, c = divmod(i, cols)
        sheet.paste(thumb, (c * thumb_size, r * thumb_size))

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, format="PNG")
    return path
