from objects import *
from airline_data import airlines
from airport_data import airports
import random

airline = random.choice(list(airlines.values()))

print(airline)