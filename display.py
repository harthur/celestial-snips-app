from sense_hat import SenseHat
import math


class SenseDisplay:
    """
    Using the LED display on the Sense HAT to display cardinal direction
    arrows and moon phases
    """

    size = 8
    on_color = (0, 0, 255)  # blue

    def __init__(self):
        self.sense = SenseHat()

        # To get good results with the magnetometer you must first calibrate it using
        # the program in RTIMULib/Linux/RTIMULibCal
        # The calibration program will produce the file RTIMULib.ini
        # Copy it into the same folder as your Python code

    def display_direction(self, degrees=0):
        """ 
        Take the cardinal direction in degrees, and display
        an "arrow" on the Sense HAT pointing in that direction.
        """

        # Hard code this, as magnetometer calibration didn't work
        # TODO: Adjust direction to the current orientation of the HAT
        north = 0
        adjusted_degrees = 180 - (int(degrees) + north) % 360

        radians = math.radians(adjusted_degrees)
        x = math.floor(math.sin(radians) * (self.size / 2 - 0.001) + self.size / 2)
        y = math.floor(math.cos(radians) * (self.size / 2 - 0.001) + self.size / 2)

        self.sense.clear()
        self.sense.set_pixel(int(x), int(y), self.on_color)

    def display_moon_phase(self, phase_info):
        (trend, phase, illumination) = phase_info

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

    def display_heart(self):
        self.sense.show_message("<3")

    def clear_display(self):
        self.sense.clear()
