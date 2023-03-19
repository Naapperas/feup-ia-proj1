"""
State representation in this simulation
"""


from copy import deepcopy
from typing import List
from graph.graph import Graph
from models.establishment import Establishment


class State:
    """
    The state of the problem, encoding every useful parameter
    """

    def __init__(self):
        self.routes: List[List[Establishment]] = []
        self.network: Graph | None = None

        pass

    def value(self) -> float:
        """
        Returns the value of the current state, to be used in evaluation functions
        """

        return 0.0

    def copy(self):
        """
        Returns a copy of this state that can be modified without persisting changes to this instance
        """
        return deepcopy(self)
