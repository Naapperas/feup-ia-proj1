"""
Classes and functions related to calculating 
the best neighbor after a set amount of iterations
"""


from models.network import Network
from simulation.state import State

from .crossover import CrossoverGenerator
from .generator import Generator
from .mutation import MutationGenerator
from .random import RandomGenerator
from .shuffle import ShuffleGenerator


class BestAfterGenerator(Generator):
    """
    Calculates the best neighbor found after a set number of iterations
    """

    def __init__(
        self,
        network: Network,
        generators: list[Generator],
        num_iters: int,
    ):
        if generators == []:
            generators = [CrossoverGenerator(), MutationGenerator(), ShuffleGenerator()]

        self.generator = RandomGenerator(generators)
        self.network = network
        self.num_iters = num_iters

    def apply(self, state: State) -> State:
        best_state = state.copy()
        best_value = best_state.value(self.network)

        for _ in range(self.num_iters):
            generator = self.generator.random_generator()

            new_state = generator.apply(best_state)

            if new_state.value(self.network) < best_value:
                best_state = new_state
                best_value = best_state.value(self.network)

        return best_state

    def name(self) -> str:
        return "Best After N"
