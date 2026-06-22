from __future__ import annotations

import math
from dataclasses import dataclass

from .ray import Ray
from .vector import Vec3


@dataclass(frozen=True, slots=True)
class Camera:
    position: Vec3
    look_at: Vec3
    up: Vec3
    fov_degrees: float
    width: int
    height: int

    @property
    def basis(self) -> tuple[Vec3, Vec3, Vec3]:
        forward = (self.look_at - self.position).normalize()
        right = forward.cross(self.up).normalize()
        true_up = right.cross(forward)
        return forward, right, true_up

    def ray_for_pixel(self, px: float, py: float) -> Ray:
        forward, right, true_up = self.basis
        aspect = self.width / self.height
        scale = math.tan(math.radians(self.fov_degrees) / 2)
        ndc_x = (2 * (px / self.width) - 1) * aspect * scale
        ndc_y = (1 - 2 * (py / self.height)) * scale
        direction = (forward + right * ndc_x + true_up * ndc_y).normalize()
        return Ray(self.position, direction)
