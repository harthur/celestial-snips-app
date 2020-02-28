import re

import arrow
import xmltodict

from spotthestation import SpotTheStation


class ISS:
    """Provides information about upcoming ISS sightings from Virginia."""

    MIN_DURATION_MINS = 4

    MIN_ALT_DEGREES = 40

    def __init__(self, iss_feed_provider=None):
        if iss_feed_provider is None:
            self.iss_feed_provider = SpotTheStation()
        else:
            self.iss_feed_provider = iss_feed_provider

    def get_next_sighting(self, start_dt):
        """Get the next "good" ISS sighting after the given start time"""
        rss_str = self.iss_feed_provider.get_sightings_rss()

        rss_data = xmltodict.parse(rss_str)
        items = rss_data["rss"]["channel"]["item"]

        for item in items:
            content = item["description"]
            sighting = self._parse_sighting(content)

            if (
                sighting["time"] > start_dt
                and sighting["duration_mins"] > self.MIN_DURATION_MINS
                and sighting["alt_degrees"] > self.MIN_ALT_DEGREES
            ):
                return sighting

    def _parse_sighting(self, str):
        """Extract single sighting info from a spotthestation.gov RSS XML string"""

        # Example sighting text:
        # "Date: Wednesday Mar 4, 2020 <br/> Time: 6:19 AM <br/>
        # Duration: 1 minute <br/> Maximum Elevation: 10° <br/>
        # Approach: 10° above N <br/> Departure: 10° above NNE <br/>"

        lines = str.split("<br/>")
        pairs = [line.strip().split(":", 1) for line in lines if line]
        sighting = {name: value.strip() for name, value in pairs}

        # Parse their time string, which looks like "Monday Jan 20, 2020 6:34 PM"
        time_str = sighting["Date"] + " " + sighting["Time"]
        time = arrow.get(time_str, "dddd MMM D, YYYY h:mm A", tzinfo="US/Eastern")
        dt = time.to("utc").naive

        duration = int(re.search(r"\d+", sighting["Duration"]).group(0))
        elevation = int(sighting["Maximum Elevation"].strip("°"))
        approach_dir = sighting["Approach"].split(" ")[-1]
        depart_dir = sighting["Departure"].split(" ")[-1]

        return {
            "time": dt,
            "duration_mins": duration,
            "alt_degrees": elevation,
            "approach_dir": approach_dir,
            "depart_dir": depart_dir,
        }
