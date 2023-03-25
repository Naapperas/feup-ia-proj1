"""
Classes and methods related to running the simulation of the problem
"""


import math

from simulation.graph import Graph, parse_graph
from models.establishment import Establishment
from models.parse import parse_model
from simulation.network import Network
from simulation.state import State


class Simulation:
    """
    Class responsible for coordinating the simulation
    """

    def __init__(
        self,
        depot: Establishment,
        graph: Graph,
        establishments: list[Establishment],
    ):
        self.establishments = establishments
        self.num_establishments = len(establishments)
        # self.state = State.initial_state(establishments, self.get_num_carriers())
        self.state = State([])
        self.network = Network(depot, graph)

    def get_num_carriers(self) -> int:
        """
        Returns the expected amount of carriers needed to run this simulation
        """

        return math.floor(0.1 * self.num_establishments)

    @staticmethod
    def setup() -> "Simulation":
        """
        Sets up the simulation
        """
        establishments = parse_model("./resources/establishments.csv", Establishment)
        graph = parse_graph("./resources/distances.csv")

        depot = establishments.pop(0)

        return Simulation(depot, graph, list(establishments))
