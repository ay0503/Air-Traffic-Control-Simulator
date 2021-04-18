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
    
L = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
selection = L[0:5]
selection = L[]
print(selection)