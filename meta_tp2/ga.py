from typing import List
from operator import attrgetter
import numpy as np


class Individual(object):
    """
    A class used to represent an Individual in float-based Genetic Algorithms

    ...

    Attributes
    ----------
    kind : type
        the individual specific representation (float, for now)
    value : FloatList
        the list of float parameters that represents the float-based individual
    fitness : float
        the fitness value attatched to this individual
    generation : int
        the generation that generated the individual

    Methods
    -------
    """

    kind = float

    def __init__(self, value: List[float] = [], generation: int = 0) -> None:
        self.fitness = None
        self.value = value
        self.generation = generation


class Generation(object):
    def __init__(self, number: int, population: List[Individual]):
        self.number = number
        self.population = population
        self.stats = {"min": None, "max": None, "std": None, "mean": None, "best": None}

    def evaluate_stats(self):
        fitness_values = list(map(lambda i: i.fitness, self.population))

        self.stats = {
            "min": np.min(fitness_values),
            "max": np.max(fitness_values),
            "mean": np.mean(fitness_values),
            "std": np.std(fitness_values),
            "best": sorted(self.population, key=attrgetter("fitness"), reverse=True)[0],
        }


def generate_initial_generation(ind_generator: function, pop_size: int = 100):
    pop = [ind_generator() for _i in range(pop_size)]
    return Generation(number=0, population=pop)
