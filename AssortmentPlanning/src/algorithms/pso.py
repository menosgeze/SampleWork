from __future__ import annotations
from copy import copy
import numpy as np
import pandas as pd
from particles import Particle, Swarm

class StochasticParticleSwarmOptimizer:
    """This class defines a stochastic particle swarm optimizer
    for binary selection.
    """
    def __init__(
        self,
        compute_objective,
        item_sizes: pd.DataFrame,
        capacity: float,
        # cognitive_probability: float = 0.1,
        # social_probability: float = 0.3,
        # random_swaps: int = 2,
    ):
        self.swarm = None
        self.item_sizes = item_sizes
        self.capacity = capacity
        # self.cognitive_probability = cognitive_probability
        # self.social_probability = social_probability
        # self.random_swaps = random_swaps
        self.compute_objective = compute_objective

    def is_initialized(self):
        return self.swarm is not None

    def get_agent_size(self, agent):
        item_sizes = self.item_sizes
        return item_sizes[item_sizes['item'].isin(agent.selection)]['size'].sum()
    
    def _increase_size_to_capacity(
        self, 
        agent: Particle, 
        rng: np.random._generator.Generator
    ):
        this_size = self.get_agent_size(agent)
        
        if this_size > self.capacity:
            return agent
        
        increased_selection = list(agent.selection)
        ordering = rng.choice(
            item_sizes[~item_sizes['item'].isin(agent.selection)].index,
            len(item_sizes) - len(agent.selection),
            replace=False
        )
        capacity_remaining = capacity - this_size
        
        for index, row in item_sizes.iloc[ordering, :].iterrows():
            if row['size'] <= capacity_remaining:
                increased_selection.append(row['item'])
                capacity_remaining -= row['size']

            if capacity_remaining == 0:
                break

        return Particle(tuple(sorted(increased_selection)))

    def _decrease_size_to_capacity(
        self,
        agent: Particle,
        rng: np.random._generator.Generator
    ):
        this_capacity = self.get_agent_size(agent)
        if this_capacity <= self.capacity:
            return agent
        
        decreased_selection = list(agent.selection)
        ordering = rng.choice(
            item_sizes[item_sizes['item'].isin(agent.selection)].index,
            len(agent.selection),
            replace=False
        )

        for index, row in item_sizes.iloc[ordering, :].iterrows():
            if this_capacity > capacity:
                decreased_selection.remove(row['item'])
                this_capacity -= row['size']
            if this_capacity <= capacity:
                break
   
        return Particle(selection=tuple(sorted(decreased_selection)))

    def adjust_capacity(
        self,
        agent: Particle,
        rng: np.random._generator.Generator
    ):
        this_capacity = self.get_agent_size(agent)
        if this_capacity < self.capacity:
            return self._increase_size_to_capacity(agent, rng)
        
        if this_capacity > self.capacity:
            return self._decrease_size_to_capacity(agent, rng)

        return agent

    def _initialize_agents(
        self,
        n_agents: int,
        rng: np.random._generator.Generator,
        custom: list = None,
    ):
        if custom is None:
            custom = []
            
        if len(custom) >= n_agents:
            return [
                self.adjust_capacity(agent, rng)
                for agent in custom[:n_agents]
            ]
        
        custom = [
            self.adjust_capacity(agent, rng)
            for agent in custom
        ]
        
        n_new_agents = n_agents - len(custom)
        
        for _ in range(n_new_agents):
            raw_agent = Particle(selection=rng.permutation(item_sizes['item'].to_list()))
            new_agent = optimizer.adjust_capacity(raw_agent, rng)
            custom.append(new_agent)
        
        return custom

    def init_swarm(self, n_agents: int, rng: np.random._generator.Generator, custom: list = None):
        agents = self._initialize_agents(n_agents, rng, custom)
        for agent in agents:
            objective = self.compute_objective(agent)
            agent.objective = objective
            
        cognitive_agents = [copy(agent) for agent in agents]
        social_agent = copy(
            sorted(
                agents,
                key = lambda agent: agent.objective
            )[-1]
        )
        self.swarm = Swarm(
            all_items=tuple(sorted(self.item_sizes['item'].to_list())),
            agents=agents,
            cognitive_agents=cognitive_agents,
            social_agent=social_agent
        )
        
    def random_swaps(self, agent: Particle, n_swaps: int):
        missing_items = item_sizes[
            ~item_sizes['item'].isin(agent.selection)
        ]['item'].to_list()
        n_swaps = min([
            n_swaps,
            len(missing_items),
            len(agent.selection)
        ])
        drop_items = rng.choice(agent.selection, n_swaps, replace=False)
        add_items = rng.choice(missing_items, n_swaps, replace=False)
        return Particle(sorted(tuple(
            [
                item for item in list(agent.selection) + list(add_items)
                if item not in drop_items
            ]
        )))
