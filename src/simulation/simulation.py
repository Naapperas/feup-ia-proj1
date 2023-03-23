"""
Classes and methods related to running the simulation of the problem
"""


import math
from graph.graph import Graph
from models.establishment import Establishment
from state.state import State


class Simulation:
    """
    Class responsible for coordinating the simulation
    """

    def __init__(
        self,
        depot: Establishment,
        state: State,
        network: Graph,
        establishments: list[Establishment],
    ):
        self.depot = depot
        self.state = state
        self.network = network
        self.establishments = establishments

    @staticmethod
    def get_num_carriers(establishments: list[Establishment]) -> int:
        """
        Returns the expected amount of carriers needed to run this simulation
        """

        return math.floor(0.1 * len(establishments))

    def get_state(self) -> State:
        """
        Returns this simulation's current state
        """

        return self.state

    def set_state(self, new_state: State):
        """
        Sets this simulation's current state
        """

        self.state = new_state
