"""
Dataclasses for the particle swarm optimization.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Particle:
    """Dataclass with attrs: `selection` tuple[int] and `objective` float."""

    selection: tuple = field(default_factory=tuple)
    objective: float | int = 0


@dataclass
class Swarm:
    """Dataclass with attrs:
    `agents` (list[Particle]),
    `cognitive_agents` (list[Particle]),
    `social_agent` (Particle)
    `history` (dict)
    """

    all_items: list
    agents: list = field(default_factory=list)
    cognitive_agents: list = field(default_factory=list)
    social_agent: Particle = Particle()
    history: dict = field(default_factory=dict)
