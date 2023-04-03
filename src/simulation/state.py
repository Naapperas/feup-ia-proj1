"""
State representation in this simulation
"""


from copy import deepcopy

from debug import Printable
from models.brigade import Brigade
from models.network import Network
from models.route import Route
from .heuristics.initial_state.generator import Generator
from .heuristics.initial_state.random import RandomGenerator


class State(Printable):
    """
    The state of the problem, encoding every useful parameter
    """

    def __init__(
        self,
        brigades: list[Brigade],
    ):
        self.brigades = brigades
        self.cached_value = 0

    @staticmethod
    def initial_state(
        network: Network,
        num_carriers: int,
        generator: Generator = RandomGenerator(),
    ) -> "State":
        """
        Generates the initial state from the given list of establishments
        using the given generator.

        By default it uses a random generator to generate the initial state
        """

        establishments = network.establishments

        brigades = [[network.depot] for _ in range(num_carriers)]

        establishments_copy = {e.establishment_id: e for e in establishments}

        while len(establishments_copy) > 0:
            for brigade in brigades:
                # in case we exhaust every establishment
                if len(establishments_copy) == 0:
                    break

                previous = brigade[-1]
                establishment = generator.next(
                    establishments_copy, previous, network.graph
                )
                establishments_copy.pop(establishment.establishment_id)
                brigade.append(establishment)

        return State([Brigade(Route(brigade)) for brigade in brigades])

    def value(self, network: Network) -> float:
        """
        Returns the value of the current state, to be used in evaluation functions.

        This value is based on the current network
        which tells how the different routes are connected
        """

        self.cached_value = sum(
            map(lambda b: b.total_waiting_time(network), self.brigades), 0
        )
        return self.cached_value

    def copy(self):
        """
        Returns a copy of this state that can be modified without
        persisting changes to this instance
        """

        return deepcopy(self)
