import random
import copy

def uniform(individual_1, individual_2):
  children_01, children_02 = Individual(), Individual()

  for i in range(len(individual_1.value)):
    if (random.uniform(0, 1) <= 0.5):
      children_01.value[i] = individual_1.value[i]
      children_02.value[i] = individual_2.value[i]
    else:
      children_01.value[i] = individual_2.value[i]
      children_02.value[i] = individual_1.value[i]
  return children_01, children_02

def one_point(individual_1, individual_2):
  children_01, children_02 = copy.copy(individual_1), copy.copy(individual_2)

  cutIndex = random.randint(1, len(individual_1.value) - 1)

  children_01[cutIndex:], children_02[cutIndex:] = individual_2[cutIndex:], individual_1[cutIndex:]
  return children_01, children_02
