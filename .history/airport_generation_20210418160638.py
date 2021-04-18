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

def generateRunway(airport):
    return Runway(rwy, pos, hdg, length, airport)

def generateAirport(pos):
    code = generateCode()
    size = generateSize()
    runways = []
    return Airport(code, pos, runways, size)

def addRunways(airport):
    for count in runwayCount(airport.size):
        airport.runways.append(generateRunway())