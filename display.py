from sense_hat import SenseHat
import math

class SenseDisplay():
  """
  Using the LED display on the Sense HAT to display cardinal direction
  arrows and moon phases
  """
  size = 8
  on_color = (0, 0, 255) # blue
  
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
    # Adjust direction to the current orientation of the HAT 
    north = self.sense.get_compass()
    print("NORTH: %s" % north)
    adjusted_degrees = 180 - (int(degrees) + north) % 360

    radians = math.radians(adjusted_degrees)
    x = math.floor(math.sin(radians) * (self.size / 2 - .001) + self.size / 2)
    y = math.floor(math.cos(radians) * (self.size / 2 - .001) + self.size / 2)
  
    self.sense.clear()
    self.sense.set_pixel(int(x), int(y), self.on_color)
