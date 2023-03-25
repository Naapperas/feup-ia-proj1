"""
State representation in this simulation
"""


from copy import deepcopy
from typing import Type

from debug import Printable
from models import Brigade
from models.establishment import Establishment
from models.route import Route
from simulation.heuristics.initial_state.generator import Generator
from simulation.heuristics.initial_state.random import RandomGenerator
from simulation.network import Network
from simulation.graph import Graph


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
        network: Network,
        num_carriers: int,
        generator: Type[Generator] = RandomGenerator,
    ) -> "State":
        """
        Generates the initial state from the given list of establishments
        using the given generator.

        By default it uses a random generator to generate the initial state
        """

        brigades = [[network.depot] for _ in range(num_carriers)]

        establishments_copy = {e.establishment_id: e for e in establishments}

        while len(establishments_copy) > 0:
            for i, b in enumerate(brigades):
                previous = b[-1]
                establishment = generator.next(
                    establishments_copy, previous, network.graph
                )
                establishments_copy.pop(establishment.establishment_id)
                brigades[i].append(establishment)

        return State([Brigade(Route(b)) for b in brigades])

    def value(self, network: Network) -> float:
        """
        Returns the value of the current state, to be used in evaluation functions.

        This value is based on the current network
        which tells how the different routes are connected
        """

        return sum(map(lambda b: b.total_waiting_time(network), self.brigades), 0)

    def copy(self):
        """
        Returns a copy of this state that can be modified without
        persisting changes to this instance
        """
        return deepcopy(self)
