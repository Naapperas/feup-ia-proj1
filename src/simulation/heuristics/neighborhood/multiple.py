"""
Classes and methods related to generating neighboring states by applying several other generators in succession
"""

from simulation.state import State

from .generator import Generator


class MultiGenerator(Generator):
    """
    A class for generating neighboring states, applying several other in succession.
    """

    def __init__(self, generators: list[Generator]):
        self.generators = generators

    def apply(self, state: State) -> State:
        new_state = state.copy()

        for generator in self.generators:
            new_state = generator.apply(new_state)

        return new_state

    def name(self) -> str:
        return "Multi Generator"
