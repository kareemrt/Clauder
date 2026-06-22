from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> "Vec3":
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: float) -> "Vec3":
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__

    def multiply(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def dot(self, other: "Vec3") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def normalize(self) -> "Vec3":
        length = self.length()
        if length == 0:
            return self
        return self * (1.0 / length)

    def reflect(self, normal: "Vec3") -> "Vec3":
        return self - normal * (2 * self.dot(normal))

    def clamp(self, lo: float = 0.0, hi: float = 1.0) -> "Vec3":
        return Vec3(
            min(max(self.x, lo), hi),
            min(max(self.y, lo), hi),
            min(max(self.z, lo), hi),
        )

    def to_rgb(self) -> tuple[int, int, int]:
        c = self.clamp()
        return (round(c.x * 255), round(c.y * 255), round(c.z * 255))
