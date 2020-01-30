import urllib.request
import xmltodict
import arrow
import re


class ISS:
    """Class for getting ISS sightings -- hardcoded for Virginia"""

    RSS_URL = "https://spotthestation.nasa.gov/sightings/xml_files/United_States_Virginia_Charlottesville.xml"

    MIN_DURATION_MINS = 4

    MIN_ALT_DEGREES = 40

    def __init__(self):
        pass

    def get_next_sighting(self, start_dt):
        """Get the next "good" ISS sighting after the given start time"""
        rss_str = self._get_sightings_rss()

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

    def _get_sightings_rss(self):
        with urllib.request.urlopen(self.RSS_URL) as resp:
            xml = resp.read()
            return xml

    def _parse_sighting(self, str):
        lines = str.split("<br/>")
        pairs = [line.strip().split(":", 1) for line in lines if line]
        sighting = {name: value.strip() for name, value in pairs}

        # Parse bespoke time string, which looks like: "Monday Jan 20, 2020 6:34 PM"
        time_str = sighting["Date"] + " " + sighting["Time"]
        time = arrow.get(time_str, "dddd MMM D, YYYY h:mm A", tzinfo="US/Eastern")
        dt = time.to("utc").naive

        duration = int(re.search("\d+", sighting["Duration"]).group(0))
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

