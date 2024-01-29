__from__ future import annotations
from dataclasses import dataclass, field
import numpy as np
import pandas as pd

@dataclass
class Particle:
    selection: list = field(default_factory=list)
    objective: float | int = 0

@dataclass
class Swarm:
    all_items: list
    agents: list = field(default_factory=list)
    cognitive_agents: list = field(default_factory=list)
    social_agent: Particle = Particle()
    history: dict = field(default_factory=dict)

class StochasticParticleSwarmOptimizer:
    """This class defines a stochastic particle swarm optimizer
    for binary selection.
    """
    def __init__(
        self,
        item_sizes: pd.DataFrame,
        capacity: float,
        cognitive_probability: float = 0.1,
        social_probability: float = 0.3,
        random_swaps: int = 2
    ):
        self.swarm = None
        self.item_sizes = item_sizes
        self.capacity = capacity
        self.cognitive_probability = cognitive_probability
        self.social_probability = social_probability
        self.random_swaps = random_swaps

    def is_initialized(self):
        return self.swarm is not None

    def _increase_size_to_capacity(
        self, 
        agent: Particle, 
        rng: np.random._generator.Generator
    ):
        pass

    def _decrease_size_to_capacity(
        self,
        agent: Particle,
        rng: np.random._generator.Generator
    ):
        pass

    def initialize_agents(
        self,
        n_agents: int,
        custom: list = None,
        rng: np.random._generator.Generator
    ) -> list:
        pass



