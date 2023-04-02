"""
Classes and functions related to calculating 
the best neighbour after a set ammount of iterations
"""


from models.network import Network
from simulation.state import State

from .crossover import CrossoverGenerator
from .generator import Generator
from .mutation import MutationGenerator
from .random import RandomGenerator


class FirstBestGenerator(Generator):  # pylint: disable=too-few-public-methods
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
            generators = [CrossoverGenerator(), MutationGenerator()]

        self.generator = RandomGenerator(generators)
        self.network = network
        self.num_iters = num_iters

    def apply(self, state: State) -> State:
        generator = self.generator.random_generator()

        best_state = generator.apply(state)
        best_value = best_state.value(self.network)

        for _ in range(self.num_iters):
            new_state = generator.apply(state)

            if new_state.value(self.network) < best_value:
                best_state = new_state
                best_value = best_state.value(self.network)

        # FALLBACK, should never happen
        return state.copy()
