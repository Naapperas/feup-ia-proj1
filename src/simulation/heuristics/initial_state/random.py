"""
Random selection for the initial state
"""

from copy import deepcopy
from random import sample

from models.establishment import Establishment

from .generator import Generator


class RandomGenerator(Generator):  # pylint: disable=too-few-public-methods
    """
    Generator that takes a random sample from the population provided
    """

    @staticmethod
    def generate(
        establishments: list[Establishment], num_carriers: int
    ) -> tuple[list[Establishment], list[Establishment]]:
        establishments_copy = deepcopy(establishments)

        route_establishments = sample(
            establishments_copy, len(establishments_copy) // num_carriers
        )

        # generate random initial state
        for establishment in route_establishments:
            establishments_copy.remove(establishment)

        return (route_establishments, establishments_copy)
