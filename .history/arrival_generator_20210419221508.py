from objects import *
from airline_data import airlines, airlineHubs
from airport_data import airports
from aircraft_data import aircrafts
import random

airport = Airport("KLAX", [0,0], [], 'A', [330, 12])

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
    result = []
    for aircraft in aircrafts:
        result.append(aircraft)
    random.shuffle(result)
    return random.choice(result)

# TODO don't create flights that violate constraints
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
    # left side
    if pos[0] == 0 and pos[1] > height / 2:
        return int(random.randrange(60, 80))
    elif pos[0] == 0 and pos[1] <= height / 2:
        return int(random.randrange(100, 120))
    # top side
    elif pos[1] == 0 and pos[0] < width / 2:
        return int(random.randrange(150, 170))
    elif pos[1] == 0 and pos[0] >= width / 2:
        return int(random.randrange(190, 210))
    # right side
    elif pos[0] == width and pos[1] > height / 2:
        return int(random.randrange(280, 300))
    elif pos[0] == width and pos[1] <= height / 2:
        return int(random.randrange(240, 260))
    # bottom side
    elif pos[1] == height and pos[0] > width / 2:
        return int(random.randrange(330, 350))
    elif pos[1] == height and pos[0] <= width / 2:
        return int(random.randrange(10, 30))

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
    return Arrival(callsign, type, pos, newHeading(pos, width, height), 
                    newSpeed(), newAltitude(), 0, start, end)

def createDeparture(airport):
    runway = random.choice(airport.runways)
    pos = runway.pos
    callsign = newCallsign()
    type = newType(aircrafts)
    code = callsignToAirline(callsign)
    end, start = newRoute(code, airport)
    return Departure(callsign, type, pos, runway.hdg, 
                    int(0), int(0), int(0), start, end, runway)


""" while True:
    createArrival(1280, 720, KLAX) """
#print(newType(aircrafts))
#pprint(vars(createArrival(123, 123, KLAX)))