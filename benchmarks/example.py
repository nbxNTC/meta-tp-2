import random
from meta_tp2.ga import Individual
from meta_tp2.selection import SelectionType
from meta_tp2.crossover import CrossoverType


#
# Minimizar x^2 sujeito a x * 3 > 2 e x / 5 < 2
# Dominio x em [0, 20]
#

# Parâmetros
POPULATION_SIZE = 200
CROSSOVER_RATE = 0.9
SELECTION = SelectionType.TOURNAMENT
CROSSOVER = CrossoverType.UNIFORM


def individual_generation():
    return Individual(
        [
            # 0 <= X <= 20
            random.uniform(0, 20)
        ]
    )
