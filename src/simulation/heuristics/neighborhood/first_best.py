"""
Classes and functions related to calculating 
the first neighbor that is better than the given one
"""


from models.network import Network
from simulation.state import State

from .crossover import CrossoverGenerator
from .generator import Generator
from .mutation import MutationGenerator
from .random import RandomGenerator


class FirstBestGenerator(Generator):  # pylint: disable=too-few-public-methods
    """
    Calculates the first neighbor that is better than the given one
    """

    def __init__(
        self,
        network: Network,
        generators: list[Generator],
    ):
        if generators == []:
            generators = [CrossoverGenerator(), MutationGenerator()]

        self.generator = RandomGenerator(generators)
        self.network = network

    def apply(self, state: State) -> State:
        generator = self.generator.random_generator()

        while True:
            new_state = generator.apply(state)

            # should change to abstract fitness function, perhaps
            if new_state.value(self.network) < state.value(self.network):
                return new_state

        # FALLBACK, should never happen
        return state.copy()
