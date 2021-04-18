from objects import * 
from airport_data import airports
from aircraft_data import  aircrafts
from airline_data import airlines
import string, random

# TODO generate airport code ### pool from first letter and others random, pos = constant, runways, size random choice from A-F
# TODO generate runways rwy ### depends on heading, pos = ### may depend on heading, 
# TODO hdg = ###, length = random range of range based on size, airport = constant
# TODO MAYBE link continents to continents of airlines

continentCodes = ["K", "C", "S", "U", "Z", "R", "Y", "V", "B", "O", "E", "L"]
letters = list(string.ascii_uppercase)
airport = Airport("KLAX", [0,0], [], 'A')
# airport parameters

def generateCode():
    code = random.choice(continentCodes)
    for count in range(3):
        code += random.choice(letters)
    return code

def generateSize():
    return random.choice(["A", "B", "C", "D", "E", "F"])

def runwayCount(size):
    mass = ord(size) - ord("A")
    if mass < 2:
        return 1
    return mass

# runway parameters

def newLength(airport):
    if ord(airport.size) < ord("B"):
        return random.randrange(500, 2000)
    elif ord(airport.size) < ord("C"):
        return random.randrange(3000, 5000)
    else: 
        diff = ord(airport.size) - ord("A")
        return random.randrange(6000 + diff * 1000, 7000 + diff * 1000)

def newRwyPos(base, runway):
    normRwy = normalVector(hdgVector(runway.hdg, runway.length / 3))
    pos = list(map(lambda x,y: x+y, airport.pos, normRwy))
    return pos

# TODO generate parallel runway possibilities
def generateRunway(airport):
    pos = newRwyPos(airport)
    hdg = random.randrange(0, 360)
    length = newLength(airport)
    rwy = roundHalfUp(hdg / 10)
    return Runway(rwy, pos, hdg, length, airport)

def generateAirport(pos):
    code = generateCode()
    size = generateSize()
    runways = []
    return Airport(code, pos, runways, size)

def addRunways(airport):
    for count in runwayCount(airport.size):
        airport.runways.append(generateRunway())