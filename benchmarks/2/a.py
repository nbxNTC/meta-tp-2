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
POPULATION_SIZE = 500
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.05
SELECTION_SIZE = POPULATION_SIZE
TOURNAMENT_SIZE = 10
SELECTION = SelectionType.TOURNAMENT
CROSSOVER = CrossoverType.UNIFORM
MUTATION = MutationType.UNIFORM
MAX_NOISE_SIZE = 0.2
MAX_GENERATION = 500

MULTIPLYING_FACTOR = -1
RESTRICTION_DOMIAN_PENALTY = 25000


def objective_function(p_min, p, a, b, c, e, f):
    return (a * math.pow(p, 2)) + (b * p) + c + abs(e * math.sin(f * (p_min - p)))


generating_units_variables = [
    {a: 0.00028, b: 8.10, c: 550, e: 300, f: 0.035},
    {a: 0.00056, b: 8.10, c: 309, e: 200, f: 0.042},
    {a: 0.00056, b: 8.10, c: 307, e: 150, f: 0.042},
    {a: 0.00324, b: 7.74, c: 240, e: 150, f: 0.063},
    {a: 0.00324, b: 7.74, c: 240, e: 150, f: 0.063},
    {a: 0.00324, b: 7.74, c: 240, e: 150, f: 0.063},
    {a: 0.00324, b: 7.74, c: 240, e: 150, f: 0.063},
    {a: 0.00324, b: 7.74, c: 240, e: 150, f: 0.063},
    {a: 0.00324, b: 7.74, c: 240, e: 150, f: 0.063},
    {a: 0.00284, b: 8.60, c: 126, e: 100, f: 0.084},
    {a: 0.00284, b: 8.60, c: 126, e: 100, f: 0.084},
    {a: 0.00284, b: 8.60, c: 126, e: 100, f: 0.084},
    {a: 0.00284, b: 8.60, c: 126, e: 100, f: 0.084},
]


restrictions_domains = [
    {p_min: 0, p_max: 680},
    {p_min: 0, p_max: 360},
    {p_min: 0, p_max: 360},
    {p_min: 60, p_max: 180},
    {p_min: 60, p_max: 180},
    {p_min: 60, p_max: 180},
    {p_min: 60, p_max: 180},
    {p_min: 60, p_max: 180},
    {p_min: 60, p_max: 180},
    {p_min: 40, p_max: 120},
    {p_min: 40, p_max: 120},
    {p_min: 55, p_max: 120},
    {p_min: 55, p_max: 120},
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
    for i in len(range(generating_units)):
        penalty += restriction_domain(i, generating_units[i])

    if penalty > 0:
        return None, None

    objective_function_values = []
    for i in len(range(generating_units)):
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
        objective_function_values,
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
    df_data = []

    generation = generate_initial_generation(individual_generation, POPULATION_SIZE)
    evaluate_population(generation.population)
    for i in range(len(generation.population)):
        while generation.population[i].fitness is None:
            generation.population[i] = individual_generation(gen=generation.number)
            evaluate_individual(generation.population[i])

    if debug:
        generation.print_stats()
    generation.evaluate_stats()
    stats_data = generation.stats
    stats_data["gen"] = generation.number
    stats_data["best"] = "{}".format(stats_data["best"])
    df_data.append(stats_data)

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
        stats_data = generation.stats
        stats_data["gen"] = generation.number
        stats_data["best"] = "{}".format(stats_data["best"])
        df_data.append(stats_data)

        if generation.number == MAX_GENERATION:
            break

    df = pd.DataFrame(df_data)
    df.to_json(
        "./results/2_a/run_{}_{}.json".format(
            run_index, datetime.datetime.now().isoformat()
        )
    )


# EXECUCOES
for i in range(30):
    print("Run {}".format(i))
    run(i)