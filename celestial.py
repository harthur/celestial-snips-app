import astropy.units as u
from astroplan import Observer
from astropy.time import Time

nyc_observer = Observer(
  longitude=-74.0060*u.deg,
  latitude=40.7128*u.deg,
  elevation=0*u.m,
  name="NYC",
  timezone="US/Eastern"
)

def get_next_moon_rise_str():
    return "08:45PM"
    # rise_time = nyc_observer.moon_rise_time(Time.now(), which='next')
    # dt = nyc_observer.astropy_time_to_datetime(rise_time)
    # return dt.strftime("%I:%M%p")

# altaz = nyc_observer.moon_altaz(moon_rise_time)
# altaz.az