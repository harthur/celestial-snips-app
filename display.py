from sense_hat import SenseHat
import math


class SenseDisplay:
    """Interacts with the LED display on the Raspberry Pi Sense HAT
    
    Methods for displaying direction pixels and moon phase images, as well as
    clearing the display.
    """

    size = 8
    on_color = (0, 0, 255)  # blue

    def __init__(self):
        self.sense = SenseHat()

    def display_direction(self, degrees=0):
        """Take the cardinal direction in degrees and light up a pixel in that direction."""

        # Hard code North, as magnetometer calibration didn't work.
        # TODO: Adjust direction to the current orientation of the HAT
        # using sense.get_compass() and calibrating with RTIMULibCal
        north = 0
        adjusted_degrees = 180 - (int(degrees) + north) % 360
        radians = math.radians(adjusted_degrees)

        # Pretend there's a circle on the grid, and light up the LED on the edge
        # of the circle in the direction we want to "point" to.
        x = math.floor(math.sin(radians) * (self.size / 2 - 0.001) + self.size / 2)
        y = math.floor(math.cos(radians) * (self.size / 2 - 0.001) + self.size / 2)

        self.sense.clear()
        self.sense.set_pixel(int(x), int(y), self.on_color)

    def display_moon_phase(self, phase_info):
        """Display an image of the moon at the given phase."""

        (trend, _, illumination) = phase_info

        percent = round(illumination * 10) * 10

        if percent == 100:
            img_fname = "full100.png"
        elif percent == 0:
            img_fname = "new0.png"
        else:
            img_fname = "%s%s.png" % (trend, percent)

        # The full white is too bright
        self.sense.low_light = True

        self.sense.load_image("phase-images/%s" % img_fname)

    def clear_display(self):
        """Turn off all of the LEDs off the display"""
        self.sense.clear()
