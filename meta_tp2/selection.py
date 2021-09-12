import random
from enum import Enum


def tournament(population, selectionSize, tournamentSize):
    tournamentResult = []

    for i in range(selectionSize):
        randomSelection = random.sample(population, k=tournamentSize)

        best = randomSelection[0]
        for individual in randomSelection:
            if individual.fitness < best.fitness:
                best = individual
        tournamentResult.append(best)

    return tournamentResult


def roulette(population, selectionSize):
    populationFitnessSum = 0
    for individual in population:
        populationFitnessSum += individual.fitness

    rouletteResult = []

    for i in range(selectionSize):
        randomValue = random.uniform(0, populationFitnessSum)

        iterationFitnessSum = 0
        for individual in population:
            iterationFitnessSum += individual.fitness
            if iterationFitnessSum >= randomValue:
                rouletteResult.append(individual)
                break

    return rouletteResult


class SelectionType(Enum):
    TOURNAMENT = tournament
    ROULETTE = roulette
