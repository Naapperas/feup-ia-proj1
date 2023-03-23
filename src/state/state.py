"""
State representation in this simulation
"""


from copy import deepcopy
from debug import Printable
from graph import Graph
from models import Brigade, Establishment


class State(Printable):
    """
    The state of the problem, encoding every useful parameter
    """

    def __init__(
        self,
        establishments: list[Establishment],
        brigades: list[Brigade],
        network: Graph,
    ):
        self.establishments = establishments
        self.brigades = brigades
        self.network = network

    def value(self) -> float:
        """
        Returns the value of the current state, to be used in evaluation functions
        """

        return 0.0

    def copy(self):
        """
        Returns a copy of this state that can be modified without
        persisting changes to this instance
        """
        return deepcopy(self)
