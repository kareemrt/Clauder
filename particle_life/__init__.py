"""Particle Life: a toroidal artificial-life simulation driven by pairwise attraction rules."""

from .simulation import ParticleSystem, SimulationConfig
from .presets import PRESETS, get_preset

__all__ = ["ParticleSystem", "SimulationConfig", "PRESETS", "get_preset"]
