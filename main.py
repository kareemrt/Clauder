#!/usr/bin/env python3
"""FoodSave — entry point."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="foodsave",
        description="FoodSave: AI-powered food waste reduction assistant",
    )
    parser.add_argument(
        "--db", default="foodsave.db",
        help="Path to the SQLite database (default: foodsave.db)",
    )
    parser.add_argument(
        "--version", action="store_true", help="Print version and exit"
    )
    args = parser.parse_args()

    if args.version:
        from foodsave import __version__
        print(f"FoodSave v{__version__}")
        return

    from foodsave.cli import run_cli
    run_cli(db_path=args.db)


if __name__ == "__main__":
    main()
