"""
Classes and methods related to running the simulation of the problem
"""


import math
from dataclasses import dataclass, field
from time import perf_counter
from typing import Callable, Generator, Optional

from config import Config
from models.establishment import Establishment
from models.parse import parse_model
from simulation.heuristics.neighborhood.crossover import CrossoverGenerator
from simulation.heuristics.neighborhood.generator import (
    Generator as NeighborhoodGenerator,
)
from simulation.heuristics.neighborhood.mutation import MutationGenerator
from simulation.heuristics.neighborhood.random import RandomGenerator
from simulation.heuristics.neighborhood.shuffle import ShuffleGenerator

from .graph import Graph, parse_graph
from .heuristics.meta.metaheuristic import Metaheuristic
from .state import State


class SimulationConfig:
    """
    Class responsible for holding the configuration of the simulation
    """

    def __init__(
        self,
        heuristic: Optional[Metaheuristic],
        fitness_function: Optional[Callable[[State], float]],
        neighborhood_generator: Optional[NeighborhoodGenerator],
    ):
        real_neighborhood_generator = (
            neighborhood_generator
            if neighborhood_generator is not None
            else RandomGenerator(
                [
                    MutationGenerator(),
                    CrossoverGenerator(),
                    ShuffleGenerator(),
                ],
                randomize=True,
            )
        )

        real_fitness_function: Callable[[State], float] = (
            fitness_function
            if fitness_function is not None
            else lambda state: -state.value()
        )

        self.heuristic = (
            heuristic
            if heuristic is not None
            else Metaheuristic(real_neighborhood_generator, real_fitness_function)
        )


@dataclass(init=False)
class SimulationStatistics:  # pylint: disable=too-many-instance-attributes
    """
    Collect statistics about the simulation
    """

    runtime: float = -1.0
    # best_solution_runtime: float = -1.0

    total_iterations: int = -1
    # best_solution_iterations: int = -1

    values: list[float] = field(default_factory=list[float])

    best_solution: State

    metaheuristic_name: str = ""
    initial_state_generator_name: str = ""


class Simulation:
    """
    Class responsible for coordinating the simulation
    """

    def __init__(
        self,
        depot: Establishment,
        establishments: list[Establishment],
        graph: Graph,
        config: SimulationConfig,
    ):
        """Creates a new Simulation with the given parameters

        Args:
            depot (Establishment): the depot of this simulation
            graph (Graph): the graph of this simulation (aka, an adjacency matrix)
            establishments (list[Establishment]): the list of establishments to use
            heuristic (Metaheuristic, optional): The metaheuristic to use when optimizing the problem's solution. Defaults to None.
        """
        self.stats = SimulationStatistics()
        self.state = State([], depot, establishments, graph)
        self.num_establishments = len(
            establishments
        )  # HACK: this is a hack, but it works

        self.heuristic = config.heuristic

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

        iterations = 0
        start = perf_counter()

        values: list[float] = [self.state.value()]

        for new_state in self.heuristic.optimize(self.state):
            self.state = new_state
            values.append(self.state.cached_value)

            yield self.state

            iterations += 1

        end = perf_counter()

        self.stats.values = values
        self.stats.runtime = end - start
        self.stats.total_iterations = iterations
        self.stats.best_solution = self.state

    @staticmethod
    def setup(simulation_config: SimulationConfig) -> "Simulation":
        """
        Sets up the simulation
        """
        num_establishments_to_parse = int(Config.get("NUM_MODELS_TO_PARSE"))

        establishments = parse_model(
            "./resources/dataset/establishments.csv",
            Establishment,
            num_establishments_to_parse,
        )
        graph = parse_graph("./resources/dataset/distances.csv")

        depot = establishments.pop(0)

        return Simulation(depot, establishments, graph, simulation_config)
