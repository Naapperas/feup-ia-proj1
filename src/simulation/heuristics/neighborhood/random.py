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

    def __init__(self, generators: list[Generator], randomize: bool = False):
        assert len(generators) > 0, "No generators provided"

        self.randomize = randomize
        self.generators = generators
        self.generator = self.random_generator()

    def apply(self, state: State) -> State:
        new_state = self.generator.apply(state)

        if self.randomize:
            self.generator = self.random_generator()

        return new_state

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
