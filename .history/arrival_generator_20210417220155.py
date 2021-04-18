from objects import *
from airline_data import airlines, airlineHubs
from airport_data import airports
from aircraft_data import aircrafts
import random

def randNo(len):
    return random.randrange(10 ** (len - 1), 10 ** len)

def newCallsign():
    airline = random.choice(list(airlines.keys()))
    no = randNo(random.randrange(2,5))
    callsign = f"{airline}{no}"
    return callsign

def callsignToAirline(callsign):
    code = ''
    for letter in callsign:
        if letter.isalpha():
            code += letter
    return code

def newType(aircrafts):
    type = random.choice(aircrafts)

def newAltitude():
    alts = [7000, 8000, 9000, 10000]
    return random.choice(alts)

def newSpeed():
    spds = [210, 220, 230, 240, 250]
    return random.choice(spds)

def newPos(width, height):
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    choices = [[x, 0], [0, y], [width, y], [x, height]]
    return random.choice(choices)

# TODO create heading generation based on quadrants
def newHeading(pos, width, height):
    if pos[0] == 0:
        return int(random.randrange(40, 120))
    elif pos[1] == 0:
        return int(random.randrange(130, 210))
    elif pos[0] == width:
        return int(random.randrange(220, 300))
    elif pos[1] == height:
        hdgs = list(range(310, 360)) + list(range(0, 30))
        return int(random.choice(hdgs))

def newRoute(code, airport):
    start = random.choice(airlineHubs[code])
    end = airport.code 
    return start, end

def createArrival(width, height, airport):
    pos = newPos(width, height)
    callsign = newCallsign()
    type = newType(aircrafts)
    code = callsignToAirline(callsign)
    start, end = newRoute(code, airport)
    return Flight(newCallsign(), pos, newHeading(pos, width, height), 
                    newSpeed(), newAltitude(), 0, start, end)


#pprint(vars(createArrival(123, 123, KLAX)))