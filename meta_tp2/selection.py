import random

def tournament(population, tournamentSize):
  tournamentResult = []

  for i in range(len(population)):
    randomSelection = random.sample(population, k=tournamentSize)

    best = randomSelection[0]
    for individual in randomSelection:
        if individual.fitness < best.fitness:
            best = individual
    tournamentResult.append(best)

  return tournamentResult
