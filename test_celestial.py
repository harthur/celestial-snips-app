import unittest
from datetime import datetime
from celestial import Celestial


class TestCelestial(unittest.TestCase):
    """Testing the Celestial class for getting sun/moon rise and set dates"""

    def setUp(self):
        self.celestial = Celestial()

    def test_get_next_event_after_dt_moon_rise_same_day(self):
        start_dt = datetime(2019, 12, 2, 0, 0, 0)
        event_dt = datetime(2019, 12, 2, 17, 15, 0)
        expected = (event_dt, 112)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "moon", "rise"), expected
        )

    def test_get_next_event_after_dt_moon_rise_next_day(self):
        start_dt = datetime(2019, 12, 2, 18, 0, 0)
        event_dt = datetime(2019, 12, 3, 17, 47, 0)
        expected = (event_dt, 108)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "moon", "rise"), expected
        )

    def test_get_next_event_after_dt_moon_set(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        event_dt = datetime(2019, 12, 3, 3, 45, 0)
        expected = (event_dt, 250)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "moon", "set"), expected
        )

    def test_get_next_event_after_dt_sun_rise(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        event_dt = datetime(2019, 12, 3, 12, 16, 0)
        expected = (event_dt, 118)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "sun", "rise"), expected
        )

    def test_get_next_event_after_dt_sun_set(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        event_dt = datetime(2019, 12, 2, 21, 57, 0)
        expected = (event_dt, 242)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "sun", "set"), expected
        )

    def test_get_next_event_after_dt_venus_rise(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        event_dt = datetime(2019, 12, 2, 14, 29, 0)
        expected = (event_dt, 122)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "venus", "rise"), expected
        )

    def test_get_next_event_after_dt_venus_set(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        event_dt = datetime(2019, 12, 2, 23, 47, 0)
        expected = (event_dt, 238)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "venus", "set"), expected
        )

    def test_get_next_full_moon(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        expected = datetime(2019, 12, 12, 5, 12)

        self.assertEqual(self.celestial.get_next_moon_event("full", start_dt), expected)

    def test_get_next_new_moon(self):
        start_dt = datetime(2019, 12, 2, 13, 0, 0)
        expected = datetime(2019, 12, 26, 5, 13)

        self.assertEqual(self.celestial.get_next_moon_event("new", start_dt), expected)
