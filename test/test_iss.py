import unittest
from datetime import datetime
from pathlib import Path

from iss import ISS
from spotthestation import SpotTheStation
from unittest.mock import Mock


class TestISS(unittest.TestCase):
    """Testing the ISS class for getting next ISS sightings"""

    def setUp(self):
        path = Path(__file__).parent / "iss-feed.xml"
        with open(path, "r") as f:
            feed_xml = f.read()
            self.mock_spotter = Mock(spec=SpotTheStation)
            self.mock_spotter.get_sightings_rss.return_value = feed_xml

    def test_get_next_sighting(self):
        iss = ISS(self.mock_spotter)

        start_dt = datetime(2019, 12, 2, 0, 0, 0)

        expected = {
            "alt_degrees": 73,
            "approach_dir": "SW",
            "depart_dir": "NE",
            "duration_mins": 7,
            "time": datetime(2020, 2, 21, 11, 22),
        }

        self.assertEqual(iss.get_next_sighting(start_dt), expected)
