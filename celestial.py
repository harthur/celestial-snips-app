import astropy.units as u
from astroplan import Observer
from astropy.time import Time
import json
import datetime

class Celestial:
    MOON_FNAME = 'moon-nyc.json'
    SUN_FNAME = 'sun-nyc.json'

    ET_TZ = datetime.timezone(datetime.timedelta(hours=-5))

    def __init__(self):
        with open(Celestial.MOON_FNAME) as f:
            self.moon_chart = json.loads(f.read())
        with open(Celestial.SUN_FNAME) as f:
            self.sun_chart = json.loads(f.read())

    @staticmethod
    def get_datetime_from_iso(str):
        return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def get_time_str(dt):
        return dt.strftime("%I:%M%p")

    @staticmethod
    def get_day_str(is_tomorrow):
        return "tomorrow" if is_tomorrow else "today"

    @staticmethod
    def get_cardinal_str(degrees):
        cardinals = [
            'north',
            'north northeast',
            'east',
            'south southeast',
            'south',
            'south southwest',
            'west',
            'north northwest'
        ]
        per_cardinal = 360 / len(cardinals)

        # shift to accomodate north being in the range 337.5 - 360 and 0 - 22.5
        index = round(degrees % (360 - per_cardinal / 2) / per_cardinal)
        return cardinals[index]

    def get_next_event(self, chart, event='rise'):
        now_dt = datetime.datetime.now(tz=Celestial.ET_TZ)
        print("NOW", now_dt)
            
        for day in chart:
            if not event in day:
                continue # no rise/set that day

            [hour, minute] = day[event]['time'].split(':')
        
            dt = self.get_datetime_from_iso(day['date'])
            event_dt = datetime.datetime(dt.year, dt.month, dt.day,
                int(hour), int(minute), tzinfo=Celestial.ET_TZ)
            
            # Found the first event after the current time.
            # Assumes sequential order in the time file
            if event_dt > now_dt:
                print("FOUND", event_dt)
                is_tomorrow = event_dt.date() > now_dt.date()
                azimuth = day[event]['azimuth']

                return (event_dt, is_tomorrow, azimuth)

    def get_next_moon_event(self, event='rise'):
        return self.get_next_event(self.moon_chart, event)

    def get_next_sun_event(self, event='rise'):
        return self.get_next_event(self.sun_chart, event)

    def get_event_strs(self, event_info):
        (dt, is_tomorrow, azimuth) = event_info

        time_str = self.get_time_str(dt)
        day_str = self.get_day_str(is_tomorrow)
        cardinal_str = self.get_cardinal_str(azimuth)

        return (time_str, day_str, cardinal_str, azimuth)

    def get_next_moon_rise_str(self):
        event_info = self.get_next_moon_event('rise')
        return self.get_event_strs(event_info)

    def get_next_moon_set_str(self):
        event_info = self.get_next_moon_event('set')
        return self.get_event_strs(event_info)

    def get_next_sun_rise_str(self):
        event_info = self.get_next_sun_event('rise')
        return self.get_event_strs(event_info)

    def get_next_sun_set_str(self):
        event_info = self.get_next_sun_event('set')
        return self.get_event_strs(event_info)
