airlineList = """ 

DAL, Delta
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
