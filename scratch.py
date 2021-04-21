import math
from objects import *

#A1 = Aircraft("DAL123", [450, 330], 133, 300, 7000, 0, 'KSEA', "KLAX")

#print(A1.fltno)

# helpers

def headingToAngle(heading):
    return (360 - (heading + 270) % 360) % 360

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle), spd * math.sin(angle)


#print("heading = ", heading, "angle = ", hdgVector(heading, 300))
    
from PIL import Image
import numpy as np


pixels = [226, 137, 125, 226, 137, 125, 223, 137, 133, 223, 136, 128, 226, 138, 120, 226, 129, 116, 228, 138, 123, 227, 134, 124, 227, 140, 127, 225, 136, 119, 228, 135, 126, 225, 134, 121, 223, 130, 108, 226, 139, 119, 223, 135, 120, 221, 129, 114, 221, 134, 108, 221, 131, 113, 222, 138, 121, 222, 139, 114, 223, 127, 109, 223, 132, 105, 224, 129, 102, 221, 134, 109, 218, 131, 110, 221, 133, 113, 223, 130, 108, 225, 125, 98, 221, 130, 121, 221, 129, 111, 220, 127, 121, 223, 131, 109, 225, 127, 103, 223] 

# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('new.png')