from objects import *
from airline_data import airlines
from airport_data import airports
import random

airline = random.choice(list(airlines.keys()))

def randNo(len):
    return random.randrange(10 ** (len - 1), 10 ** len)

print(randNo(2))