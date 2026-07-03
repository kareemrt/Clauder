"""Disco: a reflective floor and a grid of colourful metallic spheres."""

import math
from raytracer import Scene, Camera, Sphere, Plane, Material, PointLight, AmbientLight, Vec3


_PALETTE = [
    Vec3(1.0, 0.2, 0.3),  # red
    Vec3(0.2, 0.8, 1.0),  # cyan
    Vec3(1.0, 0.8, 0.1),  # gold
    Vec3(0.4, 1.0, 0.4),  # green
    Vec3(0.8, 0.2, 1.0),  # purple
    Vec3(1.0, 0.5, 0.1),  # orange
]


def build_disco_scene(t: float = 0.0, width: int = 80, height: int = 40):
    scene = Scene()
    scene.ambient = AmbientLight(Vec3(0.05, 0.05, 0.08))
    scene.background = Vec3(0.01, 0.01, 0.03)

    # ── mirrored floor ─────────────────────────────────────────────────────
    scene.add(Plane(
        Vec3(0, -1.4, 0),
        Vec3(0, 1, 0),
        Material(
            color=Vec3(0.7, 0.7, 0.8),
            checker_color=Vec3(0.05, 0.05, 0.08),
            checker_scale=1.2,
            diffuse=0.2, specular=0.8, shininess=120,
            reflectivity=0.55,
        ),
    ))

    # ── 5 × 3 grid of metallic spheres ────────────────────────────────────
    cols, rows = 5, 3
    for row in range(rows):
        for col in range(cols):
            idx = (row * cols + col) % len(_PALETTE)
            color = _PALETTE[idx]
            x = (col - cols // 2) * 1.6
            z = row * 1.6 + 4.0
            # each sphere bobs at different phase
            y = math.sin(t + col * 0.7 + row * 1.1) * 0.3 - 0.3
            scene.add(Sphere(
                Vec3(x, y, z),
                0.58,
                Material(
                    color=color,
                    diffuse=0.4, specular=1.0, shininess=160,
                    reflectivity=0.45,
                ),
            ))

    # ── spinning coloured lights ────────────────────────────────────────────
    n_lights = 3
    for i in range(n_lights):
        angle = t * 1.5 + i * (2 * math.pi / n_lights)
        lx = math.cos(angle) * 5
        lz = math.sin(angle) * 3 + 6
        light_color = _PALETTE[i * 2 % len(_PALETTE)]
        scene.add_light(PointLight(Vec3(lx, 4, lz), light_color, intensity=1.5))

    # Soft fill from above
    scene.add_light(PointLight(Vec3(0, 8, 6), Vec3(0.4, 0.4, 0.6), intensity=0.5))

    aspect = (width * 0.5) / height
    camera = Camera(
        position=Vec3(0, 2.5, -3.5),
        look_at=Vec3(0, -0.3, 5),
        up=Vec3(0, 1, 0),
        fov_deg=65,
        aspect=aspect,
    )
    return scene, camera
