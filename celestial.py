import astropy.units as u
from astroplan import Observer
from astropy.time import Time
import json
import datetime

MOON_FNAME = 'moon-nyc.json'
ET_TZ = datetime.timezone(datetime.timedelta(hours=5))

class Celestial:
    def __init__(self):
        with open(MOON_FNAME) as f:
            self.moon_chart = json.loads(f.read())

    @staticmethod
    def get_datetime_from_iso(str):
        return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_next_moon_event(self, kind='rise'):
        now_dt = datetime.datetime.now(tz=ET_TZ)
            
        for day in self.moon_chart:
            if not kind in day:
                continue # no rise/set that day

            [hour, minute] = day[kind]['time'].split(':')
        
            dt = self.get_datetime_from_iso(day['date'])
            event_dt = datetime.datetime(dt.year, dt.month, dt.day,
                int(hour), int(minute), tzinfo=ET_TZ)
            
            # Found the first event after the current time.
            # Assumes sequential order in the time file
            if event_dt > now_dt:
                azimuth = day[kind]['azimuth']
                return (event_dt, azimuth)

    def get_next_moon_rise_str(self):
        (rise_dt, azimuth) = self.get_next_moon_event('rise')
        return (rise_dt.strftime("%I:%M%p"), azimuth)

    def get_next_moon_set_str(self):
        (set_dt, azimuth) = self.get_next_moon_event('set')
        return (set_dt.strftime("%I:%M%p"), azimuth)
