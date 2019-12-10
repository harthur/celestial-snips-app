class CelestialStrings:
  """Construct voice messages for Celestial app using data"""

    @staticmethod
    def get_time_str(dt):
        return dt.strftime("%I:%M%p")

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
    def get_day_str(is_tomorrow):
        return "tomorrow" if is_tomorrow else "today"

    @staticmethod
    def get_event_message(body, event, event_info):
        (dt, is_tomorrow, azimuth) = event_info

        time_str = CelestialStrings.get_time_str(dt)
        day_str = CelestialStrings.get_day_str(is_tomorrow)
        dir_str = CelestialStrings.get_cardinal_str(azimuth)

        return "The next %s%s is at %s %s, in the %s" % (body, event, time_str, day_str, dir_str)

