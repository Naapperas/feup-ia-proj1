"""
Classes and methods related to running the simulation of the problem
"""


import math

from models.establishment import Establishment
from models.network import Network
from models.parse import parse_model
from simulation.graph import Graph, parse_graph
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
        self.state = State([])
        self.network = Network(depot, graph)

    def get_num_carriers(self) -> int:
        """
        Returns the expected amount of carriers needed to run this simulation
        """

        return math.floor(float(0.1 * self.num_establishments))

    @staticmethod
    def setup() -> "Simulation":
        """
        Sets up the simulation
        """
        establishments: list[Establishment] = parse_model(
            "./resources/dataset/establishments.csv", Establishment
        )
        graph = parse_graph("./resources/dataset/distances.csv")

        depot = establishments.pop(0)

        return Simulation(depot, graph, list(establishments))
