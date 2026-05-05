"""Procedural planet rendering with surface texture, atmosphere, and rim light."""
import numpy as np
from .noise import fbm


PLANET_THEMES = {
    "gas_giant": {
        "bands": True,
        "colors": [(0.65, 0.45, 0.25), (0.85, 0.70, 0.45), (0.95, 0.85, 0.65),
                   (0.70, 0.50, 0.30), (0.55, 0.40, 0.20)],
        "atmo_color": (0.80, 0.60, 0.30),
        "atmo_strength": 0.45,
    },
    "ice_world": {
        "bands": False,
        "colors": [(0.55, 0.70, 0.90), (0.80, 0.90, 1.00), (0.95, 0.98, 1.00),
                   (0.40, 0.55, 0.75), (0.65, 0.80, 0.95)],
        "atmo_color": (0.70, 0.85, 1.00),
        "atmo_strength": 0.35,
    },
    "lava_world": {
        "bands": False,
        "colors": [(0.15, 0.03, 0.01), (0.50, 0.10, 0.01), (0.90, 0.30, 0.05),
                   (1.00, 0.55, 0.10), (1.00, 0.85, 0.30)],
        "atmo_color": (1.00, 0.35, 0.05),
        "atmo_strength": 0.55,
    },
    "ocean_world": {
        "bands": False,
        "colors": [(0.02, 0.08, 0.35), (0.05, 0.20, 0.60), (0.10, 0.40, 0.80),
                   (0.20, 0.65, 0.85), (0.55, 0.88, 0.95)],
        "atmo_color": (0.30, 0.65, 1.00),
        "atmo_strength": 0.40,
    },
    "desert_world": {
        "bands": False,
        "colors": [(0.35, 0.20, 0.05), (0.65, 0.42, 0.15), (0.85, 0.65, 0.30),
                   (0.90, 0.78, 0.55), (0.70, 0.55, 0.25)],
        "atmo_color": (0.90, 0.65, 0.25),
        "atmo_strength": 0.30,
    },
}


def _sphere_mask(size: int) -> tuple:
    """Returns (mask, nx, ny, nz) for a unit sphere."""
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j]
    r2 = x * x + y * y
    mask = r2 <= 1.0
    nz = np.sqrt(np.clip(1.0 - r2, 0, 1))
    return mask, x, y, nz


def render_planet(size: int, theme_name: str, rng: np.random.Generator,
                  light_dir: np.ndarray = None) -> np.ndarray:
    """Render a planet as a size x size RGBA float array."""
    if light_dir is None:
        light_dir = np.array([0.6, 0.4, 0.8])
    light_dir = light_dir / (np.linalg.norm(light_dir) + 1e-9)
    theme = PLANET_THEMES[theme_name]
    colors = [np.array(c) for c in theme["colors"]]
    atmo_col = np.array(theme["atmo_color"])
    atmo_str = theme["atmo_strength"]

    mask, nx, ny, nz = _sphere_mask(size)

    # Surface texture via fBm
    surface = fbm(size, size, octaves=6, lacunarity=2.1, gain=0.5,
                  base_scale=size / 3.5, rng=rng)

    if theme["bands"]:
        # Gas giant: horizontal banding + noise distortion
        band_noise = fbm(size, size, octaves=4, lacunarity=2.0, gain=0.45,
                         base_scale=size / 8.0, rng=rng) * 0.3
        ys = np.linspace(0, 1, size)
        band_base = np.sin(ys * np.pi * 12 + band_noise.T).T * 0.5 + 0.5
        surface = surface * 0.3 + band_base * 0.7

    surface = np.clip(surface, 0, 1)

    # Map surface value to color via multi-stop interpolation
    n_colors = len(colors)
    rgb_surface = np.zeros((size, size, 3))
    step = 1.0 / (n_colors - 1)
    for i in range(n_colors - 1):
        t0, t1 = i * step, (i + 1) * step
        seg_mask = (surface >= t0) & (surface < t1)
        alpha = np.where(seg_mask, (surface - t0) / (step + 1e-9), 0.0)
        for ch in range(3):
            rgb_surface[:, :, ch] += seg_mask * (
                colors[i][ch] * (1 - alpha) + colors[i + 1][ch] * alpha
            )
    rgb_surface[:, :, :] += (surface >= 1.0 - step)[:, :, np.newaxis] * colors[-1]
    rgb_surface = np.clip(rgb_surface, 0, 1)

    # Lambertian diffuse lighting
    diffuse = np.clip(
        nx * light_dir[0] + ny * light_dir[1] + nz * light_dir[2], 0, 1
    )
    ambient = 0.08
    lit = rgb_surface * (ambient + (1 - ambient) * diffuse[:, :, np.newaxis])

    # Specular highlight
    half = light_dir + np.array([0, 0, 1])
    half = half / (np.linalg.norm(half) + 1e-9)
    spec_raw = np.clip(
        nx * half[0] + ny * half[1] + nz * half[2], 0, 1
    ) ** 28
    lit = np.clip(lit + spec_raw[:, :, np.newaxis] * 0.35, 0, 1)

    # Atmospheric rim glow
    rim = np.clip(1.0 - nz, 0, 1) ** 1.5
    lit = lit * (1 - rim[:, :, np.newaxis] * atmo_str) + \
          atmo_col * rim[:, :, np.newaxis] * atmo_str

    # Compose RGBA
    rgba = np.zeros((size, size, 4), dtype=np.float32)
    rgba[:, :, :3] = np.where(mask[:, :, np.newaxis], np.clip(lit, 0, 1), 0)
    rgba[:, :, 3] = mask.astype(float)
    return rgba
