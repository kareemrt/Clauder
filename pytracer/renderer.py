from __future__ import annotations

import random
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Optional

from .camera import Camera
from .ray import Ray
from .scene import Scene
from .shapes import Hit
from .vector import Vec3

DEFAULT_MAX_DEPTH = 3
DEFAULT_SAMPLES = 4


def closest_hit(ray: Ray, scene: Scene) -> Optional[Hit]:
    closest: Optional[Hit] = None
    for obj in scene.objects:
        hit = obj.intersect(ray)
        if hit is not None and (closest is None or hit.t < closest.t):
            closest = hit
    return closest


def in_shadow(point: Vec3, light, scene: Scene) -> bool:
    to_light = light.position - point
    distance = to_light.length()
    shadow_ray = Ray(point, to_light.normalize())
    hit = closest_hit(shadow_ray, scene)
    return hit is not None and hit.t < distance


def shade(hit: Hit, ray: Ray, scene: Scene, depth: int, max_depth: int) -> Vec3:
    material = hit.material
    view_dir = -ray.direction
    color = material.color * (material.ambient * scene.ambient_light)

    for light in scene.lights:
        if in_shadow(hit.point, light, scene):
            continue
        light_dir = (light.position - hit.point).normalize()
        diffuse_intensity = max(hit.normal.dot(light_dir), 0.0)
        color = color + material.color.multiply(light.color) * (
            material.diffuse * diffuse_intensity * light.intensity
        )
        half_dir = (light_dir + view_dir).normalize()
        spec_intensity = max(hit.normal.dot(half_dir), 0.0) ** material.shininess
        color = color + light.color * (material.specular * spec_intensity * light.intensity)

    if material.reflectivity > 0 and depth < max_depth:
        reflected_dir = ray.direction.reflect(hit.normal)
        reflected_ray = Ray(hit.point + hit.normal * 1e-4, reflected_dir)
        reflected_color = trace(reflected_ray, scene, depth + 1, max_depth)
        color = color * (1 - material.reflectivity) + reflected_color * material.reflectivity

    return color


def trace(ray: Ray, scene: Scene, depth: int = 0, max_depth: int = DEFAULT_MAX_DEPTH) -> Vec3:
    hit = closest_hit(ray, scene)
    if hit is None:
        return scene.background(ray.direction)
    return shade(hit, ray, scene, depth, max_depth)


def render_row(args: tuple) -> tuple[int, list[tuple[int, int, int]]]:
    y, camera, scene, samples, max_depth, seed = args
    rng = random.Random(seed)
    pixels = []
    for x in range(camera.width):
        color = Vec3(0, 0, 0)
        for _ in range(samples):
            jitter_x = x + (rng.random() if samples > 1 else 0.5)
            jitter_y = y + (rng.random() if samples > 1 else 0.5)
            ray = camera.ray_for_pixel(jitter_x, jitter_y)
            color = color + trace(ray, scene, 0, max_depth)
        pixels.append((color * (1.0 / samples)).to_rgb())
    return y, pixels


def render(
    camera: Camera,
    scene: Scene,
    samples: int = DEFAULT_SAMPLES,
    max_depth: int = DEFAULT_MAX_DEPTH,
    workers: int = 1,
    progress: Optional[Callable[[int, int], None]] = None,
) -> dict[int, list[tuple[int, int, int]]]:
    rows: dict[int, list[tuple[int, int, int]]] = {}
    tasks = [(y, camera, scene, samples, max_depth, y) for y in range(camera.height)]

    if workers <= 1:
        for task in tasks:
            y, pixels = render_row(task)
            rows[y] = pixels
            if progress:
                progress(y, camera.height)
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for i, (y, pixels) in enumerate(pool.map(render_row, tasks)):
                rows[y] = pixels
                if progress:
                    progress(i, camera.height)

    return rows
