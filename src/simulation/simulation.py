"""
Classes and methods related to running the simulation of the problem
"""


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
