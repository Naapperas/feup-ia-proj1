"""
Classes and methods related to generating 
neighboring states by applying a random generator
"""

import random
from simulation.state import State

from .generator import Generator


class RandomGenerator(Generator):
    """
    A class for generating neighboring states,
    applying a random generator out of the given state generator.
    """

    def __init__(self, generators: list[Generator]):
        assert len(generators) > 0, "No generators provided"

        self.generators = generators
        self.generator = self.random_generator()

    def apply(self, state: State) -> State:
        return self.generator.apply(state)

    def random_generator(self) -> Generator:
        """Returns a random generator from the list of generators
        passed in the constructor.

        Returns:
            Generator: the random generator

        Yields:
            Generator: the random generator
        """
        return random.choice(self.generators)

    def name(self) -> str:
        return "Random Generator"
