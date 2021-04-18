from objects import *

aircraftList = """ 

A225, Antonov 225 Mriya

A319, Airbus A319, C
A320, Airbus A320, C
A321, Airbus A321, C
A330, Airbus A330, E
A333, Airbus A330-300, E
A338, Airbus A330-800 Neo, E
A339, Airbus A330-900 Neo, E
A346, Airbus A340-600, F
A350, Airbus A350, E
A358, Airbus A350-800, E
A359, Airbus A350-900, E
A35K, Airbus A350-1000, E
A388, Airbus A380-800, F

B727, Boeing 727, C
B732, Boeing 737-200, C
B736, Boeing 737-600, C
B737, Boeing 737-700, C
B738, Boeing 737-800, C
B739, Boeing 737-900, C
B744, Boeing 747-400, F
B748, Boeing 747-8 Intercontinental, F
B74F, Boeing 747-8 Freighter, F
B752, Boeing 757-200, D
B753, Boeing 757-300, D
B762, Boeing 767-200, D
B763, Boeing 767-300, D
B772, Boeing 777-200, E
B77L, Boeing 777-200LR, E
B773, Boeing 777-300, E
B77W, Boeing 777-300ER, E
B77F, Boeing 777-200 Freighter, E
B788, Boeing 787-8, E
B789, Boeing 787-9, E
B78J, Boeing 787-10, E

C210, Cessna 210 Centurion, A
C208, Cessna 208 Caravan, A
C172, Cessna 172, A
C25B, Cessna Citation CJ3, B
C500, Cessna Citation I, B
C510, Cessna Citation Mustang, B

E175, Embraer 175, B
E190, Embraer 190, B
E170, Embraer 170, B
E545, Embraer Legacy 450, B

MD11, McDonnell Douglas MD-11, D
MD82, McDonnell Douglas MD-82, B
"""

aircrafts = dict()
for line in aircraftList.splitlines():
    if len(line) > 4:
        code, properties = line.split(", ")[0], line.split(", ")[1:]
        aircrafts[code] = properties

print(aircrafts[B738])