from objects import *
from airline_data import airlines
from airport_data import airports
import random

def randNo(len):
    return random.randrange(10 ** (len - 1), 10 ** len)

airline = random.choice(list(airlines.keys()))
length = random.randrange(2,5)
no = randNo(length)

