from objects import *
from airline_data import airlines
from airport_data import airports
import random

airline = random.choice(list(airlines.keys()))

def randFlNo(len):
    random.randrange(10 ** (len - 1), 10 ** len)
