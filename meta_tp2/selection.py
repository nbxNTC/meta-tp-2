import random

def tournament(population, tournamentSize):
  tournamentResult = []

  for i in range(len(population)):
    randomSelection = random.sample(population, k=tournamentSize)
    print(randomSelection)
    tournamentResult.append(min(randomSelection))

  print(tournamentResult)
  return tournamentResult
