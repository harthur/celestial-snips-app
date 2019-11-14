import astropy.units as u
from astroplan import Observer
from astropy.time import Time
import json
import datetime

ET_TZ = datetime.timezone(datetime.timedelta(hours=5))

def get_datetime_from_iso(str):
    return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ')

def get_next_moon_rise_str():
    return "8:35PM"

def get_next_moon_set_str():
    with open('moon-nyc.json') as f:
        chart = json.loads(f.read())
        now_dt = datetime.datetime.now(tz=ET_TZ)
        
        for day in chart:
            if not 'set' in day:
                continue

            [hour, minute] = day['set']['time'].split(':')
        
            dt = get_datetime_from_iso(day['date'])
            set_dt = datetime.datetime(dt.year, dt.month, dt.day,
                int(hour), int(minute), tzinfo=ET_TZ)
            
            # Found the first moonset after the current time.
            # Assumes sequential order in the file
            if set_dt > now_dt:
                return set_dt.strftime("%I:%M%p")
