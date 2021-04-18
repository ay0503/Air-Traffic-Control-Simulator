airlines = dict()

airlineList = """ 

DAL, Delta Airlines
AAL, American Airlines
KAL, Korean Airlines

"""

for line in airlineList:
    code, name = line.split(", ")[0], line.split(",")[1]
    airlines[code] = name