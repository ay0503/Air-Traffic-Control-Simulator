
#! Airport Data for Future Real World Mode Implementation

airportList = """ 

KLAX, Los Angeles International Airport
RKSI, Incheon International Airport
OMDB, Dubai International Airport

"""

for line in airportList.splitlines():
    airports = dict()
    if len(line) > 10:
        code, name = line.split(", ")[0], line.split(", ")[1]
        airports[code] = name
