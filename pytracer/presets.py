from __future__ import annotations

from .camera import Camera
from .lights import PointLight
from .materials import Material
from .scene import Scene
from .shapes import Plane, Sphere
from .vector import Vec3


def _checkerboard_floor() -> Plane:
    return Plane(
        point=Vec3(0, 0, 0),
        normal=Vec3(0, 1, 0),
        material=Material(color=Vec3(0.9, 0.9, 0.9), specular=0.1, shininess=10),
        checker_material=Material(color=Vec3(0.08, 0.08, 0.1), specular=0.1, shininess=10),
        checker_size=1.0,
    )


def showcase(width: int = 640, height: int = 480) -> tuple[Camera, Scene]:
    floor = _checkerboard_floor()
    red_sphere = Sphere(
        Vec3(-1.4, 0.7, -0.5), 0.7, Material(Vec3(0.9, 0.2, 0.2), reflectivity=0.1)
    )
    mirror_sphere = Sphere(
        Vec3(0.4, 0.9, -1.5),
        0.9,
        Material(Vec3(0.9, 0.9, 0.9), reflectivity=0.85, specular=1.0, shininess=300),
    )
    blue_sphere = Sphere(
        Vec3(1.6, 0.5, 0.6), 0.5, Material(Vec3(0.25, 0.55, 0.9), reflectivity=0.35)
    )

    scene = Scene(
        objects=[floor, red_sphere, mirror_sphere, blue_sphere],
        lights=[
            PointLight(Vec3(-4, 6, 2), Vec3(1, 1, 1), intensity=1.0),
            PointLight(Vec3(4, 3, 4), Vec3(1, 0.9, 0.8), intensity=0.55),
        ],
        ambient_light=0.15,
    )
    camera = Camera(
        position=Vec3(0, 1.4, 4.5),
        look_at=Vec3(0, 0.5, -0.5),
        up=Vec3(0, 1, 0),
        fov_degrees=60,
        width=width,
        height=height,
    )
    return camera, scene


def reflective_trio(width: int = 640, height: int = 480) -> tuple[Camera, Scene]:
    floor = _checkerboard_floor()
    colors = [Vec3(0.85, 0.2, 0.3), Vec3(0.2, 0.8, 0.4), Vec3(0.25, 0.4, 0.9)]
    spheres = [
        Sphere(
            Vec3((i - 1) * 1.4, 0.6, -0.4 + i * 0.2),
            0.6,
            Material(colors[i], reflectivity=0.7, specular=1.0, shininess=400),
        )
        for i in range(3)
    ]
    scene = Scene(
        objects=[floor, *spheres],
        lights=[
            PointLight(Vec3(0, 6, 3), Vec3(1, 1, 1), intensity=1.0),
            PointLight(Vec3(-5, 2, -2), Vec3(0.7, 0.8, 1.0), intensity=0.4),
        ],
        ambient_light=0.12,
    )
    camera = Camera(
        position=Vec3(0, 1.6, 5),
        look_at=Vec3(0, 0.5, -0.2),
        up=Vec3(0, 1, 0),
        fov_degrees=55,
        width=width,
        height=height,
    )
    return camera, scene


def macro(width: int = 640, height: int = 480) -> tuple[Camera, Scene]:
    big_mirror = Sphere(
        Vec3(0, 1.0, 0), 1.0, Material(Vec3(1.0, 1.0, 1.0), reflectivity=0.9, specular=1.0, shininess=500)
    )
    orbiting = [
        Sphere(Vec3(-1.6, 0.35, 1.2), 0.35, Material(Vec3(0.95, 0.35, 0.2))),
        Sphere(Vec3(1.7, 0.3, 1.0), 0.3, Material(Vec3(0.3, 0.9, 0.4))),
        Sphere(Vec3(0.2, 0.25, 1.9), 0.25, Material(Vec3(0.95, 0.85, 0.2))),
    ]
    floor = _checkerboard_floor()
    scene = Scene(
        objects=[floor, big_mirror, *orbiting],
        lights=[
            PointLight(Vec3(-3, 5, 3), Vec3(1, 1, 1), intensity=1.0),
            PointLight(Vec3(3, 2, -3), Vec3(0.8, 0.85, 1.0), intensity=0.5),
        ],
        ambient_light=0.12,
    )
    camera = Camera(
        position=Vec3(0, 1.8, 4.2),
        look_at=Vec3(0, 1.0, 0),
        up=Vec3(0, 1, 0),
        fov_degrees=50,
        width=width,
        height=height,
    )
    return camera, scene


PRESETS = {
    "showcase": showcase,
    "reflective-trio": reflective_trio,
    "macro": macro,
}
