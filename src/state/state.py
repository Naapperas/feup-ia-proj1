"""
State representation in this simulation
"""


from copy import deepcopy
from typing import Type

from debug import Printable
from graph.graph import Graph
from models import Brigade
from models.establishment import Establishment
from models.route import Route
from simulation.heuristics.initial_state.generator import Generator
from simulation.heuristics.initial_state.random import RandomGenerator


class State(Printable):
    """
    The state of the problem, encoding every useful parameter
    """

    def __init__(
        self,
        brigades: list[Brigade],
    ):
        self.brigades = brigades

    @staticmethod
    def initial_state(
        establishments: list[Establishment],
        num_carriers: int,
        generator: Type[Generator] = RandomGenerator,
    ) -> "State":
        """
        Generates the initial state from the given list of establishments
        using the given generator.

        By default it uses a random generator to generate the initial state
        """

        brigades: list[Brigade] = []

        establishments_copy = deepcopy(establishments)

        for _ in range(num_carriers):
            route_establishments, establishments_copy = generator.generate(
                establishments_copy, num_carriers
            )

            route: Route = Route(
                route_establishments
            )  # do this in order to correctly model other calculations
            brigade: Brigade = Brigade(route)

            brigades.append(brigade)

        return State(brigades)

    def value(self, network: Graph, depot: Establishment) -> float:
        """
        Returns the value of the current state, to be used in evaluation functions.

        This value is based on the current network
        which tells how the different routes are connected
        """

        return sum(
            map(lambda b: b.total_waiting_time(network, depot), self.brigades), 0
        )

    def copy(self):
        """
        Returns a copy of this state that can be modified without
        persisting changes to this instance
        """
        return deepcopy(self)
