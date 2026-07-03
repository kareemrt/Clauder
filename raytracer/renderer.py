"""Core ray tracing algorithm: Phong shading, shadows, reflections."""

from .vector import Vec3
from .ray import Ray
from .scene import Scene


EPSILON = 1e-4


class Renderer:
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth

    def trace(self, ray: Ray, scene: Scene, depth: int = 0) -> Vec3:
        if depth > self.max_depth:
            return Vec3(0, 0, 0)

        rec = scene.hit(ray)
        if rec is None:
            return self._sky(ray)

        mat = rec.material
        point = rec.point
        normal = rec.normal

        # ambient
        color = mat.color.hadamard(scene.ambient.color) * mat.ambient

        for light in scene.lights:
            to_light = (light.position - point)
            dist = to_light.length()
            l_dir = to_light / dist

            # shadow test
            shadow_ray = Ray(point + normal * EPSILON, l_dir)
            shadow_hit = scene.hit(shadow_ray, EPSILON, dist - EPSILON)
            if shadow_hit is not None:
                continue

            # diffuse (Lambertian)
            n_dot_l = max(0.0, normal.dot(l_dir))
            diffuse_contrib = mat.color.hadamard(light.color) * (
                mat.diffuse * n_dot_l * light.intensity
            )

            # specular (Blinn-Phong)
            view_dir = (-ray.direction).normalize()
            half_vec = (l_dir + view_dir).normalize()
            n_dot_h = max(0.0, normal.dot(half_vec))
            import math
            spec_factor = math.pow(n_dot_h, mat.shininess) if n_dot_h > 0 else 0.0
            specular_contrib = light.color * (mat.specular * spec_factor * light.intensity)

            # soft distance attenuation
            attenuation = 1.0 / (1.0 + 0.02 * dist + 0.005 * dist * dist)

            color = color + (diffuse_contrib + specular_contrib) * attenuation

        # reflection
        if mat.reflectivity > 0 and depth < self.max_depth:
            reflect_dir = ray.direction.reflect(normal)
            reflect_ray = Ray(point + normal * EPSILON, reflect_dir)
            reflect_color = self.trace(reflect_ray, scene, depth + 1)
            color = color * (1.0 - mat.reflectivity) + reflect_color * mat.reflectivity

        return color.clamp()

    def _sky(self, ray: Ray) -> Vec3:
        # gradient sky: deep blue at horizon → dark navy at zenith
        t = 0.5 * (ray.direction.normalize().y + 1.0)
        horizon = Vec3(0.6, 0.75, 0.9)
        zenith = Vec3(0.05, 0.08, 0.2)
        return zenith * t + horizon * (1.0 - t)

    def render(self, scene: Scene, camera, width: int, height: int) -> list:
        """Return a 2-D list of Vec3 color values (row-major)."""
        pixels = []
        for row in range(height):
            scanline = []
            for col in range(width):
                u = col / (width - 1)
                v = 1.0 - row / (height - 1)
                ray = camera.get_ray(u, v)
                scanline.append(self.trace(ray, scene))
            pixels.append(scanline)
        return pixels
