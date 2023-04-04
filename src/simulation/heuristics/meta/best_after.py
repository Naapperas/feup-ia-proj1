"""
Classes and methods related to generating the best solution after a set number of iterations
"""

from typing import Callable, Generator

from models.network import Network
from simulation import State
from simulation.heuristics.meta.metaheuristic import Metaheuristic
from simulation.heuristics.neighborhood.generator import Generator as NeighborGenerator


class BestAfterN(Metaheuristic):
    """
    A class for implementing a variation of "steepest-accent" hill-climbing.
    """

    def __init__(
        self,
        generator: NeighborGenerator,
        fitness_func: Callable[[State], float],
        network: Network,
        num_iters: int,
    ):
        self.generator = generator
        self.fitness_func = fitness_func
        self.establish_network = network
        self.num_iters = num_iters

    def optimize(self, initial_state: State) -> Generator[State, None, State]:
        best_state = initial_state.copy()
        best_value = self.fitness_func(best_state)

        while True:
            for _ in range(self.num_iters):
                new_state = self.generator.apply(best_state)

                if (candidate := self.fitness_func(new_state)) > best_value:
                    best_state = new_state
                    best_value = candidate

            if best_value == self.fitness_func(
                initial_state
            ):  # this will get stuck in a local optimum
                break

            yield best_state

        return best_state
