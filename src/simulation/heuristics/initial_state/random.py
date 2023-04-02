"""
Random selection for the initial state
"""

from random import choice

from models.establishment import Establishment
from simulation.graph import Graph

from .generator import Generator


class RandomGenerator(Generator):  # pylint: disable=too-few-public-methods
    """
    Generator that returns a random establishment
    """

    def next(
        self,
        establishments: dict[int, Establishment],
        previous: Establishment,  # pylint: disable=unused-argument
        graph: Graph,  # pylint: disable=unused-argument
    ) -> Establishment:
        return choice(list(establishments.values()))
