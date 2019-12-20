import unittest
from datetime import datetime
from celestial import Celestial


class TestCelestial(unittest.TestCase):
    """Testing the Celestial class for getting sun/moon rise and set dates"""

    def setUp(self):
        self.celestial = Celestial()

    def test_get_next_event_after_dt_moon_rise_same_day(self):
        start_dt = datetime(2019, 12, 2, 0, 0, 0, tzinfo=Celestial.ET_TZ)
        event_dt = datetime(2019, 12, 2, 12, 15, 0, tzinfo=Celestial.ET_TZ)
        expected = (event_dt, False, 112)

        self.assertEqual(
            self.celestial.get_next_event_after_dt(start_dt, "moon", "rise"), expected
        )
