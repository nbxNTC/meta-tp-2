from meta_tp2.ga import Individual
import random
import copy
from enum import Enum


def uniform(individual_1, individual_2):
    children_01, children_02 = Individual(), Individual()

    for i in range(len(individual_1.value)):
        if random.uniform(0, 1) <= 0.5:
            children_01.value[i] = individual_1.value[i]
            children_02.value[i] = individual_2.value[i]
        else:
            children_01.value[i] = individual_2.value[i]
            children_02.value[i] = individual_1.value[i]
    return children_01, children_02


def one_point(individual_1, individual_2):
    children_01, children_02 = copy.copy(individual_1), copy.copy(individual_2)

    cut_index = random.randint(1, len(individual_1.value) - 1)

    children_01[cut_index:], children_02[cut_index:] = (
        individual_2[cut_index:],
        individual_1[cut_index:],
    )
    return children_01, children_02


class CrossoverType(Enum):
    UNIFORM = uniform
    ONE_POINT = one_point
