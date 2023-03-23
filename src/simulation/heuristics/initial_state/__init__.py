"""
Generator function for the initial state
"""

from copy import deepcopy
from models.brigade import Brigade
from models.establishment import Establishment
from models.route import Route
from state.state import State

from .generator import Generator
from .random import *


def initial_state(
    establishments: list[Establishment],
    num_carriers: int,
    generator: Generator = RandomGenerator(),
) -> State:
    """
    Generates the initial state from the given list of establishments
    using the given generator.

    By default it uses a random generator to generate the initial state
    """

    brigades: list[Brigade] = []

    establishments_copy = deepcopy(establishments[1:])

    for _ in range(num_carriers):
        route_establishments, establishments_copy = generator.generate(
            establishments_copy, num_carriers
        )

        route: Route = Route(route_establishments)
        brigade: Brigade = Brigade(route)

        brigades.append(brigade)

    return State(brigades)
