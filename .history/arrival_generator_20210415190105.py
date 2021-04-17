from objects import *
from airline_data import airlines
from airport_data import airports
import random

def randNo(len):
    return random.randrange(10 ** (len - 1), 10 ** len)

def newCallsign():
    airline = random.choice(list(airlines.keys()))
    no = randNo(random.randrange(2,5))
    callsign = f"{airline}{no}"
    return callsign

def newAltitude():
    alts = [7000, 8000, 9000, 10000, 11000]
    return random.randrange(7000, 10000)