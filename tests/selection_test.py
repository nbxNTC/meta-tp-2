from meta_tp2.ga import Individual
from meta_tp2.selection import tournament
from tests import *
from unittest import TestCase

import pytest
import random

# def generateRandomValue():
#     return [random.uniform(0, 10) for _i in range(2)]

# random_population = [Individual(generateRandomValue()) for _i in range(10)]


class TestGA(TestCase):
    def test_tournament_returns_empty_if_population_empty(self):
        # ind = Individual()
        pop = []
        tourn_result = tournament([], 5)
        self.assertEqual(tourn_result, [])

    def test_tournament_raises_if_tourn_size_greater_than_pop_size(self):
        # ind = Individual()
        pop = [Individual(), Individual(), Individual()]
        with self.assertRaises(ValueError) as e:
            tournament(pop, 4)
            self.assertEqual(str(e), "Sample larger than population or is negative")
