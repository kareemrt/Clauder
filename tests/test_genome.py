import random
import unittest

from genesis.genome import (
    METABOLISM_RANGE,
    REPRO_THRESHOLD_RANGE,
    SPEED_RANGE,
    VISION_RANGE,
    Genome,
)


class TestGenome(unittest.TestCase):
    def test_random_stays_within_bounds(self):
        rng = random.Random(1)
        for _ in range(200):
            g = Genome.random(rng)
            self.assertTrue(SPEED_RANGE[0] <= g.speed <= SPEED_RANGE[1])
            self.assertTrue(VISION_RANGE[0] <= g.vision <= VISION_RANGE[1])
            self.assertTrue(METABOLISM_RANGE[0] <= g.metabolism <= METABOLISM_RANGE[1])
            self.assertTrue(REPRO_THRESHOLD_RANGE[0] <= g.repro_threshold <= REPRO_THRESHOLD_RANGE[1])

    def test_mutate_stays_within_bounds(self):
        rng = random.Random(2)
        g = Genome.random(rng)
        for _ in range(500):
            g = g.mutate(rng)
            self.assertTrue(SPEED_RANGE[0] <= g.speed <= SPEED_RANGE[1])
            self.assertTrue(VISION_RANGE[0] <= g.vision <= VISION_RANGE[1])
            self.assertTrue(METABOLISM_RANGE[0] <= g.metabolism <= METABOLISM_RANGE[1])
            self.assertTrue(REPRO_THRESHOLD_RANGE[0] <= g.repro_threshold <= REPRO_THRESHOLD_RANGE[1])

    def test_upkeep_cost_increases_with_speed_and_vision(self):
        cheap = Genome(speed=1, vision=1, metabolism=1.0, repro_threshold=10.0)
        expensive = Genome(speed=3, vision=8, metabolism=1.0, repro_threshold=10.0)
        self.assertLess(cheap.upkeep_cost(), expensive.upkeep_cost())


if __name__ == "__main__":
    unittest.main()
