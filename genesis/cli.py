"""Command-line entrypoint for Genesis."""

from __future__ import annotations

import argparse
import csv
import os

from genesis.render_ansi import watch
from genesis.simulation import DEFAULT_FOOD_DENSITY, Simulation
from genesis.svgchart import line_chart, world_snapshot


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genesis", description="A zero-dependency evolution simulator.")
    sub = parser.add_subparsers(dest="command", required=True)

    common = [
        ("width", int, 60, "grid width"),
        ("height", int, 30, "grid height"),
        ("population", int, 80, "starting population"),
        ("food-density", float, DEFAULT_FOOD_DENSITY, "fraction of cells kept stocked with food"),
        ("seed", int, None, "random seed for reproducibility"),
    ]

    run_p = sub.add_parser("run", help="run headless and write stats + SVG visuals")
    for name, kind, default, help_text in common:
        run_p.add_argument(f"--{name}", type=kind, default=default, help=help_text)
    run_p.add_argument("--ticks", type=int, default=1500, help="number of ticks to simulate")
    run_p.add_argument("--record-every", type=int, default=5, help="sample stats every N ticks")
    run_p.add_argument("--out-dir", default="assets", help="output directory for CSV + SVGs")

    watch_p = sub.add_parser("watch", help="watch the simulation live in the terminal")
    for name, kind, default, help_text in common:
        watch_p.add_argument(f"--{name}", type=kind, default=default, help=help_text)
    watch_p.add_argument("--ticks", type=int, default=2000, help="number of ticks to simulate")
    watch_p.add_argument("--fps", type=float, default=12.0, help="frames per second")

    return parser


def _make_simulation(args: argparse.Namespace) -> Simulation:
    return Simulation(
        width=args.width,
        height=args.height,
        population=args.population,
        food_density=args.food_density,
        seed=args.seed,
    )


def cmd_run(args: argparse.Namespace) -> None:
    sim = _make_simulation(args)
    history = sim.run(args.ticks, record_every=args.record_every)

    os.makedirs(args.out_dir, exist_ok=True)

    csv_path = os.path.join(args.out_dir, "stats.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tick", "population", "food_count", "avg_speed", "avg_vision",
                          "avg_metabolism", "avg_repro_threshold", "avg_energy"])
        for s in history:
            writer.writerow([s.tick, s.population, s.food_count, f"{s.avg_speed:.3f}",
                              f"{s.avg_vision:.3f}", f"{s.avg_metabolism:.3f}",
                              f"{s.avg_repro_threshold:.3f}", f"{s.avg_energy:.3f}"])

    population_svg = line_chart(
        {"population": [s.population for s in history], "food": [s.food_count for s in history]},
        title="Population & Food Over Time",
    )
    with open(os.path.join(args.out_dir, "population.svg"), "w") as f:
        f.write(population_svg)

    traits_svg = line_chart(
        {
            "avg_speed": [s.avg_speed for s in history],
            "avg_vision": [s.avg_vision for s in history],
            "avg_metabolism": [s.avg_metabolism for s in history],
        },
        title="Genome Trait Evolution",
    )
    with open(os.path.join(args.out_dir, "traits.svg"), "w") as f:
        f.write(traits_svg)

    with open(os.path.join(args.out_dir, "world_snapshot.svg"), "w") as f:
        f.write(world_snapshot(sim.world))

    final = history[-1] if history else None
    print(f"Ran {sim.tick_count} ticks. Final population: {final.population if final else 0}")
    print(f"Wrote stats and SVGs to {args.out_dir}/")


def cmd_watch(args: argparse.Namespace) -> None:
    sim = _make_simulation(args)
    watch(sim, args.ticks, fps=args.fps)


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        cmd_run(args)
    elif args.command == "watch":
        cmd_watch(args)


if __name__ == "__main__":
    main()
