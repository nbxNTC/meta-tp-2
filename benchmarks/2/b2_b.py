import datetime
from operator import attrgetter
import random
import math

import numpy as np
import pandas as pd

from meta_tp2.ga import Generation, Individual, generate_initial_generation
from meta_tp2.selection import SelectionType
from meta_tp2.crossover import CrossoverType
from meta_tp2.mutation import MutationType

#
# Minimizar (x1 - 10)^3 + (x2 - 20)^3
# sujeito a:
#  -(x1 - 5)^2 - (x2 - 5)^2 + 100 ≤ 0
# (x1 - 6)^2 + (x2 - 5)^2 - 82.81 ≤ 0
#
# Dominio x1 em [13, 100]
# Dominio x2 em [0, 100]
#

# Parâmetros
POPULATION_SIZE = 50
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.05
SELECTION_SIZE = POPULATION_SIZE
TOURNAMENT_SIZE = 5
SELECTION = SelectionType.TOURNAMENT
CROSSOVER = CrossoverType.ONE_POINT
MUTATION = MutationType.UNIFORM
MAX_NOISE_SIZE = 0.2
MAX_GENERATION = 500

MULTIPLYING_FACTOR = -1
RESTRICTION_DOMIAN_PENALTY = 25000


def objective_function(p_min, p, a, b, c, e, f):
    return (a * math.pow(p, 2)) + (b * p) + c + abs(e * math.sin(f * (p_min - p)))


class function_variables:
    def __init__(self, a, b, c, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.e = e
        self.f = f


generating_units_variables = [
    function_variables(0.00028, 8.10, 550, 300, 0.035),
    function_variables(0.00056, 8.10, 309, 200, 0.042),
    function_variables(0.00056, 8.10, 307, 150, 0.042),
    function_variables(0.00324, 7.74, 240, 150, 0.063),
    function_variables(0.00324, 7.74, 240, 150, 0.063),
    function_variables(0.00324, 7.74, 240, 150, 0.063),
    function_variables(0.00324, 7.74, 240, 150, 0.063),
    function_variables(0.00324, 7.74, 240, 150, 0.063),
    function_variables(0.00324, 7.74, 240, 150, 0.063),
    function_variables(0.00284, 8.60, 126, 100, 0.084),
    function_variables(0.00284, 8.60, 126, 100, 0.084),
    function_variables(0.00284, 8.60, 126, 100, 0.084),
    function_variables(0.00284, 8.60, 126, 100, 0.084),
]


class domain:
    def __init__(self, p_min, p_max):
        self.p_min = p_min
        self.p_max = p_max


restrictions_domains = [
    domain(0, 680),
    domain(0, 360),
    domain(0, 360),
    domain(60, 180),
    domain(60, 180),
    domain(60, 180),
    domain(60, 180),
    domain(60, 180),
    domain(60, 180),
    domain(40, 120),
    domain(40, 120),
    domain(55, 120),
    domain(55, 120),
]


def restriction_domain(generating_unit, p):
    if (
        p < restrictions_domains[generating_unit].p_min
        or p > restrictions_domains[generating_unit].p_max
    ):
        return RESTRICTION_DOMIAN_PENALTY

    return 0


def fitness(generating_units):
    penalty = 0
    for i in range(len(generating_units)):
        penalty += restriction_domain(i, generating_units[i])

    if penalty > 0:
        return None, None

    objective_function_values = []
    for i in range(len(generating_units)):
        objective_function_values.append(
            objective_function(
                restrictions_domains[i].p_min,
                generating_units[i],
                generating_units_variables[i].a,
                generating_units_variables[i].b,
                generating_units_variables[i].c,
                generating_units_variables[i].e,
                generating_units_variables[i].f,
            )
        )

    return (
        MULTIPLYING_FACTOR * (sum(objective_function_values) + penalty),
        sum(objective_function_values),
    )


def individual_generation(gen=0):
    new_generating_units = []
    for i in range(13):
        new_generating_units.append(
            random.uniform(restrictions_domains[i].p_min, restrictions_domains[i].p_max)
        )

    return Individual(new_generating_units, gen)


def evaluate_individual(individual):
    fit, obj_fun_values = fitness(individual.value)
    individual.fitness = fit
    individual.objective_function_value = obj_fun_values


def evaluate_population(population):
    for individual in population:
        evaluate_individual(individual)


def get_best_fitness(population):
    new_best_fitness = population[0].fitness
    for individual in population:
        if individual.fitness > new_best_fitness:
            new_best_fitness = individual.fitness


def run(run_index, debug=False):
    best_of_run = None

    generation = generate_initial_generation(individual_generation, POPULATION_SIZE)
    evaluate_population(generation.population)
    for i in range(len(generation.population)):
        while generation.population[i].fitness is None:
            generation.population[i] = individual_generation(gen=generation.number)
            evaluate_individual(generation.population[i])

    if debug:
        generation.print_stats()
    generation.evaluate_stats()
    best_of_run = generation.stats["best"]

    while True:
        selected = SELECTION(generation.population, SELECTION_SIZE, TOURNAMENT_SIZE)

        offspring = []
        for individual_01, individual_02 in zip(selected[0::2], selected[1::2]):
            if random.uniform(0, 1) < CROSSOVER_RATE:
                children_01, children_02 = CROSSOVER(individual_01, individual_02)

                children_01.generation = generation.number
                children_02.generation = generation.number

                offspring.append(children_01)
                offspring.append(children_02)
            else:
                offspring.append(individual_01)
                offspring.append(individual_02)

        for individual in offspring:
            if random.uniform(0, 1) < MUTATION_RATE:
                individual = MUTATION(individual, MAX_NOISE_SIZE)

        evaluate_population(offspring)
        for i in range(len(offspring)):
            while offspring[i].fitness is None:
                offspring[i] = individual_generation(gen=generation.number)
                evaluate_individual(offspring[i])

        generation = Generation(generation.number + 1, offspring)
        if debug:
            generation.print_stats()

        generation.evaluate_stats()
        best_of_run = generation.stats["best"]

        if generation.number == MAX_GENERATION:
            break

    return best_of_run


# EXECUCOES
best_of_runs = []
for i in range(30):
    print("Run {}".format(i))
    best_of_run = run(i)

    bof = {
        "fitness": best_of_run.fitness,
        "objective_function_value": best_of_run.objective_function_value,
        "value": str(best_of_run.value),
        "generation": str(best_of_run.generation),
        "run": i,
    }
    best_of_runs.append(bof)

df = pd.DataFrame(best_of_runs)
df.to_json("./results/2_b_{}.json".format(datetime.datetime.now().isoformat()))
