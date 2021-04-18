from objects import *
from airline_data import airlines, airlineHubs
from airport_data import airports
from atc_simulator import *
import random

KLAX = Airport("KLAX", [[0, -6, 83], [0, -11, 83], [0, +6, 83], [0, +11, 83]])

def randNo(len):
    return random.randrange(10 ** (len - 1), 10 ** len)

def newCallsign():
    airline = random.choice(list(airlines.keys()))
    no = randNo(random.randrange(2,5))
    callsign = f"{airline}{no}"
    return callsign

def newAltitude():
    alts = [7000, 8000, 9000, 10000, 11000]
    return random.choice(alts)

def newSpeed():
    spds = [210, 220, 230, 240, 250]
    return random.choice(spds)

def newPos(width, height):
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    choices = [[x, 0], [0, y], [width, y], [x, height]]
    return random.choice(choices)

def newHeading(pos, width, height):
    if pos[0] == 0:
        return int(random.randrange(40, 120))
    elif pos[1] == 0:
        return int(random.randrange(130, 210))
    elif pos[0] == width:
        return int(random.randrange(220, 300))
    elif pos[1] == height:
        range = range(310, 360) + range(0, 30)
        return int(random.randrange(310, 30))

def newRoute(code, airport):
    start = random.choice(airlineHubs[code])
    end = airport.code 
    return start, end

def createArrival():
    pos = newPos()
    start, end = newRoute()
    return Aircraft(newCallsign(), pos, hdg, newSpeed(), newAltitude(),
                    0, start, end)