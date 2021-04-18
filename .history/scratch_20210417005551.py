import math
from objects import *

A1 = Aircraft("DAL123", [450, 330], 133, 300, 7000, 0, 'KSEA', "KLAX")

#print(A1.fltno)

# helpers

def headingToAngle(heading):
    return (360 - (heading + 270) % 360) % 360

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle), spd * math.sin(angle)

for heading in range(0, 360, 30):
    pass
    #print("heading = ", heading, "angle = ", headingToAngle(heading))
    #print("heading = ", heading, "angle = ", hdgVector(heading, 300))
    
def add(x):
    return x + 5

print(add(5))
add5 = lambda add, x: x + 5
print(add5(5))