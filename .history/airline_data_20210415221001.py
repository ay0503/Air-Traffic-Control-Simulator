airlineList = """ 

DAL, Delta, KSEA, KATL, KJFK, KMDW, KSLC, KLGA, LFPG, EHAM
AAL, American, KDFW, KLAX, KMIA, KORD, KPHL, KJFK, KPHX, KLGA
KAL, Korean Air, RKSI
JAL, Japan Air, RJTT, RJAA
BAW, British Airways, EGLL, EGKK
SWA, Southwest, KLAS, KATL, KBWI, KMDW, KDEN, KLAX
UAL, United, KIAD, KJFK
AFL, Air France, LFPO, LFPG
DLH, Lufthansa, EDDF, EDDM

"""

airlines = dict()
for line in airlineList.splitlines():
    if len(line) > 4:
        code, name = line.split(", ")[0], line.split(", ")[1]
        airlines[code] = name

airlineHubs = dict()
for line in airlineList.splitlines():
    hubs = []
    data = line.split(", ")[2:]
    for hub in data:
        if len(data) > 0:
            code = line.split(", ")[0]
            airlineHubs[code] = airlineHubs.get(code, hubs) + [hub]

print(airlineHubs['KAL'])
