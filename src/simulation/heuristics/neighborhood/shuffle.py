"""
Classes and functions related to performing a mutation on a given state
"""


import random
from models.brigade import Brigade
from models.route import Route
from simulation.state import State

from .generator import Generator


class ShuffleGenerator(Generator):
    """
    Performs a shuffle on a given state, changing every route
    """

    def apply(self, state: State) -> State:
        new_state = state.copy()

        brigade_index = random.randint(0, len(new_state.brigades) - 1)

        brigade = new_state.brigades[brigade_index]
        new_state.brigades = (
            new_state.brigades[:brigade_index] + new_state.brigades[brigade_index + 1 :]
        )

        route_establishments = brigade.route.route_establishments
        random.shuffle(route_establishments)

        new_state.brigades.append(Brigade(Route(route_establishments)))

        return new_state

    def name(self) -> str:
        return "Shuffle"
