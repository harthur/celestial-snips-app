import urllib


class SpotTheStation:
    """Class for interacting with spotthestation.gov which provides an RSS of ISS sightings
    
    This class is hard-coded to provide info for Virginia.
    """

    RSS_URL = "https://spotthestation.nasa.gov/sightings/xml_files/United_States_Virginia_Charlottesville.xml"

    def __init__(self):
        pass

    @staticmethod
    def get_sightings_rss():
        """Get the XML text of the RSS feed for spotthestation.gov"""
        with urllib.request.urlopen(SpotTheStation.RSS_URL) as resp:
            xml = resp.read()
            return xml
