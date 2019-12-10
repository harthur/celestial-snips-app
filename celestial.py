import astropy.units as u
from astroplan import Observer
from astropy.time import Time
import json
import datetime


class Celestial:
    """Getting moon and sun rise and set times from hard-coded charts for Virginia"""

    CHART_FNAMES = {"moon": "./charts/moon-nyc.json", "sun": "./charts/sun-nyc.json"}
    ET_TZ = datetime.timezone(datetime.timedelta(hours=-5))

    def __init__(self):
        self.charts = {}

        with open(Celestial.MOON_FNAME) as f:
            self.charts["moon"] = json.loads(f.read())
        with open(Celestial.SUN_FNAME) as f:
            self.charts["sun"] = json.loads(f.read())

    @staticmethod
    def get_datetime_from_iso(str):
        return datetime.datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_next_event(self, body="moon", event="rise"):
        now_dt = datetime.datetime.now(tz=Celestial.ET_TZ)

        for day in self.charts[body]:
            if not event in day:
                continue  # no rise/set that day

            [hour, minute] = day[event]["time"].split(":")

            dt = self.get_datetime_from_iso(day["date"])
            event_dt = datetime.datetime(
                dt.year,
                dt.month,
                dt.day,
                int(hour),
                int(minute),
                tzinfo=Celestial.ET_TZ,
            )

            # Found the first event after the current time.
            # Assumes sequential order in the time file
            if event_dt > now_dt:
                is_tomorrow = event_dt.date() > now_dt.date()
                azimuth = day[event]["azimuth"]

                return (event_dt, is_tomorrow, azimuth)
