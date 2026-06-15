"""Primordia: a vectorized particle-life simulator.

A minimal set of physical rules -- pairwise attraction and repulsion
between "species" of particles -- gives rise to cells, swarms, chains,
and predator/prey-like chases. No biology is hard-coded; it all emerges
from the interaction matrix.
"""

from primordia.simulation import ParticleLife, SimulationConfig

__all__ = ["ParticleLife", "SimulationConfig"]
__version__ = "0.1.0"
