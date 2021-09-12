import random
import math
from meta_tp2.ga import Individual, generate_initial_generation
from meta_tp2.selection import SelectionType
from meta_tp2.crossover import CrossoverType
from meta_tp2.mutation import MutationType

#
# Minimizar x^2 sujeito a x * 3 > 2 e x / 5 < 0,2
# Dominio x em [0, 20]
#

# Need to maximize = 1 / Need to minimize = -1
MULTIPLYING_FACTOR = 1
RESTRICTION_01_PENALTY = 10
RESTRICTION_02_PENALTY = 10

def fitness(x):
  penalty = 0
  if ((x * 3) <= 2): penalty += RESTRICTION_01_PENALTY
  if ((x / 5) >= 0.2): penalty += RESTRICTION_01_PENALTY
  return (MULTIPLYING_FACTOR * math.pow(x, 2)) - penalty

# Parâmetros
POPULATION_SIZE = 200
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.05
SELECTION_SIZE = POPULATION_SIZE
TOURNAMENT_SIZE = 5
SELECTION = SelectionType.TOURNAMENT
CROSSOVER = CrossoverType.UNIFORM
MUTATION = MutationType.UNIFORM
MAX_NOISE_SIZE = 0.1
MAX_GENERATION = 100

def individual_generation():
  return Individual(
    [
      # 0 <= X <= 20
      random.uniform(0, 20)
    ]
  )

def evaluate_population(population):
  for individual in population:
    individual.fitness = fitness(individual.value[0])

def get_best_fitness(population):
  new_best_fitness = population[0].fitness
  for individual in population:
    if (individual.fitness > new_best_fitness):
      new_best_fitness = individual.fitness

generation = generate_initial_generation(individual_generation, POPULATION_SIZE)
evaluate_population(generation.population)
best_fitness = get_best_fitness(generation.population)

while (True):
  selected = SELECTION(generation.population, SELECTION_SIZE, TOURNAMENT_SIZE)

  offspring = []
  for individual_01, individual_02 in zip(selected[0::2], selected[1::2]):
    if random.uniform(0, 1) < CROSSOVER_RATE:
      children_01, children_02 = CROSSOVER(individual_01, individual_02)
      offspring.append(children_01)
      offspring.append(children_02)
    else:
      offspring.append(individual_01)
      offspring.append(individual_02)

  for individual in offspring:
    if random.uniform(0, 1) < MUTATION_RATE:
      individual = MUTATION(individual, MAX_NOISE_SIZE)

  evaluate_population(offspring)
  generation = Generation(generation.number + 1, offspring)
  offspring_best_fitness = get_best_fitness(generation.population)

  if (generation.number == MAX_GENERATION): break
