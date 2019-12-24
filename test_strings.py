import unittest

from celestial import Celestial
from strings import CelestialStrings
from datetime import datetime
import pytest
import math


class TestCelestial(unittest.TestCase):
    """Testing the CelestialStrings class for generating celestial answers for TTS to read aloud"""

    def setUp(self):
        ...

    def test_get_local_time_str(self):
        input = datetime(2019, 12, 1, 13, 24, 0, 0)
        expected = "08:24AM"

        self.assertEqual(CelestialStrings.get_local_time_str(input), expected)

    def test_get_cardinal_str(self):
        self.assertEqual(
            CelestialStrings.get_cardinal_str(0), "north", "0 degrees is North"
        )
        self.assertEqual(
            CelestialStrings.get_cardinal_str(50),
            "north northeast",
            "50 degrees is NNE",
        )
        self.assertEqual(
            CelestialStrings.get_cardinal_str(88), "east", "88 degrees is East"
        )
        self.assertEqual(
            CelestialStrings.get_cardinal_str(180), "south", "180 degrees is South"
        )
        self.assertEqual(
            CelestialStrings.get_cardinal_str(350), "north", "350 degrees is North"
        )

    def test_get_event_message(self):
        body = "moon"
        event = "rise"
        dt = datetime(2019, 12, 1, 13, 24, 0, 0)
        event_info = (dt, True, 120)

        self.assertEqual(
            CelestialStrings.get_event_message(body, event, event_info),
            "The next moon rise is at 08:24AM tomorrow, in the south southeast",
        )

    def test_get_moon_phase_message(self):
        phase_info = ("waning", "crescent", 10)

        self.assertEqual(
            CelestialStrings.get_moon_phase_message(phase_info),
            "The moon is a waning crescent",
        )
