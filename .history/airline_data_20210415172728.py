airlineList = """ 

DAL, Delta
AAL, American
KAL, Korean
BAW, British Airways

"""

airlines = dict()
for line in airlineList.splitlines():
    if len(line) > 4:
        code, name = line.split(", ")[0], line.split(", ")[1]
        airlines[code] = name

print(airlines)