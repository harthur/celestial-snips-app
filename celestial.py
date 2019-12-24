import astropy.units as u
from astroplan import Observer
from astropy.time import Time
from astroplan import moon
import json
import datetime


class Celestial:
    """Getting moon and sun rise and set times from hard-coded charts for Virginia"""

    BODIES = ["moon", "sun"]

    def __init__(self):
        self.charts = {}
        for body in self.BODIES:
            fname = "./charts/%s-va.json" % body
            with open(fname) as f:
                self.charts[body] = json.loads(f.read())

    @staticmethod
    def get_datetime_from_iso(str):
        return datetime.datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_next_event(self, body="moon", event="rise"):
        now_dt = datetime.datetime.now()

        return self.get_next_event_after_dt(now_dt, body, event)

    def get_next_event_after_dt(self, start_dt, body="moon", event="rise"):
        """Get the next rise/set by looking up the date in a chart of rise/set
        times as obtained from the US Naval Observatory at https://aa.usno.navy.mil
        Other methods, such as using astropy's astroplan, were too slow."""

        for day in self.charts[body]:
            if not event in day:
                continue  # no rise/set that day

            event_dt = self.get_datetime_from_iso(day[event]["time"])

            # Found the first event after the current time.
            # Assumes sequential order in the time file
            if event_dt > start_dt:
                is_tomorrow = event_dt.date() > start_dt.date()
                azimuth = day[event]["azimuth"]

                return (event_dt, is_tomorrow, azimuth)

    def get_moon_phase(self):
        # These numbers are just guesses.
        phases = {
            "new": (0, 0.005),
            "crescent": (0.005, 0.47),
            "quarter": (0.47, 0.53),
            "gibbous": (0.53, 0.9925),
            "full": (0.9925, 1),
        }
        now_dt = datetime.datetime.now()

        illumination = moon.moon_illumination(Time(now_dt))

        for phase, (lower, upper) in phases.items():
            if lower < illumination <= upper:
                current_phase = phase
                break

        yesterday = Time(now_dt - datetime.timedelta(hours=1))
        trend = (
            "waning" if moon.moon_illumination(yesterday) > illumination else "waxing"
        )

        return (trend, current_phase, illumination)
