import unittest

# from celestial import Celestial
import pytest
from hypothesis import strategies, given
import math
from decimal import Decimal


def squared(x):
    return x ** 2


def sqrt(x):
    return x ** 0.5


class TestCelestial(unittest.TestCase):
    """Testing the Celestial class for moon and sunrise times"""

    def setUp(self):
        ...
        # self.celest = Celestial()

    def test_get_cardinal_str(self):
        input = 0
        expected = "north"

        self.assertEqual(1, 1, "one equals two")
        self.assertAlmostEqual()
        # self.assertEqual(Celestial.get_cardinal_str(input), expected, '0 degrees is North')


@given(strategies.integers(1))
def test_add_subtract(n):
    assert squared(sqrt(n)) == n


if __name__ == "__main__":
    unittest.main()
