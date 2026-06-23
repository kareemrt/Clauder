"""Strange Attractors Explorer — numerical exploration of chaotic dynamical systems."""

from .systems import SYSTEMS, AttractorSystem
from .integrator import integrate

__all__ = ["SYSTEMS", "AttractorSystem", "integrate"]

__version__ = "0.1.0"
