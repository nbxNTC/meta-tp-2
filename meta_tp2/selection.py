import random

def tournament(population, selection_size, tournament_size):
  if len(population) == 0: return []
  tournament_result = []

  for i in range(selection_size):
    random_selection = random.sample(population, k=tournament_size)

    best = random_selection[0]
    for individual in random_selection:
        if individual.fitness > best.fitness:
            best = individual
    tournament_result.append(best)

  return tournament_result

def roulette(population, selection_size):
    population_fitness_sum = 0
    for individual in population:
        population_fitness_sum += individual.fitness

    roulette_result = []

    for i in range(selection_size):
        random_value = random.uniform(0, population_fitness_sum)

        iteration_fitness_sum = 0
        for individual in population:
            iteration_fitness_sum += individual.fitness
            if iteration_fitness_sum >= random_value:
                roulette_result.append(individual)
                break

    return roulette_result
