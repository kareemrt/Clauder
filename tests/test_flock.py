import statistics
import unittest

from murmuration.flock import Flock, FlockConfig
from murmuration.vector import Vector2, toroidal_delta


class TestFlock(unittest.TestCase):
    def test_seeded_initialization_is_deterministic(self):
        a = Flock(n_boids=20, seed=42)
        b = Flock(n_boids=20, seed=42)
        for ba, bb in zip(a.boids, b.boids):
            self.assertEqual(ba.position, bb.position)
            self.assertEqual(ba.velocity, bb.velocity)

    def test_different_seeds_diverge(self):
        a = Flock(n_boids=20, seed=1)
        b = Flock(n_boids=20, seed=2)
        positions_a = [boid.position for boid in a.boids]
        positions_b = [boid.position for boid in b.boids]
        self.assertNotEqual(positions_a, positions_b)

    def test_positions_stay_within_toroidal_bounds(self):
        config = FlockConfig(width=50, height=30)
        flock = Flock(n_boids=30, config=config, seed=7)
        for _ in range(100):
            flock.step()
        for boid in flock.boids:
            self.assertGreaterEqual(boid.position.x, 0)
            self.assertLess(boid.position.x, config.width)
            self.assertGreaterEqual(boid.position.y, 0)
            self.assertLess(boid.position.y, config.height)

    def test_speed_never_exceeds_max(self):
        config = FlockConfig(width=80, height=40, max_speed=5.0)
        flock = Flock(n_boids=25, config=config, seed=3)
        for _ in range(60):
            flock.step()
        for boid in flock.boids:
            self.assertLessEqual(boid.speed(), config.max_speed + 1e-6)

    def test_separation_spreads_out_an_overcrowded_cluster(self):
        # Pack every boid into a tiny region; separation should push the
        # average pairwise distance up over time.
        config = FlockConfig(width=200, height=200, separation_radius=8.0, neighbor_radius=20.0)
        flock = Flock(n_boids=15, config=config, seed=5)
        for boid in flock.boids:
            boid.position = Vector2(100 + (hash(id(boid)) % 5) * 0.1, 100 + (hash(id(boid)) % 3) * 0.1)

        def avg_pairwise_distance():
            boids = flock.boids
            total, count = 0.0, 0
            for i, b1 in enumerate(boids):
                for b2 in boids[i + 1:]:
                    total += toroidal_delta(b1.position, b2.position, config.width, config.height).length()
                    count += 1
            return total / count

        before = avg_pairwise_distance()
        for _ in range(30):
            flock.step()
        after = avg_pairwise_distance()
        self.assertGreater(after, before)

    def test_predator_closes_distance_on_nearest_prey(self):
        config = FlockConfig(width=200, height=200, fear_radius=5.0)
        flock = Flock(n_boids=10, n_predators=1, config=config, seed=11)
        predator = flock.predators[0]
        # Place the predator far from everyone except one deliberately close,
        # stationary prey so the chase isn't confounded by the prey's own motion.
        predator.position = Vector2(0, 0)
        predator.velocity = Vector2(0, 0)
        target = flock.prey[0]
        target.position = Vector2(50, 0)
        target.velocity = Vector2(0, 0)
        for other in flock.prey[1:]:
            other.position = Vector2(150, 150)
            other.velocity = Vector2(0, 0)

        initial_distance = toroidal_delta(predator.position, target.position, config.width, config.height).length()
        for _ in range(40):
            flock.step()
        final_distance = toroidal_delta(predator.position, target.position, config.width, config.height).length()
        self.assertLess(final_distance, initial_distance)

    def test_prey_evade_nearby_predator(self):
        config = FlockConfig(width=200, height=200, fear_radius=30.0, evasion_weight=5.0)
        flock = Flock(n_boids=5, n_predators=1, config=config, seed=9)
        predator = flock.predators[0]
        predator.position = Vector2(100, 100)
        predator.velocity = Vector2(0, 0)
        for boid in flock.prey:
            boid.position = Vector2(105, 100)
            boid.velocity = Vector2(0, 0)

        distances_before = [
            toroidal_delta(b.position, predator.position, config.width, config.height).length()
            for b in flock.prey
        ]
        for _ in range(10):
            flock.step()
        distances_after = [
            toroidal_delta(b.position, predator.position, config.width, config.height).length()
            for b in flock.prey
        ]
        self.assertGreater(statistics.mean(distances_after), statistics.mean(distances_before))


if __name__ == "__main__":
    unittest.main()
