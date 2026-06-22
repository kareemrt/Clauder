from pytracer.materials import Material
from pytracer.ray import Ray
from pytracer.shapes import Plane, Sphere
from pytracer.vector import Vec3

MATERIAL = Material(color=Vec3(1, 0, 0))


def test_sphere_hit_from_outside():
    sphere = Sphere(Vec3(0, 0, -5), 1.0, MATERIAL)
    ray = Ray(Vec3(0, 0, 0), Vec3(0, 0, -1))
    hit = sphere.intersect(ray)
    assert hit is not None
    assert hit.t == 4.0
    assert hit.normal == Vec3(0, 0, 1)


def test_sphere_miss():
    sphere = Sphere(Vec3(5, 5, -5), 1.0, MATERIAL)
    ray = Ray(Vec3(0, 0, 0), Vec3(0, 0, -1))
    assert sphere.intersect(ray) is None


def test_sphere_behind_ray_is_ignored():
    sphere = Sphere(Vec3(0, 0, 5), 1.0, MATERIAL)
    ray = Ray(Vec3(0, 0, 0), Vec3(0, 0, -1))
    assert sphere.intersect(ray) is None


def test_plane_hit():
    plane = Plane(point=Vec3(0, 0, 0), normal=Vec3(0, 1, 0), material=MATERIAL)
    ray = Ray(Vec3(0, 5, 0), Vec3(0, -1, 0))
    hit = plane.intersect(ray)
    assert hit is not None
    assert hit.t == 5.0
    assert hit.point == Vec3(0, 0, 0)


def test_plane_checker_pattern_alternates():
    plane = Plane(
        point=Vec3(0, 0, 0),
        normal=Vec3(0, 1, 0),
        material=MATERIAL,
        checker_material=Material(color=Vec3(0, 0, 1)),
        checker_size=1.0,
    )
    ray_a = Ray(Vec3(0.5, 5, 0.5), Vec3(0, -1, 0))
    ray_b = Ray(Vec3(1.5, 5, 0.5), Vec3(0, -1, 0))
    hit_a = plane.intersect(ray_a)
    hit_b = plane.intersect(ray_b)
    assert hit_a.material != hit_b.material
