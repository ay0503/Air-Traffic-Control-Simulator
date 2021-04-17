from objects import *

aircraftList = """ 

A225

A319
A320
A321
A330
A333
A338
A339
A346
A350
A358
A359
A35K

B727, Boeing 727
B732,
B736
B737
B738
B739
B744
B748
B752
B753
B762
B763
B772
B77L
B773
B77W
B788
B789
B78J

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
