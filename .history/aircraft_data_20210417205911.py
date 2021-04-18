from objects import *

aircraftList = """ 

# Antonov
A225, Antonov 225 Mriya, F, 5

# Airbus
A319, Airbus A319, C, 1
A320, Airbus A320, C, 0
A321, Airbus A321, C, 0
A330, Airbus A330, E, 1
A333, Airbus A330-300, E, 1
A338, Airbus A330-800 Neo, E, 2
A339, Airbus A330-900 Neo, E, 2
A346, Airbus A340-600, F, 3
A350, Airbus A350, E, 2
A358, Airbus A350-800, E, 2
A359, Airbus A350-900, E, 2
A35K, Airbus A350-1000, E, 2
A388, Airbus A380-800, F, 2

# Boeing
B727, Boeing 727, C, 3
B732, Boeing 737-200, C, 1
B736, Boeing 737-600, C, 1
B737, Boeing 737-700, C, 0
B738, Boeing 737-800, C, 0
B739, Boeing 737-900, C, 0
B744, Boeing 747-400, F, 1
B748, Boeing 747-8 Intercontinental, F, 3
B74F, Boeing 747-8 Freighter, F, 3
B752, Boeing 757-200, D, 2
B753, Boeing 757-300, D, 2
B762, Boeing 767-200, D, 2
B763, Boeing 767-300, D, 2
B772, Boeing 777-200, E, 1
B77L, Boeing 777-200LR, E, 1
B773, Boeing 777-300, E, 1
B77W, Boeing 777-300ER, E, 1
B77F, Boeing 777-200 Freighter, E, 1
B788, Boeing 787-8, E, 1
B789, Boeing 787-9, E, 1
B78J, Boeing 787-10, E, 1

# Cessna
C210, Cessna 210 Centurion, A, 4
C208, Cessna 208 Caravan, A, 4
C172, Cessna 172, A, 3
C25B, Cessna Citation CJ3, B, 4
C500, Cessna Citation I, B, 4
C510, Cessna Citation Mustang, B, 4

# Embraer
E175, Embraer 175, B, 2
E190, Embraer 190, B, 2
E170, Embraer 170, B, 2
E545, Embraer Legacy 450, B, 4

# McDonnell Douglas
MD11, McDonnell Douglas MD-11, D, 2
MD82, McDonnell Douglas MD-82, B, 2
"""

aircrafts = dict()
for line in aircraftList.splitlines():
    if len(line) > 4:
        code, properties = line.split(", ")[0], line.split(", ")[1:]
        aircrafts[code] = properties
