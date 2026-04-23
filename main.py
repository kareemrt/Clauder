#!/usr/bin/env python3
"""
EvoLife — Conway's Game of Life + Genetic Evolution Simulator

Usage:
    python main.py simulate [--pattern NAME] [--steps N] [--theme THEME]
    python main.py evolve [--generations N] [--population N] [--goal GOAL]
    python main.py patterns
    python main.py demo
"""

import sys
import time
import argparse
import numpy as np

from evolife.grid import Grid
from evolife.evolution import GeneticEvolver, FitnessGoal
from evolife.renderer import Renderer
from evolife.patterns import get_pattern, list_patterns
from evolife.stats import StatsTracker, SimulationRecord


def cmd_simulate(args):
    """Run and visualize a single Game of Life simulation."""
    renderer = Renderer(theme=args.theme, glyph=args.glyph)
    renderer.clear()
    print(renderer.render_logo())

    try:
        pattern = get_pattern(args.pattern)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    grid = Grid(args.width, args.height)
    ox = (args.width - pattern.shape[1]) // 2
    oy = (args.height - pattern.shape[0]) // 2
    grid.seed(pattern, offset_x=ox, offset_y=oy)

    renderer.hide_cursor()
    try:
        born, died = 0, 0
        for step in range(args.steps):
            renderer.move_home()
            print(renderer.render_logo())
            print(renderer.render_grid(grid.cells, title=f"Pattern: {args.pattern}"))
            print()
            print(renderer.render_stats_bar(grid.generation, grid.population, born, died))
            print()
            if grid.is_extinct():
                print("  [EXTINCT] All cells died.")
                break
            if grid.is_stable():
                print("  [STABLE] Pattern has stabilized.")
                break
            born, died = grid.step()
            time.sleep(args.delay)
    except KeyboardInterrupt:
        pass
    finally:
        renderer.show_cursor()


def cmd_evolve(args):
    """Run the genetic algorithm to evolve optimal seed patterns."""
    renderer = Renderer(theme=args.theme)
    renderer.clear()
    print(renderer.render_logo())

    goal_map = {
        "lifespan": FitnessGoal.maximize_lifespan,
        "population": FitnessGoal.maximize_population,
        "balanced": FitnessGoal.balanced,
        "oscillator": FitnessGoal.oscillator,
    }
    fitness_fn = goal_map.get(args.goal, FitnessGoal.balanced)

    evolver = GeneticEvolver(
        population_size=args.population,
        genome_size=args.genome_size,
        grid_width=args.width,
        grid_height=args.height,
        max_sim_steps=args.sim_steps,
        mutation_rate=args.mutation_rate,
        fitness_fn=fitness_fn,
        rng_seed=args.seed,
    )

    tracker = StatsTracker()
    evolver.initialize()

    print(f"  Evolving {args.population} genomes over {args.generations} generations...")
    print(f"  Goal: {args.goal} | Genome size: {args.genome_size}x{args.genome_size}\n")

    renderer.hide_cursor()
    try:
        def on_generation(evo):
            stats = evo.stats()
            tracker.record_evolution(stats)
            renderer.move_home()
            print(renderer.render_logo())
            best = evo.best()
            print(renderer.render_genome(best.genome, label=f"  Best Genome (Gen {evo.generation})"))
            print()
            print(f"  {renderer.render_stats_bar(0, best.max_pop, 0, 0, evo_gen=evo.generation, best_fitness=best.fitness, best_lifespan=best.lifespan)}")
            print()
            print(renderer.render_evolution_chart(tracker.evolution_log, width=40))
            print()

        evolver.evolve(generations=args.generations, callback=on_generation)

    except KeyboardInterrupt:
        pass
    finally:
        renderer.show_cursor()

    print("\n" + "=" * 60)
    print("  EVOLUTION COMPLETE")
    print("=" * 60)
    best = evolver.best()
    print(f"\n  Best individual — Fitness: {best.fitness:.2f}")
    print(f"  Lifespan: {best.lifespan} generations | Max population: {best.max_pop}")
    print(f"\n  Genome ({args.genome_size}x{args.genome_size}):")
    print(renderer.render_genome(best.genome))
    print()

    if args.replay:
        print("  Replaying best genome in Game of Life...\n")
        time.sleep(1)
        _replay_best(best.genome, renderer, args)


def _replay_best(genome: np.ndarray, renderer: Renderer, args) -> None:
    """Replay the best evolved genome in the GoL visualizer."""
    grid = Grid(args.width, args.height)
    ox = (args.width - genome.shape[1]) // 2
    oy = (args.height - genome.shape[0]) // 2
    grid.seed(genome, offset_x=ox, offset_y=oy)

    renderer.hide_cursor()
    try:
        born, died = 0, 0
        for _ in range(args.sim_steps):
            renderer.move_home()
            print(renderer.render_logo())
            print(renderer.render_grid(grid.cells, title="Best Evolved Genome Replay"))
            print()
            print(renderer.render_stats_bar(grid.generation, grid.population, born, died))
            if grid.is_extinct() or grid.is_stable():
                break
            born, died = grid.step()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        renderer.show_cursor()


