airlineList = """ 

DAL, Delta, 
AAL, American
KAL, Korean Air
BAW, British Airways
SWA, Southwest
UAL, United
AFL, Air France
DLH, Lufthansa

"""

airlines = dict()
for line in airlineList.splitlines():
    if len(line) > 4:
        code, name = line.split(", ")[0], line.split(", ")[1]
        airlines[code] = name

for line in airlineList.splitlines():
    code = airlineList.splitlines().split(", ")[0]
    hubs = airlineList.splitlines().split(", ")[2:]
    if len(line) > 4:
        code, name = line.split(", ")[0], line.split(", ")[1]
        airlines[code] = name


for i in range(len(airlineList.splitlines()) - 2):
    
    if len(line) > 4:
        code = data.split(", ")[0]
        hub = data.split(", ")[i + 2]
