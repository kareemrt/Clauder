from pathlib import Path
import numpy as np
from PIL import Image


def save_rgb(rgb: np.ndarray, path: str | Path, title: str = "") -> Path:
    """Save an (H, W, 3) uint8 array as a PNG."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.fromarray(rgb, mode="RGB")
    img.save(path, format="PNG", optimize=False)
    print(f"  saved → {path}  ({rgb.shape[1]}×{rgb.shape[0]})")
    return path


def render_contact_sheet(images: list[tuple[np.ndarray, str]],
                          output_path: str | Path,
                          cols: int = 2) -> Path:
    """
    Arrange multiple (rgb, label) images into a contact-sheet PNG.
    All images are scaled to the same size for the sheet.
    """
    if not images:
        raise ValueError("no images to arrange")

    rows = (len(images) + cols - 1) // cols
    # Determine uniform cell size from first image
    h0, w0 = images[0][0].shape[:2]
    cell_h, cell_w = h0, w0

    padding = 12
    total_h = rows * cell_h + (rows + 1) * padding
    total_w = cols * cell_w + (cols + 1) * padding

    canvas = np.zeros((total_h, total_w, 3), dtype=np.uint8)

    for idx, (rgb, _label) in enumerate(images):
        row = idx // cols
        col = idx % cols
        y0 = padding + row * (cell_h + padding)
        x0 = padding + col * (cell_w + padding)
        # Resize if needed
        if rgb.shape[:2] != (cell_h, cell_w):
            img = Image.fromarray(rgb).resize((cell_w, cell_h), Image.LANCZOS)
            rgb = np.array(img)
        canvas[y0:y0 + cell_h, x0:x0 + cell_w] = rgb

    return save_rgb(canvas, output_path, title="Contact Sheet")
