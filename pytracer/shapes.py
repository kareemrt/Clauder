from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from .materials import Material
from .ray import Ray
from .vector import Vec3


@dataclass(frozen=True, slots=True)
class Hit:
    t: float
    point: Vec3
    normal: Vec3
    material: Material


class Shape:
    def intersect(self, ray: Ray) -> Optional[Hit]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Sphere(Shape):
    center: Vec3
    radius: float
    material: Material

    def intersect(self, ray: Ray) -> Optional[Hit]:
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None
        sqrt_d = math.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)
        t = t1 if t1 > 1e-4 else t2
        if t <= 1e-4:
            return None
        point = ray.point_at(t)
        normal = (point - self.center).normalize()
        return Hit(t, point, normal, self.material)


@dataclass(frozen=True, slots=True)
class Plane(Shape):
    point: Vec3
    normal: Vec3
    material: Material
    checker_material: Optional[Material] = None
    checker_size: float = 1.0

    def intersect(self, ray: Ray) -> Optional[Hit]:
        denom = ray.direction.dot(self.normal)
        if abs(denom) < 1e-6:
            return None
        t = (self.point - ray.origin).dot(self.normal) / denom
        if t <= 1e-4:
            return None
        point = ray.point_at(t)
        material = self._material_at(point)
        normal = self.normal if denom < 0 else -self.normal
        return Hit(t, point, normal, material)

    def _material_at(self, point: Vec3) -> Material:
        if self.checker_material is None:
            return self.material
        checker = (
            math.floor(point.x / self.checker_size) + math.floor(point.z / self.checker_size)
        ) % 2
        return self.material if checker == 0 else self.checker_material
