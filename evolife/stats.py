"""Statistics tracking and reporting for EvoLife."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import time


@dataclass
class SimulationRecord:
    """Record of a single GoL simulation run."""
    genome_hash: str
    lifespan: int
    max_population: int
    final_population: int
    fitness: float
    timestamp: float = field(default_factory=time.time)


class StatsTracker:
    def __init__(self):
        self.records: List[SimulationRecord] = []
        self.evolution_log: List[dict] = []
        self.start_time = time.time()

    def record_sim(self, record: SimulationRecord) -> None:
        self.records.append(record)

    def record_evolution(self, stats: dict) -> None:
        stats["elapsed"] = time.time() - self.start_time
        self.evolution_log.append(stats)

    def summary(self) -> dict:
        if not self.records:
            return {}
        lifespans = [r.lifespan for r in self.records]
        pops = [r.max_population for r in self.records]
        fitnesses = [r.fitness for r in self.records]
        return {
            "total_simulations": len(self.records),
            "avg_lifespan": sum(lifespans) / len(lifespans),
            "best_lifespan": max(lifespans),
            "avg_max_pop": sum(pops) / len(pops),
            "best_max_pop": max(pops),
            "best_fitness": max(fitnesses),
            "elapsed_seconds": time.time() - self.start_time,
        }

    def format_summary(self) -> str:
        s = self.summary()
        if not s:
            return "No simulations recorded."
        return (
            f"Total Simulations : {s['total_simulations']}\n"
            f"Best Fitness      : {s['best_fitness']:.2f}\n"
            f"Best Lifespan     : {s['best_lifespan']} generations\n"
            f"Best Max Pop      : {s['best_max_pop']} cells\n"
            f"Avg Lifespan      : {s['avg_lifespan']:.1f}\n"
            f"Elapsed Time      : {s['elapsed_seconds']:.1f}s\n"
        )
