from objects import *

aircraftList = """ 

B727
B736
B737
B738
B739
B7

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
