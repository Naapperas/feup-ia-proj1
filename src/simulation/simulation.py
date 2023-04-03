"""
Classes and methods related to running the simulation of the problem
"""


import math
from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Generator

from models.establishment import Establishment
from models.network import Network
from models.parse import parse_model
from simulation.heuristics.neighborhood.crossover import CrossoverGenerator
from simulation.heuristics.neighborhood.mutation import MutationGenerator
from simulation.heuristics.neighborhood.random import RandomGenerator

from .graph import Graph, parse_graph
from .heuristics.meta.metaheuristic import Metaheuristic
from .heuristics.meta.simulated_annealing import SimulatedAnnealing
from .state import State


@dataclass
class Statistics:
    runtime: float
    best_solution_runtime: float

    total_iterations: int
    best_solution_iterations: int


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
            heuristic (Metaheuristic, optional): The metaheuristic to use when optimizing the problem's solution. Defaults to None.
        """
        self.stats = Statistics(0, 0, 0, 0)
        self.state = State([])
        self.network = Network(depot, graph, establishments)
        self.num_establishments = len(establishments)

        if heuristic is None:
            default_neighbor_generator = RandomGenerator(
                [
                    MutationGenerator(),
                    CrossoverGenerator(),
                ]
            )
            default_fitness_function: Callable[[State], float] = lambda s: -s.value(
                self.network
            )

            self.heuristic = SimulatedAnnealing(
                default_neighbor_generator,
                default_fitness_function,
                cooling_factor=0.999,
                limit_temp=1e-8,
            )
        else:
            self.heuristic = heuristic

    def get_num_carriers(self) -> int:
        """
        Returns the expected amount of carriers needed to run this simulation
        """

        return math.floor(0.1 * self.num_establishments)

    def run(self) -> Generator[State, None, None]:
        """Runs the simulation, yielding the state of the simulation at each iteration

        Yields:
            State: The state of the simulation at each iteration
        """

        start = perf_counter()
        optimal_start = start

        optimal_end = optimal_start

        for new_state in self.heuristic.optimize(self.state):
            optimal_end = perf_counter()
            self.state = new_state
            yield self.state

        end = perf_counter()

        self.stats.runtime = end - start

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
