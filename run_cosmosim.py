#!/usr/bin/env python3
"""Launch Cosmosim from the project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cosmosim.main import main

if __name__ == '__main__':
    main()
