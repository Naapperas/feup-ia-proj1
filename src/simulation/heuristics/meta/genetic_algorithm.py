from typing import Callable
from simulation import State
from metaheuristic import Metaheuristic
import random
from typing import Callable, Generator

from metaheuristic import Metaheuristic

from simulation import State
from simulation.heuristics.neighborhood.generator import Generator as NeighborGenerator


class GeneticAlgorithm(Metaheuristic):
    """
    A class for implementing genetic algorithms.

    Attributes:
        generator (NeighborGenerator): the generator for generating neighboring states
        fitness_func (Callable[[State], float]): the fitness function
        population_size (int): the size of the population to use in the genetic algorithm
        crossover_rate (float): the probability that two parents will breed
        mutation_rate (float): the probability that a single gene will mutate
    """

    def __init__(
        self,
        generator: NeighborGenerator,
        fitness_func: Callable[[State], float],
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
    ):
        """
        Initializes the genetic algorithm.

        Args:
            generator (NeighborGenerator): the generator for generating neighboring states
            fitness_func (Callable[[State], float]): the fitness function
            population_size (int): the size of the population to use in the genetic algorithm
            crossover_rate (float): the probability that two parents will breed
            mutation_rate (float): the probability that a single gene will mutate
        """
        super().__init__(generator, fitness_func)
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def optimize(self, initial_state: State) -> Generator[State, None, State]:
        """
        Runs the genetic algorithm to optimize the specified initial state.

        Returns:
            State: the final state that was reached by the genetic algorithm
        """
        # Create initial population
        population = [initial_state.copy() for _ in range(self.population_size)]

        # Run iterations until termination condition is met
        while True:
            yield max(population, key=self.fitness_func)

            # Evaluate fitness of all individuals
            fitness_scores = [
                self.fitness_func(individual) for individual in population
            ]

            # Check if termination condition is met
            if self.is_termination_condition_met(population, fitness_scores):
                break

            # Select parents for reproduction
            parents = self.select_parents(population, fitness_scores)

            # Breed new individuals from parents
            offspring = self.breed(parents)

            # Mutate offspring
            mutated_offspring = self.mutate(offspring)

            # Add mutated offspring to population
            population += mutated_offspring

            # Keep the best individuals
            population = self.keep_best_individuals(population)

        return max(population, key=self.fitness_func)

    # TODO: Change the termination condition
    def is_termination_condition_met(
        self, population: list[State], fitness_scores: list[float]
    ) -> bool:
        """
        Checks if the termination condition is met for the genetic algorithm.

        In this implementation, the termination condition is met when the maximum fitness
        score is equal to 1.

        Args:
            population (list): the current population
            fitness_scores (list): the fitness scores of the individuals in the population

        Returns:
            bool: True if the termination condition is met, False otherwise
        """
        return max(fitness_scores) == 1.0

    def select_parents(
        self, population: list[State], fitness_scores: list[float]
    ) -> list[State]:
        """
        Selects parents for reproduction in the genetic algorithm.

        In this implementation, the parents are selected using tournament selection.

        Args:
            population (list): the current population
            fitness_scores (list): the fitness scores of the individuals in the population

        Returns:
            list: the selected parents
        """
        parents: list[State] = []
        for _ in range(len(population)):
            tournament = random.sample(range(len(population)), 2)
            if fitness_scores[tournament[0]] > fitness_scores[tournament[1]]:
                parents.append(population[tournament[0]])
            else:
                parents.append(population[tournament[1]])

        return parents

    def breed(self, parents: list[State]) -> list[State]:
        """
        Breeds new individuals from parents in the genetic algorithm.

        In this implementation, the offspring is created using uniform crossover.

        Args:
            parents (list): the selected parents

        Returns:
            list: the offspring
        """
        offspring: list[State] = []
        for _ in range(self.population_size):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if random.random() < self.crossover_rate:
                child = parent1.copy()
                for j in range(len(child)):
                    if random.random() < 0.5:
                        child[j] = parent2[j]
                offspring.append(child)
            else:
                offspring.append(parent1)
        return offspring

    def mutate(self, offspring: list) -> list:
        """
        Mutates offspring in the genetic algorithm.

        In this implementation, the mutation is performed using bit flip mutation.

        Args:
            offspring (list): the offspring to mutate

        Returns:
            list: the mutated offspring
        """
        mutated_offspring = []
        for i in range(len(offspring)):
            individual = offspring[i]
            for j in range(len(individual)):
                if random.random() < self.mutation_rate:
                    individual[j] = 1 - individual[j]
            mutated_offspring.append(individual)
        return mutated_offspring

    def keep_best_individuals(self, population: list[State]) -> list[State]:
        """
        Keeps the best individuals in the population.

        In this implementation, the best individuals are determined using elitism.

        Args:
            population (list): the population to select the best individuals from

        Returns:
            list: the best individuals
        """
        fitness_scores = [self.fitness_func(individual) for individual in population]
        sorted_population = [
            x for _, x in sorted(zip(fitness_scores, population), reverse=True)
        ]
        return sorted_population[: self.population_size]
