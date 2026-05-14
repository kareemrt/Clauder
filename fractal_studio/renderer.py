"""Render fractals to PNG files and an HTML gallery."""
import base64
import math
import os
from typing import List, Optional, Tuple

from .colormaps import get_color
from .fractals import burning_ship, julia, mandelbrot, newton_cubic
from .png_writer import write_png
from .presets import PRESETS

# Newton fractal uses three fixed root colors (dark base + bright highlight).
_NEWTON_COLORS = [
    ((170, 35, 35),  (255, 120, 120)),   # root 0 — reds
    ((35,  70, 200), (120, 160, 255)),   # root 1 — blues
    ((35, 155, 50),  (130, 230, 140)),   # root 2 — greens
]


def _pixel_coords(px: int, py: int, width: int, height: int,
                  cx: float, cy: float, zoom: float) -> Tuple[float, float]:
    """Map pixel (px, py) to complex-plane (real, imag).

    zoom is half-height in complex units; the x-axis is scaled by aspect ratio.
    The y-axis is flipped so that positive imaginary is up.
    """
    aspect = width / height
    real = cx + (px / width  - 0.5) * 2.0 * zoom * aspect
    imag = cy - (py / height - 0.5) * 2.0 * zoom   # flip y
    return real, imag


def _escape_color(smooth: float, palette: str, cycle: float) -> Tuple[int, int, int]:
    if smooth == 0.0:
        return (0, 0, 0)
    t = (smooth % cycle) / cycle
    return get_color(t, palette)


def _newton_color(root_idx: int, frac: float) -> Tuple[int, int, int]:
    if root_idx < 0:
        return (8, 8, 12)
    dark, light = _NEWTON_COLORS[root_idx % len(_NEWTON_COLORS)]
    brightness = 1.0 - math.sqrt(frac)          # fast convergence → bright
    return tuple(int(d + brightness * (l - d)) for d, l in zip(dark, light))


def render_preset(key: str, width: int = 320, height: int = 240) -> List[Tuple[int, int, int]]:
    """Render one preset and return a flat list of (r, g, b) pixels."""
    p = PRESETS[key]
    cx, cy = p["center"]
    zoom     = p["zoom"]
    max_iter = p["max_iter"]
    ftype    = p["type"]
    palette  = p.get("palette", "inferno")
    cycle    = p.get("cycle", 32.0)

    pixels = []
    for py in range(height):
        for px in range(width):
            real, imag = _pixel_coords(px, py, width, height, cx, cy, zoom)

            if ftype == "mandelbrot":
                smooth = mandelbrot(real, imag, max_iter)
                color  = _escape_color(smooth, palette, cycle)

            elif ftype == "julia":
                smooth = julia(real, imag, p["cx"], p["cy"], max_iter)
                color  = _escape_color(smooth, palette, cycle)

            elif ftype == "burning_ship":
                smooth = burning_ship(real, imag, max_iter)
                color  = _escape_color(smooth, palette, cycle)

            elif ftype == "newton":
                root_idx, frac = newton_cubic(real, imag, max_iter)
                color = _newton_color(root_idx, frac)

            else:
                color = (0, 0, 0)

            pixels.append(color)

    return pixels


def render_gallery(output_dir: str, width: int = 320, height: int = 240,
                   verbose: bool = True) -> str:
    """Render all presets, write PNGs, and produce a self-contained HTML gallery.

    Returns the path of the generated HTML file.
    """
    os.makedirs(output_dir, exist_ok=True)
    generated = []

    for key, preset in PRESETS.items():
        if verbose:
            print(f"  Rendering {preset['name']} ...", flush=True)
        pixels   = render_preset(key, width, height)
        png_path = os.path.join(output_dir, f"{key}.png")
        write_png(png_path, pixels, width, height)
        generated.append((key, preset, png_path))
        if verbose:
            print(f"    Saved: {png_path}", flush=True)

    html_path = os.path.join(output_dir, "gallery.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(_build_html(generated))

    return html_path


# ── HTML / CSS ──────────────────────────────────────────────────────────────

def _build_html(generated: list) -> str:
    cards = []
    for key, preset, png_path in generated:
        with open(png_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        label = preset["type"].replace("_", " ").title()
        cards.append(f"""
        <div class="card">
            <img src="data:image/png;base64,{b64}" alt="{preset['name']}" loading="lazy">
            <div class="info">
                <h3>{preset['name']}</h3>
                <p>{preset['description']}</p>
                <span class="tag">{label}</span>
            </div>
        </div>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fractal Studio — Gallery</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:#08080f;color:#ddddf0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}}
  header{{text-align:center;padding:3.5rem 1rem 2rem;background:linear-gradient(180deg,#160824 0%,#08080f 100%)}}
  h1{{font-size:2.8rem;font-weight:800;letter-spacing:-1px;
      background:linear-gradient(135deg,#a78bfa,#60a5fa,#34d399);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
  header p{{margin-top:.75rem;color:#7070a0;font-size:1.05rem}}
  .gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));
            gap:1.75rem;max-width:1300px;margin:2rem auto;padding:0 1.5rem}}
  .card{{background:#111120;border:1px solid #22223a;border-radius:14px;
         overflow:hidden;transition:transform .2s,box-shadow .2s}}
  .card:hover{{transform:translateY(-5px);box-shadow:0 24px 48px rgba(0,0,0,.6)}}
  .card img{{width:100%;display:block}}
  .info{{padding:1.25rem}}
  .info h3{{font-size:1.1rem;font-weight:600;color:#c8c8f0;margin-bottom:.35rem}}
  .info p{{color:#606080;font-size:.88rem;line-height:1.55;margin-bottom:.75rem}}
  .tag{{display:inline-block;padding:.2rem .65rem;background:#1a1a2e;
        border:1px solid #303060;border-radius:100px;font-size:.73rem;
        color:#7878c0;text-transform:uppercase;letter-spacing:.06em}}
  footer{{text-align:center;padding:3rem;color:#303050;font-size:.82rem}}
</style>
</head>
<body>
<header>
  <h1>Fractal Studio</h1>
  <p>Mathematical beauty rendered in pure Python — zero external dependencies</p>
</header>
<main class="gallery">{"".join(cards)}
</main>
<footer>Generated by Fractal Studio &bull; Pure Python stdlib only</footer>
</body>
</html>"""
