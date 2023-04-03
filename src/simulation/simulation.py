"""
Classes and methods related to running the simulation of the problem
"""


import math
from typing import Generator

from models.establishment import Establishment
from models.network import Network
from models.parse import parse_model
from simulation.graph import Graph, parse_graph
from simulation.heuristics.meta.metaheuristic import Metaheuristic
from simulation.heuristics.neighborhood.first_best import FirstBestGenerator
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
        heuristic: Metaheuristic | None = None,
    ):
        """Creates a new Simulation with the given parameters

        Args:
            depot (Establishment): the depot of this simulation
            graph (Graph): the graph of this simulation (aka, an adjacency matrix)
            establishments (list[Establishment]): the list of establishments to use
            heuristic (Metaheuristic | None, optional): The metaheuristic to use when optimizing the problem's solution. Defaults to None.
        """
        self.state = State([])
        self.network = Network(depot, graph, establishments)

        if heuristic is None:
            neighbor_generator = FirstBestGenerator(self.network, [])
            
            self.heuristic = Metaheuristic(neighbor_generator, lambda s: s.value(self.network))
        else:
            self.heuristic = heuristic


    def get_num_carriers(self) -> int:
        """
        Returns the expected amount of carriers needed to run this simulation
        """

        return math.floor(float(0.1 * len(self.network.establishments)))

    def run(self) -> Generator[State, None, None]:
        while True:
            # TODO: figure out how to break out of this
            # TODO: collect metrics
            self.state = self.heuristic.optimize(self.state)
            yield self.state


    @staticmethod
    def setup() -> "Simulation":
        """
        Sets up the simulation
        """
        establishments = parse_model(
            "./resources/dataset/establishments.csv", Establishment
        )
        graph = parse_graph("./resources/dataset/distances.csv")

        depot = establishments.pop(0)

        return Simulation(depot, graph, list(establishments))
