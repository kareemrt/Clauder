#!/usr/bin/env python3
"""
Example: Programmatic usage of EvoLife's evolution engine.

Run:
    python examples/demo.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evolife.evolution import GeneticEvolver, FitnessGoal
from evolife.grid import Grid
from evolife.patterns import get_pattern


def example_simple_evolution():
    """Evolve patterns to maximize lifespan over 10 generations."""
    print("=" * 50)
    print("Example: Evolving for maximum lifespan")
    print("=" * 50)

    evolver = GeneticEvolver(
        population_size=20,
        genome_size=8,
        grid_width=40,
        grid_height=30,
        max_sim_steps=150,
        fitness_fn=FitnessGoal.maximize_lifespan,
        rng_seed=42,
    )

    evolver.initialize()

    for gen in range(10):
        evolver.evolve(generations=1)
        stats = evolver.stats()
        print(f"  Gen {gen+1:>2} | Best fitness: {stats['best_fitness']:>7.1f} | "
              f"Best lifespan: {stats['best_lifespan']:>4} | "
              f"Best max pop: {stats['best_max_pop']:>4}")

    best = evolver.best()
    print(f"\nBest individual:")
    print(f"  Lifespan: {best.lifespan} | Max pop: {best.max_pop} | Fitness: {best.fitness:.2f}")
    print(f"  Genome ({best.genome.shape[0]}x{best.genome.shape[1]}):")
    for row in best.genome:
        print("  " + "".join("█" if c else "·" for c in row))


def example_classic_patterns():
    """Demonstrate running classic patterns in the GoL grid."""
    print("\n" + "=" * 50)
    print("Example: Classic pattern statistics")
    print("=" * 50)

    for pname in ["glider", "acorn", "pulsar", "diehard"]:
        pattern = get_pattern(pname)
        grid = Grid(60, 40)
        ox = (60 - pattern.shape[1]) // 2
        oy = (40 - pattern.shape[0]) // 2
        grid.seed(pattern, offset_x=ox, offset_y=oy)

        max_pop = grid.population
        for _ in range(500):
            grid.step()
            if grid.population > max_pop:
                max_pop = grid.population
            if grid.is_extinct() or grid.is_stable():
                break

        status = "extinct" if grid.is_extinct() else "stable" if grid.is_stable() else "running"
        print(f"  {pname:<12} → lifespan: {grid.generation:>4} gen | "
              f"max pop: {max_pop:>4} | status: {status}")


if __name__ == "__main__":
    example_simple_evolution()
    example_classic_patterns()
    print("\nDone! Run 'python main.py --help' for the interactive CLI.")
