from objects import *

aircraftList = """ 

A225

A319, Airbus A319
A320, Airbus A320
A321, Airbus A321
A330, Airbus A330
A333, Airbus A330-300
A338, Airbus A330-800 Neo
A339, Airbus A330-900 Neo
A346, Airbus A340-600
A350, Airbus A350
A358, Airbus A350-800
A359, Airbus A350-900
A35K, Airbus A350-1000
A388, Airbus A380-800

B727, Boeing 727
B732, Boeing 737-200
B736, Boeing 737-600
B737, Boeing 737-700
B738, Boeing 737-800
B739, Boeing 737-900
B744, Boeing 747-400
B748, Boeing 747-8i
B752, Boeing 757-200
B753, Boeing 757-300
B762, Boeing 767-200
B763, Boeing 767-300
B772, Boeing 777-200
B77L, Boeing 777-200LR
B773, Boeing 777-300
B77W, Boeing 777-300ER
B788, Boeing 787-8
B789, Boeing 787-9
B78J, Boeing 787-10

C210
C208
C187
C25B
C500
C510

E175
E190
E179
E545

MD11
MD82
MD83
MD87
"""

aircrafts = dict()
for line in aircraftList.splitlines():
    if len(line) > 4:
        code, name = line.split(", ")[0], line.split(", ")[1]
        aircrafts[code] = name

aircraftHubs = dict()
for line in aircraftList.splitlines():
    hubs = []
    data = line.split(", ")[2:]
    for hub in data:
        if len(data) > 0:
            code = line.split(", ")[0]
            aircraftHubs[code] = airlineHubs.get(code, hubs) + [hub]
