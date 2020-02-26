import unittest
from datetime import datetime
from iss import ISS


class TestCelestial(unittest.TestCase):
    """Testing the ISS class for getting next ISS sightings"""

    def setUp(self):
        self.iss = ISS()

    def test_get_next_sighting(self):
        # TODO: mock the RSS feed of spotthestation

        start_dt = datetime(2019, 12, 2, 0, 0, 0)

        expected = {
            "alt_degrees": 66,
            "approach_dir": "NW",
            "depart_dir": "SE",
            "duration_mins": 6,
            "time": datetime(2020, 2, 7, 23, 51),
        }

        self.assertEqual(self.iss.get_next_sighting(start_dt), expected)
