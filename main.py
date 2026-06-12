#!/usr/bin/env python3
"""Convenience entry point: ``python main.py --preset cells``."""

import sys

from particle_life.cli import main

if __name__ == "__main__":
    sys.exit(main())
