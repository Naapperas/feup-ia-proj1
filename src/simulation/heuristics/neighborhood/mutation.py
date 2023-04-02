"""
Classes and functions related to performing a mutation on a given state
"""


import random
from models.brigade import Brigade
from simulation.state import State

from .generator import Generator


class MutationGenerator(Generator):  # pylint: disable=too-few-public-methods
    """
    Performs a mutation on a given state, changing a single route
    """

    def apply(self, state: State) -> State:
        new_state = state.copy()

        brigade_index = random.randint(0, len(new_state.brigades) - 1)

        brigade = new_state.brigades[brigade_index]
        new_state.brigades = (
            new_state.brigades[:brigade_index] + new_state.brigades[brigade_index + 1 :]
        )

        num_establishments = len(brigade.route)
        i, j = random.sample(range(num_establishments), 2)

        old_route = brigade.route
        old_route[i], old_route[j] = old_route[j], old_route[i]

        new_state.brigades.append(Brigade(old_route))

        return new_state
