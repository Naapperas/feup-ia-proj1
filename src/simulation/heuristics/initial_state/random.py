"""
Random selection for the initial state
"""

from copy import deepcopy
from random import choice

from models.establishment import Establishment
from ...graph import Graph

from .generator import Generator


class RandomGenerator(Generator):  # pylint: disable=too-few-public-methods
    """
    Generator that takes a random sample from the population provided
    """

    @staticmethod
    def next(
        establishments: dict[int, Establishment],
        previous: Establishment,
        graph: Graph,
    ) -> Establishment:
        return choice(list(establishments.values()))
