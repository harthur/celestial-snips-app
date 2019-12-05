#!/usr/bin/env python3.5

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from display import SenseDisplay
from celestial import Celestial

import os
import pwd

CONFIG_INI = "config.ini"

# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_CONFIDENCE_THRESHOLD = 0.65

class CelestialApp:
    """
    Handlers for intents for a "Celestial" Snips voice assistant
    Reports Moon and Sun rising and setting times as well as cardinal directions.
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        self.display = SenseDisplay()
        self.celestial = Celestial()

        # Start listening to MQTT
        # Must be last. Anything after this line won't be reached!
        self.start_blocking()

    def moonrise_callback(self, hermes, intent_message):
        if (intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD):
            return

        (time_str, day_str, azimuth) = self.celestial.get_next_moon_rise_str()

        self.display.display_direction(azimuth)

        msg = "The next moonrise is at %s %s at %s degrees from North"
           % (time_str, day_str, azimuth)

        hermes.publish_end_session(intent_message.session_id, msg)

    @staticmethod
    def moonset_callback(hermes, intent_message):
        if (intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD):
            return

        time_str = self.celestial.get_next_moon_set_str()

        hermes.publish_end_session(intent_message.session_id,
          "The moon will set at %s" % time_str)

    @staticmethod
    def sunrise_callback(hermes, intent_message):
        if (intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD):
            return
        hermes.publish_end_session(intent_message.session_id,
        "The sun will rise at 6:45 AM today")

    @staticmethod
    def sunset_callback(hermes, intent_message):
        if (intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD):
            return
        hermes.publish_end_session(intent_message.session_id,
        "The sun will set at 5:15 PM today")

    # register callback function to its intent and start listen to MQTT bus
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent('harthur:Moonrise', self.moonrise_callback)\
            .subscribe_intent('harthur:Moonset', self.moonset_callback)\
            .subscribe_intent('harthur:Sunrise', self.sunrise_callback)\
            .subscribe_intent('harthur:Sunset', self.sunset_callback)\
            .loop_forever()


if __name__ == "__main__":
    CelestialApp()
