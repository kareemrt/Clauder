"""Scene container and Camera."""

import math
from typing import List, Optional
from .vector import Vec3
from .ray import Ray
from .objects import HitRecord
from .light import AmbientLight, PointLight


class Camera:
    def __init__(
        self,
        position: Vec3,
        look_at: Vec3,
        up: Vec3,
        fov_deg: float,
        aspect: float,
    ):
        self.position = position
        fov_rad = math.radians(fov_deg)
        h = math.tan(fov_rad / 2)

        w = (position - look_at).normalize()
        u = up.cross(w).normalize()
        v = w.cross(u)

        viewport_h = 2.0 * h
        viewport_w = aspect * viewport_h

        self._horizontal = u * viewport_w
        self._vertical = v * viewport_h
        self._lower_left = (
            position - self._horizontal / 2 - self._vertical / 2 - w
        )

    def get_ray(self, s: float, t: float) -> Ray:
        direction = (
            self._lower_left
            + self._horizontal * s
            + self._vertical * t
            - self.position
        )
        return Ray(self.position, direction)


class Scene:
    def __init__(self):
        self.objects: List = []
        self.lights: List[PointLight] = []
        self.ambient: AmbientLight = AmbientLight()
        self.background: Vec3 = Vec3(0.05, 0.07, 0.12)

    def add(self, obj):
        self.objects.append(obj)
        return self

    def add_light(self, light):
        self.lights.append(light)
        return self

    def hit(self, ray, t_min=1e-4, t_max=1e18) -> Optional[HitRecord]:
        closest: Optional[HitRecord] = None
        for obj in self.objects:
            rec = obj.intersect(ray, t_min, t_max if closest is None else closest.t)
            if rec is not None:
                closest = rec
        return closest
