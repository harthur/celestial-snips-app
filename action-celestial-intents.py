#!/usr/bin/env python3.5

from hermes_python.hermes import Hermes
from display import SenseDisplay
from celestial import Celestial
from strings import CelestialStrings
import datetime

import os
import pwd

# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_CONFIDENCE_THRESHOLD = 0.45


class CelestialApp:
    """
    Handlers for intents for a "Celestial" Snips voice assistant
    Reports Moon, Sun etc. rising and setting times as well as cardinal directions.
    And the current moon phase
    """

    def __init__(self):
        self.display = SenseDisplay()
        self.celestial = Celestial()

        # Start listening to MQTT
        # Must be last. Anything after this line won't be reached!
        self.start_blocking()

    def moonrise_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "moon", "rise")

    def moonset_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "moon", "set")

    def sunrise_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "sun", "rise")

    def sunset_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "sun", "set")

    def venus_rise_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "venus", "rise")

    def venus_set_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "venus", "set")

    def mars_rise_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "mars", "rise")

    def mars_set_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "mars", "set")

    def jupiter_rise_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "jupiter", "rise")

    def jupiter_set_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "jupiter", "set")

    def orion_rise_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "orion", "rise")

    def orion_set_callback(self, hermes, intent_message):
        self.handle_event_intent(hermes, intent_message, "orion", "set")

    def moon_phase_callback(self, hermes, intent_message):
        if intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD:
            return

        phase_info = self.celestial.get_moon_phase()

        self.display.display_moon_phase(phase_info)

        msg = CelestialStrings.get_moon_phase_message(phase_info)
        hermes.publish_end_session(intent_message.session_id, msg)

    def full_moon_callback(self, hermes, intent_message):
        self.handle_next_moon_event_intent(hermes, intent_message, "full")

    def new_moon_callback(self, hermes, intent_message):
        self.handle_next_moon_event_intent(hermes, intent_message, "new")

    def handle_next_moon_event_intent(self, hermes, intent_message, event):
        if intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD:
            return
        self.display.clear_display()

        now = datetime.datetime.now()
        event_dt = self.celestial.get_next_moon_event(event, start_dt=now)
        msg = CelestialStrings.get_next_moon_event_message(event, event_dt)
        hermes.publish_end_session(intent_message.session_id, msg)

    def clear_display_callback(self, hermes, intent_message):
        if intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD:
            return

        self.display.clear_display()

        hermes.publish_end_session(intent_message.session_id, "")

    def handle_event_intent(self, hermes, intent_message, body, event):
        """Handle an "event" intent: rise or set of a celestial body"""
        if intent_message.intent.confidence_score < INTENT_CONFIDENCE_THRESHOLD:
            return

        event_info = self.celestial.get_next_event(body, event)
        (event_dt, azimuth) = event_info

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
            ).subscribe_intent(
                "harthur:VenusRise", self.venus_rise_callback
            ).subscribe_intent(
                "harthur:VenusSet", self.venus_set_callback
            ).subscribe_intent(
                "harthur:MarsRise", self.mars_rise_callback
            ).subscribe_intent(
                "harthur:MarsSet", self.mars_set_callback
            ).subscribe_intent(
                "harthur:JupiterRise", self.jupiter_rise_callback
            ).subscribe_intent(
                "harthur:JupiterSet", self.jupiter_set_callback
            ).subscribe_intent(
                "harthur:OrionRise", self.orion_rise_callback
            ).subscribe_intent(
                "harthur:OrionSet", self.orion_set_callback
            ).subscribe_intent(
                "harthur:MoonPhase", self.moon_phase_callback
            ).subscribe_intent(
                "harthur:FullMoon", self.full_moon_callback
            ).subscribe_intent(
                "harthur:NewMoon", self.new_moon_callback
            ).subscribe_intent(
                "harthur:ClearDisplay", self.clear_display_callback
            ).loop_forever()


if __name__ == "__main__":
    CelestialApp()
