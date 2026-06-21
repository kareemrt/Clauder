import unittest

from genesis.simulation import Simulation


class TestSimulation(unittest.TestCase):
    def test_seeded_runs_are_deterministic(self):
        history_a = Simulation(width=20, height=20, population=30, seed=42).run(100)
        history_b = Simulation(width=20, height=20, population=30, seed=42).run(100)
        self.assertEqual(
            [(s.tick, s.population, s.food_count) for s in history_a],
            [(s.tick, s.population, s.food_count) for s in history_b],
        )

    def test_population_never_negative(self):
        history = Simulation(width=15, height=15, population=20, seed=7).run(300)
        self.assertTrue(all(s.population >= 0 for s in history))

    def test_no_organisms_share_a_cell(self):
        sim = Simulation(width=10, height=10, population=15, seed=3)
        sim.run(50)
        positions = [(o.x, o.y) for o in sim.world.organisms()]
        self.assertEqual(len(positions), len(set(positions)))

    def test_starvation_without_food_drives_extinction(self):
        sim = Simulation(width=10, height=10, population=10, food_density=0.0, seed=5)
        history = sim.run(500)
        self.assertEqual(history[-1].population, 0)


if __name__ == "__main__":
    unittest.main()
