def headingToAngle(heading):
    return (heading + 270) % 360

for heading in range(0, 360):
    print(headingToAngle(heading))