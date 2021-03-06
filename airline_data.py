
#! Airline Data for Game

# https://abbreviations.yourdictionary.com/articles/airline-abbreviations-for-major-carriers.html

airlineList = """ 

DAL, Delta, KSEA, KATL, KJFK, KMDW, KSLC, KLGA, LFPG, EHAM
AAL, American, KDFW, KLAX, KMIA, KORD, KPHL, KJFK, KPHX, KLGA
KAL, Korean Air, RKSI
JAL, Japan Air, RJTT, RJAA
BAW, British Airways, EGLL, EGKK
SWA, Southwest, KLAS, KATL, KBWI, KMDW, KDEN, KLAX
UAL, United, KIAD, KJFK
AFR, Air France, LFPO, LFPG
AFL, Aeroflot, UUEE
DLH, Lufthansa, EDDF, EDDM
ACA, Air Canada, CYVR, CYYC
AAR, Asiana, RKSI, RKSS
CAL, China Airlines, RCTP
CCA, Air China, ZBAA, ZBAD, ZSPD, ZUUU
TAM, LATAM Brazil, SBGR, SBAR
CPA, Cathay Pacific, VHHH
UAE, Emirates, OMDB
FDX, Fedex, KMIA, KDFW, KMEM
KLM, KLM, EHAM
QFA, Qantas, YSSY, YPPH, YMML
SWR, Swiss Air, LSZH
SQC, Singapore, WSSS
THA, Thai Airways, VTBS
THY, Turkish Airlines, LFTM
CLX, Cargolux, ELLX

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
