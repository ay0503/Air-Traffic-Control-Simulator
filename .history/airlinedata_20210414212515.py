airlines = dict()

airlineList = """ 

DAL, Delta Airlines
AAL, American Airlines
KAL, Korean Airlines

"""

for line in airlineList.splitlines():
    print line.split(", ")
    code, name = line.split(", ")[0], line.split(",")[1]
    airlines[code] = name