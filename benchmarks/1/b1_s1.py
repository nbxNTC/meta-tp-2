import random
import math

import numpy as np
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
RESTRICTION_1_PENALTY_FACTOR = 10
RESTRICTION_2_PENALTY_FACTOR = 10


def objective_function(x1, x2):
    return math.pow((x1 - 10), 3) + math.pow((x2 - 20), 3)


def restriction1(x1, x2):
    restriction_value = -math.pow((x1 - 5), 2) - math.pow((x2 - 5), 2) + 100
    return RESTRICTION_1_PENALTY_FACTOR * min(0, restriction_value)


def restriction2(x1, x2):
    restriction_value = math.pow((x1 - 6), 2) + math.pow((x2 - 5), 2) - 82.81
    return RESTRICTION_2_PENALTY_FACTOR * min(0, restriction_value)


def restriction_domain(x1, x2):
    if x1 < 13 or x1 > 100:
        return RESTRICTION_DOMIAN_PENALTY
    if x2 < 0 or x2 > 100:
        return RESTRICTION_DOMIAN_PENALTY

    return 0


def fitness(x1, x2):
    penalty = np.sum(
        [restriction1(x1, x2), restriction2(x1, x2), restriction_domain(x1, x2)]
    )
    if penalty > 0:
        return None, None
    objective_function_value = objective_function(x1, x2)

    return (
        MULTIPLYING_FACTOR * (objective_function_value + penalty),
        objective_function_value,
    )


def individual_generation(gen=0):
    return Individual(
        [
            # 13 <= X1 <= 100
            random.uniform(13, 100),
            # 0 <= X2 <= 100
            random.uniform(0, 100),
        ],
        gen,
    )


def evaluate_individual(individual):
    fit, obj_fun_value = fitness(*individual.value)
    individual.fitness = fit
    individual.objective_function_value = obj_fun_value


def evaluate_population(population):
    for individual in population:
        evaluate_individual(individual)


def get_best_fitness(population):
    new_best_fitness = population[0].fitness
    for individual in population:
        if individual.fitness > new_best_fitness:
            new_best_fitness = individual.fitness


generation = generate_initial_generation(individual_generation, POPULATION_SIZE)
evaluate_population(generation.population)
for i in range(len(generation.population)):
    while generation.population[i].fitness is None:
        generation.population[i] = individual_generation(gen=generation.number)
        evaluate_individual(generation.population[i])


generation.print_stats()

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
    generation.print_stats()

    if generation.number == MAX_GENERATION:
        break
