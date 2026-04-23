"""Genetic algorithm to evolve Game of Life initial patterns."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import List, Callable, Tuple, Optional
from .grid import Grid
from .patterns import random_genome


@dataclass
class Individual:
    genome: np.ndarray       # Binary 2D array — the initial pattern
    fitness: float = 0.0
    lifespan: int = 0        # Generations survived before extinction/stability
    max_pop: int = 0         # Peak population reached


class FitnessGoal:
    """Preset fitness functions for different evolutionary goals."""

    @staticmethod
    def maximize_lifespan(individual: Individual) -> float:
        return float(individual.lifespan)

    @staticmethod
    def maximize_population(individual: Individual) -> float:
        return float(individual.max_pop)

    @staticmethod
    def balanced(individual: Individual) -> float:
        return individual.lifespan * 0.5 + individual.max_pop * 0.5

    @staticmethod
    def oscillator(individual: Individual, target_period: int = 2) -> float:
        """Reward stable oscillation (non-extinction, non-trivial stability)."""
        if individual.lifespan < 10:
            return 0.0
        return float(individual.max_pop) * (1.0 / (1.0 + abs(individual.lifespan - 50)))


class GeneticEvolver:
    """
    Evolves Game of Life seed patterns using a genetic algorithm.

    Selection:  Tournament selection
    Crossover:  Uniform crossover
    Mutation:   Bit-flip mutation
    """

    def __init__(
        self,
        population_size: int = 30,
        genome_size: int = 10,
        grid_width: int = 40,
        grid_height: int = 30,
        max_sim_steps: int = 200,
        mutation_rate: float = 0.05,
        crossover_rate: float = 0.7,
        elite_count: int = 3,
        fitness_fn: Optional[Callable] = None,
        rng_seed: Optional[int] = None,
    ):
        self.population_size = population_size
        self.genome_size = genome_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.max_sim_steps = max_sim_steps
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_count = elite_count
        self.fitness_fn = fitness_fn or FitnessGoal.balanced
        self.rng = np.random.default_rng(rng_seed)

        self.population: List[Individual] = []
        self.generation = 0
        self.history: List[dict] = []  # Per-generation stats
        self.best_ever: Optional[Individual] = None

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def initialize(self) -> None:
        """Create an initial random population."""
        self.population = [
            Individual(genome=random_genome(self.genome_size, rng=self.rng))
            for _ in range(self.population_size)
        ]
        self.generation = 0
        self.history = []
        self.best_ever = None

    def evolve(self, generations: int = 1, callback: Optional[Callable] = None) -> None:
        """Run the genetic algorithm for N generations."""
        for _ in range(generations):
            self._evaluate_all()
            self.history.append(self._stats())
            if callback:
                callback(self)
            self._reproduce()
            self.generation += 1

    def best(self) -> Optional[Individual]:
        """Return the best individual ever evaluated across all generations."""
        return self.best_ever

    def stats(self) -> dict:
        """Return stats for the most recently evaluated generation."""
        if self.history:
            return self.history[-1]
        return self._stats()

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #

    def _simulate(self, genome: np.ndarray) -> Tuple[int, int]:
        """Run a GoL simulation and return (lifespan, max_population)."""
        g = Grid(self.grid_width, self.grid_height)
        ox = (self.grid_width - self.genome_size) // 2
        oy = (self.grid_height - self.genome_size) // 2
        g.seed(genome, offset_x=ox, offset_y=oy)

        max_pop = g.population
        lifespan = 0

        for _ in range(self.max_sim_steps):
            g.step()
            if g.population > max_pop:
                max_pop = g.population
            if g.is_extinct() or g.is_stable():
                break
            lifespan += 1

        return lifespan, max_pop

    def _evaluate_all(self) -> None:
        for ind in self.population:
            lifespan, max_pop = self._simulate(ind.genome)
            ind.lifespan = lifespan
            ind.max_pop = max_pop
            ind.fitness = self.fitness_fn(ind)
        gen_best = max(self.population, key=lambda i: i.fitness)
        if self.best_ever is None or gen_best.fitness > self.best_ever.fitness:
            self.best_ever = Individual(
                genome=gen_best.genome.copy(),
                fitness=gen_best.fitness,
                lifespan=gen_best.lifespan,
                max_pop=gen_best.max_pop,
            )

    def _tournament_select(self, k: int = 3) -> Individual:
        contestants = self.rng.choice(self.population, size=k, replace=False)  # type: ignore[arg-type]
        return max(contestants, key=lambda i: i.fitness)

    def _crossover(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        if self.rng.random() > self.crossover_rate:
            return a.copy(), b.copy()
        mask = self.rng.integers(0, 2, size=a.shape, dtype=bool)
        child1 = np.where(mask, a, b).astype(np.uint8)
        child2 = np.where(mask, b, a).astype(np.uint8)
        return child1, child2

    def _mutate(self, genome: np.ndarray) -> np.ndarray:
        flip_mask = self.rng.random(size=genome.shape) < self.mutation_rate
        mutated = genome.copy()
        mutated[flip_mask] ^= 1
        return mutated

    def _reproduce(self) -> None:
        sorted_pop = sorted(self.population, key=lambda i: i.fitness, reverse=True)
        elites = [Individual(genome=ind.genome.copy()) for ind in sorted_pop[: self.elite_count]]

        children: List[Individual] = list(elites)
        while len(children) < self.population_size:
            parent_a = self._tournament_select()
            parent_b = self._tournament_select()
            g1, g2 = self._crossover(parent_a.genome, parent_b.genome)
            g1 = self._mutate(g1)
            g2 = self._mutate(g2)
            children.append(Individual(genome=g1))
            if len(children) < self.population_size:
                children.append(Individual(genome=g2))

        self.population = children

    def _stats(self) -> dict:
        fitnesses = [i.fitness for i in self.population]
        lifespans = [i.lifespan for i in self.population]
        pops = [i.max_pop for i in self.population]
        return {
            "generation": self.generation,
            "best_fitness": max(fitnesses),
            "avg_fitness": sum(fitnesses) / len(fitnesses),
            "best_lifespan": max(lifespans),
            "best_max_pop": max(pops),
        }
