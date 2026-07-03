"""Classic three-sphere scene with a checkerboard floor."""

import math
from raytracer import Scene, Camera, Sphere, Plane, Material, PointLight, AmbientLight, Vec3


def build_classic_scene(t: float = 0.0, width: int = 80, height: int = 40):
    """
    t  — animation parameter in [0, 2π]
    """
    scene = Scene()
    scene.ambient = AmbientLight(Vec3(0.12, 0.14, 0.20))
    scene.background = Vec3(0.04, 0.06, 0.12)

    # ── floor ──────────────────────────────────────────────────────────────
    floor_mat = Material(
        color=Vec3(0.85, 0.85, 0.85),
        checker_color=Vec3(0.15, 0.15, 0.2),
        checker_scale=1.5,
        diffuse=0.7,
        specular=0.1,
        reflectivity=0.15,
    )
    scene.add(Plane(Vec3(0, -1.2, 0), Vec3(0, 1, 0), floor_mat))

    # ── spheres ────────────────────────────────────────────────────────────
    r = 2.5  # orbit radius
    bob = math.sin(t * 2) * 0.15

    # Left sphere: ruby red, very reflective
    angle1 = t
    scene.add(Sphere(
        Vec3(math.cos(angle1) * r, 0.0 + bob, math.sin(angle1) * r + 3),
        0.9,
        Material(
            color=Vec3(0.9, 0.15, 0.15),
            diffuse=0.6, specular=0.9, shininess=80.0,
            reflectivity=0.4,
        ),
    ))

    # Centre sphere: glass-like silver
    angle2 = t + 2 * math.pi / 3
    scene.add(Sphere(
        Vec3(math.cos(angle2) * r, 0.15 + bob, math.sin(angle2) * r + 3),
        1.1,
        Material(
            color=Vec3(0.9, 0.92, 1.0),
            diffuse=0.3, specular=1.0, shininess=200.0,
            reflectivity=0.65,
        ),
    ))

    # Right sphere: ocean blue, matte
    angle3 = t + 4 * math.pi / 3
    scene.add(Sphere(
        Vec3(math.cos(angle3) * r, -0.1 + bob, math.sin(angle3) * r + 3),
        0.8,
        Material(
            color=Vec3(0.1, 0.4, 0.9),
            diffuse=0.85, specular=0.4, shininess=32.0,
            reflectivity=0.1,
        ),
    ))

    # Small accent sphere (gold)
    scene.add(Sphere(
        Vec3(0, -0.7, 3.5),
        0.45,
        Material(
            color=Vec3(1.0, 0.75, 0.1),
            diffuse=0.5, specular=1.0, shininess=128.0,
            reflectivity=0.5,
        ),
    ))

    # ── lights ─────────────────────────────────────────────────────────────
    scene.add_light(PointLight(Vec3(5, 8, -2), Vec3(1.0, 0.95, 0.85), intensity=1.2))
    scene.add_light(PointLight(Vec3(-6, 4, 1), Vec3(0.3, 0.4, 0.9), intensity=0.6))

    aspect = (width * 0.5) / height  # × 0.5 because chars are doubled
    camera = Camera(
        position=Vec3(0, 2.5, -5),
        look_at=Vec3(0, 0, 3),
        up=Vec3(0, 1, 0),
        fov_deg=55,
        aspect=aspect,
    )
    return scene, camera
