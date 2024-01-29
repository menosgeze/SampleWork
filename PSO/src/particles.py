"""
Contains data classes with for the particle swarm optimization.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Particle:
    """Defines the selection and objective."""
    selection: tuple = field(default_factory=tuple)
    objective: float | int = 0


@dataclass
class Swarm:
    """Defines the swarm containing agents: particles, cognitive particles,
    and social particle.
    """
    all_items: list
    agents: list = field(default_factory=list)
    cognitive_agents: list = field(default_factory=list)
    social_agent: Particle = Particle()
    history: dict = field(default_factory=dict)
