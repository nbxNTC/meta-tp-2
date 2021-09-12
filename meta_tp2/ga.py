from typing import List, Callable
from operator import attrgetter
from functools import reduce
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

    def __format__(self, format_spec: str) -> str:
        return "f({}) = {}".format(str(self.value), str(self.fitness))


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

    def print_stats(self):
        self.evaluate_stats()
        print("~~~ GERAÇÃO {} ~~~".format(self.number))
        data = reduce(
            lambda x, y: x + y, [list(self.stats.keys()), list(self.stats.values())]
        )
        print_table(data, 5, 20)


def print_table(data, cols, wide):
    """Prints formatted data on columns of given width."""
    n, r = divmod(len(data), cols)
    pat = "{{:{}}} ".format(wide)
    line = "\n".join(pat * cols for _ in range(n))
    last_line = pat * r
    print(line.format(*data))
    print(last_line.format(*data[n * cols :]))


def generate_initial_generation(ind_generator: Callable, pop_size: int = 100):
    pop = [ind_generator() for _i in range(pop_size)]
    return Generation(number=0, population=pop)
