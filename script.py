# from meta_tp2.ga import Individual
from meta_tp2.selection import tournament
from meta_tp2.selection import roulette
from meta_tp2.ga import Individual

population = []
for i in range(5):
    individual = Individual([i, i + 1])
    individual.fitness = individual.value[0] + individual.value[1]
    population.append(individual)

tournament_result = tournament(population, len(population), 3)
print(len(tournament_result))

roulette_result = roulette(population, len(population))
print(len(roulette_result))
