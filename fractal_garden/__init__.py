"""Fractal Garden: grow plants and fractal curves from L-systems as SVG art."""

from .garden import grow
from .species import SPECIES, Species, get

__version__ = "0.1.0"

__all__ = ["grow", "SPECIES", "Species", "get", "__version__"]
