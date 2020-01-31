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
        input = datetime(2019, 12, 1, 13, 24)
        expected = "08:24AM"

        self.assertEqual(CelestialStrings.get_local_time_str(input), expected)

    def test_get_day_str_today(self):
        start_dt = datetime(2019, 12, 1, 0, 0)
        event_dt = datetime(2019, 12, 1, 3, 4)
        expected = "today"
        self.assertEqual(CelestialStrings.get_day_str(start_dt, event_dt), expected)

    def test_get_day_str_tomorrow(self):
        start_dt = datetime(2019, 12, 1, 0, 0)
        event_dt = datetime(2019, 12, 2, 3, 4)
        expected = "tomorrow"
        self.assertEqual(CelestialStrings.get_day_str(start_dt, event_dt), expected)

    def test_get_day_str_next_week(self):
        start_dt = datetime(2019, 12, 1, 0, 0)
        event_dt = datetime(2019, 12, 8, 3, 4)
        expected = "Saturday, December 07"
        self.assertEqual(CelestialStrings.get_day_str(start_dt, event_dt), expected)

    def test_get_cardinal_str(self):
        self.assertEqual(
            CelestialStrings.get_cardinal_str(0), "north", "0 degrees is North"
        )
        self.assertEqual(
            CelestialStrings.get_cardinal_str(50), "northeast", "50 degrees is NE",
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

    def test_get_cardinal_str_from_abbr(self):
        self.assertEqual(CelestialStrings.get_cardinal_str_from_abbr("N"), "north")
        self.assertEqual(
            CelestialStrings.get_cardinal_str_from_abbr("SSE"), "south southeast"
        )

    def test_get_event_message(self):
        body = "moon"
        event = "rise"
        dt = datetime(2019, 12, 1, 13, 24)
        event_info = (dt, 120)

        self.assertEqual(
            CelestialStrings.get_event_message(body, event, event_info),
            "The next moonrise is at 08:24AM Sunday, December 01, in the southeast",
        )

    def test_get_event_message_planet(self):
        body = "venus"
        event = "set"
        dt = datetime(2019, 12, 1, 13, 24)
        event_info = (dt, 120)

        self.assertEqual(
            CelestialStrings.get_event_message(body, event, event_info),
            "The next venus set is at 08:24AM Sunday, December 01, in the southeast",
        )

    def test_get_moon_phase_message(self):
        phase_info = ("waning", "crescent", 10)

        self.assertEqual(
            CelestialStrings.get_moon_phase_message(phase_info),
            "The moon is a waning crescent",
        )

    def test_get_next_moon_event_message(self):
        start_dt = datetime(2019, 12, 1, 0, 0)
        event_dt = datetime(2019, 12, 8, 3, 4)

        expected = "The next full moon is on Saturday, December 07, at 10:04PM"
        self.assertEqual(
            CelestialStrings.get_next_moon_event_message("full", event_dt), expected
        )

    def test_get_next_iss_sighting_message(self):
        sighting = {
            "alt_degrees": 66,
            "approach_dir": "NW",
            "depart_dir": "SE",
            "duration_mins": 6,
            "time": datetime(2020, 2, 7, 23, 51),
        }

        expected = "You can see the space station Friday, February 07 at 06:51PM, moving from the northwest to the southeast"

        self.assertEqual(
            CelestialStrings.get_next_iss_sighting_message(sighting), expected
        )
