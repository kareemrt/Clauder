"""Nebula — N-body gravitational simulator."""
from .physics import Body, Simulation
from .scenarios import SCENARIOS

__version__ = "1.0.0"
__all__ = ["Body", "Simulation", "SCENARIOS"]
