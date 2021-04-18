from objects import *

aircraftList = """ 

A225, Antonov 225 Mriya

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
B748, Boeing 747-8 Intercontinental
B74F, Boeing 747-8 Freighter
B752, Boeing 757-200
B753, Boeing 757-300
B762, Boeing 767-200
B763, Boeing 767-300
B772, Boeing 777-200
B77L, Boeing 777-200LR
B773, Boeing 777-300
B77W, Boeing 777-300ER
B77F, Boeing 777-200 Freighter
B788, Boeing 787-8
B789, Boeing 787-9
B78J, Boeing 787-10

C210, Cessna 210 Centurion
C208, Cessna 208 Caravan
C172, Cessna 172
C25B, Cessna Citation CJ3
C500, Cessna Citation I
C510, Cessna Citation Mustang

E175, Embraer 175
E190, Embraer 190
E170, Embraer 170
E545, Embraer Legacy 450

MD11, McDonnell Douglas MD-11
MD82, McDonnell Douglas MD-82
MD83, McDonnell Douglas MD-83
MD87, McDonnell Douglas MD-87
"""

aircrafts = dict()
for line in aircraftList.splitlines():
    if len(line) > 4:
        code, properties = line.split(", ")[0], line.split(", ")[1:]
        aircrafts[code] = properties
