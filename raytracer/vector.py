"""3D vector math — the foundation of everything."""

import math


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # ── arithmetic ─────────────────────────────────────────────────────────
    def __add__(self, o):  return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)
    def __sub__(self, o):  return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)
    def __neg__(self):     return Vec3(-self.x, -self.y, -self.z)
    def __mul__(self, s):  return Vec3(self.x * s, self.y * s, self.z * s)
    def __rmul__(self, s): return self.__mul__(s)
    def __truediv__(self, s): return Vec3(self.x / s, self.y / s, self.z / s)

    # ── products ───────────────────────────────────────────────────────────
    def dot(self, o):   return self.x * o.x + self.y * o.y + self.z * o.z
    def cross(self, o):
        return Vec3(
            self.y * o.z - self.z * o.y,
            self.z * o.x - self.x * o.z,
            self.x * o.y - self.y * o.x,
        )
    def hadamard(self, o): return Vec3(self.x * o.x, self.y * o.y, self.z * o.z)

    # ── geometry ───────────────────────────────────────────────────────────
    def length_sq(self): return self.dot(self)
    def length(self):    return math.sqrt(self.length_sq())
    def normalize(self):
        l = self.length()
        return self / l if l > 1e-12 else Vec3(0, 0, 0)
    def reflect(self, n):
        return self - n * (2.0 * self.dot(n))

    # ── color helpers ──────────────────────────────────────────────────────
    def clamp(self, lo=0.0, hi=1.0):
        return Vec3(
            max(lo, min(hi, self.x)),
            max(lo, min(hi, self.y)),
            max(lo, min(hi, self.z)),
        )
    def luminance(self):
        # perceptual luminance (ITU-R BT.709)
        return 0.2126 * self.x + 0.7152 * self.y + 0.0722 * self.z

    def __repr__(self):
        return f"Vec3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
