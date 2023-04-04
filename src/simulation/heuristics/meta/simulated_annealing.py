import math
import random
from typing import Callable, Generator
from config import Config

from simulation import State
from simulation.heuristics.neighborhood.generator import Generator as NeighborGenerator

from .metaheuristic import Metaheuristic


MAX_ITERATIONS_WITHOUT_IMPROVEMENT = int(
    Config.get("SA_MAX_ITERATIONS_WITHOUT_IMPROVEMENT")
)


class SimulatedAnnealing(Metaheuristic):
    """
    A class for implementing simulated annealing.

    Attributes:
        generator (Generator): the generator for generating neighboring states
        fitness_func (Callable[[State], float]): the fitness function
        initial_temperature (float): the initial temperature for simulated annealing
        cooling_factor (float): the cooling factor for simulated annealing
        limit_temp (float): the limit temperature for simulated annealing
    """

    def __init__(
        self,
        generator: NeighborGenerator,
        fitness_func: Callable[[State], float],
        initial_temperature: float = 100.0,
        cooling_factor: float = 0.95,
        limit_temp: float = 1,
    ):
        """
        Initializes the simulated annealing algorithm.

        Args:
            generator (Generator): the generator for generating neighboring states
            fitness_func (Callable[[State], float]): the fitness function
            initial_temperature (float): the initial temperature for simulated annealing
            cooling_factor (float): the cooling factor for simulated annealing
            limit_temp (float): the limit temperature for simulated annealing
        """
        super().__init__(generator, fitness_func)
        self.initial_temperature = initial_temperature
        self.cooling_factor = cooling_factor
        self.limit_temp = limit_temp

    def optimize(self, initial_state: State) -> Generator[State, None, State]:
        """
        Runs the simulated annealing algorithm to optimize the specified initial state.

        Returns:
            State: the final state that was reached by the simulated annealing algorithm
        """

        prev_deltas: list[float] = [
            -1 for _ in range(MAX_ITERATIONS_WITHOUT_IMPROVEMENT)
        ]

        current_state = initial_state
        current_fitness = self.fitness_func(current_state)
        temperature = self.initial_temperature

        while temperature > self.limit_temp:
            yield current_state
            print(f"Annealing... (temp: {temperature})")
            neighbor = self.generator.apply(current_state)
            neighbor_fitness = self.fitness_func(neighbor)

            delta = neighbor_fitness - current_fitness

            if delta > 0:
                current_state = neighbor
                current_fitness = neighbor_fitness
                print("Better state found!")
            else:
                delta = neighbor_fitness - current_fitness
                prev_deltas.append(delta)
                if len(prev_deltas) > MAX_ITERATIONS_WITHOUT_IMPROVEMENT:
                    prev_deltas.pop(0)

                if all(val == 0 for val in prev_deltas) or len(set(prev_deltas)) == 1:
                    break

                probability = math.exp(delta / temperature)

                if random.random() < probability:
                    current_state = neighbor
                    current_fitness = neighbor_fitness
                    print(f"Worse state accepted with probability {probability}!")

            temperature *= self.cooling_factor

        return current_state
