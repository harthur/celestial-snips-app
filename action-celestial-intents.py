#!/usr/bin/env python3.5

from hermes_python.hermes import Hermes
from display import SenseDisplay
from celestial import Celestial
from strings import CelestialStrings

import os
import pwd

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
        self.display = SenseDisplay()
        self.celestial = Celestial()

        # Start listening to MQTT
        # Must be last. Anything after this line won't be reached!
        self.start_blocking()

    def moonrise_callback(self, hermes, intent_message):
        self.handle_event(hermes, intent_message, "moon", "rise")

    def moonset_callback(self, hermes, intent_message):
        self.handle_event(hermes, intent_message, "moon", "set")

    def sunrise_callback(self, hermes, intent_message):
        self.handle_event(hermes, intent_message, "sun", "rise")

    def sunset_callback(self, hermes, intent_message):
        self.handle_event(hermes, intent_message, "sun", "set")

    def handle_event(self, hermes, intent_message, body, event):
        """Handle an "event" intent: a rise or set of a celestial body"""
        if intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD:
            return

        event_info = self.celestial.get_next_event(body, event)
        (event_dt, is_tomorrow, azimuth) = event_info

        self.display.display_direction(azimuth)

        msg = CelestialStrings.get_event_message(body, event, event_info)
        hermes.publish_end_session(intent_message.session_id, msg)

    # register callback function to its intent and start listen to MQTT bus
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent(
                "harthur:Moonrise", self.moonrise_callback
            ).subscribe_intent(
                "harthur:Moonset", self.moonset_callback
            ).subscribe_intent(
                "harthur:Sunrise", self.sunrise_callback
            ).subscribe_intent(
                "harthur:Sunset", self.sunset_callback
            ).loop_forever()


if __name__ == "__main__":
    CelestialApp()
