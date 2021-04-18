airlineList = """ 

KLAX, Los Angeles International Airport
RKSI, Incheon International Airport

"""

for line in airlineList.splitlines():
    airlines = dict()
    if len(line) > 10:
        code, name = line.split(", ")[0], line.split(", ")[1]
        airlines[code] = name