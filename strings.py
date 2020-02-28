import datetime
import pytz


class CelestialStrings:
    """Constructs different voice response messages for the Celestial app"""

    # Assume all times are said in local time for the ET timezone
    ET_TZ = pytz.timezone("US/Eastern")

    def __init__(self):
        pass

    @staticmethod
    def _get_local_time_str(dt):
        """Get a string for the US/Eastern wall time given a datetime object."""
        utc_dt = pytz.utc.localize(dt)
        et_dt = utc_dt.astimezone(CelestialStrings.ET_TZ)

        return et_dt.strftime("%I:%M%p")

    @staticmethod
    def _get_cardinal_str(degrees):
        """Get cardinal direction string from azimuth angle."""
        cardinals = [
            "north",
            "northeast",
            "east",
            "southeast",
            "south",
            "southwest",
            "west",
            "northwest",
        ]
        per_cardinal = 360 / len(cardinals)

        # shift to accomodate north being in the range 337.5 - 360 and 0 - 22.5
        index = round(degrees % (360 - per_cardinal / 2) / per_cardinal)
        return cardinals[index]

    @staticmethod
    def _get_cardinal_str_from_abbr(abbr):
        """Get cardinal direction string from its abbreviation."""

        full_str = {
            "N": "north",
            "NE": "northeast",
            "NNE": "north northeast",
            "E": "east",
            "SE": "southeast",
            "SSE": "south southeast",
            "S": "south",
            "SW": "southwest",
            "SSW": "south southwest",
            "W": "west",
            "NW": "northwest",
            "NNW": "north northwest",
        }
        return full_str[abbr]

    @staticmethod
    def _get_day_str(start_dt, event_dt):
        """Get a colloquial string for how this day relates to a start date.
        
        e.g. if the `start_dt` is the same day as the `event_dt`, returns "today"
        """

        local_start = pytz.utc.localize(start_dt).astimezone(CelestialStrings.ET_TZ)
        local_event = pytz.utc.localize(event_dt).astimezone(CelestialStrings.ET_TZ)

        if local_event.date() == local_start.date():
            return "today"

        if (local_event.date() - local_start.date()) == datetime.timedelta(days=1):
            return "tomorrow"

        return local_event.strftime("%A, %B %d")

    @staticmethod
    def get_event_message(body, event, event_info):
        """Get a string announcing the next rise or set for a body."""
        (dt, azimuth) = event_info

        now = datetime.datetime.now()
        day_str = CelestialStrings._get_day_str(now, dt)
        time_str = CelestialStrings._get_local_time_str(dt)
        dir_str = CelestialStrings._get_cardinal_str(azimuth)

        event_str = (
            body + event if body == "moon" or body == "sun" else body + " " + event
        )

        return "The next %s is at %s %s, in the %s" % (
            event_str,
            time_str,
            day_str,
            dir_str,
        )

    @staticmethod
    def get_moon_phase_message(phase_info):
        """Get a string announcing the moon phase, based on the given info."""
        (trend, phase, _) = phase_info

        if phase == "full":
            return "It's a full moon today"
        if phase == "new":
            return "It's a new moon today"
        if phase == "quarter" and trend == "waxing":
            return "First quarter"
        if phase == "quarter" and trend == "waning":
            return "Last quarter"
        return "The moon is a %s %s" % (trend, phase)

    @staticmethod
    def get_next_moon_event_message(event, event_dt):
        """Get a string announcing the next full or new moon, given a date"""

        now = datetime.datetime.now()
        day_str = CelestialStrings._get_day_str(now, event_dt)
        time_str = CelestialStrings._get_local_time_str(event_dt)
        return "The next %s moon is on %s, at %s" % (event, day_str, time_str)

    @staticmethod
    def get_next_iss_sighting_message(sighting):
        """Get a string announcing next ISS sighting from an ISS sighting object"""

        dt = sighting["time"]
        now = datetime.datetime.now()
        day_str = CelestialStrings._get_day_str(now, dt)
        time_str = CelestialStrings._get_local_time_str(dt)
        from_dir = CelestialStrings._get_cardinal_str_from_abbr(
            sighting["approach_dir"]
        )
        to_dir = CelestialStrings._get_cardinal_str_from_abbr(sighting["depart_dir"])

        return (
            "You can see the space station %s at %s, moving from the %s to the %s"
            % (day_str, time_str, from_dir, to_dir)
        )
