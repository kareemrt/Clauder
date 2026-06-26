"""The flocking simulation: Craig Reynolds' boids, plus predators.

Each boid steers according to three local rules computed over its
neighbourhood, on a toroidal (wrap-around) plane:

  separation  - steer away from flockmates that are too close
  alignment   - steer towards the average heading of nearby flockmates
  cohesion    - steer towards the average position of nearby flockmates

Predators (if any) ignore these rules and simply chase the nearest
prey boid; ordinary boids gain a fourth ``evasion`` rule that steers
them away from any predator within ``fear_radius``.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from .boid import Boid
from .vector import Vector2, toroidal_delta


@dataclass
class FlockConfig:
    width: float = 120.0
    height: float = 60.0
    max_speed: float = 6.0
    max_force: float = 0.6
    neighbor_radius: float = 14.0
    separation_radius: float = 5.0
    fear_radius: float = 18.0
    predator_speed: float = 7.5
    separation_weight: float = 1.6
    alignment_weight: float = 1.0
    cohesion_weight: float = 1.0
    evasion_weight: float = 2.2


class Flock:
    def __init__(self, n_boids: int, n_predators: int = 0,
                 config: FlockConfig | None = None, seed: int | None = None):
        self.config = config or FlockConfig()
        rng = random.Random(seed)
        self.boids: list[Boid] = []
        for _ in range(n_boids):
            pos = Vector2(rng.uniform(0, self.config.width), rng.uniform(0, self.config.height))
            angle = rng.uniform(0, math.tau)
            speed = rng.uniform(self.config.max_speed * 0.4, self.config.max_speed)
            vel = Vector2(speed * math.cos(angle), speed * math.sin(angle))
            self.boids.append(Boid(pos, vel))
        for _ in range(n_predators):
            pos = Vector2(rng.uniform(0, self.config.width), rng.uniform(0, self.config.height))
            angle = rng.uniform(0, math.tau)
            vel = Vector2(self.config.predator_speed * math.cos(angle), self.config.predator_speed * math.sin(angle))
            self.boids.append(Boid(pos, vel, is_predator=True))

    @property
    def prey(self) -> list[Boid]:
        return [b for b in self.boids if not b.is_predator]

    @property
    def predators(self) -> list[Boid]:
        return [b for b in self.boids if b.is_predator]

    def step(self, dt: float = 1.0) -> None:
        cfg = self.config
        prey = self.prey
        predators = self.predators
        new_velocities: dict[int, Vector2] = {}

        for boid in prey:
            separation = Vector2()
            alignment = Vector2()
            cohesion = Vector2()
            n_close, n_near = 0, 0

            for other in prey:
                if other is boid:
                    continue
                delta = toroidal_delta(boid.position, other.position, cfg.width, cfg.height)
                dist = delta.length()
                if dist == 0 or dist > cfg.neighbor_radius:
                    continue
                n_near += 1
                alignment = alignment + other.velocity
                cohesion = cohesion + (boid.position - delta)
                if dist < cfg.separation_radius:
                    separation = separation + delta * (1.0 / dist)
                    n_close += 1

            steer = Vector2()
            if n_close:
                steer = steer + (separation / n_close).limited(cfg.max_force) * cfg.separation_weight
            if n_near:
                avg_heading = (alignment / n_near).normalized() * cfg.max_speed
                steer = steer + (avg_heading - boid.velocity).limited(cfg.max_force) * cfg.alignment_weight
                center = cohesion / n_near
                desired = center - boid.position
                steer = steer + desired.limited(cfg.max_force) * cfg.cohesion_weight

            evasion = Vector2()
            for pred in predators:
                delta = toroidal_delta(boid.position, pred.position, cfg.width, cfg.height)
                dist = delta.length()
                if 0 < dist < cfg.fear_radius:
                    evasion = evasion + delta.normalized() * (cfg.fear_radius - dist)
            if evasion.length() > 0:
                steer = steer + evasion.limited(cfg.max_force * 2) * cfg.evasion_weight

            new_velocities[id(boid)] = (boid.velocity + steer).limited(cfg.max_speed)

        for pred in predators:
            nearest, nearest_dist = None, None
            for boid in prey:
                dist = toroidal_delta(pred.position, boid.position, cfg.width, cfg.height).length()
                if nearest_dist is None or dist < nearest_dist:
                    nearest, nearest_dist = boid, dist
            if nearest is not None:
                delta = toroidal_delta(nearest.position, pred.position, cfg.width, cfg.height)
                chase = delta.normalized() * cfg.predator_speed
                new_velocities[id(pred)] = (pred.velocity + (chase - pred.velocity).limited(cfg.max_force)).limited(cfg.predator_speed)

        for boid in self.boids:
            boid.velocity = new_velocities.get(id(boid), boid.velocity)
            boid.position = boid.position + boid.velocity * dt
            boid.position.x %= cfg.width
            boid.position.y %= cfg.height
