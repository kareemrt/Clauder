"""Simplified solar system: Sun + three planets + a moon."""

import math
from raytracer import Scene, Camera, Sphere, Plane, Material, PointLight, AmbientLight, Vec3


def build_solar_scene(t: float = 0.0, width: int = 80, height: int = 40):
    scene = Scene()
    scene.ambient = AmbientLight(Vec3(0.02, 0.02, 0.04))
    scene.background = Vec3(0.0, 0.0, 0.03)

    # ── sun ────────────────────────────────────────────────────────────────
    scene.add(Sphere(
        Vec3(0, 0, 6),
        1.5,
        Material(
            color=Vec3(1.0, 0.85, 0.2),
            ambient=1.0, diffuse=0.0, specular=0.0,
        ),
    ))

    # ── planets ────────────────────────────────────────────────────────────
    def planet(orbit_r, speed, phase, radius, color, reflectivity=0.05):
        angle = t * speed + phase
        cx = math.cos(angle) * orbit_r
        cz = math.sin(angle) * orbit_r + 6
        scene.add(Sphere(
            Vec3(cx, 0, cz),
            radius,
            Material(color=color, diffuse=0.8, specular=0.3,
                     shininess=30, reflectivity=reflectivity),
        ))
        return cx, cz

    # Mercury
    planet(2.2, 4.1, 0.0, 0.18, Vec3(0.7, 0.6, 0.5))
    # Venus
    planet(3.0, 1.6, 1.0, 0.3, Vec3(0.9, 0.75, 0.4))
    # Earth
    ex, ez = planet(4.0, 1.0, 2.5, 0.35, Vec3(0.2, 0.5, 0.9), reflectivity=0.15)
    # Mars
    planet(5.0, 0.53, 0.8, 0.25, Vec3(0.8, 0.3, 0.1))

    # Moon (orbits Earth)
    moon_angle = t * 8 + 0.3
    scene.add(Sphere(
        Vec3(ex + math.cos(moon_angle) * 0.65, math.sin(moon_angle) * 0.2, ez + 0.65 * math.sin(moon_angle) * 0.4),
        0.09,
        Material(color=Vec3(0.75, 0.75, 0.7), diffuse=0.7, specular=0.1),
    ))

    # ── starfield (very small bright spheres far away) ─────────────────────
    import random
    rng = random.Random(42)
    for _ in range(18):
        sx = rng.uniform(-12, 12)
        sy = rng.uniform(-5, 5)
        sz = rng.uniform(18, 30)
        bri = rng.uniform(0.7, 1.0)
        scene.add(Sphere(
            Vec3(sx, sy, sz),
            0.04,
            Material(color=Vec3(bri, bri, bri * 0.95), ambient=1.0, diffuse=0, specular=0),
        ))

    # ── sun acts as point light ────────────────────────────────────────────
    scene.add_light(PointLight(Vec3(0, 0, 6), Vec3(1.0, 0.92, 0.7), intensity=2.0))
    scene.add_light(PointLight(Vec3(0, 8, -2), Vec3(0.1, 0.1, 0.3), intensity=0.3))

    aspect = (width * 0.5) / height
    camera = Camera(
        position=Vec3(0, 3.5, -4),
        look_at=Vec3(0, 0, 6),
        up=Vec3(0, 1, 0),
        fov_deg=70,
        aspect=aspect,
    )
    return scene, camera
