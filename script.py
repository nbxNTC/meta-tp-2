# from meta_tp2.ga import Individual
from meta_tp2.selection import tournament
from meta_tp2.selection import roulette
from meta_tp2.ga import Individual

population = []
for i in range(5):
    individual = Individual([i, i + 1])
    individual.fitness = individual.value[0] + individual.value[1]
    population.append(individual)

tournamentResult = tournament(population, len(population))
print(len(tournamentResult))

rouletteResult = roulette(population, len(population))
print(len(rouletteResult))
