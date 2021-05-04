from objects import * 
from airport_data import airports
from aircraft_data import  aircrafts
from airline_data import airlines
from weather import winds, storm
import string, random

# continent codes https://en.wikipedia.org/wiki/ICAO_airport_code#/media/File:ICAO_FirstLetter.svg
continentCodes = ["K", "C", "S", "U", "Z", "R", "Y", "V", "O", "E", "L"]
letters = list(string.ascii_uppercase)
sizes = ["A", "B", "C", "D", "E", "F"]

#* size guideline (custom based on aircraft classes)
#* farm, airstrip - A, regional - B, metropolitan - C, semi-international - D
#* average international - E, major international - F

# airport parameters
def generateCode(size):
    code = random.choice(continentCodes)
    for count in range(3):
        code += random.choice(letters)
    return code

# generates airport size from classes "A" to "F"
def generateSize(sizes):
    return random.choice(sizes)

# generates runway count for airport based on size
def runwayCount(size):
    mass = ord(size) - ord("A")
    if mass < 2:
        return 1
    return mass

# varying runway length by airport size
""" def newLength(airport):
    if ord(airport.size) < ord("B"):
        return random.randrange(500, 2000)
    elif ord(airport.size) < ord("C"):
        return random.randrange(3000, 5000)
    else: 
        diff = ord(airport.size) - ord("A")
        return random.randrange(6000 + diff * 1000, 7000 + diff * 1000) """

# generates runway position based on radius vector from airport position
def newRwyPos(hdg, length):
    normRwy = normalVector(hdgVector(hdg, length / 1500))
    pos = list(map(lambda x,y: x+y, [0,0], normRwy))
    return pos

# generates runway with a heading tangent to the circle with the center airport
# will keep generating until reasonably distanced runways are created
def generateRunway(airport):
    hdg = random.randrange(0, 360)
    length = 11000
    pos = newRwyPos(hdg, length)
    for runway in airport.runways:
        while distance(pos, runway.pos) < 15 and abs(hdg - runway.hdg) < 20:
            hdg = random.randrange(0, 360)
            pos = newRwyPos(hdg, length)
    rwy = roundHalfUp(hdg / 10)
    return Runway(rwy, pos, hdg, length, airport)

# sets wind for runways corresponding to wind map position
def generateWind(runways):
    spd = random.randrange(2,15)
    avg = 0
    for runway in runways:
            avg += runway.hdg
    return [int(avg / len(runways)), spd]

# generates airport object with parameters generated above
def generateAirport(pos):
    size = generateSize(sizes)
    code = generateCode(size)
    runways = []
    airport = Airport(code, pos, runways, size)
    airport.weather = Weather(airport, winds, storm)
    airport.wind = airport.weather.winds[int(pos[1] // 20)][int(pos[0] // 20)]
    for count in range(runwayCount(airport.size)):
        airport.runways.append(generateRunway(airport))
    return airport