def cmd_patterns(args):
    """List available built-in patterns."""
    renderer = Renderer(theme=args.theme)
    print(renderer.render_logo())
    print("  Available Patterns:")
    print("  " + "─" * 40)
    for name in list_patterns():
        try:
            p = get_pattern(name)
            if p is not None:
                pop = int(p.sum())
                print(f"  {name:<20} {p.shape[0]}x{p.shape[1]:>2}  ({pop} live cells)")
            else:
                print(f"  {name:<20} (random, generated at runtime)")
        except Exception:
            pass
    print()


def cmd_demo(args):
    """Run a quick demo showcasing patterns and evolution."""
    import os

    renderer = Renderer(theme="matrix")
    renderer.clear()
    print(renderer.render_logo())
    print("  Running DEMO — showcasing built-in patterns...\n")
    time.sleep(1)

    for pname in ["glider", "pulsar", "acorn"]:
        pattern = get_pattern(pname)
        grid = Grid(40, 20)
        ox = (40 - pattern.shape[1]) // 2
        oy = (20 - pattern.shape[0]) // 2
        grid.seed(pattern, offset_x=ox, offset_y=oy)

        renderer.hide_cursor()
        born, died = 0, 0
        for step in range(60):
            renderer.move_home()
            print(renderer.render_logo())
            print(f"  Pattern: {pname.upper()}")
            print(renderer.render_grid(grid.cells))
            print()
            print("  " + renderer.render_stats_bar(grid.generation, grid.population, born, died))
            if grid.is_extinct() or grid.is_stable():
                break
            born, died = grid.step()
            time.sleep(0.08)

        renderer.show_cursor()
        print(f"\n  Pattern '{pname}' complete. Next in 2s...\n")
        time.sleep(2)

    print("  Demo complete! Run 'python main.py evolve' to start evolution.\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evolife",
        description="EvoLife — Conway's Game of Life + Genetic Evolution Simulator",
    )
    sub = parser.add_subparsers(dest="command")

    # ── simulate ──────────────────────────────────────────────────
    sim = sub.add_parser("simulate", help="Run and visualize a single GoL simulation")
    sim.add_argument("--pattern", default="glider", choices=list_patterns(), help="Seed pattern")
    sim.add_argument("--steps", type=int, default=300, help="Max simulation steps")
    sim.add_argument("--delay", type=float, default=0.08, help="Delay between steps (seconds)")
    sim.add_argument("--width", type=int, default=50, help="Grid width")
    sim.add_argument("--height", type=int, default=25, help="Grid height")
    sim.add_argument("--theme", default="matrix", choices=["matrix", "ocean", "fire", "mono", "plasma"])
    sim.add_argument("--glyph", default="block", choices=["block", "dot", "square", "ascii"])

    # ── evolve ────────────────────────────────────────────────────
    evo = sub.add_parser("evolve", help="Run genetic algorithm to evolve optimal patterns")
    evo.add_argument("--generations", type=int, default=20, help="Number of evolution generations")
    evo.add_argument("--population", type=int, default=30, help="Population size")
    evo.add_argument("--genome-size", type=int, default=10, dest="genome_size", help="Genome grid size (NxN)")
    evo.add_argument("--goal", default="balanced", choices=["lifespan", "population", "balanced", "oscillator"])
    evo.add_argument("--sim-steps", type=int, default=200, dest="sim_steps", help="Max GoL steps per evaluation")
    evo.add_argument("--mutation-rate", type=float, default=0.05, dest="mutation_rate")
    evo.add_argument("--seed", type=int, default=None, help="Random seed")
    evo.add_argument("--width", type=int, default=50)
    evo.add_argument("--height", type=int, default=25)
    evo.add_argument("--theme", default="matrix", choices=["matrix", "ocean", "fire", "mono", "plasma"])
    evo.add_argument("--replay", action="store_true", help="Replay best genome after evolution")

    # ── patterns ──────────────────────────────────────────────────
    pat = sub.add_parser("patterns", help="List available built-in patterns")
    pat.add_argument("--theme", default="matrix", choices=["matrix", "ocean", "fire", "mono", "plasma"])

    # ── demo ──────────────────────────────────────────────────────
    demo = sub.add_parser("demo", help="Quick demo of patterns and evolution")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "simulate":
        cmd_simulate(args)
    elif args.command == "evolve":
        cmd_evolve(args)
    elif args.command == "patterns":
        cmd_patterns(args)
    elif args.command == "demo":
        cmd_demo(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
