"""
State representation in this simulation
"""


from copy import deepcopy
from debug import Printable
from graph.graph import Graph
from models import Brigade
from models.establishment import Establishment


class State(Printable):
    """
    The state of the problem, encoding every useful parameter
    """

    def __init__(
        self,
        brigades: list[Brigade],
    ):
        self.brigades = brigades

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
