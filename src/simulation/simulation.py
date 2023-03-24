"""
Classes and methods related to running the simulation of the problem
"""


import math
from graph import parse_graph

from graph.graph import Graph
from models.establishment import Establishment
from models.parse import parse_model
from simulation.network import Network
from simulation.state import State

# For development purposes
_NUM_MODELS_TO_PARSE: int = 20


class Simulation:
    """
    Class responsible for coordinating the simulation
    """

    def __init__(
        self,
        depot: Establishment,
        state: State,
        graph: Graph,
        establishments: list[Establishment],
    ):
        self.state = state
        self.network = Network(depot, graph)
        self.establishments = establishments

    @staticmethod
    def get_num_carriers(establishments: list[Establishment]) -> int:
        """
        Returns the expected amount of carriers needed to run this simulation
        """

        return math.floor(0.1 * len(establishments))

    @staticmethod
    def setup() -> "Simulation":
        """
        Sets up the simulation
        """
        establishments = parse_model(
            "./resources/establishments.csv", Establishment, _NUM_MODELS_TO_PARSE
        )
        network = parse_graph("./resources/distances.csv")

        depot, establishments = establishments[0], establishments[1:]

        num_carriers: int = Simulation.get_num_carriers(establishments)

        state: State = State.initial_state(establishments, num_carriers)

        return Simulation(depot, state, network, establishments)

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

    def get_network(self) -> Network:
        """
        Returns this simulation's network
        """

        return self.network
