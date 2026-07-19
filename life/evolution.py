"""
Genetic algorithm that breeds Conway's Game of Life starting configurations
optimised for "interestingness": long lifespan, rich state diversity, and
strong population throughout the run.
"""
from __future__ import annotations

import copy
import numpy as np
from life.board import Board


class Individual:
    def __init__(self, width: int, height: int, density: float = 0.3, seed: int | None = None):
        self.width = width
        self.height = height
        rng = np.random.default_rng(seed)
        self.genome: np.ndarray = rng.choice(
            [0, 1], size=(height, width), p=[1 - density, density]
        ).astype(np.uint8)
        self.fitness: float = 0.0
        self.metadata: dict = {}

    # ------------------------------------------------------------------ #
    def evaluate(self, max_gens: int = 200) -> float:
        board = Board(self.width, self.height)
        board.grid = self.genome.copy()

        initial_pop = board.population()
        if initial_pop == 0:
            self.fitness = 0.0
            return 0.0

        alive_gens = 0
        total_pop = initial_pop
        max_pop = initial_pop
        seen: set[bytes] = {board.fingerprint()}
        unique_states = 1
        loops_detected = 0

        for _ in range(max_gens):
            board.step()
            fp = board.fingerprint()
            pop = board.population()

            if pop == 0:
                break

            alive_gens += 1
            total_pop += pop
            max_pop = max(max_pop, pop)

            if fp in seen:
                loops_detected += 1
                if loops_detected > 3:
                    break
            else:
                seen.add(fp)
                unique_states += 1

        longevity   = alive_gens / max_gens
        diversity   = min(unique_states / max_gens, 1.0)
        avg_density = (total_pop / max(alive_gens, 1)) / (self.width * self.height)
        density_score = 1.0 - abs(avg_density - 0.2)  # reward ~20% density

        self.fitness = 0.35 * longevity + 0.40 * diversity + 0.25 * density_score
        self.metadata = {
            "alive_gens": alive_gens,
            "unique_states": unique_states,
            "max_pop": max_pop,
        }
        return self.fitness

    # ------------------------------------------------------------------ #
    def crossover(self, other: "Individual") -> "Individual":
        child = Individual.__new__(Individual)
        child.width, child.height = self.width, self.height
        child.fitness = 0.0
        child.metadata = {}
        mask = np.random.rand(self.height, self.width) > 0.5
        child.genome = np.where(mask, self.genome, other.genome).astype(np.uint8)
        return child

    def mutate(self, rate: float = 0.02) -> "Individual":
        flip = np.random.rand(self.height, self.width) < rate
        self.genome = np.where(flip, 1 - self.genome, self.genome).astype(np.uint8)
        return self

    def clone(self) -> "Individual":
        c = copy.deepcopy(self)
        c.fitness = 0.0
        return c


class Evolution:
    """
    (μ + λ) evolutionary strategy:
      - Evaluate all individuals
      - Keep top μ (elite_frac of pop_size)
      - Fill next generation from crossover + mutation of survivors
    """

    def __init__(
        self,
        pop_size: int = 30,
        board_width: int = 40,
        board_height: int = 20,
        elite_frac: float = 0.4,
        mutation_rate: float = 0.015,
        eval_gens: int = 200,
    ):
        self.pop_size = pop_size
        self.w = board_width
        self.h = board_height
        self.elite_n = max(2, int(pop_size * elite_frac))
        self.mutation_rate = mutation_rate
        self.eval_gens = eval_gens

        self.population: list[Individual] = [
            Individual(board_width, board_height, density=0.25 + 0.15 * np.random.rand())
            for _ in range(pop_size)
        ]
        self.best: Individual | None = None
        self.generation = 0
        self.log: list[dict] = []

    def step(self) -> Individual:
        """Run one generation and return the current best individual."""
        for ind in self.population:
            ind.evaluate(self.eval_gens)

        self.population.sort(key=lambda x: x.fitness, reverse=True)
        current_best = self.population[0]

        if self.best is None or current_best.fitness > self.best.fitness:
            self.best = copy.deepcopy(current_best)

        self.log.append({
            "gen": self.generation,
            "best_fitness": self.best.fitness,
            "mean_fitness": float(np.mean([i.fitness for i in self.population])),
        })

        # Breed next generation
        elite = self.population[: self.elite_n]
        next_gen: list[Individual] = [copy.deepcopy(e) for e in elite]

        rng = np.random.default_rng()
        while len(next_gen) < self.pop_size:
            p1, p2 = rng.choice(self.elite_n, size=2, replace=False)
            child = elite[p1].crossover(elite[p2])
            child.mutate(self.mutation_rate)
            next_gen.append(child)

        self.population = next_gen
        self.generation += 1
        return self.best

    def run(self, generations: int = 20, callback=None) -> Individual:
        for _ in range(generations):
            best = self.step()
            if callback:
                callback(self.generation, best)
        return self.best  # type: ignore
