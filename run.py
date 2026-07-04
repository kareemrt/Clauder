#!/usr/bin/env python3
"""TerminalQuest launcher — run from the repo root."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from terminalquest.main import main

if __name__ == "__main__":
    main()
