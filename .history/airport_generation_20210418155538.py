from objects import * 
from airport_data import airports
from aircraft_data import  aircrafts
from airline_data import airlines
import string, random

# TODO generate airport code ### pool from first letter and others random, pos = constant, runways, size random choice from A-F
# TODO generate runways rwy ### depends on heading, pos = ### may depend on heading, 
# TODO hdg = ###, length = random range of range based on size, airport = constant

continentCode = ["K", "C", "S", "U", "Z", "R", "Y", "V", "B", "O", "E", "L"]
letters = string.ascii_uppercase()
print(letters)

def generateCode():
    pass

def generateAirport():
    return Airport()