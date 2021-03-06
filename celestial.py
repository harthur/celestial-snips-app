import datetime
import json
from pathlib import Path
import astropy.units as u
from astroplan import Observer
from astropy.time import Time
from astroplan import moon


class Celestial:
    """Provides information about celestial sightings relative to Virginia.

    Methods:
     - get_next_event_after_dt: Get next rise or set of a given celestial body.
     - get_next_moon_event: Get next full or new moon.
     - get_moon_phase: Get the current moon phase.
    """

    BODIES = ["moon", "sun", "venus", "mars", "jupiter", "orion"]

    MOON_EVENTS = ["full", "new"]

    def __init__(self):
        dirname = Path(__file__).parent

        self.charts = {}
        for body in self.BODIES:
            fname = dirname / ("charts/%s-va.json" % body)
            with open(fname) as f:
                self.charts[body] = json.loads(f.read())

        self.moon_charts = {}
        for event in self.MOON_EVENTS:
            fname = dirname / ("charts/%s-moon.json" % event)
            with open(fname) as f:
                self.moon_charts[event] = json.loads(f.read())

    @staticmethod
    def _get_datetime_from_iso(str):
        return datetime.datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_next_event(self, body="moon", event="rise"):
        now_dt = datetime.datetime.now()

        return self.get_next_event_after_dt(now_dt, body, event)

    def get_next_event_after_dt(self, start_dt, body="moon", event="rise"):
        """Get the next rise/set after a given time.

        Fetches date by searching the chart of rise/set times as obtained from
        the US Naval Observatory at https://aa.usno.navy.mil.
        """
        # Other methods, such as using astropy's astroplan, were too slow.

        for day in self.charts[body]:
            if not event in day:
                continue  # no rise/set that day

            event_dt = self._get_datetime_from_iso(day[event]["time"])

            # Found the first event after the current time.
            # Assumes sequential order in the chart
            if event_dt > start_dt:
                azimuth = day[event]["azimuth"]

                return (event_dt, azimuth)

    def get_next_moon_event(self, event, start_dt):
        """Get the time of the next new or full moon after the given date."""
        for date in self.moon_charts[event]:
            event_dt = self._get_datetime_from_iso(date)
            # Assume cronological order in list
            if event_dt > start_dt:
                return event_dt

    def get_moon_phase(self):
        """Get the current moon phase and waxing/waning information."""
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
