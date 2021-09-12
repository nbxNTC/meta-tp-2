from enum import Enum
import random

def uniform(children, max_noise_size):
  random_index = random.randint(0, len(children.value) - 1)

  noise = random.uniform(0, max_noise_size) * children.value[random_index]
  multiplying_factor = random.choice([-1, 1])

  children.value[random_index] += noise * multiplying_factor

  return children

class MutationType(Enum):
    UNIFORM = uniform
