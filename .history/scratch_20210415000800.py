def headingToAngle(heading):
    return 360 - (heading + 270) % 360

for heading in range(0, 360, 30):
    print("heading = ", heading, "angle = ", headingToAngle(heading))