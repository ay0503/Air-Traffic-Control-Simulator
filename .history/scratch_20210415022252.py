import math

def headingToAngle(heading):
    return (360 - (heading + 270) % 360) % 360

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle * math.pi), spd * math.sin(angle * math.pi)

for heading in range(0, 360, 30):
    #print("heading = ", heading, "angle = ", headingToAngle(heading))
    print("heading = ", heading, "angle = ", hdgVector(heading, 30))