"""
Classes and functions related to performing a crossover on a given state
"""

import random

from models.brigade import Brigade
from models.route import Route
from simulation.state import State

from .generator import Generator


class CrossoverGenerator(Generator):
    """
    Neighborhood generator that performs a crossover on the given state.
    """

    @staticmethod
    def generate(state: State) -> State:
        new_state = state.copy()

        num_brigades = len(new_state.brigades)

        # select 2 random brigades
        i, j = random.sample(range(num_brigades), 2)
        first_brigade, second_brigade = (
            new_state.brigades[j],
            new_state.brigades[i],
        )

        # remove the old brigades from the previous state
        new_state.brigades = new_state.brigades[:i] + new_state.brigades[i + 1 :]
        new_state.brigades = new_state.brigades[:j] + new_state.brigades[j + 1 :]

        # perform a crossover on the selected brigades
        crossover_point = random.randint(
            0, min(len(first_brigade.route), len(second_brigade.route)) // 2
        )

        new_state.brigades.append(
            Brigade(
                Route(
                    first_brigade.route[:crossover_point]
                    + second_brigade.route[crossover_point:]
                )
            )
        )
        new_state.brigades.append(
            Brigade(
                Route(
                    second_brigade.route[:crossover_point]
                    + first_brigade.route[crossover_point:]
                )
            )
        )

        return new_state
