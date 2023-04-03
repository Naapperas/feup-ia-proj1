from typing import Callable
from simulation import State
from simulation.heuristics.neighborhood.generator import Generator


class Metaheuristic:
    """
    A class for implementing metaheuristics.

    Attributes:
        generator (Generator): the generator for generating neighboring states
        fitness_func (Callable[[State], float]): the fitness function
    """

    def __init__(self, generator: Generator, fitness_func: Callable[[State], float]):
        """
        Initializes the metaheuristic.

        Args:
            generator (Generator): the generator for generating neighboring states
            fitness_func (Callable[[State], float]): the fitness function
        """
        self.generator = generator
        self.fitness_func = fitness_func

    def optimize(self, initial_state: State) -> State:
        """
        Runs the metaheuristic to optimize the specified initial state.

        Returns:
            State: the final state that was reached by the metaheuristic
        """
        current_state = initial_state
        while True:
            new_state = self.generator.apply(current_state)
            if self.fitness_func(new_state) > self.fitness_func(current_state):
                current_state = new_state
            else:
                break
        return current_state