"""Scene objects: Sphere, Plane, and their Material descriptor."""

import math
from dataclasses import dataclass, field
from typing import Optional, Tuple
from .vector import Vec3
from .ray import Ray


@dataclass
class Material:
    color: Vec3 = field(default_factory=lambda: Vec3(1, 1, 1))
    ambient: float = 0.15
    diffuse: float = 0.8
    specular: float = 0.5
    shininess: float = 32.0
    reflectivity: float = 0.0
    # checkerboard scale (0 = solid color)
    checker_scale: float = 0.0
    checker_color: Vec3 = field(default_factory=lambda: Vec3(0.1, 0.1, 0.1))


@dataclass
class HitRecord:
    t: float
    point: Vec3
    normal: Vec3
    material: "Material"
    front_face: bool = True


class Sphere:
    def __init__(self, center: Vec3, radius: float, material: Material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray: Ray, t_min=1e-4, t_max=1e18) -> Optional[HitRecord]:
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        half_b = oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        disc = half_b * half_b - a * c
        if disc < 0:
            return None
        sqrt_d = math.sqrt(disc)
        t = (-half_b - sqrt_d) / a
        if t < t_min or t > t_max:
            t = (-half_b + sqrt_d) / a
            if t < t_min or t > t_max:
                return None
        point = ray.at(t)
        outward_normal = (point - self.center) / self.radius
        front_face = ray.direction.dot(outward_normal) < 0
        normal = outward_normal if front_face else -outward_normal
        return HitRecord(t, point, normal, self.material, front_face)


class Plane:
    """Infinite plane defined by a point and a normal."""

    def __init__(self, point: Vec3, normal: Vec3, material: Material):
        self.point = point
        self.normal = normal.normalize()
        self.material = material

    def intersect(self, ray: Ray, t_min=1e-4, t_max=1e18) -> Optional[HitRecord]:
        denom = ray.direction.dot(self.normal)
        if abs(denom) < 1e-8:
            return None
        t = (self.point - ray.origin).dot(self.normal) / denom
        if t < t_min or t > t_max:
            return None
        point = ray.at(t)
        front_face = denom < 0
        normal = self.normal if front_face else -self.normal
        mat = self._checker_material(point) if self.material.checker_scale > 0 else self.material
        return HitRecord(t, point, normal, mat, front_face)

    def _checker_material(self, point: Vec3) -> Material:
        s = self.material.checker_scale
        ix = int(math.floor(point.x / s))
        iz = int(math.floor(point.z / s))
        even = (ix + iz) % 2 == 0
        color = self.material.color if even else self.material.checker_color
        return Material(
            color=color,
            ambient=self.material.ambient,
            diffuse=self.material.diffuse,
            specular=self.material.specular,
            shininess=self.material.shininess,
            reflectivity=self.material.reflectivity,
        )
