import datetime
import pytz


class CelestialStrings:
    """Construct voice response messages for the Celestial app"""

    # Assume all times are said in local time for the ET timezone
    ET_TZ = pytz.timezone("US/Eastern")

    def __init__(self):
        pass

    @staticmethod
    def get_local_time_str(dt):
        # Say the time in their local time (assumed to be Eastern/US)
        utc_dt = pytz.utc.localize(dt)
        et_dt = utc_dt.astimezone(CelestialStrings.ET_TZ)

        return et_dt.strftime("%I:%M%p")

    @staticmethod
    def get_cardinal_str(degrees):
        cardinals = [
            "north",
            "north northeast",
            "east",
            "south southeast",
            "south",
            "south southwest",
            "west",
            "north northwest",
        ]
        per_cardinal = 360 / len(cardinals)

        # shift to accomodate north being in the range 337.5 - 360 and 0 - 22.5
        index = round(degrees % (360 - per_cardinal / 2) / per_cardinal)
        return cardinals[index]

    @staticmethod
    def get_day_str(start_dt, event_dt):
        local_start = pytz.utc.localize(start_dt).astimezone(CelestialStrings.ET_TZ)
        local_event = pytz.utc.localize(event_dt).astimezone(CelestialStrings.ET_TZ)

        if local_event.date() == local_start.date():
            return "today"

        if (local_event.date() - local_start.date()) == datetime.timedelta(days=1):
            return "tomorrow"

        return local_event.strftime("%A, %B %d")

    @staticmethod
    def get_event_message(body, event, event_info):
        (dt, azimuth) = event_info

        now = datetime.datetime.now()
        day_str = CelestialStrings.get_day_str(now, dt)
        time_str = CelestialStrings.get_local_time_str(dt)
        dir_str = CelestialStrings.get_cardinal_str(azimuth)

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
        (trend, phase, illumination) = phase_info

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
        now = datetime.datetime.now()
        day_str = CelestialStrings.get_day_str(now, event_dt)
        time_str = CelestialStrings.get_local_time_str(event_dt)
        return "The next %s moon is on %s, at %s" % (event, day_str, time_str)

