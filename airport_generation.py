from objects import * 
from airport_data import airports
from aircraft_data import  aircrafts
from airline_data import airlines
from pprint import pprint
from weather import winds
import string, random

# continent codes https://en.wikipedia.org/wiki/ICAO_airport_code#/media/File:ICAO_FirstLetter.svg
continentCodes = ["K", "C", "S", "U", "Z", "R", "Y", "V", "B", "O", "E", "L"]
letters = list(string.ascii_uppercase)
#airport = Airport("KLAX", [0,0], [], 'A', [330, 12])
sizes = ["A", "B", "C", "D", "E", "F"]

#* size guideline  
#* farm, airstrip - A, regional - B, metropolitan - C, semi-international - D
#* average international - E, major international - F

# airport parameters
def generateCode():
    code = random.choice(continentCodes)
    for count in range(3):
        code += random.choice(letters)
    return code

def generateSize(sizes):
    return random.choice(sizes)

def runwayCount(size):
    mass = ord(size) - ord("A")
    if mass < 2:
        return 1
    return mass

""" # runway parameters
def newLength(airport):
    if ord(airport.size) < ord("B"):
        return random.randrange(500, 2000)
    elif ord(airport.size) < ord("C"):
        return random.randrange(3000, 5000)
    else: 
        diff = ord(airport.size) - ord("A")
        return random.randrange(6000 + diff * 1000, 7000 + diff * 1000) """

def newRwyPos( hdg, length):
    normRwy = normalVector(hdgVector(hdg, length / 1500))
    pos = list(map(lambda x,y: x+y, [0,0], normRwy))
    return pos

def generateRunway(airport):
    hdg = random.randrange(0, 360)
    length = 11000
    pos = newRwyPos(hdg, length)
    for runway in airport.runways:
        while distance(pos, runway.pos) < 4 and abs(hdg - runway.hdg) < 10:
            hdg = random.randrange(0, 360)
            pos = newRwyPos(hdg, length)
    rwy = roundHalfUp(hdg / 10)
    return Runway(rwy, pos, hdg, length, airport)

def generateWind(runways):
    spd = random.randrange(2,15)
    avg = 0
    for runway in runways:
            avg += runway.hdg
    return [int(avg / len(runways)), spd]

def generateAirport(pos):
    code = generateCode()
    size = generateSize(sizes)
    runways = []
    airport = Airport(code, pos, runways, size, winds)
    for count in range(runwayCount(airport.size)):
        airport.runways.append(generateRunway(airport))
        #pprint(f"Runway: {vars(airport.runways[count])}")
    airport.wind = generateWind(runways)
    return airport


"""         if runway.hdg > 180:
            avg += ((runway.hdg + 180) % 360)
        else: """