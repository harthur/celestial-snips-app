from sense_hat import SenseHat
import math

class SenseDisplay():
  """
  Display 
  """
  size = 8
  
  @staticmethod
  def loc(index):
    row = math.floor(index / SenseDisplay.size)
    col = index % SenseDisplay.size
    return (row, col)
    
  # map of direction (in degrees) to pixel indices on the Sense HAT
  # in order to display an "arrow" pointing in that direction.
  direction_to_pixels = {
    0: {(0,3), (0,4), (1,3), (1,4), (2,3), (2,4)},
    45: {(0,7), (1,6), (2,5)},
    90: {(3,5), (3,6), (3,7), (4,5), (4,6), (4,7)},
    135: {(5,5), (6,6), (7,7)},
    180: {(5,3), (5,4), (6,3), (6,4), (7,3), (7,4)},
    225: {(5,2), (6,1), (7,0)},
    270: {(3,0), (3,1), (3,2), (4,0), (4,1), (4,2)},
    315: {(0,0), (1,1), (2,2)}
  }
  
  on_color = [255, 255, 255] # white
  off_color = [0, 0, 0] # off
  
  def __init__(self):
    self.sense = SenseHat()
  
  # Take the cardinal direction in degrees, and display
  # an "arrow" on Sense HAT pointing in that direction.
  def display_direction(self, degrees=0):
    # Adjust direction to the current orientation of the HAT 
    
    
    on_pixels = self.direction_to_pixels[degrees]
    pixels = [
      self.on_color if self.loc(i) in on_pixels else self.off_color
      for i in range(64)
    ]
    self.sense.set_pixels(pixels)




display = SenseDisplay()
display.display_direction(225)

# mark = [
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O,
# O, O, O, O, O, O, O, O
# ]