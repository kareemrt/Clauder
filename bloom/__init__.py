"""Bloom — a continuous cellular automaton in the Lenia/SmoothLife family."""

from .world import World
from .kernel import build_kernel, growth

__all__ = ["World", "build_kernel", "growth"]
