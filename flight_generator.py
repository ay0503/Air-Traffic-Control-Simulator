from objects import *
from airline_data import airlines, airlineHubs
from airport_data import airports
from aircraft_data import aircrafts
import random, copy

#airport = Airport("KLAX", [0,0], [], 'A', [330, 12])

# generates new 4 digit number for flight number
def randNo(len):
    return random.randrange(10 ** (len - 1), 10 ** len)

# generates new callsign for the flight
def newCallsign():
    airline = random.choice(list(airlines.keys()))
    no = randNo(random.randrange(2,5))
    callsign = f"{airline}{no}"
    return callsign

# returns airline code from callsign
def callsignToAirline(callsign):
    code = ''
    for letter in callsign:
        if letter.isalpha():
            code += letter
    return code

# generates new aircraft type from existing data to assign to flight
# will not create aircraft that violates airport size restrictions
def newType(aircrafts, airport):
    result = []
    for aircraft in aircrafts:
        if airport.check_size_limits(aircraft):
            result.append(aircraft)
    random.shuffle(result)
    return random.choice(result)

# generates a reasonable new altitude for approach
# TODO don't create flights that violate constraints
def newAltitude():
    alts = [7000, 8000, 9000, 10000]
    return random.choice(alts)

# generates a new starting speed based on size
def newSpeed(size):
    # size based speeds make gameplay very slow
    """ if size == "A":
        return random.choice([80, 90, 100, 110]) """
    spds = [210, 220, 230, 240, 250]
    return random.choice(spds)

# returns a new position for the aircraft on the edge of the map
def newPos(width, height):
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    choices = [[x, 0], [0, y], [width, y], [x, height]]
    return random.choice(choices)

# returns a heading based on 8 rectangular sections of the map
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

# generates a new route starting from a random airport to the arrival airport
def newArrivalRoute(code, airport):
    start = random.choice(airlineHubs[code])
    end = airport.code
    return start, end

# generates a new route departing from the game airport to a random waypoint
def newDepartureRoute(airport):
    start = airport.code
    end = random.choice(airport.waypoints)
    return start, end

# generates a remaining fuel level for flights approaching airport
# 25% fuel remaining average during approach
def newArrivalFuel(size):
    if size == 'A':
        fuel = 0.25 * 535
    else: 
        # based on linear regression of aircraft fuel capacity data
        fuel = 0.25 * ((ord(size) - ord("A")) * 42742 - 82945)
    return fuel

# generates fuel for departing aircraft based on size
# size to fuel relation based on linear regression line of real world data
def newDepartureFuel(size):
    if size == 'A':
        fuel = 535
    else: 
        # based on linear regression of aircraft fuel capacity data
        fuel = ((ord(size) - ord("A") + 2) * 42742 - 82945)
    return fuel

# generates a octal code used for flight squawk code
# 7500, 7600, and 7700 are non-normal codes only used in special scenarios
def newSquawkCode():
    code = 0
    for i in range(4):
        if i == 0:
            code += random.randrange(1,8) * 10 ** 3
        else: code += random.randrange(8) * 10 ** (3 - i)
    if code in [7500, 7600, 7700]:
        code = newSquawkCode()
    return code

# generates arrival with parameters generated above
def createArrival(width, height, airport):
    pos = newPos(width, height)
    callsign = newCallsign()
    type = newType(aircrafts, airport)
    code = callsignToAirline(callsign)
    fuel = newArrivalFuel(type.size)
    start, end = newArrivalRoute(code, airport)
    return Arrival(callsign, type, pos, newHeading(pos, width, height), 
                    newSpeed(type.size), newAltitude(), 0, start, end, fuel)

# generates departure with parameters generated above
def createDeparture(airport):
    runway = random.choice(airport.runways)
    pos = copy.copy(runway.pos)
    callsign = newCallsign()
    type = newType(aircrafts, airport)
    fuel = newDepartureFuel(type.size)
    start, end = newDepartureRoute(airport)
    return Departure(callsign, type, pos, copy.copy(runway.hdg), 
                    0, 0, 0, start, end, runway, fuel)
